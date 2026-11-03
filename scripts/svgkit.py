"""Small helpers for drawing the profile SVGs.

Every graphic is drawn twice, once for GitHub's light theme and once for dark,
and the README picks the right one with <picture>. Animations use SMIL
(<animate>) and CSS keyframes inside the SVG, since a README can't run
JavaScript. They play once on load and then hold.
"""

THEMES = {
    "light": {
        "bg": "#ffffff", "card": "#f6f8fa", "border": "#d0d7de",
        "ink": "#1f2328", "ink2": "#59636e", "muted": "#818b98",
        "grid": "#e1e6eb", "accent": "#2a78d6", "accent_soft": "#2a78d6",
        "fan": "#2a78d6", "fan_op": "0.14", "neutral": "#afb8c1",
    },
    "dark": {
        "bg": "#0d1117", "card": "#161b22", "border": "#30363d",
        "ink": "#f0f6fc", "ink2": "#9198a1", "muted": "#6e7681",
        "grid": "#262c36", "accent": "#3987e5", "accent_soft": "#3987e5",
        "fan": "#3987e5", "fan_op": "0.26", "neutral": "#4a525c",
    },
}

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', "
        "Helvetica, Arial, sans-serif")

EASE = 'calcMode="spline" keyTimes="0;1" keySplines="0.25 0.1 0.25 1"'


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def svg_open(w, h, t, title, extra_css=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">
<title>{esc(title)}</title>
<style>
  text {{ font-family: {FONT}; font-variant-numeric: tabular-nums; }}
  .fade {{ opacity: 0; animation: fade .6s ease-out forwards; }}
  .rise {{ opacity: 0; animation: rise .7s cubic-bezier(.25,.1,.25,1) forwards; }}
  @keyframes fade {{ to {{ opacity: 1; }} }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .fade, .rise {{ animation: none; opacity: 1; }}
  }}
  {extra_css}
</style>
"""


def delay(sec):
    return f'style="animation-delay:{sec:.2f}s"'


def reveal_clip(cid, x, y, w, h, begin, dur):
    """A clip rect that grows left to right, used to draw lines in."""
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="0" height="{h}">'
            f'<animate attributeName="width" from="0" to="{w}" begin="{begin}s" '
            f'dur="{dur}s" fill="freeze" {EASE}/></rect></clipPath>')


def bar(x, base_y, w, h, color, begin, dur=0.8, r=3):
    """Vertical bar that grows up from the baseline."""
    return (f'<rect x="{x:.1f}" y="{base_y}" width="{w:.1f}" height="0" rx="{r}" fill="{color}">'
            f'<animate attributeName="height" from="0" to="{h:.1f}" begin="{begin}s" dur="{dur}s" fill="freeze" {EASE}/>'
            f'<animate attributeName="y" from="{base_y}" to="{base_y - h:.1f}" begin="{begin}s" dur="{dur}s" fill="freeze" {EASE}/>'
            f'</rect>')


def hbar(x, y, w, h, color, begin, dur=0.8, r=3):
    """Horizontal bar that grows right from x."""
    return (f'<rect x="{x}" y="{y:.1f}" width="0" height="{h}" rx="{r}" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{w:.1f}" begin="{begin}s" dur="{dur}s" fill="freeze" {EASE}/>'
            f'</rect>')


def text(x, y, s, size, color, weight=400, anchor="start", cls="", d=None,
         spacing=None):
    extra = f' letter-spacing="{spacing}"' if spacing is not None else ""
    c = f' class="{cls}"' if cls else ""
    st = f" {delay(d)}" if d is not None else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}"{extra}{c}{st}>{esc(s)}</text>')
