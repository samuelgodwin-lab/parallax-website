"""Composite a flat screen PNG into a mockup PSD's smart-object quad.
usage: mock.py <psd> <screen.png> <out.png>"""
import sys, numpy as np
from PIL import Image
from psd_tools import PSDImage
import psd_tools.api.layers as L

def coeffs(dst, src):
    # perspective coeffs mapping output(dst) -> input(src) for PIL
    A=[];B=[]
    for (x,y),(u,v) in zip(dst,src):
        A.append([x,y,1,0,0,0,-u*x,-u*y]); B.append(u)
        A.append([0,0,0,x,y,1,-v*x,-v*y]); B.append(v)
    return np.linalg.solve(np.array(A,float),np.array(B,float)).tolist()

psd_path, scr_path, out_path = sys.argv[1:4]
psd = PSDImage.open(psd_path)
so = [l for l in psd.descendants() if l.kind=='smartobject' and l.visible and l.opacity>0][0]
tb = so.smart_object.transform_box
quad = [(tb[0],tb[1]),(tb[2],tb[3]),(tb[4],tb[5]),(tb[6],tb[7])]
if quad[0][0] > quad[1][0]:  # smart object placed mirrored: map the screen to the visual corners
    quad = [quad[1], quad[0], quad[3], quad[2]]
x0,y0,x1,y1 = so.bbox
scr = Image.open(scr_path).convert('RGBA')
W,H = scr.size
SS=2  # supersample the warp
dst=[((qx-x0)*SS,(qy-y0)*SS) for qx,qy in quad]
src=[(0,0),(W,0),(W,H),(0,H)]
warped = scr.transform(((x1-x0)*SS,(y1-y0)*SS), Image.PERSPECTIVE, coeffs(dst,src), Image.BICUBIC)
warped = warped.resize((x1-x0,y1-y0), Image.LANCZOS)
arr = np.asarray(warped).astype(np.float32)/255.0
color, shape = arr[...,:3], arr[...,3:4]
def patched(channel=None, **kw):
    if channel=='color': return color
    if channel=='shape': return shape
    if channel is None: return np.concatenate([color,shape],-1)
    return L.SmartObjectLayer.numpy(so, channel, **kw)
so.numpy = patched
img = psd.composite(layer_filter=lambda l: l.is_visible())
img.convert('RGB').save(out_path)
print('ok', out_path, img.size)
