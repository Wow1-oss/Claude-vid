import cv2, numpy as np, json
from regions import R
UI = {  # carousel nav UI to remove (x,y,w,h)
 "hook":[(40,1258,410,62),(935,1258,110,62)],
 "problem":[(935,25,110,50),(450,1266,180,48),(885,1258,160,62)],
 "reveal":[(935,18,110,52),(50,1266,340,66)],
 "bundle":[(905,18,150,52),(842,1250,200,72)],
 "cta":[(935,12,120,50)],
}
KEY = {"h1","h2","h3","p1","p2","p3","r1","r2","r3","r4","b1","b2","t1","t2","pr"}
FLAT = {"cov"}            # plate filled flat cream (wipe reveal)
PATCH = set()
CUR={}
rng = np.random.default_rng(3)
CREAM={}
def mode(img):
    q=(img.reshape(-1,3)//6).astype(np.int32); k=q[:,0]*10000+q[:,1]*100+q[:,2]
    v,c=np.unique(k,return_counts=True); m=v[c.argmax()]
    sel=img.reshape(-1,3)[k==m]; return sel.mean(0)
def textmask(img, x,y,w,h, thr=26):
    roi = img[y:y+h, x:x+w].astype(np.int16)
    bg = CUR["cream"]
    d = np.abs(roi-bg).max(2)
    return (d>thr).astype(np.uint8)*255, bg
meta={}
for n in ["hook","problem","reveal","bundle","cta"]:
    src = cv2.imread(f"src/{n}.png", cv2.IMREAD_UNCHANGED)[:,:,:3]
    clean = src.copy(); CUR["cream"]=mode(src)
    for (x,y,w,h) in UI.get(n,[]):
        m = np.zeros(src.shape[:2],np.uint8)
        roi=src[y:y+h,x:x+w].astype(np.int16); b=np.concatenate([roi[0],roi[-1],roi[:,0],roi[:,-1]]); bgl=np.median(b,0)
        m[y:y+h,x:x+w]=((np.abs(roi-bgl).max(2))>40).astype(np.uint8)*255
        m = cv2.dilate(m,np.ones((9,9),np.uint8))
        clean = cv2.inpaint(clean,m,7,cv2.INPAINT_TELEA)
    cv2.imwrite(f"img/{n}_clean.png", clean)
    plate = clean.copy()
    for k,(im,x,y,w,h) in R.items():
        if im!=n: continue
        crop = clean[y:y+h,x:x+w]
        if k in KEY:
            tm,bg = textmask(clean,x,y,w,h,22)
            roi = crop.astype(np.int16); d = np.abs(roi-bg).max(2).astype(np.float32)
            a = np.clip((d-10)/22,0,1); a = cv2.dilate(a,np.ones((3,3),np.uint8))
            rgba = np.dstack([crop, (a*255).astype(np.uint8)])
            cv2.imwrite(f"img/L_{k}.png", rgba)
            m = np.zeros(src.shape[:2],np.float32); m[y:y+h,x:x+w]=cv2.dilate(tm,np.ones((15,15),np.uint8))/255.
            m = cv2.GaussianBlur(m,(0,0),3)[...,None]
            fill = bg[None,None,:]+rng.normal(0,2.5,plate.shape[:2]+(1,))
            plate = np.clip(plate*(1-m)+fill*m,0,255).astype(np.uint8)
        else:
            cv2.imwrite(f"img/L_{k}.png", crop)
            if k in FLAT:
                tm,bg = textmask(clean,x-14,y-14,w+28,h+28)
                noise = rng.normal(0,3,(h,w,1))
                plate[y:y+h,x:x+w] = np.clip(CUR['cream'][None,None,:]+noise,0,255).astype(np.uint8)
            elif k in PATCH:
                m = np.zeros(src.shape[:2],np.uint8); m[y+4:y+h-4,x+4:x+w-4]=255
                plate = cv2.inpaint(plate,m,9,cv2.INPAINT_TELEA)
    cv2.imwrite(f"img/{n}_plate.jpg", plate, [cv2.IMWRITE_JPEG_QUALITY,93])
    cv2.imwrite(f"img/{n}_clean.jpg", clean, [cv2.IMWRITE_JPEG_QUALITY,93])
json.dump({k:list(v) for k,v in R.items()}, open("regions.json","w"))
