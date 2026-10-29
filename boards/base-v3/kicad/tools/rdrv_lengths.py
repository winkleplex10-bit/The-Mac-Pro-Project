import pcbnew,re,math,sys,json
b=pcbnew.LoadBoard('/workspace/backups/bp-v3-redrivers-20261028/backplane.kicad_pcb')
pads={}
for f in b.GetFootprints():
  if f.GetReference() in ('J1','J9','J10'):
    for p in f.Pads():
      n=p.GetNetname()
      if re.match(r'F[PS]_(TX|RX)\d+_P$',n): pads.setdefault(n,{})[f.GetReference()]=(p.GetPosition().x/1e6,p.GetPosition().y/1e6)
L={}
for t in b.GetTracks():
  n=t.GetNetname()
  if n in pads and t.GetClass()=='PCB_TRACK': L[n]=L.get(n,0)+t.GetLength()/1e6
oc=lambda a,c:(lambda dx,dy:max(dx,dy)+(math.sqrt(2)-1)*min(dx,dy))(abs(a[0]-c[0]),abs(a[1]-c[1]))
def run(U,out=None,lim=45):
  rows=[]
  for n in sorted(pads,key=lambda s:(s[:2],s[3:5],int(re.search(r'\d+',s[3:]).group()))):
    d=pads[n]; face='J9' if n.startswith('FP') else 'J10'; lane=int(re.search(r'(\d+)_P',n).group(1))
    u='U20' if n.startswith('FP') else ('U21' if lane<4 else 'U22'); c=U[u]
    s1=oc(d['J1'],c); s2=oc(c,d[face]); rows.append((n[:-2],d['J1'],d[face],u,s1,s2,L.get(n,0)))
  if out:
    with open(out,'w') as f:
      f.write('pair,J1_pad_xy,face_pad_xy(J9=GPU-face proxy; J10=SSD),redriver,seg_A_J1_to_redriver_mm(octilinear),seg_B_redriver_to_face_mm(octilinear),direct_routed_today_mm,flag\n')
      for n,a,c,u,s1,s2,l in rows:
        fl=' '.join(x for x,v in (('A>60' if u=='U20' else 'A>45',s1>(60 if u=='U20' else 45)),('B>45',s2>45)) if v)
        f.write(f"{n},{a[0]:.1f}/{a[1]:.1f},{c[0]:.1f}/{c[1]:.1f},{u},{s1:.1f},{s2:.1f},{l:.1f},{fl}\n")
  for u in ('U20','U21','U22'):
    r=[x for x in rows if x[3]==u]
    print(u,U[u],'A %.1f-%.1f'%(min(x[4] for x in r),max(x[4] for x in r)),'B %.1f-%.1f'%(min(x[5] for x in r),max(x[5] for x in r)),'B>45:',[x[0] for x in r if x[5]>45],'A>45:',[x[0] for x in r if x[4]>45])
if __name__=='__main__':
  for name,U in json.loads(sys.argv[1]).items(): print('==',name); run(U)
