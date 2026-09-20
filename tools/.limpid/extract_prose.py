#!/usr/bin/env python3
"""Pull the reader-facing prose out of a self-contained game page.

The games are one `index.html` each, so the prose a player reads lives in two
places: the static body markup (headings, subtitles, the scoring explainer) and
the string literals in the content data at the top of the `<script>` (cards,
reveals, the field manual, the glossary). Limpid grades LaTeX, Markdown and
plain prose; it has no HTML mode, and pointed at the raw file it grades the
stylesheet and the engine as if they were sentences. This lifts out the prose
and writes a Markdown file limpid can read, plus a JSON map from each output
line back to the line of `index.html` it came from, so a finding can be traced
to the string that produced it.

The drill message pairs (`a` and `b`) are excluded by default. One of the two is
deliberately the weaker message a well-meaning person actually sends: flabby by
design, and grading it as the author's prose measures the wrong thing.

    python3 extract_prose.py tools/research-projects/index.html out.md out.map.json
"""
import argparse
import json
import re
from html import unescape

# Keys whose values are identifiers, CSS, seeds or dial names rather than prose.
NON_PROSE_KEYS = {
    "id", "ruleId", "group", "better", "res", "req", "reqTrait", "seed", "seeds",
    "lean", "kind", "fx", "risk", "href", "url", "cls", "icon", "type", "tag", "ax",
}
# Quoted in-character messages: written to be picked apart, not to be graded.
IN_CHARACTER_KEYS = {"a", "b"}

STRING_RE = re.compile(
    r'(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?P<q>["\'`])(?P<val>(?:\\.|(?!(?P=q))[^\\])*)(?P=q)',
    re.S,
)


def strip_tags(chunk):
    chunk = re.sub(r"<(script|style|svg|noscript)\b.*?</\1>", " ", chunk, flags=re.S | re.I)
    return unescape(re.sub(r"<[^>]+>", " ", chunk))


def body_prose(lines, start, end):
    """Visible text runs in the static markup, one entry per source line."""
    out, inside_skipped = [], 0
    for i in range(start, end):
        raw = lines[i]
        if re.search(r"<(script|style|svg)\b", raw, re.I):
            inside_skipped += 1
        if inside_skipped:
            if re.search(r"</(script|style|svg)>", raw, re.I):
                inside_skipped -= 1
            continue
        text = re.sub(r"\s+", " ", strip_tags(raw)).strip()
        if len(text) >= 25 and " " in text:
            out.append((i + 1, "markup", text))
    return out


def script_prose(lines, start, end, exclude):
    """Prose-bearing string literals in the content data."""
    out = []
    for i in range(start, end):
        for m in STRING_RE.finditer(lines[i]):
            key, val = m.group("key"), m.group("val")
            if key in NON_PROSE_KEYS or key in exclude:
                continue
            val = val.replace("\\n", " ").replace('\\"', '"').replace("\\'", "'")
            val = re.sub(r"<[^>]+>", " ", val)
            val = re.sub(r"\$\{[^}]*\}", "X", val)  # template holes become a token
            val = re.sub(r"\s+", " ", val).strip()
            # An unbalanced paren means the regex clipped a template literal.
            if len(val) < 30 or " " not in val or val.count("(") != val.count(")"):
                continue
            out.append((i + 1, key, val))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("page")
    ap.add_argument("out_md")
    ap.add_argument("out_map")
    ap.add_argument("--include-messages", action="store_true",
                    help="also grade the quoted drill messages (a/b)")
    args = ap.parse_args()

    lines = open(args.page, encoding="utf-8").read().split("\n")
    body_i = next(i for i, l in enumerate(lines) if "<body" in l.lower())
    script_i = next(i for i, l in enumerate(lines) if l.strip().startswith("<script"))
    script_end = next(i for i, l in enumerate(lines) if "</script>" in l)

    exclude = set() if args.include_messages else IN_CHARACTER_KEYS
    items = body_prose(lines, body_i, script_i) + script_prose(lines, script_i, script_end, exclude)

    md, mapping = [], {}
    for html_line, key, text in items:
        md.append(text)
        mapping[len(md)] = {"html_line": html_line, "key": key, "text": text}
        md.append("")
        mapping[len(md)] = {"html_line": html_line, "key": key, "text": ""}

    with open(args.out_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    with open(args.out_map, "w", encoding="utf-8") as fh:
        json.dump(mapping, fh, indent=0)
    print(f"{args.page}: {len(items)} prose units -> {args.out_md}")


if __name__ == "__main__":
    main()
