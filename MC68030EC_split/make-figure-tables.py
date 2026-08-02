#!/usr/bin/env python3
"""Regenerate the specification tables embedded in the figure-NN-*.md files
from the CSVs, so the figure pages never drift from the extracted data.

Each managed block in a markdown file looks like:

    <!-- BEGIN TABLE from=ac-electrical-specifications.csv table=clock -->
    ...generated markdown table...
    <!-- END TABLE -->

where the attributes select rows:
    from=   CSV filename (required)
    table=  value of the CSV's `table` column
    nums=   comma-separated list of `num` values, in the order to emit;
            the empty string selects the unnumbered row

Run with no arguments to update every figure-*.md in this directory.
"""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRADES = [("20 MHz", "f20"), ("25 MHz", "f25"), ("33.33 MHz", "f33"),
          ("40 MHz", "f40"), ("50 MHz", "f50")]
CIRCLED = {"1": "①", "2": "②", "3": "③", "4": "④", "5": "⑤",
           "6": "⑥", "7": "⑦", "8": "⑧", "9": "⑨"}

BLOCK = re.compile(
    r"(?P<open><!--\s*BEGIN TABLE(?P<attrs>[^>]*?)-->\n)"
    r".*?"
    r"(?P<close><!--\s*END TABLE\s*-->)",
    re.S)


def cell(lo, hi):
    """Render one min/max pair the way a datasheet reader expects to see it."""
    if lo and hi:
        return "%s–%s" % (lo, hi)      # en dash: a closed range
    if hi:
        return "≤ %s" % hi        # max only
    if lo:
        return "≥ %s" % lo        # min only
    return "—"                         # neither: not specified


def callouts(num):
    parts = [p.strip() for p in num.split(",") if p.strip()]
    marks = [CIRCLED[p] for p in parts if p in CIRCLED]
    return " ".join(marks) if len(marks) == len(parts) and marks else "—"


def render(attrs):
    a = dict(re.findall(r"(\w+)=([^\s]+)", attrs))
    rows = list(csv.DictReader(open(os.path.join(HERE, a["from"]))))
    if "table" in a:
        rows = [r for r in rows if r["table"] == a["table"]]
    if "nums" in a:
        want = a["nums"].replace("_", " ").split("|")
        idx = {r["num"]: r for r in rows}
        rows = [idx[n] for n in want if n in idx]

    out = ["| On figure | Num. | Characteristic | Unit | " +
           " | ".join(g for g, _ in GRADES) + " |",
           "|:-:|:-:|---|:-:|" + "--:|" * len(GRADES)]
    for r in rows:
        vals = [cell(r["%s_min" % k], r["%s_max" % k]) for _, k in GRADES]
        out.append("| %s | %s | %s | %s | %s |" % (
            callouts(r["num"]), r["num"] or "—",
            r["characteristic"], r["unit"], " | ".join(vals)))
    return "\n".join(out) + "\n"


def main(paths):
    for p in paths:
        src = open(p).read()
        n = [0]

        def sub(m):
            n[0] += 1
            return m.group("open") + render(m.group("attrs")) + m.group("close")

        new = BLOCK.sub(sub, src)
        if n[0] == 0:
            print("%-44s no managed table blocks" % os.path.basename(p))
            continue
        changed = new != src
        if changed:
            open(p, "w").write(new)
        print("%-44s %d block(s) %s" % (os.path.basename(p), n[0],
                                        "updated" if changed else "already current"))


if __name__ == "__main__":
    args = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "figure-*.md")))
    if not args:
        sys.exit("no figure-*.md files found in %s" % HERE)
    main(args)
