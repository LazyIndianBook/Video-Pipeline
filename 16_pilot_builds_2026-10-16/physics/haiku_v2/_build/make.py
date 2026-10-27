#!/usr/bin/env python3
"""make.py: assemble scenes/sNN.html from _build fragments. The runtime is inlined into every scene (no external script)."""
import pathlib

B = pathlib.Path(__file__).resolve().parent
OUT = B.parent / "scenes"
head = (B / "shell_head.html").read_text(encoding="utf-8")
runtime = (B / "runtime.js").read_text(encoding="utf-8")
BOT = ('<div id="think_plate" class="plate"><span data-fx="display.ui.think_prompt"></span></div>\n')
DISC = ('<div id="disclosure" class="disc" data-rv="1"></div>\n')
TAIL = '</div></div>\n<div id="bot" class="zone">\n' + BOT + '{DISC}' + '</div>\n</div>\n<script>\n'
END = '</script>\n</body>\n</html>\n'
for n in ("01", "02", "03", "04", "05"):
    hero = (B / f"hero_s{n}.html").read_text(encoding="utf-8")
    tail = TAIL.replace("{DISC}", DISC if n == "05" else "")
    h = head.replace("__SCENE__", f"s{n}")
    if n in ("01", "02", "04"):
        h = h.replace('<div id="hero">', '<div id="hero" style="top:150px">')
    html = h + hero + tail + runtime + END
    (OUT / f"s{n}.html").write_text(html, encoding="utf-8")
    print("wrote", f"s{n}.html", len(html))
