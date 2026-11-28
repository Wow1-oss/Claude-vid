# Wanderlogika — Passport, Plans & Besties · Launch Video (v2 preview, 13 s)

**Format:** 9:16 · 1080×1920 · 30 fps · **13.0 s** · MP4 (H.264 + AAC, -14 LUFS)
**Style:** Retro travel scrapbook commercial (paper texture, washi tape, torn edges, dotted flight paths, stamps)
**Palette:** Cream #F7F0DF · Blue #085BE5 · Yellow #FFD326 · Pink #F83C92 · Black #171717
**Fonts:** Anton (stamps, tagline) + DM Sans 700 (URL). All other headlines are the **original carousel artwork**, masked out and animated, not retyped. That avoids spelling risk and keeps the brand look the same.
**Music:** original retro-pop track, 120 BPM, D–Bm–G–A, generated in code so it is royalty-free. Every scene cut lands on a beat (2.0 / 4.0 / 6.5 / 8.5 s).

## Scene-by-scene

| # | Time | Source image | Visual / motion | On-screen text | Audio |
|---|---|---|---|---|---|
| 1 | 0.00–2.00 | 01 Curiosity Hook | Camera **pull-out** 1.16→1.0. Headline slams in, yellow band wipes, sub-line slides up. Blue plane flies along a **dotted flight path** that draws itself across the top band. Pin drops at the end. Top and bottom bands move in parallax. | (original) Girls' trip planning… minus the group-chat chaos? / Your next DIY trip starts here. | Thud on beat 1, swish, pop, soft plane whoosh. Music starts at full energy (no intro gap). |
| 2 | 2.00–4.00 | 02 Planning Problem | **Blue paper-rip** sweep. "TOO MANY TABS." slides in from left, "TOO MANY OPINIONS." from right. The 5 sticky notes (Bali? Tokyo? Seoul? Europe? Langkawi?) **pop one after another**. Pink pill wipes in. Camera **push-in** to 1.07 on the stressed faces. | (original) Too many tabs. Too many opinions. / Let's make the plan feel manageable. | Paper rip, swishes, 5 ticks, riser 3.4 s, music ducks 3.6–4.0 s (tension before the reveal) |
| 3 | 4.00–6.50 | 03 Product Reveal | **Pink paper-rip** and a boom on the drop (4.0 s). "MEET" stamps down, the "PASSPORT, PLANS" yellow band wipes in, "& BESTIES" slams in, description slides up. **Ebook cover wipe-reveal** (bottom→top) + light sweep across it. Pink **"NEW · JUST LAUNCHED · WANDERLOGIKA" passport stamp** lands top-right. Camera **push-in** toward the cover (1.09). | (original) Meet Passport, Plans & Besties + stamp NEW | Boom, stamp thud, swish, hit, stamp |
| 4 | 6.50–8.50 | 04 Bundle & Price | **Yellow paper-rip**. "TWO GUIDES." slams in, "ONE SMARTER WAY TO TRAVEL." slides in. Card *Guide 01* (46-page) lifts toward camera with a shadow, then *Guide 02* (45 + 1 prompts, Bonus Included). New postage-stamp sticker drops in. A cream dotted flight path + plane draws across the bottom band. Camera **pull-out**. | (original) Two guides… / 46-page travel guide / 45 + 1 AI travel prompts / Bonus included | Rip, thud, swish, 2 pops, plane whoosh |
| 5 | 8.50–13.00 | 05 Purchase CTA | **Blue paper-rip**. Headline lines slam in, "Get the complete digital bundle for USD $9." pink bar stamps in, the original **"AVAILABLE NOW ON GUMROAD"** button lifts and settles slightly larger. A new crisp URL pill and the tagline (3 phrases, staggered) slide up. Light sweep on the button at 11.2 s. Slow camera drift (no frozen frames). **CTA fully readable 9.95 → 13.0 s (3.05 s)**; the button is readable from 9.3 s (3.7 s). | Ready to plan your next girls' trip? / USD $9 / AVAILABLE NOW ON GUMROAD / wanderlog.gumroad.com/l/passport-plans-besties / EXPLORE MORE. PLAN SMARTER. TRAVEL CONFIDENTLY. | Rip, thuds, pop, stamp + "ding" on the button, ticks, final chord at 12.0 s, fade to 13.0 s |

## Animation timeline (key frames)

```
0.00 ▌S1 h1 slam ─ 0.40 h2 band wipe ─ 0.80 h3 up ─ cam 1.16→1.00 ─ plane path 0.15–1.70 ─ 1.65 pin
1.75 ▌RIP blue (swap 2.06)
2.05 │S2 p1 ←slide  2.40 p2 slide→  2.62–3.10 sticky-note pops  3.25 p3 wipe  cam push 1.07
3.40 │   riser · 3.6–4.0 music duck
3.75 ▌RIP pink (swap 4.06) · BOOM 4.0
4.05 │S3 MEET stamp 4.30 band 4.50 BESTIES 4.65 desc 4.75 cover wipe 5.20 gleam 5.50 NEW stamp · cam push 1.09
6.25 ▌RIP yellow (swap 6.56)
6.55 │S4 b1 slam 6.80 b2 slide 7.10 card-01 lift 7.40 card-02 lift 7.55 flight path 7.60 sticker
8.25 ▌RIP blue (swap 8.56)
8.55 │S5 t1 8.80 t2 9.05 price bar 9.30 button + ding 9.45 URL 9.65/9.80/9.95 tagline 11.2 shine 12.0 chord
13.00■ end
```

Motion rules: every entrance uses ease-out (power3/expo) and every exit ease-in. Nothing grows from scale 0. There is only one slight overshoot (the CTA button). There are no fades to black and no dissolves.

## Masking / separation (original artwork kept as-is)

| Element | Method |
|---|---|
| Headlines, sub-lines, bands, price bar (all 5 images) | Cropped from the original at 1:1 and the cream background keyed to alpha. A "clean plate" sits underneath with the area filled in cream, so the text can animate in without a ghost copy behind it. |
| Ebook cover (img 03) | Cropped 1:1 and revealed in place with a clip-path wipe. No scale or warp. |
| Guide cards, sticky notes, Gumroad button | 1:1 crops that only "lift" (uniform scale ≥ 1 + shadow) in place. No distortion. |
| Carousel UI ("Swipe to explore", 01/05–05/05, page dots, Swipe pill) | Removed by local inpainting, because it means nothing in a video. On image 04 the new postage-stamp sticker covers that spot. |
| 4:5 → 9:16 | Each 1080×1350 image keeps its full width at 1:1 scale (no stretch). It sits as a scrapbook print with torn edges, a shadow and washi tape on a cream paper-texture background, with dotted flight paths on top and torn blue/pink/yellow strips at the bottom. The CTA card is cropped at y=1170 (the original URL/tagline under it was low-contrast over the photo), and a crisp URL + tagline is added below it. |

## Safe zones
Top 0–190 px: decoration only (flight path, pin). Bottom 1536–1920 px: no text (paper strips only). The new CTA text is inside x 100–940 and y 1338–1530.

## Added text (spelling checked)
- NEW · JUST LAUNCHED · WANDERLOGIKA
- wanderlog.gumroad.com/l/passport-plans-besties
- EXPLORE MORE. PLAN SMARTER. TRAVEL CONFIDENTLY.
