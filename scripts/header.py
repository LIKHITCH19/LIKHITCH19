"""Profile header: name and focus on the left, a forecast chart on the right.

The chart is Chipotle's restaurant-level margin: reported for 2024 and 2025,
then my Oct 30 reforecast for 2026 and 2027 with the Upside/Downside range.
Figures come from the chipotle-fpa-forecast repo.
"""

from svgkit import THEMES, svg_open, text, reveal_clip, EASE

W, H = 1000, 300


MW, MH = 360, 470   # phone layout: text on top, chart below


def header(t, m=False):
    c = THEMES[t]
    w, h = (MW, MH) if m else (W, H)
    o = [svg_open(w, h, t, "Likhit Vardhan Chiliveri, Business Analyst. "
                  "Chart: Chipotle restaurant margin 26.7% (2024), 25.4% (2025), "
                  "forecast 23.4% (2026) and 22.4% (2027, range 20.6% to 23.9%)")]
    o.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" '
             f'fill="{c["card"]}" stroke="{c["border"]}"/>')
    if m:
        o += who_phone(c)
        o.append('<g transform="translate(-485.3,224) scale(0.842)">')
        o += chart(c)
        o.append("</g>")
    else:
        o += who_desktop(c)
        o.append(f'<line x1="574" y1="36" x2="574" y2="{H-36}" stroke="{c["border"]}"/>')
        o += chart(c)
    o.append("</svg>\n")
    return "\n".join(o)


def who_phone(c):
    o = [text(20, 36, "BUSINESS ANALYST \u00b7 FP&A", 11.5, c["accent"], 700,
              spacing=1.4, cls="fade", d=0.0),
         text(20, 76, "Likhit Vardhan", 30, c["ink"], 700, cls="rise", d=0.1),
         text(20, 112, "Chiliveri", 30, c["ink"], 700, cls="rise", d=0.2)]
    for i, line in enumerate(["I build the model, tie every number",
                              "back to its source, and say what it",
                              "means for the business."]):
        o.append(text(20, 146 + i * 20, line, 14, c["ink2"], 400, cls="fade",
                      d=0.5 + i * 0.05))
    o.append(text(20, 218, "FP&A intern @ NOV Inc. \u00b7 Denton, TX", 12,
                  c["muted"], 500, cls="fade", d=0.8))
    o.append(text(20, 236, "Excel, SQL, Python, Tableau, Power BI", 12,
                  c["muted"], 500, cls="fade", d=0.8))
    return o


def who_desktop(c):
    o = []
    o.append(text(44, 62, "BUSINESS ANALYST · FP&A", 13, c["accent"], 700,
                  spacing=1.6, cls="fade", d=0.0))
    o.append(text(44, 108, "Likhit Vardhan", 40, c["ink"], 700, cls="rise", d=0.1))
    o.append(text(44, 154, "Chiliveri", 40, c["ink"], 700, cls="rise", d=0.2))
    o.append(text(44, 196, "I build the model, tie every number back to", 15.5,
                  c["ink2"], 400, cls="fade", d=0.5))
    o.append(text(44, 218, "its source, and say what it means for the business.",
                  15.5, c["ink2"], 400, cls="fade", d=0.55))
    o.append(text(44, 262, "FP&A intern @ NOV Inc.  ·  Denton, TX  ·  Excel, SQL, Python, Tableau, Power BI",
                  13, c["muted"], 500, cls="fade", d=0.8))
    return o


