"""Project tiles: one card per repo, a headline number and a small chart."""

import textwrap

from svgkit import THEMES, svg_open, text, bar, hbar, reveal_clip, esc

W, H = 480, 230
CX0, CX1 = 300, 456          # chart area, x
CY0, CY1 = 52, 178           # chart area, y (CY1 is the baseline)


MW, MH = 360, 330             # phone layout
DISP = (405, 194)             # desktop display size, fits two per row


def frame(t, kicker, title, big, label, caption, chart, aria, m=False):
    """One card. m=True: phone layout. m="w": wide layout for mid-size screens."""
    c = THEMES[t]
    wide = m == "w"           # mid-size screens: one card per row, chart pushed right
    if wide:
        m = False
    w, h = (MW, MH) if m else ((800, H) if wide else (W, H))
    x = 18 if m else 24
    out = [svg_open(w, h, t, aria, disp=None if (m or wide) else DISP)]
    out.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="12" '
               f'fill="{c["card"]}" stroke="{c["border"]}"/>')
    top = 32 if m else 38
    out.append(text(x, top, kicker, 11.5, c["muted"], 600, spacing=1.2,
                    cls="fade", d=0.0))
    out.append(text(x, top + 26, title, 17, c["ink"], 600, cls="fade", d=0.1))
    out.append(text(x, top + 74, big, 34, c["ink"], 700, cls="rise", d=0.35))
    out.append(text(x, top + 98, label, 12.5, c["ink2"], 400, cls="fade", d=0.5))
    lines = textwrap.wrap(" ".join(caption), 24) if m else caption
    y0 = 172 if m else 166
    for i, line in enumerate(lines):
        out.append(text(x, y0 + i * 18, line, 12.5, c["ink2"], 400,
                        cls="fade", d=0.65 + i * 0.05))
    out.append(text(x, h - 22 if m else 210, "Open repo \u2192", 12,
                    c["accent"], 600, cls="fade", d=0.9))
    if m:
        chart = f'<g transform="translate(-114,114)">{chart}</g>'
    elif wide:
        chart = f'<g transform="translate(215,-24) scale(1.15)">{chart}</g>'
    out.append(chart)
    out.append("</svg>\n")
    return "\n".join(out)


def pair_bars(t, items, fmt, vmax, begin=0.5):
    """Two or three vertical bars with value and name labels."""
    c = THEMES[t]
    n = len(items)
    gap = 18
    bw = (CX1 - CX0 - gap * (n - 1)) / n
    bw = min(bw, 52)
    total = bw * n + gap * (n - 1)
    x = CX0 + (CX1 - CX0 - total) / 2
    out = [f'<line x1="{CX0}" y1="{CY1}" x2="{CX1}" y2="{CY1}" stroke="{c["grid"]}"/>']
    for i, (name, v, hi) in enumerate(items):
        h = (CY1 - CY0 - 18) * v / vmax
        color = c["accent"] if hi else c["neutral"]
        bx = x + i * (bw + gap)
        out.append(bar(bx, CY1, bw, h, color, begin + i * 0.15))
        out.append(text(bx + bw / 2, CY1 - h - 7, fmt(v), 12.5, c["ink"], 600,
                        "middle", cls="fade", d=begin + 0.6 + i * 0.15))
        out.append(text(bx + bw / 2, CY1 + 17, name, 11.5, c["ink2"], 400,
                        "middle", cls="fade", d=begin + 0.3))
    return "\n".join(out)


def h_bars(t, items, fmt, vmax, begin=0.5):
    """Horizontal bars, name above each bar, value at the end."""
    c = THEMES[t]
    n = len(items)
    row = (CY1 - CY0 + 10) / n
    maxw = CX1 - CX0 - 44
    out = []
    for i, (name, v, hi) in enumerate(items):
        y = CY0 + i * row
        w = max(3, maxw * v / vmax)
        color = c["accent"] if hi else c["neutral"]
        out.append(text(CX0, y + 10, name, 11.5, c["ink2"], 400, cls="fade",
                        d=begin))
        out.append(hbar(CX0, y + 16, w, 12, color, begin + 0.1 + i * 0.15))
        out.append(text(CX0 + w + 6, y + 26.5, fmt(v), 12, c["ink"], 600,
                        cls="fade", d=begin + 0.7 + i * 0.15))
    return "\n".join(out)


