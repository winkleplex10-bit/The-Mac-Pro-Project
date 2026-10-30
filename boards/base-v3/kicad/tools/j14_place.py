# 2026-10-29: place J14 MCIO-124 vertical, top side, (150,130) rot 180; clear courtyard; rip broken tracks (no reroute)
import pcbnew, csv, json, math
P='backplane.kicad_pcb'
b=pcbnew.LoadBoard(P); mm=pcbnew.FromMM; tm=lambda v:v/1e6
old=b.FindFootprintByReference('J14')
oldnets={p.GetNumber():p.GetNetname() for p in old.Pads() if p.GetNumber()}
lib=pcbnew.FootprintLoad('MP62_Placeholders.pretty','MP62_MCIO_124P_Vertical_SMT_TE2360189_PLACEHOLDER')
lib.SetReference('J14'); lib.SetValue(old.GetValue())
for f in ('MPN','Manufacturer','Datasheet'):
  pass
lib.SetPath(old.GetPath()); 
try: lib.SetSheetname(old.GetSheetname()); lib.SetSheetfile(old.GetSheetfile())
except Exception: pass
b.Add(lib); lib.SetPosition(pcbnew.VECTOR2I(mm(150),mm(130))); lib.SetOrientationDegrees(180)
nb={n.GetNetname():n for n in b.GetNetInfo().NetsByName().values()} if False else None
miss=[]
for p in lib.Pads():
  n=p.GetNumber()
  if n in oldnets: p.SetNet(b.FindNet(oldnets[n]))
  elif n=='SH' or n=='MP': p.SetNet(b.FindNet('GND'))
  elif n: miss.append(n)
b.Remove(old)
# verify vs csv
bad=[]
for r in csv.DictReader(open('/workspace/docs/pinmaps/base-cbj3-j14-mcio-map.csv')):
  c=r['base_j14_contact']; want=r['base_net']
  got=[p.GetNetname() for p in lib.Pads() if p.GetNumber()==c]
  if not got or got[0]!=want: bad.append((c,want,got))
j=lib; cy=j.GetCourtyard(pcbnew.F_CrtYd).BBox()
KO=(min(127,tm(cy.GetLeft())),min(124,tm(cy.GetTop())),max(173,tm(cy.GetRight())),max(137,tm(cy.GetBottom())))
print('J14 crtyd',tm(cy.GetLeft()),tm(cy.GetTop()),tm(cy.GetRight()),tm(cy.GetBottom()),'KO',KO,'pinmap mismatches',bad,'unnetted pads',miss)
fixed={'J1','J11','J12','J13','J14','H3','U20','U23','U21','U22'}
def box(m,c=0.2):
  bb=m.GetBoundingBox(False); return (tm(bb.GetLeft())-c,tm(bb.GetTop())-c,tm(bb.GetRight())+c,tm(bb.GetBottom())+c)
ov=lambda a,b_:a[0]<b_[2] and b_[0]<a[2] and a[1]<b_[3] and b_[1]<a[3]
F=[m for m in b.GetFootprints() if not m.IsFlipped()]
movers=[m for m in F if m.GetReference() not in fixed and ov(box(m,0),KO)]
# board outline
ed=b.GetBoardEdgesBoundingBox()
poly=pcbnew.SHAPE_POLY_SET(); b.GetBoardPolygonOutlines(poly)
def inboard(bx):
  for x,y in ((bx[0],bx[1]),(bx[2],bx[1]),(bx[0],bx[3]),(bx[2],bx[3])):
    if not poly.Contains(pcbnew.VECTOR2I(mm(x),mm(y))): return False
  # 1 mm edge margin
  return all(poly.Contains(pcbnew.VECTOR2I(mm(x),mm(y))) for x,y in ((bx[0]-1,bx[1]-1),(bx[2]+1,bx[3]+1),(bx[0]-1,bx[3]+1),(bx[2]+1,bx[1]-1)))
H3=(169,127,175,133); J13k=box(b.FindFootprintByReference('J13'),0.5)
stat=[box(m) for m in F if m not in movers]
# pad->track map before move
oldpad={}
for m in movers:
  oldpad[m.GetReference()]=[(p.GetPosition(),p.GetNetname(),p) for p in m.Pads()]
