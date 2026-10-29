import pcbnew,math
P='backplane.kicad_pcb'; b=pcbnew.LoadBoard(P); mm=pcbnew.FromMM
def maxr(cx,cy,deg):
  a=math.radians(deg); return max(math.hypot(cx+sx*22.1*math.cos(a)+sy*8.72*math.sin(a)-150, cy-sx*22.1*math.sin(a)+sy*8.72*math.cos(a)-100) for sx in(1,-1) for sy in(1,-1))
for ref,deg in (('J11',-46.7),('J12',46.5)):
  f=b.FindFootprintByReference(ref); c=f.GetPosition(); cx,cy=c.x/1e6,c.y/1e6
  # normal direction outward = radial of centre
  ux,uy=(cx-150),(cy-100); L=math.hypot(ux,uy); ux/=L; uy/=L
  lo,hi=-5,0
  for _ in range(60):
    m=(lo+hi)/2
    if maxr(cx+m*ux,cy+m*uy,deg)>60.535: hi=m
    else: lo=m
  nx,ny=cx+lo*ux,cy+lo*uy
  f.SetPosition(pcbnew.VECTOR2I(mm(nx),mm(ny)))
  print(ref,'shift %.2f mm radial -> KiCad (%.2f, %.2f) rot %.1f ; stock frame (%.2f, %.2f) r %.2f ; corner r %.3f'%(lo,nx,ny,deg,nx-150,100-ny,math.hypot(nx-150,ny-100),maxr(nx,ny,deg)))
pcbnew.SaveBoard(P,b)
