# How I Edit AI Product Videos with Claude Code (Step by Step)

These are the exact steps I followed to edit three short product videos (UGC-style ads, 9:16) with Claude Code. I never opened a video editor. I did everything from the Claude app on my phone.

| # | Video | What happened |
|---|-------|---------------|
| 1 | **SimHome** side table | First try. I installed HyperFrames, wrote a plain prompt, approved a preview, rendered |
| 2 | **CYMBO** Cleansing Gel | Reused video 1 as a template, used the RB Digital skill, added a watermark |
| 3 | **FUNEZI** Travel Adapter | Pasted the finished template prompt. Only one correction before the render |

Each video got easier because I reused what worked in the one before.

---

## What you need

- **Claude app** (phone or web) with access to **Claude Code** (cloud sessions)
- **A GitHub account** and an empty repository (mine is called `Claude-vid`). This is where Claude keeps the project files and the final renders
- **Google Drive** for your raw clips and the finished videos
- **Your raw footage**: talking-head or UGC clips of the product, plus a product photo or spec sheet

---

## PHASE 0: One-time setup (do this once)

### Step 1: Connect GitHub
In the Claude app, connect your GitHub account and install the **Claude GitHub App** on your repo. Then start a Claude Code session on that repo.

> My message after I'd done it: *"Please check, i have connect and install"*

### Step 2: Install HyperFrames
HyperFrames is the tool Claude uses to build and render the video (animations, captions, SFX, colour grade).

> My prompt: **`Install hyperframe`**

Claude installs it into the repo and commits it.

### Step 3: Set up the cloud environment
Claude needs network access to **download from Google Drive** and to use the **transcription models**. I created an environment called `Claude-vid` that allows both. Pick this environment every time you start a new video session.

### Step 4: Connect the Google Drive connector
Go to **claude.ai → Settings → Connectors** and connect **Google Drive**, so Claude can upload the finished video to your folder.

> ⚠️ I learned this the hard way. On my first video, Claude couldn't upload to Drive because the connector wasn't connected. **Connectors only load when a session starts.** Connect it first, then open a new session.

### Step 5: Turn on the video skill
Enable the **RB Digital Video Edit** skill (`anthropic-skills:rbdigital-videoedit`). It already knows how to transcribe, cut pauses, add hooks, captions, SFX, music and colour grading. Your prompt only has to say what's specific to your video.

---

## PHASE 1: Prepare your footage (every video)

### Step 6: Make an INPUT folder in Google Drive
- Put all the raw clips in it
- Also put in the **product image or spec sheet**. Claude uses it for feature callouts and overlays
- Share it as **"Anyone with the link can view"**

### Step 7: Make an OUTPUT folder in Google Drive
This is where you want `Final.mp4`, `Final.srt` (subtitles) and `cover.jpg` (thumbnail) to go.

---

## PHASE 2: Send the master prompt

### Step 8: Start a NEW session and paste the prompt

**My very first prompt (video 1, before I had a template):**

```
Aku nak kau edit video dalam link folder ni: <LINK DRIVE> ni guna hyperframe.
Make sure kau buang semua awkward pause dan apa-apa yang repeatable.
Kau transcribe dulu video ni, so kau akan tahu kat mana nak masukkan animation,
sound effects, motion design, dekat mana-mana yang kau rasa patut.
Lepas tu aku nak kau letak hook yang kuat, and then kau color grade-kan,
bagi video ni nampak premium, dan adjust-kan lighting dia.
Aku tak nak kau render dulu. Tunjukkan aku preview dulu.
```

**My reusable template (videos 2 and 3), copy this one:**

```
/anthropic-skills:rbdigital-videoedit

Guna skill RB Digital Video Edit dengan HyperFrames.

Aku nak kau edit video dalam link folder ni: <LINK FOLDER INPUT>
Produk: <NAMA PRODUK + BRAND>. CTA: <contoh: Dapatkan kat link dibawah>

Make sure kau buang semua awkward pause dan apa-apa yang repeatable.
Kau transcribe dulu video ni, so kau akan tahu kat mana nak masukkan animation,
sound effects, motion design, dekat mana-mana yang kau rasa patut.
Lepas tu aku nak kau letak hook yang kuat, and then kau color grade-kan,
bagi video ni nampak premium, dan adjust-kan lighting dia.
Guna style sama macam video SimHome (Premium UGC Ad, rujuk edit/build.py dalam repo),
tapi tukar font set. Letak watermark "<NAMA BRAND KAU>".

Aku tak nak kau render dulu. Tunjukkan aku preview dulu.
Lepas aku OK, render, commit dan push ke branch git, dan upload Final.mp4,
Final.srt dan cover.jpg ke folder Drive ni: <LINK FOLDER OUTPUT>
```

<details>
<summary>English version of the template</summary>

```
/anthropic-skills:rbdigital-videoedit

Use the RB Digital Video Edit skill with HyperFrames.

Edit the video in this folder: <INPUT FOLDER LINK>
Product: <PRODUCT + BRAND>. CTA: <e.g. Get it at the link below>

Remove every awkward pause and anything repeated.
Transcribe the video first so you know where to add animation, sound effects
and motion design wherever you think they fit.
Then add a strong hook, colour grade it so it looks premium, and fix the lighting.
Use the same style as my previous video (refer to edit/build.py in the repo),
but change the font set. Add the watermark "<YOUR BRAND>".

Don't render yet. Show me a preview first.
After I approve: render, commit and push to the git branch, and upload Final.mp4,
Final.srt and cover.jpg to this Drive folder: <OUTPUT FOLDER LINK>
```
</details>

