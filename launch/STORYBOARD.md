# Wanderlogika — Passport, Plans & Besties · Launch Video (v1 preview)

**Format:** 9:16 · 1080×1920 · 30 fps · **15.0 s** · MP4 (H.264 + AAC, -14 LUFS)
**Style:** Retro travel scrapbook commercial (paper texture, washi tape, torn edges, dotted flight paths, stamps)
**Palette:** Cream #F7F0DF · Blue #085BE5 · Yellow #FFD326 · Pink #F83C92 · Black #171717
**Fonts:** Anton (stamps, tagline) + DM Sans 700 (URL). All other headlines are the **original carousel artwork**, masked out and animated, not retyped. That avoids spelling risk and keeps the brand look the same.
**Music:** original retro-pop track, 120 BPM, D–Bm–G–A, generated in code so it is royalty-free. Every scene cut lands on a beat (2.5 / 5.0 / 8.0 / 10.5 s).

## Scene-by-scene

| # | Time | Source image | Visual / motion | On-screen text | Audio |
|---|---|---|---|---|---|
| 1 | 0.00–2.50 | 01 Curiosity Hook | Camera **pull-out** 1.16→1.0. Headline slams in, yellow band wipes, sub-line slides up. Blue plane flies along a **dotted flight path** that draws itself across the top band. Pin drops at the end. Top and bottom bands move in parallax. | (original) Girls' trip planning… minus the group-chat chaos? / Your next DIY trip starts here. | Thud on beat 1, swish, pop, soft plane whoosh. Music starts at full energy (no intro gap). |
| 2 | 2.50–5.00 | 02 Planning Problem | **Blue paper-rip** sweep. "TOO MANY TABS." slides in from left, "TOO MANY OPINIONS." from right. The 5 sticky notes (Bali? Tokyo? Seoul? Europe? Langkawi?) **pop one after another**. Pink pill wipes in. Camera **push-in** to 1.07 on the stressed faces. | (original) Too many tabs. Too many opinions. / Let's make the plan feel manageable. | Paper rip, swishes, 5 ticks, riser 4.4 s, music ducks 4.6–5.0 s (tension before the reveal) |
| 3 | 5.00–8.00 | 03 Product Reveal | **Pink paper-rip** and a boom on the drop. "MEET" stamps down, the "PASSPORT, PLANS" yellow band wipes in, "& BESTIES" slams in, description slides up. **Ebook cover wipe-reveal** (bottom→top) + light sweep across it. Pink **"NEW · JUST LAUNCHED · WANDERLOGIKA" passport stamp** lands top-right. Camera **push-in** toward the cover (1.09). | (original) Meet Passport, Plans & Besties + stamp NEW | Boom, stamp thud, swish, hit, stamp |
| 4 | 8.00–10.50 | 04 Bundle & Price | **Yellow paper-rip**. "TWO GUIDES." slams in, "ONE SMARTER WAY TO TRAVEL." slides in. Card *Guide 01* (46-page) lifts toward camera with a shadow, then *Guide 02* (45 + 1 prompts, Bonus Included). New postage-stamp sticker drops in. A cream dotted flight path + plane draws across the bottom band. Camera **pull-out**. | (original) Two guides… / 46-page travel guide / 45 + 1 AI travel prompts / Bonus included | Rip, thud, swish, 2 pops, plane whoosh |
| 5 | 10.50–15.00 | 05 Purchase CTA | **Blue paper-rip**. Headline lines slam in, "Get the complete digital bundle for USD $9." pink bar stamps in, the original **"AVAILABLE NOW ON GUMROAD"** button lifts and settles slightly larger. A new crisp URL pill and the tagline (3 phrases, staggered) slide up. Light sweep on the button at 13.2 s. Slow camera drift (no frozen frames). **CTA fully readable 11.95 → 15.0 s (3.05 s)**; the button is readable from 11.3 s (3.7 s). | Ready to plan your next girls' trip? / USD $9 / AVAILABLE NOW ON GUMROAD / wanderlog.gumroad.com/l/passport-plans-besties / EXPLORE MORE. PLAN SMARTER. TRAVEL CONFIDENTLY. | Rip, thuds, pop, stamp + "ding" on the button, ticks, final chord at 14.0 s, fade to 15.0 s |

## Animation timeline (key frames)

```
0.00 ▌S1 h1 slam (8f expo) ─ cam 1.16→1.00 (0.1–2.3) ─ plane path draw 0.2–2.2
0.50 │   h2 band wipe        1.00 h3 slide-up        2.15 pin drop
2.25 ▌RIP blue (swap 2.56)
2.55 │S2 p1 ←slide   3.00 p2 slide→   3.25/3.40/3.55/3.70/3.85 sticky-note pops
4.05 │   p3 pink wipe   cam push 1.00→1.07   4.4 riser · 4.6–5.0 music duck
4.75 ▌RIP pink (swap 5.06) · BOOM 5.0
5.05 │S3 MEET stamp  5.35 band wipe  5.60 BESTIES slam  5.75 desc up
5.85 │   cover wipe-reveal (12f)  6.40 gleam  6.75 NEW stamp  6.3–7.95 cam push 1.09
7.75 ▌RIP yellow (swap 8.06)
8.05 │S4 b1 slam  8.35 b2 slide  8.75 card-01 lift  9.10 card-02 lift  9.30 sticker + bottom flight path
10.25▌RIP blue (swap 10.56)
10.55│S5 t1 slam  10.80 t2 slam  11.05 price bar  11.30 button lift + ding
11.45│   URL up   11.65/11.80/11.95 tagline phrases   13.20 button shine   14.0 final chord
15.00■ end
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
