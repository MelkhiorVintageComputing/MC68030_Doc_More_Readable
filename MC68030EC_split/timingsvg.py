#!/usr/bin/env python3
"""A very small timing-diagram renderer that emits standalone SVG.

Written for the MC68030EC/D bus-cycle figures. Deliberately minimal: it draws
only what those figures contain — a clock, two-level signals, buses with
valid/high-impedance windows, and numbered dimension callouts.

Why not an existing tool: the output has to render on GitHub, which supports
neither WaveDrom nor any Mermaid waveform type (Mermaid has none), and which
strips inline <svg> from markdown. A plain .svg file referenced as an image is
the only thing that works, so the figures are generated as files.

Coordinate system
-----------------
Time is measured in *bus states*: state Sn occupies [n, n+1). Half-state
positions are ordinary floats, so 2.5 is the middle of S2. The clock is high
during even states and low during odd ones, matching the source figures.

Vertical layout is a cursor: each signal reserves a waveform band plus a number
of `lanes` beneath it for callouts. Callouts address a lane by (signal, index).
"""

# ---------------------------------------------------------------- geometry --
W       = 96.0   # px per bus state
AMP     = 26.0   # waveform amplitude (low level to high level)
SLOPE   = 9.0    # horizontal run of an edge
LANE    = 25.0   # height of one callout lane
BAND    = 15.0   # gap between a waveform and the first lane under it
LABEL_W = 158.0  # left margin holding the signal names
R       = 13.5   # callout circle radius
AH      = 8.0    # arrowhead length
AW      = 4.6    # arrowhead half-width
LEAD    = 34.0   # leader length for callouts drawn from outside


