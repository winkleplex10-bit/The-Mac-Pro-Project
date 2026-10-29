import pcbnew,re,math,sys
b=pcbnew.LoadBoard('backplane.kicad_pcb')
oc=lambda a,c:(lambda dx,dy:max(dx,dy)+(math.sqrt(2)-1)*min(dx,dy))(abs(a[0]-c[0]),abs(a[1]-c[1]))
xy=lambda p:(p.GetPosition().x/1e6,p.GetPosition().y/1e6)
J1={p.GetNetname():xy(p) for p in b.FindFootprintByReference('J1').Pads() if re.match(r'F[PS]_(TX|RX)\d+_P$',p.GetNetname())}
J12={p.GetNetname():xy(p) for p in b.FindFootprintByReference('J12').Pads()}
gpu=xy(b.FindFootprintByReference('J11'))
GRP=['U21','U22']+[f'C{i}' for i in range(62,73)]+[f'R{i}' for i in range(111,118)]
def rows(U):
  R=[]
  for n in sorted(J1):
    lane=int(re.search(r'(\d+)_P',n).group(1))
    if n.startswith('FP'): u='U20'; face=gpu; fn='J11 centre (GPU pinout pending)'
    else: u='U21' if lane<4 else 'U22'; face=J12[n.replace('_P','_P_B')]; fn='J12 pad'
    R.append((n[:-2],J1[n],face,fn,u,oc(J1[n],U[u]),oc(U[u],face)))
  return R
def U0(): return {r:xy(b.FindFootprintByReference(r)) for r in ['U20','U21','U22']}
def bbs(refs,ex):
  out=[]
  for f in b.GetFootprints():
    if (f.GetReference() in ex)==(refs=='grp'):
      bb=f.GetCourtyard(pcbnew.B_Cu if f.IsFlipped() else pcbnew.F_Cu).BBox() if f.GetCourtyard(pcbnew.B_Cu if f.IsFlipped() else pcbnew.F_Cu).OutlineCount() else f.GetBoundingBox(False)
      out.append((f.GetReference(),f.IsFlipped(),bb.GetLeft()/1e6,bb.GetTop()/1e6,bb.GetRight()/1e6,bb.GetBottom()/1e6))
  return out
if 'search' in sys.argv:
  G=bbs('grp',GRP); O=[o for o in bbs('oth',GRP) if o[0] not in('U23',)]
  ko=[z.GetBoundingBox() for z in b.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowFootprints() and z.GetZoneName()!="EDGE_RING_KEEPOUT"]
  ko=[(k.GetLeft()/1e6,k.GetTop()/1e6,k.GetRight()/1e6,k.GetBottom()/1e6) for k in ko]
  base=U0(); best=[]
  for dx in [x*0.5 for x in range(-60,9)]:
    for dy in [y*0.5 for y in range(-40,12)]:
      ok=True
      for g in G:
        a=(g[2]+dx-0.2,g[3]+dy-0.2,g[4]+dx+0.2,g[5]+dy+0.2)
        if math.hypot(max(abs(a[0]-150),abs(a[2]-150)),max(abs(a[1]-100),abs(a[3]-100)))>56: ok=False;break
        if any(o[1]==g[1] and a[0]<o[4] and a[2]>o[2] and a[1]<o[5] and a[3]>o[3] for o in O) or any(a[0]<k[2] and a[2]>k[0] and a[1]<k[3] and a[3]>k[1] for k in ko): ok=False;break
      if not ok: continue
      U=dict(base); U['U21']=(base['U21'][0]+dx,base['U21'][1]+dy); U['U22']=(base['U22'][0]+dx,base['U22'][1]+dy)
      R=[r for r in rows(U) if r[4]!='U20']
      best.append((max(r[6] for r in R),sum(r[6]>45 for r in R),max(r[5] for r in R),dx,dy))
  best.sort(); print(best[:8])
if 'apply' in sys.argv:
  dx,dy=float(sys.argv[2]),float(sys.argv[3])
  for r in GRP:
    f=b.FindFootprintByReference(r); p=f.GetPosition(); f.SetPosition(pcbnew.VECTOR2I(p.x+pcbnew.FromMM(dx),p.y+pcbnew.FromMM(dy)))
  pcbnew.SaveBoard('backplane.kicad_pcb',b)
R=rows(U0())
for u in ['U20','U21','U22']:
  r=[x for x in R if x[4]==u]; print(u,U0()[u],'A %.1f-%.1f  B %.1f-%.1f  B>45 %d  A>60 %d'%(min(x[5] for x in r),max(x[5] for x in r),min(x[6] for x in r),max(x[6] for x in r),sum(x[6]>45 for x in r),sum(x[5]>60 for x in r)))
if 'csv' in sys.argv:
  with open('docs/gen5_redriver_segment_lengths_2026-10-28.csv','w') as f:
    f.write('pair,J1_pad_xy,face_xy,face_ref,redriver,seg_A_J1_to_redriver_mm(octilinear),seg_B_redriver_to_face_mm(octilinear),flag_over_45\n')
    for n,a,c,fn,u,s1,s2 in R: f.write(f"{n},{a[0]:.1f}/{a[1]:.1f},{c[0]:.1f}/{c[1]:.1f},{fn},{u},{s1:.1f},{s2:.1f},{' '.join(k for k,v in (('A',s1>45),('B',s2>45)) if v)}\n")
