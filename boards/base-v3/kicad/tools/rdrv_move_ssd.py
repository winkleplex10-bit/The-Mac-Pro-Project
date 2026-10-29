import pcbnew
P='backplane.kicad_pcb'; b=pcbnew.LoadBoard(P); mm=pcbnew.FromMM
new={'U21':(129.0,90.0),'U22':(136.0,90.0)}
moved=[]
for u,(nx,ny) in new.items():
  f=b.FindFootprintByReference(u); o=f.GetPosition(); d=pcbnew.VECTOR2I(mm(nx)-o.x,mm(ny)-o.y)
  nets={p.GetNetCode() for p in f.Pads() if p.GetNetCode()>0 and 'GND' not in p.GetNetname()}
  for g in b.GetFootprints():
    if g.GetReference()[0] in 'CR' and abs(g.GetPosition().x-o.x)<mm(4) and abs(g.GetPosition().y-o.y)<mm(7) and any(p.GetNetCode() in nets for p in g.Pads()):
      g.Move(d); moved.append(g.GetReference())
  f.Move(d); moved.append(u)
  nt=sum(1 for t in b.GetTracks() if t.GetNetCode() in nets)
  print(u,'->',nx,ny,'tracks on its nets',nt)
print('moved',moved)
pcbnew.SaveBoard(P,b)
