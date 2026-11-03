"""Redraw the live tile from BLS data.

Series CUUR0000SEFV: CPI-U, food away from home, US city average, not
seasonally adjusted. I pull the monthly index, work out the year-over-year
change for the last 24 months, and draw it. Runs on a schedule in GitHub
Actions (.github/workflows/live-tile.yml). Standard library only.

If BLS doesn't answer, the script leaves the last good tile alone.
"""

import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

from svgkit import THEMES
from tiles import frame, line

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "cpi_food_away_from_home.json"
SERIES = "CUUR0000SEFV"
URL = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch():
    this_year = date.today().year
    body = json.dumps({"seriesid": [SERIES],
                       "startyear": str(this_year - 3),
                       "endyear": str(this_year)}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json",
        "User-Agent": "profile-live-tile (github.com/LIKHITCH19)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if payload.get("status") != "REQUEST_SUCCEEDED":
        raise RuntimeError(f"BLS said: {payload.get('status')} {payload.get('message')}")
    rows = payload["Results"]["series"][0]["data"]
    out = {}
    for row in rows:
        p = row["period"]
        if not p.startswith("M") or p == "M13":
            continue
        try:
            out[f"{row['year']}-{p[1:]}"] = float(row["value"])
        except ValueError:
            continue          # BLS uses "-" for missing months
    return dict(sorted(out.items()))


def yoy(index):
    pts = []
    for k, v in index.items():
        y, m = k.split("-")
        prev = f"{int(y) - 1}-{m}"
        if prev in index:
            pts.append((k, (v / index[prev] - 1) * 100))
    return pts[-24:]


def nice_month(k, short=False):
    y, m = k.split("-")
    return f"{MONTHS[int(m) - 1]} '{y[2:]}" if short else f"{MONTHS[int(m) - 1]} {y}"


def render(t, pts):
    vals = [round(v, 1) for _, v in pts]
    lo, hi = min(vals), max(vals)
    pad = max(0.4, (hi - lo) * 0.25)
    n = len(pts)
    chart = line(t, "clipL", [(0, nice_month(pts[0][0], True)),
                              (n - 1, nice_month(pts[-1][0], True))],
                 vals, lambda v: f"{v:+.1f}%", lo - pad, hi + pad,
                 mark_all=False, label_idx=[])
    latest = vals[-1]
    return frame(t, "LIVE · BLS API · GITHUB ACTIONS",
                 "Restaurant menu inflation", f"{latest:+.1f}%",
                 f"CPI food away from home, y/y, {nice_month(pts[-1][0])}",
                 ["Redraws itself from BLS each week.",
                  "Price is my Chipotle model's top lever."],
                 chart,
                 f"Restaurant menu inflation: CPI food away from home up {latest:.1f}% "
                 f"year over year in {nice_month(pts[-1][0])}")


def main():
    try:
        index = fetch()
    except Exception as e:  # network or API problem: keep the old tile
        print(f"BLS fetch failed, keeping the current tile: {e}")
        return 0
    pts = yoy(index)
    if len(pts) < 12:
        print(f"Only {len(pts)} y/y points, keeping the current tile")
        return 0
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps({"series": SERIES, "index": index}, indent=1) + "\n")
    for t in THEMES:
        (ROOT / "assets" / f"live-{t}.svg").write_text(render(t, pts))
    print(f"Latest: {pts[-1][0]} {pts[-1][1]:+.2f}% y/y")
    return 0


if __name__ == "__main__":
    sys.exit(main())
