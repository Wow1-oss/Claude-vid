"""Rough cut + grade + 9:16 1080x1920 + bt709. Segments: (src, in, out, text)."""
import json, subprocess
SEG = [
 ("demonstrating2", 8.24, 9.96, "Satu adapter, settle."),        # cold open (audio under graphic)
 ("showcasing2",    0.14, 1.68, "Travel tapi gadget banyak?"),  # NEW face (makeup)
 ("showcasing2",    2.02, 3.86, "Haa, ni memang kena ada."),    # NEW face (makeup)
 ("creating",       4.06, 6.64, "Adapter ni ada 4 USB port,"), # original product close-up
 ("creating",       6.84, 7.76, "2 type C,"),
 ("creating",       8.10, 9.68, "siap ada universal soket."),
 ("woman",          0.12, 3.94, "Plug UK, EU, US, Australia pun boleh tukar-tukar."),
 ("demonstrating2", 4.10, 5.74, "Kecil je, senang masuk beg."), # NEW face (makeup)
 ("demonstrating2", 6.04, 8.02, "Sesuai untuk yang travel dengan banyak gadget."),
 ("demonstrating2", 8.24, 9.96, "Satu adapter, settle."),
]
G = ("scale=1080:1920:flags=lanczos,fps=30,"
     "eq=contrast=1.08:saturation=1.06:gamma=1.05:brightness=0.012,"
     "colorbalance=rs=0.012:gs=0.004:bs=-0.018:rm=0.014:bm=-0.012:rh=-0.008:bh=0.012,"
     "curves=master='0/0.025 0.22/0.21 0.5/0.52 0.78/0.81 1/0.975',"
     "unsharp=5:5:0.55:3:3:0.0,vignette=PI/9")
src = {"creating": 0, "woman": 1, "showcasing2": 2, "demonstrating2": 3}
fc, cat = [], ""
for i, (s, a, b, _) in enumerate(SEG):
    d = round(b - a, 3)
    fc.append(f"[{src[s]}:v]trim={a}:{b},setpts=PTS-STARTPTS,{G}[v{i}]")
    fc.append(f"[{src[s]}:a]atrim={a}:{b},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.02,afade=t=out:st={d-0.03}:d=0.03[a{i}]")
    cat += f"[v{i}][a{i}]"
fc.append(f"{cat}concat=n={len(SEG)}:v=1:a=1[vc][ac]")
fc.append("[ac]highpass=f=70,afftdn=nf=-30[ao]")
cmd = ["ffmpeg","-y","-v","error","-i","src/creating.mp4","-i","src/woman.mp4","-i","src/showcasing2.mp4","-i","src/demonstrating2.mp4","-filter_complex",";".join(fc),
       "-map","[vc]","-map","[ao]","-c:v","libx264","-crf","16","-preset","medium","-pix_fmt","yuv420p","-g","15","-r","30",
       "-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
       "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
       "-c:a","aac","-b:a","192k","footage.mp4"]
subprocess.run(cmd, check=True)
t, out = 0, []
for s, a, b, txt in SEG:
    out.append({"src": s, "in": a, "out": b, "t0": round(t, 3), "t1": round(t + b - a, 3), "text": txt}); t += b - a
json.dump(out, open("cutlist.json", "w"), ensure_ascii=False, indent=1)
print("total", round(t, 3))