**Why each line is there:**

| Line in the prompt | Why |
|---|---|
| `/anthropic-skills:rbdigital-videoedit` | Loads the video-editing skill |
| Product + CTA | Gives Claude the on-screen product name and the closing call to action |
| "buang awkward pause / repeatable" | Removes dead air, filler words and repeated takes |
| "transcribe dulu" | Claude reads what's said, so animations and SFX land on the right words |
| "hook yang kuat" | Gets attention in the first 3 seconds |
| "color grade, premium, lighting" | Makes phone footage look like an ad |
| "style sama macam video X, rujuk build.py" | Reuses your earlier video as a template. Faster and keeps your look consistent |
| "tukar font set" | Each video still looks a bit different |
| "jangan render dulu, preview dulu" | **Most important line.** You check it before Claude spends time rendering |
| "commit, push, upload" | Final files get saved in GitHub and delivered to Drive |

---

## PHASE 3: Answer Claude's questions

### Step 9: Reply to clarifying questions
Claude transcribes the clips and then usually asks a few questions. Answer them in short numbered replies. My real replies:

- Video 1: *"1. Tak perlu letak yellow basket, boleh guna kad dan butang generik. 2. Ok maintain."* (No TikTok yellow basket, use a generic card and button)
- Video 2: *"Ok confirm use Cleansing Oil."* (Claude spotted that the product said in the video didn't match my prompt and asked me which was right)
- Video 3: *"Do not include the price."*

💡 **Tip:** Check product names, prices and claims carefully. Claude takes them from the transcript, so mistakes in what was said end up on screen.

---

## PHASE 4: Preview → approve → render

### Step 10: Review the preview
Claude sends preview frames or a storyboard (for example `preview_v1.jpg`). Check the hook, captions, colours, product name and CTA.

### Step 11: Ask for changes, or approve
Ask for changes in plain words, as many rounds as you need. When you're happy:

> **"Ok please proceed to render."**

Claude renders the MP4 and checks it (length, audio loudness, file size).

---

## PHASE 5: Get your files

### Step 12: Collect the deliverables
You get:
- `Final.mp4`: the finished video (1080×1920)
- `Final.srt`: subtitle file
- `cover.jpg`: thumbnail

They're committed and pushed to your GitHub branch, and uploaded to your Drive output folder if the connector is on.

> ⚠️ **Large files:** a ~25 MB render may not upload through the Drive connector. Tap the file card in the chat to download it (or download it from GitHub), then upload it to Drive yourself. Don't accept a heavily compressed version just to make the upload work, because it'll look pixelated.

---

## PHASE 6: Make the next video faster

### Step 13: Turn a good video into a template
Once you like a result, ask Claude for the prompt to reuse it:

> *"So if i want to edit another product video using the same skill above, what prompt should i do?"*

That's where my template in Step 8 came from. The key is the line **"rujuk edit/build.py dalam repo"**: the next session copies the structure of the earlier video.

### Step 14: Add a watermark as a fixed setting
To stop people stealing my videos, I built a watermark in four short messages:

1. **Ask for ideas:** *"Give ideas how i can put watermark 'wanderlogika' in the video to ensure people dont curi my video?"*
2. **See it first:** *"Sebelum ko tambah sebagai setting, tunjukkan draft preview image how the watermark text looks like."* (Before you save it as a setting, show me a draft preview image)
3. **Adjust it:** *"Aku nak ko tukar font mcm ni, buat dia slow zoom 2 kali setiap 5 saat dan repeat. Opacity 30%."* (Change the font, slow zoom twice every 5 s on repeat, 30% opacity)
4. **Save it for every video:** *"Ok better! Now do Setting tetap + Cymbo v2"* (Make it a fixed setting and redo the CYMBO video)

Claude saved it in a `CLAUDE.md` file in the repo. Claude reads that file at the start of every session, so every new video now gets the watermark automatically, plus `artist`/`copyright` metadata in the MP4.

💡 **Use `CLAUDE.md` for anything you want in every video:** watermark, brand colours, logo, end card, preferred fonts.

---

## Quick checklist (print this)

- [ ] GitHub connected + Claude GitHub App installed *(once)*
- [ ] HyperFrames installed in the repo *(once)*
- [ ] Cloud environment allows Google Drive + transcription *(once)*
- [ ] Google Drive connector connected **before** starting the session *(once)*
- [ ] RB Digital Video Edit skill on *(once)*
- [ ] Raw clips + product image in a Drive folder shared "Anyone with the link"
- [ ] Empty output folder in Drive
- [ ] New session → paste the template → fill in links, product, CTA, watermark
- [ ] Answer Claude's questions (check product name, price, claims)
- [ ] Review the preview → ask for changes → "Ok proceed to render"
- [ ] Get Final.mp4, Final.srt, cover.jpg (download manually if Drive upload fails)

## Lessons learned

1. **Always ask for a preview first.** It saves render time, and you catch mistakes early.
2. **Use one new session per video.** It keeps things clean, and the repo carries your style forward.
3. **Reuse earlier videos as templates** (point to the earlier `build.py`).
4. **Connect connectors before you start a session**, not halfway through.
5. **Put fixed settings in `CLAUDE.md`** so you don't have to repeat them in every prompt.
6. **Short replies are fine.** "Ok maintain", "Do not include the price" and "Proceed render" were enough.
7. **Ask Claude to show you before it saves something permanently**, like I did with the watermark.
