import pcbnew,re,math,sys
b=pcbnew.LoadBoard('backplane.kicad_pcb')
oc=lambda a,c:(lambda dx,dy:max(dx,dy)+(math.sqrt(2)-1)*min(dx,dy))(abs(a[0]-c[0]),abs(a[1]-c[1]))
J1={}
for p in b.FindFootprintByReference('J1').Pads():
  n=p.GetNetname()
  if re.match(r'F[PS]_(TX|RX)\d+_P$',n): J1[n]=(p.GetPosition().x/1e6,p.GetPosition().y/1e6)
J12={p.GetNetname():(p.GetPosition().x/1e6,p.GetPosition().y/1e6) for p in b.FindFootprintByReference('J12').Pads()}
U={r:(b.FindFootprintByReference(r).GetPosition().x/1e6,b.FindFootprintByReference(r).GetPosition().y/1e6) for r in ('U20','U21','U22')}
def run(gpu_face,label,out=None):
  rows=[]
  for n in sorted(J1,key=lambda s:(s[:2],s[3:5],int(re.search(r'\d+',s[3:]).group()))):
    lane=int(re.search(r'(\d+)_P',n).group(1))
    if n.startswith('FP'): u='U20'; face=gpu_face; fname='J11 centre (GPU pinout pending)'
    else: u='U21' if lane<4 else 'U22'; face=J12[n.replace('_P','_P_B')]; fname='J12 pad'
    s1=oc(J1[n],U[u]); s2=oc(U[u],face); rows.append((n[:-2],J1[n],face,u,s1,s2,fname))
  for u in U:
    r=[x for x in rows if x[3]==u]
    print(label,u,'A %.1f-%.1f B %.1f-%.1f'%(min(x[4] for x in r),max(x[4] for x in r),min(x[5] for x in r),max(x[5] for x in r)),'B>45:',len([x for x in r if x[5]>45]),'A>45:',len([x for x in r if x[4]>45]))
  if out:
    with open(out,'w') as f:
      f.write('pair,J1_pad_xy,face_xy,face_ref,redriver,seg_A_J1_to_redriver_mm(octilinear),seg_B_redriver_to_face_mm(octilinear),flag_over_45\n')
      for n,a,c,u,s1,s2,fn in rows:
        f.write(f"{n},{a[0]:.1f}/{a[1]:.1f},{c[0]:.1f}/{c[1]:.1f},{fn},{u},{s1:.1f},{s2:.1f},{' '.join(k for k,v in (('A',s1>45),('B',s2>45)) if v)}\n")
g=b.FindFootprintByReference('J11').GetPosition()
run((g.x/1e6,g.y/1e6),'STOCK-ALIGNED(GPU right J11, SSD left J12)','docs/gen5_redriver_segment_lengths_2026-10-28.csv')
