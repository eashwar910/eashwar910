#!/usr/bin/env python3
"""Builds the small pieces: contact chips + section divider."""

INK = "#0A1114"
EDGE = "#1C2C30"
PAPER = "#E9F1EE"
MUTED = "#7E9A9B"
AMBER = "#E8B84B"
VEG = "#D4526E"
SOIL = "#C9A97B"

MONO = 'ui-monospace, "SF Mono", "DejaVu Sans Mono", Menlo, Consolas, monospace'


def chip(label, accent, glyph, width):
    h = 38
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="{width}" height="{h}" role="img" aria-label="{label}">
  <rect x="0.5" y="0.5" width="{width-1}" height="{h-1}" rx="4" fill="{INK}" stroke="{EDGE}"/>
  <rect x="1" y="1" width="4" height="{h-2}" fill="{accent}"/>
  <g fill="none" stroke="{accent}" stroke-width="1.6" transform="translate(20 11)">{glyph}</g>
  <text x="52" y="24" fill="{PAPER}" font-size="12" letter-spacing="2.6"
        font-family='{MONO}'>{label}</text>
</svg>
"""


# hand-drawn 16x16 glyphs
GLYPH_IN = (
    '<rect x="0.8" y="5" width="3" height="10"/>'
    '<circle cx="2.3" cy="1.8" r="1.6"/>'
    '<path d="M7 15 V5 M7 9 C7 5.5 13.2 5.2 13.2 9.6 V15"/>'
)
GLYPH_MAIL = (
    '<rect x="0.8" y="3" width="14" height="10" rx="1"/>'
    '<path d="M1.4 4.2 L7.8 9.4 L14.2 4.2"/>'
)

parts = {
    "chip-linkedin.svg": chip("LINKEDIN", VEG, GLYPH_IN, 158),
    "chip-email.svg": chip("EMAIL", SOIL, GLYPH_MAIL, 132),
}

DIV_W = 1200
divider = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {DIV_W} 12" width="{DIV_W}" height="12" role="presentation">
  <defs>
    <linearGradient id="d" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#2A2A2E"/>
      <stop offset="0.3" stop-color="{SOIL}"/>
      <stop offset="0.66" stop-color="{VEG}"/>
      <stop offset="1" stop-color="#6E2340"/>
    </linearGradient>
  </defs>
  <rect x="0" y="5" width="232" height="2.5" fill="url(#d)"/>
  <line x1="240" y1="6.2" x2="{DIV_W}" y2="6.2" stroke="{EDGE}" stroke-width="1.4"/>
  <g stroke="{AMBER}" stroke-opacity="0.5" stroke-width="1.2">
    <line x1="252" y1="2" x2="252" y2="10"/>
    <line x1="262" y1="4" x2="262" y2="9"/>
  </g>
</svg>
"""
parts["divider.svg"] = divider

for name, body in parts.items():
    with open(f"assets/{name}", "w") as f:
        f.write(body)
    print("wrote assets/" + name)
