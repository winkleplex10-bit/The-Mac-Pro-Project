import uuid,pcbnew,re,subprocess
U=lambda:str(uuid.uuid4())
# ---- footprint TI RGE0024M (SLVSEI3D p.55 outline, p.56 land pattern)
fn='TI_RGE0024M_VQFN-24_4x4mm_P0.5mm_2EP'
s=f'(footprint "{fn}" (version 20241229) (generator "pcbnew") (generator_version "9.0") (layer "F.Cu")\n  (descr "TI RGE0024M VQFN-24 4x4 mm, 0.5 pitch, two exposed pads: 25 = IN (2.7x1.45), 26 = GND (2.7x0.85). Source: TPS25982 datasheet SLVSEI3D (rev May 2026) p.55 outline, p.56 example land pattern (24x 0.575x0.24, extents 3.825). EP centre offsets (0.625)/(0.925) and pad-25-upper orientation read from p.5 Fig 5-1/p.56 - verify against TI CAD.")\n  (attr smd)\n'
for k,v,y,l,h in [('Reference','REF**',-3,'F.SilkS',0),('Value','TPS25982',3,'F.Fab',0),('Footprint','',0,'F.Fab',1),('Datasheet','https://www.ti.com/lit/ds/symlink/tps25982.pdf',0,'F.Fab',1),('Description','',0,'F.Fab',1)]:
  s+=f'  (property "{k}" "{v}" (at 0 {y} 0) (layer "{l}") {"(hide yes) " if h else ""}(uuid "{U()}") (effects (font (size 0.8 0.8) (thickness 0.12))))\n'
c=1.625
for i in range(6):
  o=-1.25+0.5*i
  for num,(x,y,r) in ((1+i,(-c,o,0)),(7+i,(o,c,90)),(18-i,(c,o,0)),(24-i,(o,-c,90))):
    s+=f'  (pad "{num}" smd roundrect (at {x:.3f} {y:.3f} {r}) (size 0.575 0.24) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio 0.2) (uuid "{U()}"))\n'
s+=f'  (pad "25" smd rect (at 0 -0.625) (size 2.7 1.45) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{U()}"))\n  (pad "26" smd rect (at 0 0.925) (size 2.7 0.85) (layers "F.Cu" "F.Paste" "F.Mask") (uuid "{U()}"))\n'
s+=f'  (fp_rect (start -2 -2) (end 2 2) (stroke (width 0.1) (type solid)) (fill no) (layer "F.Fab") (uuid "{U()}"))\n  (fp_rect (start -2.45 -2.45) (end 2.45 2.45) (stroke (width 0.05) (type solid)) (fill no) (layer "F.CrtYd") (uuid "{U()}"))\n  (fp_circle (center -2.4 -2.4) (end -2.25 -2.4) (stroke (width 0.15) (type solid)) (fill yes) (layer "F.SilkS") (uuid "{U()}"))\n)\n'
open(f'MP62_BP.pretty/{fn}.kicad_mod','w').write(s)
PINS={'1':('IN','EFUSE_IN'),'2':('IN','EFUSE_IN'),'3':('IN','EFUSE_IN'),'16':('IN','EFUSE_IN'),'25':('IN_PAD','EFUSE_IN'),
 '4':('GND','GND'),'5':('GND','GND'),'14':('GND','GND'),'26':('GND_PAD','GND'),
 '6':('EN/UVLO','EFUSE_EN'),'7':('ITIMER',None),'8':('ILIM','EFUSE_ILIM'),'9':('IMON','BP_12V_IMON'),'10':('RETRY_DLY','GND'),'11':('NRETRY','GND'),'12':('LDSTRT','GND'),'13':('PG','BP_12V_PG'),'15':('dVdt','EFUSE_DVDT')}
