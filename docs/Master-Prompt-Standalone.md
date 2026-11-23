# Standalone Master Prompt: Premium UGC Product Ad (9:16)

Copy everything in the box. Fill in only the **PROJECT DETAILS** part and leave the rest as it is.
It doesn't refer to any earlier video, so it works in any repo or session that has HyperFrames installed.

```
/anthropic-skills:rbdigital-videoedit

Use the RB Digital Video Edit skill with HyperFrames. Edit my product video into a 9:16 Premium UGC Ad.

=== PROJECT DETAILS (fill in) ===
Input folder (raw clips + product photo/spec sheet): <LINK>
Output folder: <LINK>
Product: <product name + brand>
Key features to highlight: <e.g. adjustable height, 360° rotation> (if empty, take them from the transcript and product photo)
CTA text: <e.g. Dapatkan kat link di bawah>
CTA button: <yellow basket / link in bio / WhatsApp / generic button>
Show price: <no / yes: RM__>
Watermark: <your brand name / none>
Caption language: <Malay / English / follow the speaker>
Target length: <15–25 s>

=== STEP 1: UNDERSTAND THE FOOTAGE ===
- Transcribe every clip with word-level timestamps.
- Cut every awkward pause, filler word, false start and repeated line. Keep the best take of each line.
- Rearrange into this story: Hook → Problem → Product reveal → Features (one per beat) → Payoff → CTA → End card.
- If the product name, price or a claim in the speech doesn't match the details above, ask me before using it.

=== STEP 2: LOOK & FEEL ===
- Format: 1080×1920, 30 fps.
- Palette: pick 4 colours from the product and its packaging (light background, main brand colour, warm accent, CTA colour). Use them in every graphic.
- Fonts: a new set of 3 Google Fonts for this project: a bold condensed display font (hook words, numbers), an elegant serif/italic (emotional words), a clean heavy sans (captions, labels, buttons).
- Colour grade: premium and warm, natural skin tones. Soft key light on the face that follows each shot, gentle vignette, fine film grain (~5%). Fix exposure and white balance per clip so every shot matches.

=== STEP 3: HOOK (first 3 seconds) ===
- Open on the strongest line or the most visual moment, never on "hi guys".
- White flash in; the camera starts zoomed in (~1.15×) and snaps to 1.0.
- 2–3 giant kinetic words from the hook line, placed behind or around the speaker without covering the face.
- Hit + whoosh SFX on the first frame.

=== STEP 4: MOTION DESIGN ===
- Problem: cooler, slightly desaturated mood. 1–2 "problem chips" (pill labels with a red ✕) slide in, get struck through, shake and fly off.
- Reveal: flash, warm glow, colour returns to full.
- Features: one animated graphic per feature, timed to the word that mentions it. Counters/gauges for numbers (size, height, capacity, hours), a rotating ring for 360°/rotation, arrow + pulsing-ring callouts pointing at product parts, before/after split where it fits.
- Payoff: the emotional line as one big serif word with small sparkles.
- CTA: a product card (photo, brand, name, CTA button) drops in; a tap finger presses the button with a ring pulse.
- End card (last ~1.2 s): product hero on the light background, a short tagline and the CTA button, designed to loop back to the hook.
- Camera: subtle punch-ins (1.05–1.12×) on key words, at most one every ~2 s.
- A thin progress bar at the bottom in the accent colour.
- Something moves every 1–2 s, but nothing covers the face or the product.

=== STEP 5: CAPTIONS ===
- Karaoke captions, 2–4 words per chunk, in the lower third (inside the TikTok/Reels safe zone).
- Each word lights up and pops as it's spoken. Keywords (product, features, numbers, CTA) get a pill highlight in the brand colour.
- Use the exact spoken words; fix obvious spelling only.

=== STEP 6: SOUND ===
- SFX tied to the motion: whoosh/swish for transitions, pop for chips and text, tick for counters, click for the tap, riser before the reveal, buzz/boom at the problem→reveal moment, chime for the reveal and end card. Keep them soft, under the voice.
- A light, upbeat music bed under the voice (~20%), ducked while speaking.
- Final mix around −14 LUFS, voice always clear.

=== STEP 7: WATERMARK (skip if "none") ===
- The brand name in white at 30% opacity, centred at chin level, slow zoom 1.0→1.12→1.0 twice every 5 s, repeating.
- "by @<brand>" on the end card. Add artist/copyright metadata to the MP4.

=== STEP 8: PREVIEW FIRST ===
Do NOT render yet. Show me:
1. The cleaned transcript and the cut list (what you removed).
2. A storyboard table: time | line spoken | visual/animation | SFX.
3. 4–6 preview stills (hook, problem, one feature, CTA, end card).
4. The palette and font set you picked.
Then wait. I'll reply with changes or "render".

=== STEP 9: AFTER I APPROVE ===
- Render Final.mp4 (H.264 + AAC, 1080×1920), Final.srt, and cover.jpg (the strongest hook frame with the hook text).
- Check before reporting: length, no black or frozen frames, captions in sync, loudness, file size.
- Commit and push to the git branch, then upload the three files to the output folder. If the upload fails because the file is too big, tell me and give me the file to download. Don't compress it to make it fit.
```

---

## What changed from the old prompt

| Old prompt said | New prompt says instead |
|---|---|
| "Guna style sama macam video SimHome, rujuk edit/build.py" | Steps 2–6 describe that style in words: story order, hook, chips, feature graphics, captions, grade, SFX |
| "letak hook yang kuat" | What a strong hook means: best line first, flash, snap zoom, giant kinetic words, hit SFX |
| "color grade-kan, nampak premium" | Warm grade, natural skin, key light on the face, vignette, grain, matched shots |
| "masukkan animation, SFX dekat mana patut" | Which animation goes with which kind of moment, and which SFX goes with which motion |
| "tukar font set" | A 3-font recipe (display / serif / sans), new every project |
| Product + CTA on one line | A fill-in block: features, CTA button type, price yes/no, watermark, language, length |
| "Tunjukkan preview dulu" | Exactly what the preview must include: cut list, storyboard, stills, palette, fonts |
| Watermark set in CLAUDE.md | Watermark rules are inside the prompt, so they work in any repo |
| Answers to Claude's questions came after the first preview | Price, CTA button and the name check are answered up front, so there are fewer back-and-forths |

## Tips

1. **Only edit the PROJECT DETAILS block.** Everything below it is your "house style". Change it only when you want a new look.
2. **Make style variations by swapping one step.** For example, replace Step 4 with "minimal motion, captions only" for a calm, aesthetic product.
3. **Test it on a video you've already edited** (for example the CYMBO clips) and compare with your earlier result before you share it with others.
4. **Optional shortcut:** paste Steps 2–7 into the repo's `CLAUDE.md` as your house style. Your daily prompt then only needs the PROJECT DETAILS plus "follow the house style in CLAUDE.md".
