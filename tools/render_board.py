import sys; 
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import pcbparse as P
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Rectangle, Circle, Ellipse, Polygon
D=P.load(sys.argv[1] if len(sys.argv)>1 else 'hardware/Fledgling.kicad_pcb')
X0,Y0,X1,Y1=100,100,190,140
PPM=40; DPI=100
BG='#0b1220'; COL={'F.Cu':'#d9534f','B.Cu':'#4a86d8'}
def pad_patch(p,fc):
    if p['shape']=='circle' or (p['shape'] in('oval','roundrect') and abs(p['w']-p['h'])<1e-6 and p['shape']=='circle'):
        return Circle((p['x'],p['y']),p['w']/2,fc=fc,ec='none')
    if p['shape']=='oval':
        return Ellipse((p['x'],p['y']),p['w'],p['h'],fc=fc,ec='none')
    return Rectangle((p['x']-p['w']/2,p['y']-p['h']/2),p['w'],p['h'],fc=fc,ec='none')
def draw(side, path, title, mirror=False, labels=True):
    fig=plt.figure(figsize=((X1-X0+4)*PPM/DPI,(Y1-Y0+4)*PPM/DPI),dpi=DPI,facecolor=BG)
    ax=fig.add_axes([0,0,1,1]); ax.set_facecolor(BG)
    ax.set_xlim(X0-2,X1+2) if not mirror else ax.set_xlim(X1+2,X0-2)
    ax.set_ylim(Y1+2,Y0-2); ax.axis('off')
    ax.add_patch(Rectangle((X0,Y0),X1-X0,Y1-Y0,fc='#10192b',ec='#e8d44d',lw=1.5))
    layers=[side] if side in COL else ['B.Cu','F.Cu']
    for L in layers:
        segs=[((s['x1'],s['y1']),(s['x2'],s['y2'])) for s in D['segs'] if s['layer']==L]
        lw=[s['w']*PPM*72/DPI for s in D['segs'] if s['layer']==L]
        ax.add_collection(LineCollection(segs,linewidths=lw,colors=COL[L],capstyle='round',alpha=0.9 if side in COL else 0.75))
    for L in layers:
        ps=[pad_patch(p,COL[L]) for p in D['pads'] if L in p['layers']]
        ax.add_collection(PatchCollection(ps,match_original=True,alpha=1))
    vs=[Circle((v['x'],v['y']),v['size']/2,fc='#b9b9b9',ec='none') for v in D['vias']]
    ax.add_collection(PatchCollection(vs,match_original=True))
    vh=[Circle((v['x'],v['y']),v['drill']/2,fc=BG,ec='none') for v in D['vias']]
    ax.add_collection(PatchCollection(vh,match_original=True))
    th=[Circle((p['x'],p['y']),p['drill']/2,fc=BG,ec='none') for p in D['pads'] if p['drill'] and p['type'] in('thru_hole','np_thru_hole')]
    ax.add_collection(PatchCollection(th,match_original=True))
    if labels:
        for f in D['fps']:
            if f['ref'] and ((side=='F.Cu' and f['layer']=='F.Cu') or (side=='B.Cu' and f['layer']=='B.Cu') or side=='both'):
                if f['ref'].startswith(('LBL','LOGO','MH')): continue
                ax.text(f['x'],f['y'],f['ref'],color='#f2f2f2',fontsize=5.2,ha='center',va='center',alpha=0.9)
    ax.text(X0,Y0-1.0,title,color='#e8e8e8',fontsize=14,ha='left' if not mirror else 'right',va='bottom')
    fig.savefig(path,dpi=DPI,facecolor=BG); plt.close(fig)
out=sys.argv[2] if len(sys.argv)>2 else 'docs/images'
import os; os.makedirs(out,exist_ok=True)
draw('F.Cu',out+'/render-top.png','Fledgling  |  top (F.Cu)')
draw('B.Cu',out+'/render-bottom.png','Fledgling  |  bottom (B.Cu), viewed from below',mirror=True)
draw('both',out+'/render-overview.png','Fledgling  |  90 x 40 mm, 4-layer  |  F.Cu (red) + B.Cu (blue), inner planes not shown',labels=False)
