import re, math
def tokenize(s):
    return re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', s)
def parse(s):
    toks=tokenize(s); stack=[[]]
    for t in toks:
        if t=='(':
            stack.append([])
        elif t==')':
            x=stack.pop(); stack[-1].append(x)
        else:
            stack[-1].append(t[1:-1] if t.startswith('"') else t)
    return stack[0][0]
def find(n,name): return [c for c in n if isinstance(c,list) and c and c[0]==name]
def f1(n,name):
    r=find(n,name); return r[0] if r else None
def num(x): return float(x)
def rot(x,y,a):
    r=math.radians(a); c,s=math.cos(r),math.sin(r)
    return x*c+y*s, -x*s+y*c
def load(path):
    b=parse(open(path).read())
    D=dict(pads=[],segs=[],vias=[],zones=[],edge=[],fps=[],nets={})
    for n in find(b,'net'):
        D['nets'][int(n[1])]=n[2]
    for fp in find(b,'footprint'):
        at=f1(fp,'at'); fx,fy=num(at[1]),num(at[2]); fa=num(at[3]) if len(at)>3 else 0
        layer=f1(fp,'layer')[1]
        ref=''
        for p in find(fp,'property'):
            if p[1]=='Reference': ref=p[2]
        D['fps'].append(dict(ref=ref,x=fx,y=fy,a=fa,layer=layer,name=fp[1]))
        for pd in find(fp,'pad'):
            pat=f1(pd,'at'); px,py=num(pat[1]),num(pat[2]); pa=num(pat[3]) if len(pat)>3 else 0
            rx,ry=rot(px,py,fa)
            sz=f1(pd,'size'); w,h=num(sz[1]),num(sz[2])
            ang=pa if len(pat)>3 else fa
            if int(round(ang))%180==90: w,h=h,w
            layers=f1(pd,'layers')[1:]
            net=f1(pd,'net'); netname=net[2] if net and len(net)>2 else (net[1] if net else '')
            dr=f1(pd,'drill'); drill=num(dr[1]) if dr and len(dr)>1 and dr[1]!='oval' else (num(dr[2]) if dr and len(dr)>2 else 0)
            D['pads'].append(dict(ref=ref,num=pd[1],type=pd[2],shape=pd[3],x=fx+rx,y=fy+ry,w=w,h=h,layers=layers,net=netname,drill=drill,fplayer=layer))
    for s in find(b,'segment'):
        st,en=f1(s,'start'),f1(s,'end')
        D['segs'].append(dict(x1=num(st[1]),y1=num(st[2]),x2=num(en[1]),y2=num(en[2]),w=num(f1(s,'width')[1]),layer=f1(s,'layer')[1],net=f1(s,'net')[1] if f1(s,'net') else ''))
    for v in find(b,'via'):
        at=f1(v,'at'); net=f1(v,'net')
        D['vias'].append(dict(x=num(at[1]),y=num(at[2]),size=num(f1(v,'size')[1]),drill=num(f1(v,'drill')[1]),net=net[1] if net else '',layers=f1(v,'layers')[1:]))
    for z in find(b,'zone'):
        net=f1(z,'net') or f1(z,'net_name'); lay=f1(z,'layer') or f1(z,'layers')
        poly=f1(z,'polygon'); pts=[]
        if poly:
            pts=[(num(p[1]),num(p[2])) for p in find(f1(poly,'pts'),'xy')]
        D['zones'].append(dict(net=net[1] if net else '',layer=lay[1] if lay else '',pts=pts,keepout=f1(z,'keepout') is not None,name=(f1(z,'name') or ['',''])[1]))
    for tag in ('gr_line','gr_rect','gr_arc'):
        for g in find(b,tag):
            if f1(g,'layer') and f1(g,'layer')[1]=='Edge.Cuts':
                pts=[]
                for k in ('start','end','mid'):
                    e=f1(g,k)
                    if e: pts.append((num(e[1]),num(e[2])))
                D['edge'].append((tag,pts))
    return D
