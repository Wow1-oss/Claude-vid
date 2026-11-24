"""Cut + grade: builds footage.mp4 (1080x1920, 30fps, bt709) from the two raw clips.
Video and audio cut separately so B-roll-style shots can be offset (no lips visible there)."""
import json, subprocess
SEG = [  # label, src, a_in, a_out, v_in, v_out, grade(brightness, gamma, sat, warmth)
 ("hook",    "using",   0.00, 1.98, 0.00, 1.98, "u1"),
 ("problem", "using",   2.08, 3.10, 2.08, 3.10, "u1"),
 ("reveal",  "using",   3.16, 4.62, 3.16, 4.62, "u2"),
 ("ports",   "using",   6.12, 7.58, 6.08, 7.54, "u3"),
 ("devices", "using",   7.66, 9.86, 7.54, 9.74, "u3"),
 ("cord",    "packing", 0.00, 3.04, 0.00, 3.04, "p1"),
 ("pack",    "packing", 3.96, 6.70, 2.20, 4.94, "p1"),
 ("payoff",  "packing", 7.54, 10.00, 7.54, 10.00, "p2"),
]
# per-shot exposure / WB match (target luma ~115, tame the orange cast, keep skin natural)
G = {
 "u1": "eq=brightness=0.03:gamma=1.06:saturation=0.98,colorbalance=rs=-0.03:bs=0.03:rm=-0.02:bm=0.02",
 "u2": "eq=brightness=0.0:gamma=1.0:saturation=1.0,colorbalance=rs=-0.03:bs=0.03:rm=-0.02:bm=0.02",
 "u3": "eq=brightness=0.01:gamma=1.03:saturation=1.0,colorbalance=rs=-0.04:bs=0.04:rm=-0.03:bm=0.03",
 "p1": "eq=brightness=0.05:gamma=1.14:saturation=1.02,colorbalance=rs=-0.03:bs=0.03:rm=-0.02:bm=0.02",
 "p2": "eq=brightness=-0.03:gamma=0.97:saturation=1.03,colorbalance=rs=0.0:bs=0.0",
}
LOOK = ("curves=master='0/0.02 0.25/0.23 0.5/0.52 0.75/0.78 1/0.97',"
        "colorbalance=rh=0.02:bh=-0.03:rm=0.01:bm=-0.015,unsharp=5:5:0.45,noise=alls=5:allf=t")
inputs = ["-i", "src/using.mp4", "-i", "src/packing.mp4"]
idx = {"using": 0, "packing": 1}
fc, vl, al, out = [], [], [], 0.0
cut = []
for k, (lab, s, ai, ao, vi, vo, g) in enumerate(SEG):
    i = idx[s]; d = ao - ai
    assert abs((vo - vi) - d) < 0.021, (lab, vo - vi, d)
    fc.append(f"[{i}:v]trim={vi}:{vi+d},setpts=PTS-STARTPTS,fps=30,scale=1080:1920:flags=lanczos,{G[g]},{LOOK}[v{k}]")
    fc.append(f"[{i}:a]atrim={ai}:{ao},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.03:.3f}:d=0.03[a{k}]")
    vl.append(f"[v{k}]"); al.append(f"[a{k}]")
    cut.append({"label": lab, "src": s, "a_in": ai, "a_out": ao, "v_in": vi, "out_start": round(out, 3), "out_end": round(out + d, 3)})
    out += d
fc.append("".join(vl) + f"concat=n={len(SEG)}:v=1:a=0,format=yuv420p[v]")
fc.append("".join(al) + f"concat=n={len(SEG)}:v=0:a=1,highpass=f=70,afftdn=nf=-30[a]")
cmd = ["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
       "-c:v", "libx264", "-crf", "16", "-g", "15", "-r", "30", "-pix_fmt", "yuv420p",
       "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
       "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "footage.mp4"]
subprocess.run(cmd, check=True)
json.dump(cut, open("cutlist.json", "w"), indent=1)
print("total", round(out, 3))
