import sys,pcbnew
sys.path.insert(0,'tools'); import rdrv_model as M
b=pcbnew.LoadBoard('backplane.kicad_pcb')
import re
SYM={}
for m in re.finditer(r'\(symbol \(lib_id "MP62_BP:[^"]+"\) \(at [^)]*\) \(unit (\d+)\)[^\n]*\(uuid "([^"]+)"\)\n    \(property "Reference" "([^"]+)"',open('backplane.kicad_sch').read()):
    SYM.setdefault(m.group(3),m.group(2))
lib='MP62_BP.pretty'
assert not b.FindFootprintByReference('U20')
def net(n):
    ni=b.FindNet(n)
    if ni is None:
        ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni)
    return ni
def place(fpname,ref,val,x,y,rot=0,back=False,nets=None,dnp=False):
    f=pcbnew.FootprintLoad(lib,fpname); f.SetReference(ref); f.SetValue(val)
    f.SetFPID(pcbnew.LIB_ID('MP62_BP',fpname))
    if ref in SYM: f.SetPath(pcbnew.KIID_PATH('/'+SYM[ref]))
    b.Add(f); f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))); f.SetOrientationDegrees(rot)
    if back: f.Flip(f.GetPosition(),pcbnew.FLIP_DIRECTION_TOP_BOTTOM if hasattr(pcbnew,'FLIP_DIRECTION_TOP_BOTTOM') else False)
    if dnp: f.SetDNP(True); f.SetExcludedFromBOM(True); f.SetExcludedFromPosFiles(True)
    if nets:
        for p in f.Pads():
            n=nets.get(p.GetNumber())
            if n: p.SetNet(net(n))
    return f
POS={'U20':(173.7,102.9,0),'U21':(158.6,102.9,0),'U22':(152.5,102.9,0),'U23':(173.7,102.9,0)}
for ref,val,fp,netm,dnp in M.ICS:
    x,y,r=POS[ref]; place(fp.split(':')[1],ref,val,x,y,r,nets={k:v[1] for k,v in netm.items() if v[1]},dnp=dnp)
# passives on B.Cu under their IC (TI: decaps directly underneath recommended, SNLS683 p.34 / SNLS668 p.28)
grp={}
for p in M.P: grp.setdefault(p[5],[]).append(p)
coords={}
def grid(items,x0,y0,cols,dx,dy):
    for i,it in enumerate(items): coords[it[0]]=(x0+(i%cols)*dx,y0+(i//cols)*dy)
g=[p for p in grp['U20'] if '0805' not in p[2]]; grid(g,POS['U20'][0]-10.2,99.0,10,2.3,1.6)
for i,p in enumerate([p for p in grp['U20'] if '0805' in p[2]]): coords[p[0]]=(POS['U20'][0]-4.2+i*4.0,105.6)
for U,cx in (('U21',POS['U21'][0]),('U22',POS['U22'][0])):
    grid([p for p in grp[U] if '0805' not in p[2]],cx-1.2,97.9,2,2.4,1.25)
    for p in grp[U]:
        if '0805' in p[2]: coords[p[0]]=(155.55,105.0)
for ref,val,fp,n1,n2,_ in M.P:
    x,y=coords[ref]; place(fp.split(':')[1],ref,val,x,y,0,back=True,nets={'1':n1,'2':n2})
b.Save('backplane.kicad_pcb'); print('saved',coords)
