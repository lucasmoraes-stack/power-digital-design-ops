"""crop_sent.py - photo stand-ins cropped from the sent-email prints in references/ into
photos/lifestyle/crop-sent-*.jpg (q85). Boxes are in px of the 1200px print. fixline=True removes the
drawn fishing line (long thin white connected strokes + limited retouch boxes). The hay-bale crop
(sep24, rotated 6.4 deg in the email) is done at the end. See photos/lifestyle/INDEX.md."""
from PIL import Image, ImageFilter, ImageChops, ImageDraw
import numpy as np, os
from pathlib import Path
KIT=Path(__file__).resolve().parents[1]
R=str(KIT/'references')+'/'
O=str(KIT.parent/'photos'/'lifestyle')+'/'
F={'sep2':'September 2.png','sep10':'Septemeber 10.png','sep15':'September 15.png','sep22':'September 22.png','sep24':'September 24.png'}
C=[ # key, name, box, fixline
 ('sep2','hunter-blind',(62,1952,1143,3228),False),
 ('sep10','utv-hunters',(0,135,1200,700),False),
 ('sep10','utv-hunter-standing',(735,135,1200,1250),False),
 ('sep10','truck-hunter',(0,2470,1200,3140),False),
 ('sep10','family-walking-card',(150,3748,1050,4122),False),
 ('sep15','family-forest-walk',(0,840,1200,1450),True),
 ('sep15','camp-chairs-family',(0,5408,1200,5922),False),
 ('sep22','sunset-boat-pocket',(0,160,592,822),False),
 ('sep22','fly-tying',(606,160,1200,610),False),
 ('sep22','boat-anglers',(606,626,1200,880),False),
 ('sep22','canoe-river',(236,2176,562,2610),False),
 ('sep22','trout-in-hand',(570,2116,886,2600),False),
 ('sep22','wading-river',(896,2176,1200,2610),False),
 ('sep22','angler-tackle-box',(0,4890,1200,5330),True),
 ('sep24','barn-door-feed-bag',(0,862,1200,1872),False),
 ('sep24','stable-horse',(0,4032,1200,4780),False),
]
def components(mask, minspan):
    H,W=mask.shape; lab=np.zeros((H,W),np.int32); keep=np.zeros((H,W),bool); n=0
    ys,xs=np.nonzero(mask)
    for y,x in zip(ys,xs):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n; pts=[]
        while st:
            cy,cx=st.pop(); pts.append((cy,cx))
            for dy in (-2,-1,0,1,2):
                for dx in (-2,-1,0,1,2):
                    ny,nx=cy+dy,cx+dx
                    if 0<=ny<H and 0<=nx<W and mask[ny,nx] and not lab[ny,nx]:
                        lab[ny,nx]=n; st.append((ny,nx))
        p=np.array(pts)
        span=max(p[:,0].max()-p[:,0].min(), p[:,1].max()-p[:,1].min())
        if span>=minspan: keep[p[:,0],p[:,1]]=True
    return keep
def fixline(im):
    a=np.asarray(im).astype(np.int16)
    lum=a.mean(2); sat=a.max(2)-a.min(2)
    med=np.asarray(im.filter(ImageFilter.MedianFilter(9))).astype(np.int16)
    mlum=med.mean(2)
    mask=(lum>170)&(sat<50)&((lum-mlum)>40)
    mask=components(mask,160)
    for (x0,y0,x1,y1) in EXTRA.get(im.size,[]):
        sub=(lum[y0:y1,x0:x1]>120)&(sat[y0:y1,x0:x1]<70)&((lum-mlum)[y0:y1,x0:x1]>18)
        mask[y0:y1,x0:x1]|=sub
    m=Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
    # inpaint: replace with a large median, then smooth the patch
    fill=im.filter(ImageFilter.MedianFilter(15))
    fill=fill.filter(ImageFilter.GaussianBlur(1.5))
    out=Image.composite(fill,im,m)
    return out, int(np.asarray(m).astype(bool).sum())
EXTRA={(1200,610):[(595,35,690,165),(555,32,600,62),(1135,200,1200,262)]}
cache={}
for k,n,box,fl in C:
    if k not in cache: cache[k]=Image.open(R+F[k]).convert('RGB')
    im=cache[k].crop(box)
    info=''
    if fl:
        im,px=fixline(im); info=f' line-px={px}'
    p=O+f'crop-sent-{k}-{n}.jpg'
    im.save(p,quality=85,optimize=True,subsampling=0)
    print(os.path.basename(p),im.size,os.path.getsize(p)//1024,'KB'+info)

im=cache['sep24'].crop((0,2500,560,3400)).rotate(-6.4,resample=Image.BICUBIC,expand=False,fillcolor=(0,0,0)).crop((46,112,451,810))
im.save(O+'crop-sent-sep24-hay-bale-seated.jpg',quality=85,optimize=True,subsampling=0)
print('crop-sent-sep24-hay-bale-seated.jpg',im.size)