def line(t, cid, labels, values, fmt, vmin, vmax, begin=0.5, dur=1.4,
         mark_all=True, label_idx=None):
    """A single-series line that draws in left to right."""
    c = THEMES[t]
    n = len(values)
    left, right = CX0 + 6, CX1 - 6
    top, bot = CY0 + 14, CY1 - 4

    def px(i):
        return left + (right - left) * i / (n - 1)

    def py(v):
        return bot - (bot - top) * (v - vmin) / (vmax - vmin)

    pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(values))
    out = [f'<defs>{reveal_clip(cid, CX0 - 4, CY0 - 10, CX1 - CX0 + 8, CY1 - CY0 + 20, begin, dur)}</defs>',
           f'<line x1="{CX0}" y1="{CY1}" x2="{CX1}" y2="{CY1}" stroke="{c["grid"]}"/>',
           f'<g clip-path="url(#{cid})">',
           f'<polyline points="{pts}" fill="none" stroke="{c["accent"]}" '
           f'stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>']
    idx = range(n) if mark_all else [n - 1]
    for i in idx:
        out.append(f'<circle cx="{px(i):.1f}" cy="{py(values[i]):.1f}" r="4" '
                   f'fill="{c["accent"]}" stroke="{c["card"]}" stroke-width="2"/>')
    out.append("</g>")
    for i in (label_idx if label_idx is not None else range(n)):
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        out.append(text(px(i), py(values[i]) - 10, fmt(values[i]), 12,
                        c["ink"], 600, anchor, cls="fade",
                        d=begin + dur * (i / max(1, n - 1)) + 0.1))
    for i, lab in labels:
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        out.append(text(px(i), CY1 + 17, lab, 11.5, c["ink2"], 400, anchor,
                        cls="fade", d=begin))
    return "\n".join(out)


# ---- the five static tiles -------------------------------------------------

def chipotle(t, m=False):
    chart = pair_bars(t, [("My forecast", 23.4, True), ("Actual", 23.3, False)],
                      lambda v: f"{v:.1f}%", 23.4)
    return frame(t, "EXCEL · PYTHON · TABLEAU", "Chipotle FP&A forecast",
                 "7 bps", "Q3 2026 restaurant margin miss",
                 ["Forecast published before earnings;",
                  "revenue within 0.9%, EPS exact."],
                 chart, "Chipotle FP&A forecast: Q3 2026 margin forecast 23.4% vs actual 23.3%", m)


def tariffs(t, m=False):
    chart = line(t, "clipT", [(0, "2024"), (1, "Jan '26"), (2, "Aug '26")],
                 [5.3, 25.9, 17.5], lambda v: f"peak {v:.1f}%", 0, 28,
                 label_idx=[1])
    return frame(t, "PYTHON · SQL · CENSUS API", "Furniture tariff exposure",
                 "5.3% → 17.5%", "effective duty rate, US furniture imports",
                 ["41K+ Census trade records; moving", "China to Vietnam cuts cost 6.1%."],
                 chart, "Furniture tariff exposure: effective duty rate rose from 5.3% in 2024 to 17.5% in Aug 2026", m)


def supply_chain(t, m=False):
    chart = h_bars(t, [("Congo, DRC", 24.9, True), ("Mozambique", 18.4, False),
                       ("Vietnam", 0.9, False)], lambda v: f"{v:.1f}%", 24.9)
    return frame(t, "PYTHON · SQL", "Health supply chain delivery",
                 "24.9%", "late deliveries in Congo, DRC",
                 ["10,324 real shipments, 88.5% on", "time; Air Charter ~5x cost per kg."],
                 chart, "Supply chain delivery: late-delivery rate 24.9% in Congo DRC, 18.4% Mozambique, 0.9% Vietnam", m)


def swiggy(t, m=False):
    chart = pair_bars(t, [("As found", 46.19, False), ("Fixed", 53.01, True)],
                      lambda v: f"₹{v:.1f}M", 53.01)
    return frame(t, "EXCEL", "Swiggy sales dashboard",
                 "13%", "of sales hidden by a stuck slicer",
                 ["197K order lines; fixed the filter so", "every KPI counts January."],
                 chart, "Swiggy sales dashboard: total sales corrected from 46.19M to 53.01M rupees", m)


def admissions(t, m=False):
    chart = h_bars(t, [("CGPA", 0.67, True), ("GRE", 0.25, False)],
                   lambda v: f"β {v:.2f}", 0.67)
    return frame(t, "PYTHON · MINITAB", "Graduate admissions model",
                 "R² 78.1%", "chance of admit from GRE and CGPA",
                 ["Corrected my own report: CGPA", "matters ~2.7x more than GRE."],
                 chart, "Graduate admissions regression: R-squared 78.1%, standardized beta CGPA 0.67 vs GRE 0.25", m)


STATIC = {
    "chipotle": chipotle, "tariffs": tariffs, "supply-chain": supply_chain,
    "swiggy": swiggy, "admissions": admissions,
}
