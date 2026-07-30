#!/usr/bin/env python3
"""Builds assets/banner.svg -- a false-colour (CIR) field mosaic header.

Everything here is hand-authored geometry: jittered field parcels, a river,
a scan sweep. No external services, no badge APIs.
"""
import random

random.seed(4108)

W, H = 1200, 340

INK = "#0A1114"
EDGE = "#1C2C30"
WATER = "#123038"
PAPER = "#E9F1EE"
MUTED = "#7E9A9B"
AMBER = "#E8B84B"

# False-colour infrared palette: vigorous canopy reads magenta/red,
# bare soil reads pale tan, water reads near-black teal.
VEG = ["#D4526E", "#BE4262", "#A8385A", "#8A2C4C", "#6E2340", "#E0708A"]
SOIL = ["#C9A97B", "#B39468", "#8E7550"]

TX, TY, TW, TH = 604, 40, 552, 260  # mosaic tile


def parcels():
    """Irregular farm plots: rows of jittered quads, some rows strip-cropped."""
    out = []
    y = TY
    rows = [46, 38, 52, 44, 40, 40]
    for ri, rh in enumerate(rows):
        strip = ri in (1, 4)  # long thin plots
        n = 3 if strip else random.randint(4, 6)
        xs = [TX]
        for i in range(1, n):
            xs.append(TX + int(TW * i / n) + random.randint(-26, 26))
        xs.append(TX + TW)
        for i in range(n):
            x0, x1 = xs[i], xs[i + 1]
            j = lambda: random.randint(-7, 7)
            pts = [
                (x0 + j(), y + j()),
                (x1 + j(), y + j()),
                (x1 + j(), y + rh + j()),
                (x0 + j(), y + rh + j()),
            ]
            if strip:
                fill = random.choice(SOIL) if random.random() < 0.45 else random.choice(VEG)
            else:
                fill = random.choice(VEG) if random.random() < 0.72 else random.choice(SOIL)
            op = round(random.uniform(0.62, 1.0), 2)
            d = " ".join(f"{p[0]},{p[1]}" for p in pts)
            out.append(f'<polygon points="{d}" fill="{fill}" fill-opacity="{op}"/>')
        y += rh
    return "\n      ".join(out)


def ticks():
    """Coordinate ticks, like the frame of a plotted raster."""
    t = []
    for i in range(1, 12):
        x = TX + TW * i / 12
        t.append(f'<line x1="{x:.0f}" y1="{TY}" x2="{x:.0f}" y2="{TY+6}"/>')
        t.append(f'<line x1="{x:.0f}" y1="{TY+TH-6}" x2="{x:.0f}" y2="{TY+TH}"/>')
    for i in range(1, 6):
        y = TY + TH * i / 6
        t.append(f'<line x1="{TX}" y1="{y:.0f}" x2="{TX+6}" y2="{y:.0f}"/>')
        t.append(f'<line x1="{TX+TW-6}" y1="{y:.0f}" x2="{TX+TW}" y2="{y:.0f}"/>')
    return "\n      ".join(t)


def brackets():
    L = 18
    c = [
        (TX, TY, 1, 1),
        (TX + TW, TY, -1, 1),
        (TX, TY + TH, 1, -1),
        (TX + TW, TY + TH, -1, -1),
    ]
    out = []
    for x, y, sx, sy in c:
        out.append(f'<path d="M{x} {y+sy*L} L{x} {y} L{x+sx*L} {y}"/>')
    return "\n      ".join(out)


SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Eashwar — computer science and AI student working on satellite imagery, image processing and ag-tech">
  <title>eashwar910 — false-colour scene header</title>
  <defs>
    <clipPath id="tile"><rect x="{TX}" y="{TY}" width="{TW}" height="{TH}"/></clipPath>
    <clipPath id="frame"><rect x="0" y="0" width="{W}" height="{H}" rx="10"/></clipPath>
    <linearGradient id="ramp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#2A2A2E"/>
      <stop offset="0.28" stop-color="#C9A97B"/>
      <stop offset="0.62" stop-color="#D4526E"/>
      <stop offset="1" stop-color="#6E2340"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#E9F1EE" stop-opacity="0"/>
      <stop offset="0.72" stop-color="#E9F1EE" stop-opacity="0.10"/>
      <stop offset="1" stop-color="#E9F1EE" stop-opacity="0.34"/>
    </linearGradient>
    <linearGradient id="vign" x1="0" y1="0" x2="1" y2="0.4">
      <stop offset="0" stop-color="{INK}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0"/>
    </linearGradient>
    <style>
      .mono {{ font-family: ui-monospace, "SF Mono", "DejaVu Sans Mono", Menlo, Consolas, monospace; }}
      .sweep {{ animation: pass 7s linear infinite; }}
      .pulse {{ animation: blink 2.4s ease-in-out infinite; }}
      @keyframes pass {{
        0%   {{ transform: translateX(-140px); }}
        100% {{ transform: translateX({TW + 20}px); }}
      }}
      @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50%      {{ opacity: 0.15; }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .sweep, .pulse {{ animation: none; }}
        .sweep {{ opacity: 0; }}
      }}
    </style>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{INK}"/>

    <!-- scene tile -->
    <g clip-path="url(#tile)">
      {parcels()}
      <!-- river -->
      <path d="M{TX-10} {TY+64} C {TX+120} {TY+96}, {TX+150} {TY+150}, {TX+280} {TY+168}
               S {TX+430} {TY+186}, {TX+TW+10} {TY+238}"
            fill="none" stroke="{WATER}" stroke-width="9" stroke-opacity="0.95"/>
      <path d="M{TX-10} {TY+64} C {TX+120} {TY+96}, {TX+150} {TY+150}, {TX+280} {TY+168}
               S {TX+430} {TY+186}, {TX+TW+10} {TY+238}"
            fill="none" stroke="#0B1F26" stroke-width="3"/>
      <!-- service road -->
      <path d="M{TX+96} {TY-6} L{TX+150} {TY+TH+6}" stroke="#0A1114" stroke-width="4" stroke-opacity="0.7"/>
      <path d="M{TX-6} {TY+112} L{TX+TW+6} {TY+92}" stroke="#0A1114" stroke-width="3" stroke-opacity="0.55"/>
      <!-- pixel grid, faint: this is raster data, not a photograph -->
      <g stroke="{INK}" stroke-opacity="0.16">
        {"".join(f'<line x1="{TX + i*8}" y1="{TY}" x2="{TX + i*8}" y2="{TY+TH}"/>' for i in range(1, TW // 8))}
        {"".join(f'<line x1="{TX}" y1="{TY + i*8}" x2="{TX+TW}" y2="{TY + i*8}"/>' for i in range(1, TH // 8))}
      </g>
      <rect x="{TX}" y="{TY}" width="140" height="{TH}" fill="url(#vign)"/>
      <!-- scan sweep -->
      <g class="sweep">
        <rect x="{TX}" y="{TY}" width="130" height="{TH}" fill="url(#sweep)"/>
        <rect x="{TX+130}" y="{TY}" width="1.5" height="{TH}" fill="{PAPER}" fill-opacity="0.6"/>
      </g>
    </g>
    <g stroke="{AMBER}" stroke-opacity="0.55" stroke-width="1">{ticks()}</g>
    <g stroke="{PAPER}" stroke-opacity="0.5" stroke-width="1.5" fill="none">{brackets()}</g>

    <!-- metadata block -->
    <g class="mono">
      <text x="48" y="72" fill="{MUTED}" font-size="11" letter-spacing="3.4">SCENE 001 / PROFILE / eashwar910</text>
      <text x="46" y="146" fill="{PAPER}" font-size="60" font-weight="700" letter-spacing="2">EASHWAR</text>
      <line x1="48" y1="172" x2="524" y2="172" stroke="{EDGE}" stroke-width="1"/>
      <text x="48" y="199" fill="{AMBER}" font-size="12.5" letter-spacing="2.6">COMPUTER SCIENCE + AI &#183; YEAR 02</text>
      <text x="48" y="226" fill="{PAPER}" fill-opacity="0.72" font-size="14" letter-spacing="0.4">satellite imagery &#183; image processing &#183; ag&#8209;tech</text>

      <!-- band ramp legend -->
      <rect x="48" y="258" width="300" height="9" fill="url(#ramp)" rx="1"/>
      <text x="48" y="285" fill="{MUTED}" font-size="10" letter-spacing="2">BARE SOIL</text>
      <text x="348" y="285" fill="{MUTED}" font-size="10" letter-spacing="2" text-anchor="end">DENSE CANOPY</text>

      <circle class="pulse" cx="404" cy="262" r="4" fill="{AMBER}"/>
      <text x="418" y="266" fill="{MUTED}" font-size="10.5" letter-spacing="2">ACQUIRING</text>

      <text x="{TX}" y="{TY+TH+24}" fill="{MUTED}" fill-opacity="0.85" font-size="10" letter-spacing="2">COMPOSITE B08 &#183; B04 &#183; B03</text>
      <text x="{TX+TW}" y="{TY+TH+24}" fill="{MUTED}" fill-opacity="0.85" font-size="10" letter-spacing="2" text-anchor="end">DRAWN BY HAND, NOT GENERATED</text>
    </g>

    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{EDGE}" stroke-width="1"/>
  </g>
</svg>
"""

with open("assets/banner.svg", "w") as f:
    f.write(SVG)
print("wrote assets/banner.svg")
