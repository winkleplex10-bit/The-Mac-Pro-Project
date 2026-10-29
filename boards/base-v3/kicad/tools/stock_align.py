import pcbnew,math,sys
P='backplane.kicad_pcb'
b=pcbnew.LoadBoard(P)
M=lambda x,y:(150+x,100-y)   # BP stock frame (y up, origin hole midpoint) -> KiCad
mm=pcbnew.FromMM
def place(ref,xy,rot):
  f=b.FindFootprintByReference(ref); X,Y=M(*xy)
  f.SetPosition(pcbnew.VECTOR2I(mm(X),mm(Y))); f.SetOrientationDegrees(rot); print(ref,'->',round(X,2),round(Y,2),rot)
if 'apply' in sys.argv:
  place('J11',(35.63,32.26),-46.7)   # GPU face, upper-right (stock GPU_R)
  place('J12',(-35.76,31.89),46.5)   # SSD face, upper-left (stock GPU_L)
S={'S1':(-52.64,13.81),'S2':(-26.57,-46.65),'S3':(26.49,-46.64),'S4':(-18.12,50.70),'S5':(18.49,50.72),'S6':(52.80,13.88)}
if 'apply' in sys.argv:
  for z in list(b.Zones()):
    if z.GetZoneName().startswith('CR-BP-1_KO_S'): b.Remove(z)
  for k,(x,y) in S.items():
    X,Y=M(x,y); z=pcbnew.ZONE(b); z.SetIsRuleArea(True); z.SetZoneName('KO6_'+k)
    z.SetDoNotAllowFootprints(True); z.SetDoNotAllowTracks(True); z.SetDoNotAllowVias(True); z.SetDoNotAllowPads(True); z.SetDoNotAllowCopperPour(True)
    ls=pcbnew.LSET.AllCuMask(); z.SetLayerSet(ls)
    o=pcbnew.SHAPE_POLY_SET(); o.NewOutline()
    for i in range(32):
      a=2*math.pi*i/32; o.Append(mm(X+3*math.cos(a)),mm(Y+3*math.sin(a)))
    z.SetOutline(o)
    b.Add(z)
  pcbnew.SaveBoard(P,b)
# reports
for ref in ['J11','J12']:
  f=b.FindFootprintByReference(ref); c=f.GetPosition(); a=math.radians(f.GetOrientationDegrees())
  for nm,(hw,hh) in (('fab44.2x17.4',(22.1,8.72)),('pads',(18.415+0.3,5.715+0.3))):
    rs=[]
    for sx,sy in ((1,1),(1,-1),(-1,1),(-1,-1)):
      x=sx*hw*math.cos(a)+sy*hh*math.sin(a); y=-sx*hw*math.sin(a)+sy*hh*math.cos(a)
      X=c.x/1e6+x; Y=c.y/1e6+y; rs.append((math.hypot(X-150,Y-100),math.hypot(X-150,Y-100.6)))
    print(ref,nm,'max r (hole-mid centre / true disc centre +0.6):','%.2f / %.2f'%(max(r[0] for r in rs),max(r[1] for r in rs)),'edge r 61.035')
# S-hole conflicts: footprint hull (courtyard if present) within 3 mm of hole centre
for k,(x,y) in S.items():
  X,Y=M(x,y); p=pcbnew.VECTOR2I(mm(X),mm(Y))
  for f in b.GetFootprints():
    cy=f.GetCourtyard(pcbnew.B_Cu if f.IsFlipped() else pcbnew.F_Cu)
    if cy.OutlineCount()==0:
      cy=f.GetBoundingHull()
    d=0 if cy.Contains(p) else math.sqrt(cy.SquaredDistance(p))/1e6
    if d<3: print(k,'CONFLICT',f.GetReference(),'gap-to-centre %.2f mm (needs >=3)'%d)
  n=sum(1 for t in b.GetTracks() if min(math.hypot(q.x/1e6-X,q.y/1e6-Y) for q in (t.GetStart(),t.GetEnd()))<3)
  if n: print(k,'track/via endpoints inside 3 mm:',n)
# stock-implied
for nm,(cx,cy_,ax) in (('GPU_R',(35.63,32.26,-46.7)),('GPU_L',(-35.76,31.89,46.5))):
  a=math.radians(ax); r=[]
  for sx in(1,-1):
    for sy in(1,-1):
      x=cx+sx*22.5*math.cos(a)-sy*9*math.sin(a); y=cy_+sx*22.5*math.sin(a)+sy*9*math.cos(a); r.append(math.hypot(x,y+0.6))
  print('stock',nm,'45x18 body max r from disc centre %.2f vs disc r 61.035'%max(r))
