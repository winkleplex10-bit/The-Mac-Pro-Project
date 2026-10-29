import pcbnew,csv
b=pcbnew.LoadBoard('backplane.kicad_pcb')
def net(n):
    ni=b.FindNet(n)
    if ni is None: ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni)
    return ni
NETS={r['position']:r['base_net'] for r in csv.DictReader(open('/workspace/docs/pinmaps/base-ssd-megarray.csv'))}
FPN='Amphenol_MegArray_84501_300P_10x30_P1.27mm_UNVERIFIED'
for ref,val,x,y,rot,nets in (('J11','MEG300 84501 GPU face (pinout: GPU Board, pending)',115.0,66.0,45,{}),('J12','MEG300 84501 SSD face (base-ssd-megarray.csv)',185.0,66.0,-45,NETS)):
    f=pcbnew.FootprintLoad('MP62_BP.pretty',FPN); f.SetFPID(pcbnew.LIB_ID('MP62_BP',FPN))
    f.SetReference(ref); f.SetValue(val)
    f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x),pcbnew.FromMM(y))); f.SetOrientationDegrees(rot)
    for p in f.Pads():
        n=nets.get(p.GetNumber())
        if n: p.SetNet(net(n))
    b.Add(f)
rm=[z for z in b.Zones() if z.GetZoneName() in ('MCIO_RIBBON_J9','MCIO_RIBBON_J10')]
fr=[b.FindFootprintByReference(r) for r in ('J9','J10')]
for z in rm: b.Remove(z)
for f in fr: b.Remove(f)
b.Save('backplane.kicad_pcb'); print('ok')
