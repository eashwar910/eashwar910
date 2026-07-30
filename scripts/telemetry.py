#!/usr/bin/env python3
"""Builds assets/telemetry.svg from the GitHub API.

No third-party badge or stats service: this reads your own public data and
draws the panel itself, in the same visual language as the header.

Usage:  python3 scripts/telemetry.py <username>
Auth:   set GITHUB_TOKEN to raise the rate limit (the workflow does this).
"""
import json
import os
import sys
import urllib.error
import urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GH_USER", "eashwar910")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
MAX_REPOS_FOR_BYTES = 60

INK = "#0A1114"
EDGE = "#1C2C30"
PAPER = "#E9F1EE"
MUTED = "#7E9A9B"
AMBER = "#E8B84B"
BANDS = ["#D4526E", "#C9A97B", "#A8385A", "#7E9A9B", "#8A2C4C", "#B39468", "#6E2340"]
REST = "#2A3A3E"
MONO = 'ui-monospace, "SF Mono", "DejaVu Sans Mono", Menlo, Consolas, monospace'


def get(path):
    req = urllib.request.Request(API + path, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USER}-profile-telemetry",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def collect():
    user = get(f"/users/{USER}")
    repos, page = [], 1
    while page <= 4:
        batch = get(f"/users/{USER}/repos?per_page=100&type=owner&sort=pushed&page={page}")
        repos += batch
        if len(batch) < 100:
            break
        page += 1

    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)

    # Language weight by bytes of code, which is fairer than counting repos.
    bytes_by_lang = {}
    for r in own[:MAX_REPOS_FOR_BYTES]:
        try:
            for lang, n in get(f"/repos/{USER}/{r['name']}/languages").items():
                bytes_by_lang[lang] = bytes_by_lang.get(lang, 0) + n
        except urllib.error.URLError:
            # Rate-limited or unreachable: fall back to the repo's primary
            # language, weighted by repository size.
            lang = r.get("language")
            if lang:
                bytes_by_lang[lang] = bytes_by_lang.get(lang, 0) + max(r.get("size", 1), 1)

    pushed = max((r.get("pushed_at") or "" for r in own), default="")
    return {
        "repos": len(own),
        "stars": stars,
        "followers": user.get("followers", 0),
        "since": (user.get("created_at") or "")[:4],
        "langs": sorted(bytes_by_lang.items(), key=lambda kv: -kv[1]),
        "pushed": pushed[:10],
    }


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(d):
    W, H = 900, 320
    total = sum(n for _, n in d["langs"]) or 1
    top = d["langs"][:6]
    other = total - sum(n for _, n in top)

    RX, RW = 452, 408          # right column: band composition
    segs, x = [], float(RX)
    for i, (lang, n) in enumerate(top):
        w = RW * n / total
        segs.append(f'<rect x="{x:.1f}" y="98" width="{max(w, 1):.1f}" height="24" fill="{BANDS[i % len(BANDS)]}"/>')
        x += w
    if other > 0:
        segs.append(f'<rect x="{x:.1f}" y="98" width="{max(RX + RW - x, 1):.1f}" height="24" fill="{REST}"/>')

    legend = []
    for i, (lang, n) in enumerate(top):
        ly = 152 + i * 24
        pct = 100.0 * n / total
        legend.append(
            f'<rect x="{RX}" y="{ly - 9}" width="10" height="10" fill="{BANDS[i % len(BANDS)]}"/>'
            f'<text x="{RX + 20}" y="{ly}" fill="{PAPER}" fill-opacity="0.86" font-size="13">{esc(lang)}</text>'
            f'<text x="{RX + RW}" y="{ly}" fill="{MUTED}" font-size="12.5" text-anchor="end">{pct:4.1f}%</text>'
        )

    facts = [
        ("PUBLIC REPOSITORIES", d["repos"]),
        ("STARS RECEIVED", d["stars"]),
        ("FOLLOWERS", d["followers"]),
        ("ON GITHUB SINCE", d["since"]),
    ]
    rows = []
    for i, (k, v) in enumerate(facts):
        y = 106 + i * 46
        rows.append(
            f'<text x="40" y="{y}" fill="{MUTED}" font-size="11.5" letter-spacing="2">{k}</text>'
            f'<text x="392" y="{y}" fill="{PAPER}" font-size="23" font-weight="700" text-anchor="end">{v}</text>'
            f'<line x1="40" y1="{y + 14}" x2="392" y2="{y + 14}" stroke="{EDGE}"/>'
        )

    nl = "\n      "
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub activity summary for {esc(USER)}">
  <title>{esc(USER)} — pass summary</title>
  <g font-family='{MONO}'>
    <rect width="{W}" height="{H}" rx="10" fill="{INK}"/>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="none" stroke="{EDGE}"/>

    <text x="40" y="54" fill="{MUTED}" font-size="11.5" letter-spacing="3.2">PASS SUMMARY / {esc(USER)}</text>
    <line x1="422" y1="38" x2="422" y2="{H-58}" stroke="{EDGE}"/>
    <text x="{RX}" y="54" fill="{MUTED}" font-size="11.5" letter-spacing="3.2">BAND COMPOSITION</text>

    {nl.join(rows)}

    <text x="{RX}" y="86" fill="{PAPER}" fill-opacity="0.7" font-size="12.5">{len(d['langs'])} languages, weighted by bytes of code</text>
    {nl.join(segs)}
    {nl.join(legend)}

    <text x="40" y="{H-22}" fill="{MUTED}" fill-opacity="0.8" font-size="10.5" letter-spacing="1.6">LAST PUSH {esc(d['pushed'])} &#183; {d['repos']} REPOSITORIES SCANNED</text>
    <text x="{W-40}" y="{H-22}" fill="{MUTED}" fill-opacity="0.8" font-size="10.5" letter-spacing="1.6" text-anchor="end">scripts/telemetry.py</text>
  </g>
</svg>
"""


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    data = collect()
    with open("assets/telemetry.svg", "w") as f:
        f.write(render(data))
    print(f"wrote assets/telemetry.svg  repos={data['repos']} langs={len(data['langs'])}")
