# Claude-vid

Short-video edits built with HyperFrames (one project folder per video: `edit/` SimHome, `cymbo/` Cymbo Cleansing Oil).

## Fixed setting: Wanderlogika watermark (every video)
Every new edit MUST include the watermark from `brand/watermark.py`:
- main mark "Wanderlogika", Montserrat ExtraBold Italic, white 30 %, centred at chin level (y 1095),
  slow zoom 1.0 → 1.12 → 1.0 twice every 5 s, repeating;
- end-card handle "by @wanderlogika";
- hidden tiled proof layer at 4 %.
In build.py: `install_font(".")`, then insert `watermark(TOTAL)` css/html/end_html/js (see docstring and `cymbo/build.py`).
Also tag the export: `-metadata artist="wanderlogika" -metadata copyright="© wanderlogika"`.
Reference look: `cymbo/preview/watermark_preview_v2.jpg`.
