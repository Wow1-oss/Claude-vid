"""Rough cut: remove dead air, J-cut cold-open (pad wipe visual under 'Makeup tebal?'), grade, 1080x1920@30 SDR bt709."""
import json, subprocess
SEG = [(0.10,1.00),(1.13,1.79),(2.08,3.64),(3.80,5.70),(5.98,6.98),(7.10,8.44),(8.55,10.02)]
Q=lambda x: round(round(x*24)/24,4)
SEG=[(Q(a),Q(b)) for a,b in SEG]
PRE = (Q(5.50), Q(0.45))   # video-only pre-hook from cotton-pad shot, replaces first 0.45s of picture
GRADE = ("scale=1080:1920:flags=lanczos,unsharp=5:5:0.45,"
         "eq=contrast=1.05:saturation=1.03:gamma=1.03:brightness=0.012,"
         "colorbalance=rs=-0.015:gs=0.0:bs=0.02:rh=0.015:bh=-0.02,"
         "curves=master='0/0.025 0.25/0.235 0.5/0.515 0.75/0.775 1/0.965',fps=30")
fc, vlab, alab = [], [], []
# video: pre-hook, then segment 0 starting PRE[1] later
vsegs = [(PRE[0], PRE[0]+PRE[1])] + [(SEG[0][0]+PRE[1], SEG[0][1])] + SEG[1:]
for i,(a,b) in enumerate(vsegs):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]"); vlab.append(f"[v{i}]")
for i,(a,b) in enumerate(SEG):
    d=b-a; fc.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d-0.025:.3f}:d=0.025[a{i}]"); alab.append(f"[a{i}]")
fc.append("".join(vlab)+f"concat=n={len(vlab)}:v=1:a=0,tpad=stop_mode=clone:stop_duration=0.2,{GRADE},vignette=PI/9[v]")
fc.append("".join(alab)+f"concat=n={len(alab)}:v=0:a=1,highpass=f=70,afftdn=nf=-30[a]")
subprocess.run(["ffmpeg","-y","-v","error","-i","src/raw.mp4","-filter_complex",";".join(fc),"-map","[v]","-map","[a]",
  "-c:v","libx264","-crf","15","-pix_fmt","yuv420p","-g","15","-color_primaries","bt709","-color_trc","bt709","-colorspace","bt709",
  "-bsf:v","h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
  "-c:a","aac","-b:a","192k","-ar","44100","-t",str(sum(b-a for a,b in SEG)),"footage.mp4"],check=True)
out=[];t=0
for a,b in SEG: out.append({"in":a,"out":b,"t":round(t,3)}); t+=b-a
json.dump({"segments":out,"prehook":PRE,"duration":round(t,3)},open("cutlist.json","w"),indent=1)
print("dur",round(t,3))