movers.sort(key=lambda m:-min(abs(tm(m.GetPosition().x)-150)/23, abs(tm(m.GetPosition().y)-130.5)/6.5))
moved=[]
for m in movers:
  x0,y0=tm(m.GetPosition().x),tm(m.GetPosition().y); bx=box(m); w=bx[2]-bx[0]; h=bx[3]-bx[1]
  ox,oy=x0-(bx[0]+bx[2])/2,y0-(bx[1]+bx[3])/2
  best=None
  for r in range(0,160):
    rr=r*0.25
    for k in range(max(1,int(2*math.pi*rr/0.5))):
      a=2*math.pi*k/max(1,int(2*math.pi*rr/0.5)); cx=(bx[0]+bx[2])/2+rr*math.cos(a); cy_=(bx[1]+bx[3])/2+rr*math.sin(a)
      cx=round(cx*20)/20; cy_=round(cy_*20)/20
      nb_=(cx-w/2,cy_-h/2,cx+w/2,cy_+h/2)
      if ov(nb_,KO) or ov(nb_,H3) or ov(nb_,J13k) or any(ov(nb_,s) for s in stat): continue
      if not inboard(nb_): continue
      best=(cx+ox,cy_+oy,nb_); break
    if best: break
  if not best: print('NO SPOT',m.GetReference()); continue
  m.SetPosition(pcbnew.VECTOR2I(mm(best[0]),mm(best[1]))); stat.append(best[2])
  moved.append((m.GetReference(),round(x0,2),round(y0,2),round(best[0],2),round(best[1],2),round(math.hypot(best[0]-x0,best[1]-y0),1)))
# rip tracks touching old pad positions, plus vias/F.Cu tracks under J14 courtyard, then dangling
dels={}
K=lambda t:t.m_Uuid.AsString()
tracks=list(b.GetTracks())
def hit(t,pt,tol=mm(0.3)):
  if t.GetClass()=='PCB_VIA': return (t.GetPosition()-pt).EuclideanNorm()<tol
  return (t.GetStart()-pt).EuclideanNorm()<tol or (t.GetEnd()-pt).EuclideanNorm()<tol
for ref,lst in oldpad.items():
  for pos,net,p in lst:
    for t in tracks:
      if t.GetNetname()==net and t.GetClass()!='PCB_VIA' and hit(t,pos): dels[K(t)]=t
cyb=(KO[0],KO[1],KO[2],KO[3])
for t in tracks:
  bb=t.GetBoundingBox(); tb=(tm(bb.GetLeft()),tm(bb.GetTop()),tm(bb.GetRight()),tm(bb.GetBottom()))
  if ov(tb,(tm(cy.GetLeft()),tm(cy.GetTop()),tm(cy.GetRight()),tm(cy.GetBottom()))) and (t.GetClass()=='PCB_VIA' or t.GetLayer()==pcbnew.F_Cu): dels[K(t)]=t
# conservative dangling cleanup: only nets already touched; endpoint is dangling only if it hits no pad, via or other track
touched={t.GetNetname() for t in dels.values()}
for it in range(40):
  new={}
  live=[t for t in tracks if K(t) not in dels and t.GetNetname() in touched]
  for t in live:
    if t.GetClass()=='PCB_VIA': continue
    for q in (t.GetStart(),t.GetEnd()):
      net=t.GetNetname()
      if any(p.HitTest(q) for m in b.GetFootprints() for p in m.Pads() if p.GetNetname()==net and (p.GetPosition()-q).EuclideanNorm()<mm(5)): continue
      if any(o is not t and K(o)!=K(t) and o.HitTest(q,mm(0.01)) and (o.GetClass()=='PCB_VIA' or o.GetLayer()==t.GetLayer()) for o in live): continue
      if any(z.GetNetname()==net and z.HitTestFilledArea(t.GetLayer(),q) for z in b.Zones()): continue
      new[K(t)]=t; break
  if not new: break
  dels.update(new)
rip={}
for t in dels.values():
  rip.setdefault(t.GetNetname(),[0,0]); rip[t.GetNetname()][1 if t.GetClass()=='PCB_VIA' else 0]+=1
  b.Remove(t)
b.Save(P)
json.dump({'moved':moved,'ripped':rip,'pinmap_bad':bad,'KO':KO},open('work/j14_place_result.json','w'),indent=1)
print('moved',len(moved)); [print(x) for x in moved]
print('ripped nets',len(rip)); [print(k,v) for k,v in sorted(rip.items())]
