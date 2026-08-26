#!/usr/bin/env python3
"""Regenerate the specification tables embedded in the figure-*.md files from
the CSVs, so the figure pages never drift from the extracted data.

Each managed block in a markdown file looks like:

    <!-- BEGIN TABLE from=ac-electrical-specifications.csv table=clock -->
    ...generated markdown table...
    <!-- END TABLE -->

where the attributes select rows and columns:
    from=   CSV filename (required)
    table=  value of the CSV's `table` column
    nums=   pipe-separated list of `num` values, in the order to emit;
            `_` stands for a space, and the empty string selects the
            unnumbered row
    grades= which speed-grade columns to print: `m68000` (six, including
            the separately binned 16.67 MHz 12F part), `mc68ec000` (five,
            no 12F and no plain 16 MHz) or `mc68008` (two).  Default m68000.

The table's own footnotes follow it, read from ac-table-notes.csv: the
column footnotes always, and a row footnote only when one of the rows
actually printed references it.  A figure page shows a handful of rows out
of a table of sixty, so printing all twelve of that table's notes would bury
the two that matter.

Run with no arguments to update every figure-*.md in this directory.
"""
import csv, glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

GRADESETS = {
    "m68000":    [("8 MHz", "f8"), ("10 MHz", "f10"), ("12.5 MHz", "f12_5"),
                  ("16.67 MHz 12F", "f16_67"), ("16 MHz", "f16"), ("20 MHz", "f20")],
    "mc68ec000": [("8 MHz", "f8"), ("10 MHz", "f10"), ("12.5 MHz", "f12_5"),
                  ("16.67 MHz", "f16_67"), ("20 MHz", "f20")],
    "mc68008":   [("8 MHz", "f8"), ("10 MHz", "f10")],
}

BLOCK = re.compile(
    r"(?P<open><!--\s*BEGIN TABLE(?P<attrs>[^>]*?)-->\n)"
    r".*?"
    r"(?P<close><!--\s*END TABLE\s*-->)",
    re.S)


def notes_for(csvname, table):
    """(column notes, row notes) for one table, each marker -> text."""
    path = os.path.join(HERE, "ac-table-notes.csv")
    if not os.path.exists(path):
        return {}, {}
    col, row = {}, {}
    for n in csv.DictReader(open(path)):
        if n["table"] != table:
            continue
        (col if n["applies_to"] else row)[n["marker"]] = n
    return col, row


def sup(marker):
    return "<sup>%s</sup>" % marker.replace("*", "&ast;")


def cell(lo, hi):
    """Render one min/max pair the way a datasheet reader expects to see it."""
    if lo and hi:
        return "%s&nbsp;–&nbsp;%s" % (lo, hi)   # en dash: a closed range
    if hi:
        return "≤ %s" % hi        # max only
    if lo:
        return "≥ %s" % lo        # min only
    return "—"                    # neither: not specified


def render(attrs):
    a = dict(re.findall(r"(\w+)=([^\s]+)", attrs))
    grades = GRADESETS[a.get("grades", "m68000")]
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
                             % (a.get("from"), a.get("table", "<all>"),
                                ", ".join(missing)))
        rows = [idx[n] for n in want]

    colnotes, rownotes = notes_for(a["from"], a.get("table", ""))
    colmark = {}
    for m, n in colnotes.items():
        for g in n["applies_to"].split("|"):
            colmark[g] = m

    head = ["%s%s" % (g, sup(colmark[k]) if k in colmark else "")
            for g, k in grades]
    out = ["| Num. | Characteristic | Unit | " + " | ".join(head) + " |",
           "|:-:|---|:-:|" + "--:|" * len(grades)]
    used = []
    for r in rows:
        vals = [cell(r["%s_min" % k], r["%s_max" % k]) for _, k in grades]
        num = r["num"] or "—"
        if r["footnotes"]:
            num += sup(r["footnotes"].replace(" ", ""))
            used += [m for m in r["footnotes"].split(",")]
        out.append("| %s | %s | %s | %s |"
                   % (num, r["characteristic"], r["unit"], " | ".join(vals)))

    # column footnotes first (* before **), then the row footnotes the
    # printed rows actually reference, in numerical order
    foot = [(m, colnotes[m]["text"]) for m in sorted(colnotes, key=len)]
    marks = {m.strip() for m in used}
    foot += [(m, rownotes[m]["text"]) for m in sorted(marks & set(rownotes), key=int)]
    # a marker the source uses but never defines is worth saying out loud
    # rather than leaving as a dangling superscript
    foot += [(m, "*not defined in this table — see README.md*")
             for m in sorted(marks - set(rownotes), key=int)]
    if foot:
        out.append("")
        for m, t in foot:
            out.append("- **%s** %s" % (m.replace("*", "&ast;"), t))
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
            print("%-52s no managed table blocks" % os.path.basename(p))
            continue
        changed = new != src
        if changed:
            open(p, "w").write(new)
        print("%-52s %d block(s) %s" % (os.path.basename(p), n[0],
                                        "updated" if changed else "already current"))


if __name__ == "__main__":
    args = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "figure-*.md")))
    if not args:
        sys.exit("no figure-*.md files found in %s" % HERE)
    main(args)
