#!/usr/bin/env python3
"""Regenerate the specification tables embedded in the figure-12-N-*.md files
from the CSVs, so the figure pages never drift from the extracted data.

Each managed block in a markdown file looks like:

    <!-- BEGIN TABLE from=ac-electrical-specifications.csv table=clock -->
    ...generated markdown table...
    <!-- END TABLE -->

where the attributes select rows:
    from=   CSV filename (required)
    table=  value of the CSV's `table` column
    nums=   pipe-separated list of `num` values, in the order to emit;
            `_` stands for a space, and the empty string selects the
            unnumbered row

Run with no arguments to update every figure-*.md in this directory.
"""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRADES = [("16.67 MHz", "f1667"), ("20 MHz", "f20"),
          ("25 MHz", "f25"), ("33.33 MHz", "f33")]

BLOCK = re.compile(
    r"(?P<open><!--\s*BEGIN TABLE(?P<attrs>[^>]*?)-->\n)"
    r".*?"
    r"(?P<close><!--\s*END TABLE\s*-->)",
    re.S)


def cell(lo, hi, lo_clk, hi_clk):
    """Render one min/max pair the way a datasheet reader expects to see it."""
    lo = "%s + %s clk" % (lo, lo_clk) if lo and lo_clk else (lo_clk + " clk" if lo_clk else lo)
    hi = "%s + %s clk" % (hi, hi_clk) if hi and hi_clk else (hi_clk + " clk" if hi_clk else hi)
    if lo and hi:
        return "%s&nbsp;–&nbsp;%s" % (lo, hi)   # en dash: a closed range
    if hi:
        return "≤ %s" % hi        # max only
    if lo:
        return "≥ %s" % lo        # min only
    return "—"                    # neither: not specified


def render(attrs):
    a = dict(re.findall(r"(\w+)=([^\s]+)", attrs))
    rows = list(csv.DictReader(open(os.path.join(HERE, a["from"]))))
    if "table" in a:
        rows = [r for r in rows if r["table"] == a["table"]]
    if "nums" in a:
        want = a["nums"].replace("_", " ").split("|")
        idx = {r["num"]: r for r in rows}
        missing = [n for n in want if n not in idx]
        if missing:
            # fail loudly: a silently dropped row would look like the figure
            # simply does not reference that specification
            raise SystemExit("%s: no such specification number(s) in %s: %s"
                             % (a.get("from"), a.get("table", "<all>"), ", ".join(missing)))
        rows = [idx[n] for n in want]

    out = ["| Num. | Characteristic | Unit | " +
           " | ".join(g for g, _ in GRADES) + " |",
           "|:-:|---|:-:|" + "--:|" * len(GRADES)]
    for r in rows:
        vals = [cell(r["%s_min" % k], r["%s_max" % k], r["min_clks"], r["max_clks"])
                for _, k in GRADES]
        out.append("| %s | %s | %s | %s |" % (
            r["num"] or "—", r["characteristic"], r["unit"], " | ".join(vals)))
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