for p in range(17,25): PINS[str(p)]=('OUT','12V_MAIN_IN')
F='(effects (font (size 1.0 1.0)))'
keys=sorted(PINS,key=int); Lk=[k for k in keys if PINS[k][0] in ('IN','IN_PAD','EN/UVLO','ILIM','ITIMER','dVdt','RETRY_DLY','NRETRY')]; Rk=[k for k in keys if k not in Lk]
pin=lambda k,x,y,a: f'      (pin passive line (at {x} {y:.2f} {a}) (length 2.54) (name "{PINS[k][0]}" {F}) (number "{k}" {F}))\n'
geo={}
body=''
for i,k in enumerate(Lk): y=12.7-2.54*i; body+=pin(k,-12.7,y,0); geo[k]=(-12.7,y)
for i,k in enumerate(Rk): y=12.7-2.54*i; body+=pin(k,12.7,y,180); geo[k]=(12.7,y)
sym=('  (symbol "TPS25982" (pin_names (offset 0.508)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n    (property "Reference" "U" (at 0 16 0) (effects (font (size 1.27 1.27))))\n    (property "Value" "TPS25982" (at 0 -30 0) (effects (font (size 1.27 1.27))))\n'
 f'    (property "Footprint" "MP62_BP:{fn}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/tps25982.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n    (property "Description" "TI 15 A 2.7-24 V smart eFuse (SLVSEI3D)" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
 '    (symbol "TPS25982_0_1" (rectangle (start -10.16 15.24) (end 10.16 -27.94) (stroke (width 0.254) (type default)) (fill (type background))))\n    (symbol "TPS25982_1_1"\n'+body+'    )\n  )\n')
lib=open('MP62_BP.kicad_sym').read()
if 'symbol "TPS25982"' not in lib: k=lib.rstrip().rfind(')'); open('MP62_BP.kicad_sym','w').write(lib[:k]+sym+')\n')
sch=open('backplane.kicad_sch').read(); assert 'TPS25982' not in sch
emb='\n'.join('  '+l if l else l for l in sym.replace('(symbol "TPS25982"','(symbol "MP62_BP:TPS25982"').split('\n'))
k=sch.find('  (lib_symbols\n')+len('  (lib_symbols\n'); sch=sch[:k]+emb+'\n'+sch[k:]
ROOT='63abcf95-882c-49fe-b391-c61af6f8ab48'
def prop(k,v,x,y,h=False): return f'    (property "{k}" "{v}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)){" (hide yes)" if h else ""}))\n'
def inst(lib,ref,val,fp,x,y,pl,uid):
    s=f'  (symbol (lib_id "MP62_BP:{lib}") (at {x:.3f} {y:.3f} 0) (unit 1) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid "{uid}")\n'+prop('Reference',ref,x,y-4)+prop('Value',val,x,y+4)+prop('Footprint',fp,x,y,True)+prop('Datasheet','',x,y,True)
    for p in pl: s+=f'    (pin "{p}" (uuid "{U()}"))\n'
    return s+f'    (instances (project "backplane" (path "/{ROOT}" (reference "{ref}") (unit 1))))\n  )\n'
def lab(n,x,y,r): return f'  (global_label "{n}" (shape passive) (at {x:.2f} {y:.2f} {0 if r else 180}) (fields_autoplaced yes) (effects (font (size 1.0 1.0)) (justify {"left" if r else "right"})) (uuid "{U()}"))\n'
def nc(x,y): return f'  (no_connect (at {x:.2f} {y:.2f}) (uuid "{U()}"))\n'
X,Y=599.44,731.52; uids={}
uids['U25']=U(); out=inst('TPS25982','U25','TPS259824LNRGE',f'MP62_BP:{fn}',X,Y,keys,uids['U25'])
for k,(px,py) in geo.items():
    n=PINS[k][1]; out+= lab(n,X+px,Y-py,px>0) if n else nc(X+px,Y-py)
