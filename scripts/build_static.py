"""Write the header and project tiles to assets/. Run: python scripts/build_static.py"""

from pathlib import Path

from svgkit import THEMES, svg_open, text
from header import header
from tiles import STATIC, W, H

ASSETS = Path(__file__).resolve().parents[1] / "assets"


def placeholder(t):
    """Shown only until the first scheduled run fills in the live tile."""
    c = THEMES[t]
    return "\n".join([
        svg_open(W, H, t, "Live tile: waiting for the first BLS update"),
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="{c["card"]}" stroke="{c["border"]}"/>',
        text(24, 38, "LIVE · BLS API · GITHUB ACTIONS", 11.5, c["muted"], 600, spacing=1.2),
        text(24, 64, "Restaurant menu inflation", 17, c["ink"], 600),
        text(24, 116, "Updating…", 30, c["ink2"], 600),
        "</svg>\n"])


def main():
    ASSETS.mkdir(exist_ok=True)
    for t in THEMES:
        (ASSETS / f"header-{t}.svg").write_text(header(t))
        for name, fn in STATIC.items():
            (ASSETS / f"{name}-{t}.svg").write_text(fn(t))
        live = ASSETS / f"live-{t}.svg"
        if not live.exists():
            live.write_text(placeholder(t))
    print("wrote", len(list(ASSETS.glob("*.svg"))), "svgs")


if __name__ == "__main__":
    main()
