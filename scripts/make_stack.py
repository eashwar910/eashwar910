#!/usr/bin/env python3
"""Renders the stack panel as aligned monospace text (paste into README)."""
import textwrap

INNER = 74          # characters between the vertical rules
LABEL = 15          # label column width
GUTTER = 2

GROUPS = [
    ("LANGUAGES", ["python", "c", "java", "typescript", "javascript", "php"]),
    ("IMAGERY / ML", ["pytorch", "tensorflow", "keras", "opencv",
                      "scikit-learn", "numpy", "pandas", "matplotlib"]),
    ("INTERFACES", ["react native", "expo", "tailwind", "node.js",
                    "javafx", "html5", "css3"]),
    ("DATA + CLOUD", ["postgres", "supabase", "firebase", "google cloud",
                      "digitalocean", "vercel", "netlify"]),
    ("WORKBENCH", ["git", "github actions", "npm", "anaconda"]),
]

W = INNER - GUTTER - LABEL - 1      # width available for instrument text
lines = []


def row(label, text):
    return f"│{' ' * GUTTER}{label:<{LABEL}}{text:<{W}} │"


lines.append("╭" + "─" * INNER + "╮")
lines.append(row("BAND", "INSTRUMENTS"))
lines.append("├" + "─" * INNER + "┤")

def pack(items):
    """Wrap on ' · ' boundaries so no instrument name is ever split."""
    out, cur = [], ""
    for it in items:
        cand = it if not cur else f"{cur} · {it}"
        if len(cand) + 2 > W and cur:
            out.append(cur + " ·")
            cur = it
        else:
            cur = cand
    out.append(cur)
    return out


for i, (name, items) in enumerate(GROUPS):
    wrapped = pack(items)
    for j, part in enumerate(wrapped):
        lines.append(row(name if j == 0 else "", part))
    if i != len(GROUPS) - 1:
        lines.append("│" + " " * INNER + "│")

lines.append("╰" + "─" * INNER + "╯")

out = "\n".join(lines)
print(out)
with open("assets/stack.txt", "w") as f:
    f.write(out + "\n")