def chart(c):
    o = []
    x0, x1, yT, yB = 600, 950, 88, 228
    vmin, vmax = 19, 28
    xs = [x0 + 20, x0 + 120, x0 + 220, x0 + 320]

    def py(v):
        return yB - (yB - yT) * (v - vmin) / (vmax - vmin)

    o.append(text(x0, 52, "Chipotle restaurant margin", 14, c["ink"], 600,
                  cls="fade", d=0.3))
    o.append(text(x0, 71, "reported, then my forecast", 12.5, c["ink2"], 400,
                  cls="fade", d=0.35))
    for v in (20, 24, 28):
        o.append(f'<line x1="{x0}" y1="{py(v):.1f}" x2="{x1}" y2="{py(v):.1f}" '
                 f'stroke="{c["grid"]}" class="fade" {delay_attr(0.3)}/>')
        o.append(text(x1 + 6, py(v) + 4, f"{v}%", 11, c["muted"], 400,
                      cls="fade", d=0.3))

    act = [26.7, 25.4]
    fc = [25.4, 23.4, 22.4]
    up, dn = 23.9, 20.6
    o.append("<defs>")
    o.append(reveal_clip("clipA", x0, 60, xs[1] - x0 + 6, 200, 0.6, 0.8))
    o.append(reveal_clip("clipF", xs[1], 60, x1 - xs[1] + 10, 200, 1.35, 1.0))
    o.append("</defs>")

    # range fan for 2027
    fan = (f"{xs[2]},{py(fc[1]):.1f} {xs[3]},{py(up):.1f} "
           f"{xs[3]},{py(dn):.1f}")
    o.append(f'<polygon points="{fan}" fill="{c["fan"]}" opacity="0">'
             f'<animate attributeName="opacity" from="0" to="{c["fan_op"]}" begin="2.2s" '
             f'dur="0.6s" fill="freeze"/></polygon>')

    o.append(f'<g clip-path="url(#clipA)"><polyline points="{xs[0]},{py(act[0]):.1f} '
             f'{xs[1]},{py(act[1]):.1f}" fill="none" stroke="{c["ink"]}" '
             f'stroke-width="2.5" stroke-linecap="round"/>')
    for i, v in enumerate(act):
        o.append(f'<circle cx="{xs[i]}" cy="{py(v):.1f}" r="4.5" fill="{c["ink"]}" '
                 f'stroke="{c["card"]}" stroke-width="2"/>')
    o.append("</g>")

    o.append(f'<g clip-path="url(#clipF)"><polyline points="'
             + " ".join(f"{xs[i+1]},{py(v):.1f}" for i, v in enumerate(fc))
             + f'" fill="none" stroke="{c["accent"]}" stroke-width="2.5" '
               f'stroke-dasharray="6 5" stroke-linecap="round"/>')
    for i, v in enumerate(fc[1:]):
        o.append(f'<circle cx="{xs[i+2]}" cy="{py(v):.1f}" r="4.5" fill="{c["accent"]}" '
                 f'stroke="{c["card"]}" stroke-width="2"/>')
    o.append("</g>")

    labels = [(0, act[0], "26.7%", 0.9, c["ink"]), (1, act[1], "25.4%", 1.3, c["ink"]),
              (2, fc[1], "23.4%", 1.9, c["accent"]), (3, fc[2], "22.4%", 2.3, c["accent"])]
    for i, v, s, d, col in labels:
        o.append(text(xs[i], py(v) - 12, s, 12.5, c["ink"], 600, "middle",
                      cls="fade", d=d))
    o.append(text(xs[3] - 10, py(up) - 6, "range", 11, c["muted"], 400, "end",
                  cls="fade", d=2.5))
    for i, yr in enumerate(["2024", "2025", "2026", "2027"]):
        o.append(text(xs[i], yB + 20, yr, 12, c["ink2"], 400, "middle",
                      cls="fade", d=0.4))
    # legend
    ly = yB + 46
    o.append(f'<line x1="{x0}" y1="{ly-4}" x2="{x0+18}" y2="{ly-4}" stroke="{c["ink"]}" stroke-width="2.5" class="fade" {delay_attr(0.5)}/>')
    o.append(text(x0 + 24, ly, "Reported", 12, c["ink2"], 400, cls="fade", d=0.5))
    o.append(f'<line x1="{x0+96}" y1="{ly-4}" x2="{x0+114}" y2="{ly-4}" stroke="{c["accent"]}" stroke-width="2.5" stroke-dasharray="6 5" class="fade" {delay_attr(0.5)}/>')
    o.append(text(x0 + 120, ly, "My forecast (Oct 30)", 12, c["ink2"], 400,
                  cls="fade", d=0.5))
    return o


def delay_attr(sec):
    return f'style="animation-delay:{sec:.2f}s"'
