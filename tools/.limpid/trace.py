#!/usr/bin/env python3
"""Turn a limpid --json run over the extracted prose back into page findings.

    tools/.limpid/check.sh --json > /tmp/run.json
    python3 tools/.limpid/trace.py /tmp/run.json                 # every finding
    python3 tools/.limpid/trace.py /tmp/run.json --min warning   # the gate

Each row names the line of `index.html` the string lives on, the content key it
came from, and the sentence itself, so a finding can be fixed at its source
rather than in the extracted copy.
"""
import argparse
import collections
import json
import os

ORDER = {"info": 0, "suggestion": 1, "warning": 2, "error": 3}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("report", help="output of check.sh --json")
    ap.add_argument("--min", default="info", choices=list(ORDER), help="lowest severity to print")
    ap.add_argument("--rule", help="only this ruleId")
    ap.add_argument("--counts", action="store_true", help="counts per rule, no rows")
    args = ap.parse_args()

    floor = ORDER[args.min]
    for f in json.load(open(args.report, encoding="utf-8")):
        path = f["file"]
        name = os.path.basename(path)[: -len(".md")]
        mapping = json.load(open(os.path.join(os.path.dirname(path), name + ".map.json"), encoding="utf-8"))
        rows = [x for x in f["findings"]
                if ORDER[x["severity"]] >= floor and (not args.rule or x["ruleId"] == args.rule)]
        print(f"== {name}  grade {f['grade']}  {f['metrics']}  ({len(rows)} shown of {f['findingCount']})")
        if args.counts:
            for (rule, sev), n in collections.Counter((x["ruleId"], x["severity"]) for x in rows).most_common():
                print(f"   {n:4d}  {sev:10s} {rule}")
            continue
        for x in rows:
            src = mapping.get(str(x["line"]), {})
            print(f"   {x['severity']:10s} {x['ruleId']:32s} index.html:{src.get('html_line')} ({src.get('key')})")
            print(f"      {x['message']}")
            print(f"      {src.get('text', '')[:180]}")


if __name__ == "__main__":
    main()
