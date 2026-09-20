# The limpid gate for the tool pages

Each tool is one `index.html`, so its prose sits in the static markup and in the
content data at the top of the `<script>`. Limpid grades LaTeX, Markdown and
plain prose; pointed at the raw file it grades the stylesheet and the engine
too, and returns a meaningless B. `extract_prose.py` lifts out the prose a
player reads, `check.sh` runs the gate over it, and `trace.py` maps each finding
back to the line of `index.html` that produced it.

```bash
tools/.limpid/check.sh                          # every tools/*/index.html
tools/.limpid/check.sh research-projects        # one page
tools/.limpid/check.sh --json > /tmp/run.json   # then:
python3 tools/.limpid/trace.py /tmp/run.json --min warning
python3 tools/.limpid/trace.py /tmp/run.json --counts
```

`LIMPID_CLI` points at `apps/cli/dist/cli.js` in the limpid repo; build it there
with `npm run build -w apps/cli`. `LIMPID_RULES` points at a house `rules.json`
— the writing-voice ban list in detector form. That file lives with the vault
rather than in this repo, and the gate runs on the shipped rubric alone when it
is absent.

## What the gate does and does not read

The quoted drill message pairs (`a` and `b`) are excluded. One of the two is
deliberately the weaker message a well-meaning person actually sends: flabby by
design, and grading it as the author's prose measures the wrong thing. Pass
`--include-messages` to the extractor to see them anyway.

What survives at `warning` and above is worth looking at. What survives at
`suggestion` is mostly the shipped rubric reading ordinary narrative English:
`never`, `always`, `may` and `could` are boosters and hedges in a paper and are
plain words in a scene, and `strunk.active-voice` counts every `is` before a
participle, including adjectives (`is jagged`). Read those rows, do not clear
them.
