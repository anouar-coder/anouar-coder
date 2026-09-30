#!/usr/bin/env python3
"""Generate assets/terminal.svg - an animated velvet terminal window."""

ESC = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}

def esc(s):
    return "".join(ESC.get(c, c) for c in s)

CMD_PROMPT = "#C77BA8"   # rose
CMD_TEXT = "#F0D98C"     # champagne gold
OUT_TEXT = "#D9C4DC"     # soft lavender

LINES = [
    ("cmd", "whoami"),
    ("out", "Anwar Ben Brahim — final-year Computer Engineering @ ENIT"),
    ("gap", ""),
    ("cmd", "focus"),
    ("out", "AI for cybersecurity · network anomaly & intrusion detection · explainable AI"),
    ("gap", ""),
    ("cmd", "currently"),
    ("out", "building an AI-driven MDR platform · open to internships & research collaborations"),
]

BAR_H = 36
FIRST_Y = 66
LH = 24
PAD_X = 28
W = 800
FS = 14

CHARS_PER_SEC = 62          # typewriter speed
LINE_PAUSE = 0.22           # extra pause after a command line


def build_line(text, delay_ms, color, width_chars):
    """Static, always-visible line.

    Animation is a boot-up reveal: it animates FROM faint TO full opacity, so if
    animations never run the text is still fully legible (base opacity is 1).
    """
    return (
        f'<text class="ln" x="{PAD_X}" y="{text[1]}" fill="{color}"'
        f' style="animation-delay:{delay_ms:.0f}ms">{esc(text[0])}</text>'
    )


def main():
    delay_ms = 260
    body = []
    y = FIRST_Y

    for kind, text in LINES:
        if kind == "gap":
            body.append("")
            y += LH
            continue

        if kind == "cmd":
            # rose "$" then champagne-gold command
            fill = CMD_TEXT
            content = f'<tspan fill="{CMD_PROMPT}">$</tspan><tspan> {esc(text)}</tspan>'
        else:
            fill = OUT_TEXT
            content = esc(text)

        body.append(
            f'<text class="ln" x="{PAD_X}" y="{y}" fill="{fill}" xml:space="preserve"'
            f' style="animation-delay:{delay_ms:.0f}ms">{content}</text>'
        )
        delay_ms += 520
        y += LH

    H = FIRST_Y + LH * (len(body) - 1) + 22
    total_ms = delay_ms
    last_len = len(LINES[-1][1])
    cur_x = PAD_X + (last_len + 2) * FS * 0.602 + 2

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"
     role="img" aria-label="Terminal: whoami, focus, currently">
  <style>
    text {{
      font-family: 'JetBrains Mono', 'Fira Code', Menlo, Consolas, 'DejaVu Sans Mono', monospace;
      font-size: {FS}px;
      white-space: pre;
    }}
    /* Base state is fully visible: if animations do not run, text stays legible.
       The animation only reveals it from faint -> full (terminal boot-up). */
    .ln {{ opacity: 1; animation: boot 420ms ease-out both; }}
    @keyframes boot {{ from {{ opacity: 0.12; }} to {{ opacity: 1; }} }}
    #cur {{ animation: blink 1.05s step-end infinite; animation-delay: {total_ms:.0f}ms; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
    #sheen {{ animation: sweep 7s ease-in-out infinite; }}
    @keyframes sweep {{
      0%   {{ transform: translateX(-160px); }}
      55%  {{ transform: translateX({W}px); }}
      100% {{ transform: translateX({W}px); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .ln, #cur, #sheen {{ animation: none; }}
    }}
  </style>

  <defs>
    <clipPath id="bar"><rect x="0" y="0" width="{W}" height="{BAR_H}"/></clipPath>
    <linearGradient id="sheenGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F6E7B4" stop-opacity="0"/>
      <stop offset="50%" stop-color="#F6E7B4" stop-opacity="0.30"/>
      <stop offset="100%" stop-color="#F6E7B4" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="velvet" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#1C0922"/>
      <stop offset="100%" stop-color="#120618"/>
    </linearGradient>
  </defs>

  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="url(#velvet)" stroke="#4A0C45"/>
  <g clip-path="url(#bar)">
    <rect x="0" y="0" width="{W}" height="{BAR_H}" fill="#2A0620"/>
    <rect id="sheen" x="-160" y="0" width="150" height="{BAR_H}" fill="url(#sheenGrad)"/>
  </g>
  <line x1="0" y1="{BAR_H}" x2="{W}" y2="{BAR_H}" stroke="#4A0C45" stroke-width="1"/>

  <circle cx="22" cy="18" r="5" fill="#C77BA8" opacity="0.9"/>
  <circle cx="40" cy="18" r="5" fill="#F0D98C" opacity="0.9"/>
  <circle cx="58" cy="18" r="5" fill="#7FB685" opacity="0.9"/>
  <text x="{W / 2}" y="22" text-anchor="middle" font-size="12" fill="#B99BB0">anwar@profile ~</text>

  <g>
{chr(10).join(("    " + b) if b else "" for b in body)}
  </g>

  <rect id="cur" x="{cur_x:.0f}" y="{FIRST_Y + LH * (len(body) - 1) - 12}" width="8" height="16" fill="#F0D98C"/>
</svg>
'''

    with open("assets/terminal.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote assets/terminal.svg")
    print(f"  viewBox   : 0 0 {W} {H}")
    print(f"  typed over: {total_ms / 1000:.2f}s")
    print(f"  cursor at : x={cur_x:.0f}  (max line width {max(len(t) for _, t in LINES) * FS * 0.602 + PAD_X:.0f} of {W})")


if __name__ == "__main__":
    main()