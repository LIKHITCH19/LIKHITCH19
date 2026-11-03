"""'How I work' strip: six steps that light up left to right."""

from svgkit import THEMES, svg_open, text

W, H = 1000, 150
STEPS = [
    ("1", "Business question", "the decision at stake"),
    ("2", "Public data", "from the source"),
    ("3", "Clean and check", "vs reported totals"),
    ("4", "SQL and Python", "analysis"),
    ("5", "Model or dashboard", "Excel or Tableau"),
    ("6", "Write-up", "findings and limits"),
]


def flow(t):
    c = THEMES[t]
    o = [svg_open(W, H, t, "How I work: business question, public data, "
                  "clean and check, SQL and Python analysis, Excel model or "
                  "dashboard, write-up")]
    n = len(STEPS)
    gap = 22
    bw = (W - 2 - gap * (n - 1)) / n
    y, bh = 18, 112
    for i, (num, l1, l2) in enumerate(STEPS):
        x = 1 + i * (bw + gap)
        d = 0.15 + i * 0.22
        o.append(f'<g class="rise" style="animation-delay:{d:.2f}s">')
        o.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="{bh}" rx="10" '
                 f'fill="{c["card"]}" stroke="{c["border"]}"/>')
        o.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="3" rx="1.5" '
                 f'fill="{c["accent"]}"/>')
        o.append(text(x + 14, y + 34, num, 13, c["accent"], 700))
        o.append(text(x + 14, y + 64, l1, 13, c["ink"], 600))
        o.append(text(x + 14, y + 84, l2, 11.5, c["ink2"], 400))
        o.append("</g>")
        if i < n - 1:
            ax = x + bw + 4
            ay = y + bh / 2
            o.append(f'<path d="M{ax:.1f},{ay} h{gap-10} m-5,-4 l5,4 l-5,4" '
                     f'fill="none" stroke="{c["muted"]}" stroke-width="1.6" '
                     f'stroke-linecap="round" stroke-linejoin="round" class="fade" '
                     f'style="animation-delay:{d+0.2:.2f}s"/>')
    o.append("</svg>\n")
    return "\n".join(o)


def flow_phone(t):
    """Phone layout: the same six steps as a vertical list."""
    c = THEMES[t]
    rh, gap = 48, 8
    h = 6 * rh + 5 * gap + 2
    o = [svg_open(360, h, t, "How I work: business question, public data, "
                  "clean and check, SQL and Python analysis, model or "
                  "dashboard, write-up")]
    for i, (num, l1, l2) in enumerate(STEPS):
        y = 1 + i * (rh + gap)
        o.append(f'<g class="rise" style="animation-delay:{0.1 + i * 0.15:.2f}s">')
        o.append(f'<rect x="1" y="{y}" width="358" height="{rh}" rx="10" '
                 f'fill="{c["card"]}" stroke="{c["border"]}"/>')
        o.append(f'<rect x="1" y="{y}" width="3" height="{rh}" rx="1.5" fill="{c["accent"]}"/>')
        o.append(text(18, y + 29, num, 13, c["accent"], 700))
        o.append(text(40, y + 21, l1, 13.5, c["ink"], 600))
        o.append(text(40, y + 38, l2, 12, c["ink2"], 400))
        o.append("</g>")
    o.append("</svg>\n")
    return "\n".join(o)