class Fig:
    def __init__(self, title, states=6, lead=0.9, trail=1.0, top=44.0, labels=None,
                 grid=True):
        self.title  = title
        self.states = states
        self.grid   = grid        # off for figures that have no clock to divide
        self.labels = labels if labels is not None else ["S%d" % i for i in range(states)]
        self.lead   = lead
        self.trail  = trail
        self.y      = top
        self.rows   = {}          # name -> dict(top, lanes, label)
        self.order  = []
        self.parts  = []          # svg fragments, drawn in order
        self.guides = []          # x positions of full-height guide lines

    # -- coordinate helpers -------------------------------------------------
    def x(self, t):
        return LABEL_W + (t + self.lead) * W

    def _lane_y(self, sig, i):
        r = self.rows[sig]
        return r["top"] + AMP + BAND + i * LANE

    def width(self):
        return self.x(self.states + self.trail) + 40

    def height(self):
        return self.y + 20

    # -- signals ------------------------------------------------------------
    def _row(self, name, label, lanes):
        self.rows[name] = {"top": self.y, "lanes": lanes, "label": label or name}
        self.order.append(name)
        self.y += AMP + BAND + lanes * LANE
        return self.rows[name]

    def clock(self, name="CLK", label=None, lanes=1):
        r = self._row(name, label, lanes)
        hi, lo = r["top"], r["top"] + AMP
        x0, x1 = self.x(-self.lead), self.x(self.states + self.trail)
        # high during even states, low during odd ones
        d = ["M %.1f,%.1f" % (x0, lo)]
        lvl = lo
        for s in range(0, self.states + 2):
            want = hi if s % 2 == 0 else lo
            a = self.x(s)
            d.append("L %.1f,%.1f L %.1f,%.1f" % (a - SLOPE / 2, lvl, a + SLOPE / 2, want))
            lvl = want
        d.append("L %.1f,%.1f" % (x1, lvl))
        self.parts.append('<path class="w" d="%s"/>' % " ".join(d))
        for s in range(self.states):
            self.guides.append(self.x(s))
        return self

    def level(self, name, edges, start=1, label=None, lanes=1, z_from=None):
        """`edges` is [(t, level), ...]; level 1 = upper rail, 0 = lower rail.

        `z_from` releases the signal to high impedance at that time, drawn as a
        mid-rail line — this is what the arbitration figure shows when the
        processor stops driving the bus.  A level of None inside `edges` does
        the same thing at that instant and lets the signal come back, which is
        what an arbitration figure needs when the bus is handed back."""
        r = self._row(name, label, lanes)
        hi, lo = r["top"], r["top"] + AMP
        mid = r["top"] + AMP / 2
        end = self.x(z_from) if z_from is not None else self.x(self.states + self.trail)
        lvl = hi if start else lo
        d = ["M %.1f,%.1f" % (self.x(-self.lead), lvl)]
        for t, v in edges:
            if z_from is not None and t >= z_from:
                continue
            want = mid if v is None else (hi if v else lo)
            a = self.x(t)
            d.append("L %.1f,%.1f L %.1f,%.1f" % (a - SLOPE / 2, lvl, a + SLOPE / 2, want))
            lvl = want
        d.append("L %.1f,%.1f" % (end - SLOPE / 2 if z_from is not None else end, lvl))
        if z_from is not None:
            d.append("L %.1f,%.1f L %.1f,%.1f"
                     % (end + SLOPE / 2, mid, self.x(self.states + self.trail), mid))
        self.parts.append('<path class="w" d="%s"/>' % " ".join(d))
        return self

    def bus(self, name, segs, label=None, lanes=1):
        """`segs` is [(t, kind), ...] with kind 'v' (valid) or 'z' (floating).

        The first entry gives the state at the left edge; each later entry is a
        transition *centred* on that time."""
        r = self._row(name, label, lanes)
        hi, lo, mid = r["top"], r["top"] + AMP, r["top"] + AMP / 2
        x0, x1 = self.x(-self.lead), self.x(self.states + self.trail)
        pts = [(x0, segs[0][1])] + [(self.x(t), k) for t, k in segs[1:]] + [(x1, segs[-1][1])]
        up, dn = [], []          # upper and lower rails, for valid stretches
        for i in range(len(pts) - 1):
            xa, ka = pts[i]
            xb, kb = pts[i + 1]
            a = xa + (SLOPE / 2 if i else 0)
            b = xb - (SLOPE / 2 if i + 2 < len(pts) else 0)
            if ka == "v":
                up.append((a, b)); dn.append((a, b))
            else:
                self.parts.append('<line class="w" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                                  % (a, mid, b, mid))
            if i + 2 < len(pts):
                # transition centred on xb
                l, rgt = xb - SLOPE / 2, xb + SLOPE / 2
                if ka == "v" and kb == "v":       # crossing
                    self.parts.append('<path class="w" d="M %.1f,%.1f L %.1f,%.1f '
                                      'M %.1f,%.1f L %.1f,%.1f"/>'
                                      % (l, hi, rgt, lo, l, lo, rgt, hi))
                elif ka == "v":                   # closing wedge
                    self.parts.append('<path class="w" d="M %.1f,%.1f L %.1f,%.1f '
                                      'M %.1f,%.1f L %.1f,%.1f"/>'
                                      % (l, hi, rgt, mid, l, lo, rgt, mid))
                else:                             # opening wedge
                    self.parts.append('<path class="w" d="M %.1f,%.1f L %.1f,%.1f '
                                      'M %.1f,%.1f L %.1f,%.1f"/>'
                                      % (l, mid, rgt, hi, l, mid, rgt, lo))
        for a, b in up:
            self.parts.append('<line class="w" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (a, hi, b, hi))
        for a, b in dn:
            self.parts.append('<line class="w" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (a, lo, b, lo))
        return self

    # -- callouts -----------------------------------------------------------
    def _arrow(self, x, y, direction):
        s = -1 if direction == "left" else 1
        self.parts.append('<path class="ah" d="M %.1f,%.1f L %.1f,%.1f L %.1f,%.1f Z"/>'
                          % (x, y, x - s * AH, y - AW, x - s * AH, y + AW))

    def _disc(self, cx, cy, text):
        self.parts.append('<circle class="disc" cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx, cy, R))
        self.parts.append('<text class="num" x="%.1f" y="%.1f">%s</text>' % (cx, cy + 4.2, text))

    def span(self, sig, lane, t1, t2, text, style="in", tick=True):
        """A dimension between two times.

        style 'in'   arrows inside the span, pointing outward, disc in the middle
        style 'outR' arrows approaching from outside, disc to the right
        style 'outL' arrows approaching from outside, disc to the left
        """
        y = self._lane_y(sig, lane)
        a, b = self.x(t1), self.x(t2)
        if style == "in" and b - a < 3.4 * R:
            style = "outR"       # too tight for a disc between the arrowheads
        if tick:
            for xx in (a, b):
                self.parts.append('<line class="tick" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                                  % (xx, y - 9, xx, y + 9))
        if style == "in":
            self.parts.append('<line class="dim" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (a, y, b, y))
            self._arrow(a, y, "left"); self._arrow(b, y, "right")
            self._disc((a + b) / 2, y, text)
        else:
            right = style == "outR"
            self.parts.append('<line class="dim" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (a - LEAD, y, a, y))
            self._arrow(a, y, "right")
            self.parts.append('<line class="dim" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (b, y, b + LEAD, y))
            self._arrow(b, y, "left")
            self._disc(b + LEAD + R if right else a - LEAD - R, y, text)
        return self

    def mark(self, sig, lane, t, text, side="right"):
        """A single-ended callout: one arrow onto one reference point."""
        y = self._lane_y(sig, lane)
        a = self.x(t)
        self.parts.append('<line class="tick" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (a, y - 9, a, y + 9))
        s = 1 if side == "right" else -1
        self.parts.append('<line class="dim" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>'
                          % (a, y, a + s * LEAD, y))
        self._arrow(a, y, "left" if side == "right" else "right")
        self._disc(a + s * (LEAD + R), y, text)
        return self

    def alt(self, sig, t0, t1, level=1):
        """A dashed alternative edge: the source draws one where a signal may
        legitimately change at either of two times."""
        r = self.rows[sig]
        a, b = (r["top"], r["top"] + AMP) if level else (r["top"] + AMP, r["top"])
        self.parts.append('<path class="alt" d="M %.1f,%.1f L %.1f,%.1f L %.1f,%.1f"/>'
                          % (self.x(t0), a, self.x(t1) - SLOPE / 2, a,
                             self.x(t1) + SLOPE / 2, b))
        return self

    def brk(self, t, note=None):
        """The drafting 'time passes here' break the source figures use."""
        x = self.x(t)
        self.parts.append('<path class="ovl" d="M %.1f,36 L %.1f,%.1f M %.1f,36 L %.1f,%.1f"/>'
                          % (x - 7, x + 5, self.y - 4, x + 5, x + 17, self.y - 4))
        if note:
            self.parts.append('<text class="st" x="%.1f" y="30">%s</text>' % (x + 5, esc(note)))
        return self

    # -- output -------------------------------------------------------------
    def svg(self):
        h, w = self.height(), self.width()
        out = []
        out.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" '
                   'width="%.0f" height="%.0f" font-family="\'DejaVu Sans\',Verdana,Arial,sans-serif" '
                   'role="img" aria-label="%s">' % (w, h, w, h, esc(self.title)))
        out.append("  <title>%s</title>" % esc(self.title))
        out.append("""  <style>
    .w    { stroke:#111; stroke-width:2.4; fill:none; stroke-linejoin:round; stroke-linecap:round; }
    .grid { stroke:#111; stroke-width:0.8; opacity:.30; }
    .tick { stroke:#111; stroke-width:0.9; opacity:.75; }
    .dim  { stroke:#111; stroke-width:1.2; }
    .lbl  { fill:#111; font-size:12.5px; font-weight:700; text-anchor:end; }
    .st   { fill:#111; font-size:12px; font-weight:700; text-anchor:middle; }
    .num  { fill:#111; font-size:11.5px; font-weight:700; text-anchor:middle; }
    .disc { stroke:#111; stroke-width:1.3; fill:#fff; }
    .ah   { fill:#111; }
    .ovl  { stroke:#111; stroke-width:1.1; fill:none; }
    .alt  { stroke:#111; stroke-width:1.6; fill:none; stroke-dasharray:7 5; }
    @media (prefers-color-scheme: dark) {
      .w,.grid,.tick,.dim,.ovl,.alt { stroke:#e8e8e8; }
      .lbl,.st,.num { fill:#e8e8e8; }
      .disc { stroke:#e8e8e8; fill:#161616; }
      .ah { fill:#e8e8e8; }
    }
  </style>""")
        # state ruler
        for s, lab in enumerate(self.labels):
            if lab:
                out.append('  <text class="st" x="%.1f" y="30">%s</text>' % (self.x(s + .5), esc(lab)))
        # full-height guides on every state boundary
        if self.grid:
            for s in range(self.states + 1):
                out.append('  <line class="grid" x1="%.1f" y1="36" x2="%.1f" y2="%.1f"/>'
                           % (self.x(s), self.x(s), h - 16))
        # signal names
        for n in self.order:
            r = self.rows[n]
            lines = r["label"].split("|")
            y0 = r["top"] + AMP / 2 + 4.5 - (len(lines) - 1) * 6.5
            for i, ln in enumerate(lines):
                out.append('  <text class="lbl" x="%.1f" y="%.1f">%s</text>'
                           % (LABEL_W - 14, y0 + i * 13, esc(ln)))
        out += ["  " + p for p in self.parts]
        out.append("</svg>")
        return "\n".join(out) + "\n"

    def write(self, path):
        open(path, "w").write(self.svg())
        return path


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))
