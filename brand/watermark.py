"""Wanderlogika watermark: fixed brand setting for every HyperFrames edit in this repo.

Usage in a project's build.py (project folder sits next to brand/):
    import sys; sys.path.insert(0, "..")
    from brand.watermark import watermark
    WM = watermark(TOTAL, end_start=VID_END)   # dict with css / html / end_html / js
    # put WM["css"] in <style>, WM["html"] before #flash, WM["end_html"] inside #end, WM["js"] in the timeline script.

Layers (see cymbo/preview/watermark_preview_v2.jpg):
  1. Main mark: "Wanderlogika", Montserrat ExtraBold Italic, white 30 %, centred at chin level,
     slow zoom 1.0 -> 1.12 -> 1.0 twice every 5 s (2.5 s per pulse), repeating to the end.
  2. End-card handle: "by @wanderlogika" under the CTA.
  3. Hidden proof layer: tiled, rotated "wanderlogika" at 4 % opacity (visible when contrast is boosted).
"""
import os, shutil

NAME = "Wanderlogika"
HANDLE = "@wanderlogika"
OPACITY = 0.30
SIZE = 64          # px
TOP = 1095         # px, chin level, just above captions (y ~1230)
ZOOM = 1.12
PULSE = 2.5        # s per zoom in+out (2 pulses per 5 s)
TILE_OPACITY = 0.045
FONT = "montserrat-800-italic.woff2"
HERE = os.path.dirname(os.path.abspath(__file__))


def install_font(project_dir="."):
    """Copy the watermark font into <project>/fonts/ and register it in fonts.css (idempotent)."""
    fd = os.path.join(project_dir, "fonts"); os.makedirs(fd, exist_ok=True)
    shutil.copy(os.path.join(HERE, "fonts", FONT), os.path.join(fd, FONT))
    css = os.path.join(fd, "fonts.css")
    rule = ('@font-face{font-family:"F WM Montserrat";src:url("' + FONT + '") format("woff2");'
            'font-weight:800;font-style:italic;font-display:block}\n'
            '.f-wm{font-family:"F WM Montserrat";font-weight:800;font-style:italic}\n')
    old = open(css).read() if os.path.exists(css) else ""
    if "F WM Montserrat" not in old:
        open(css, "a").write(("\n" if old and not old.endswith("\n") else "") + rule)


def watermark(total, end_start=None, end_color="#3c4a1c", tile_font_class="f-wm"):
    tile = "".join("<span>wanderlogika</span>" for _ in range(60))
    css = (
        f"#wm1{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:{TOP}px;font-size:{SIZE}px;"
        f"letter-spacing:.5px;color:#fff;opacity:{OPACITY};white-space:nowrap;pointer-events:none;"
        "text-shadow:0 3px 6px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.3);transform-origin:50% 50%}\n"
        f"#wmtile{{position:absolute;inset:-300px;transform:rotate(-24deg);opacity:{TILE_OPACITY};display:flex;flex-wrap:wrap;"
        "gap:90px 140px;align-content:flex-start;color:#fff;font-size:40px;pointer-events:none}\n"
        f"#wmend{{position:absolute;left:0;right:0;margin:0 auto;width:fit-content;top:1500px;font-size:38px;color:{end_color};opacity:.85}}\n"
    )
    html = f'<div id="wmtile" class="{tile_font_class}">{tile}</div><div id="wm1" class="f-wm">{NAME}</div>'
    end_html = f'<div id="wmend" class="f-wm">by {HANDLE}</div>'
    pulses, t = [], 0.0
    while t + PULSE <= total + 1e-6:
        pulses.append(round(t, 3)); t += PULSE
    js = (f"// wanderlogika watermark: slow zoom x2 every 5s, repeat\n"
          f"{pulses}.forEach(t => {{\n"
          f"  tl.to('#wm1', {{ scale:{ZOOM}, duration:{PULSE/2}, ease:'power2.inOut' }}, t);\n"
          f"  tl.to('#wm1', {{ scale:1, duration:{PULSE/2}, ease:'power2.inOut' }}, t + {PULSE/2});\n"
          f"}});\n")
    rest = total - t
    if rest > 0.3:  # partial last pulse so the zoom never freezes before the end
        js += f"tl.to('#wm1', {{ scale:{1 + (ZOOM-1)*min(1, rest/(PULSE/2))}, duration:{min(rest, PULSE/2):.3f}, ease:'power2.inOut' }}, {t:.3f});\n"
    return {"css": css, "html": html, "end_html": end_html, "js": js}