P=[('R122','249R 1% 0402 (ILIM ~6.0 A typ, SLVSEI3D p.9: 300R=4.98 A, 182R=8.13 A)','R','MP62_BP:R_0402_1005Metric','EFUSE_ILIM','GND'),
   ('R123','100k 1% 0402 (EN/UVLO top)','R','MP62_BP:R_0402_1005Metric','EFUSE_IN','EFUSE_EN'),
   ('R124','13k 1% 0402 (EN/UVLO bottom, ~10.4 V UVLO - verify V_EN p.8)','R','MP62_BP:R_0402_1005Metric','EFUSE_EN','GND'),
   ('R125','1.5k 1% 0402 (IMON, gain TBD p.9)','R','MP62_BP:R_0402_1005Metric','BP_12V_IMON','GND'),
   ('R126','10k 1% 0402 (PG pull-up)','R','MP62_BP:R_0402_1005Metric','3V3_SB','BP_12V_PG'),
   ('C80','22nF 25V X7R 0402 (dVdt, slew TBD)','C','MP62_BP:C_0402_1005Metric','EFUSE_DVDT','GND'),
   ('C81','1uF 25V X5R 0402 (IN)','C','MP62_BP:C_0402_1005Metric','EFUSE_IN','GND'),
   ('C82','10uF 25V X5R 0805 (OUT)','C','MP62_BP:C_0805_2012Metric','12V_MAIN_IN','GND')]
for i,(ref,val,lid,fp,n1,n2) in enumerate(P):
    x=650.24+(i%4)*25.4; y=723.9+(i//4)*15.24; uids[ref]=U()
    out+=inst(lid,ref,val,fp,x,y,['1','2'],uids[ref])+lab(n1,x-3.81,y,False)+lab(n2,x+3.81,y,True)
out+=f'  (text "Base 12 V eFuse U25 TPS259824LNRGE (Aidan 2026-10-28: base 12 V from J1 P12V, taken ahead of CB eFuse). EFUSE_IN = J1 v4 P12V pins A103-B106 (x8) - J1 symbol still v3: apply when the v4 J1 pinout freezes. OUT = 12V_MAIN_IN. J2 Micro-Fit now obsolete." (exclude_from_sim no) (at 599.44 708.66 0) (effects (font (size 2 2)) (justify left)) (uuid "{U()}"))\n'
j=sch.rfind('  (sheet_instances'); sch=sch[:j]+out+sch[j:]; open('backplane.kicad_sch','w').write(sch)
# ---- PCB
b=pcbnew.LoadBoard('backplane.kicad_pcb')
def net(n):
    ni=b.FindNet(n)
    if ni is None: ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni)
    return ni
X0,Y0=111.0,104.0
place=[('U25','TPS259824LNRGE',fn,0,0,0,{k:v[1] for k,v in PINS.items()})]+[(r,v,fp.split(':')[1],dx,dy,0,{'1':n1,'2':n2}) for (r,v,_,fp,n1,n2),(dx,dy) in zip(P,[(-3.6,-1.5),(-3.6,0.2),(-3.6,1.5),(3.6,1.5),(3.6,0.2),(-3.6,-2.8),(-1.0,-3.4),(3.9,-1.6)])]
fps=[pcbnew.FootprintLoad('MP62_BP.pretty',p[2]) for p in place]
for f,(ref,val,fpn,dx,dy,rot,nets) in zip(fps,place):
    f.SetFPID(pcbnew.LIB_ID('MP62_BP',fpn)); f.SetReference(ref); f.SetValue(val)
    f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(X0+dx),pcbnew.FromMM(Y0+dy)))
    for p in f.Pads():
        n=nets.get(p.GetNumber())
        if n: p.SetNet(net(n))
    b.Add(f)
subprocess.run(['kicad-cli','sch','export','netlist','-o','/tmp/n.net','backplane.kicad_sch'],capture_output=True)
t=open('/tmp/n.net').read()
for blk in re.split(r'\n\s*\(net ',t)[1:]:
    nm=re.search(r'\(name "([^"]*)"',blk).group(1)
    if nm.startswith('unconnected-'):
        for r,p in re.findall(r'\(ref "([^"]+)"\) \(pin "([^"]+)"',blk):
            if r=='U25':
                for pad in b.FindFootprintByReference(r).Pads():
                    if pad.GetNumber()==p: pad.SetNet(net(nm))
b.Save('backplane.kicad_pcb'); print('ok')
