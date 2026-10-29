import pcbnew,re,subprocess
b=pcbnew.LoadBoard('backplane.kicad_pcb')
def net(n):
    ni=b.FindNet(n)
    if ni is None: ni=pcbnew.NETINFO_ITEM(b,n); b.Add(ni)
    return ni
X,Y=118.0,96.0
parts=[('U24','TPS565208DDCR','SOT-23-6',0,0,0,{'1':'GND','2':'SW_3V3_RDRV','3':'12V_MAIN_IN','4':'FB_3V3_RDRV','5':'RDRV_BUCK_EN','6':'BST_3V3_RDRV'}),
 ('C73','10uF 25V X5R 0805','C_0805_2012Metric',-4.2,-1.3,0,{'1':'12V_MAIN_IN','2':'GND'}),('C74','10uF 25V X5R 0805','C_0805_2012Metric',-4.2,1.3,0,{'1':'12V_MAIN_IN','2':'GND'}),
 ('C75','100nF 25V X7R 0402','C_0402_1005Metric',-4.2,3.3,0,{'1':'12V_MAIN_IN','2':'GND'}),('C76','100nF 16V X7R 0402 (VBST)','C_0402_1005Metric',0,-2.8,0,{'1':'BST_3V3_RDRV','2':'SW_3V3_RDRV'}),
 ('L5','2.2uH Isat>=7A (part TBD; 4x4 fp placeholder)','L_Changjiang_FNR4030S',4.6,0,0,{'1':'SW_3V3_RDRV','2':'3V3_RDRV'}),
 ('C77','22uF 10V X5R 0805','C_0805_2012Metric',4.6,-3.7,0,{'1':'3V3_RDRV','2':'GND'}),('C78','22uF 10V X5R 0805','C_0805_2012Metric',4.6,3.7,0,{'1':'3V3_RDRV','2':'GND'}),
 ('C79','22uF 10V X5R 0805','C_0805_2012Metric',8.6,0,90,{'1':'3V3_RDRV','2':'GND'}),
 ('R118','33.2k 1% 0402 (FB top, SLVSE72B Tbl 2)','R_0402_1005Metric',0.9,2.9,0,{'1':'3V3_RDRV','2':'FB_3V3_RDRV'}),('R119','10k 1% 0402 (FB bottom)','R_0402_1005Metric',0.9,4.1,0,{'1':'FB_3V3_RDRV','2':'GND'}),
 ('R120','100k 1% 0402 (EN pull-up, always on)','R_0402_1005Metric',-1.6,4.1,0,{'1':'12V_MAIN_IN','2':'RDRV_BUCK_EN'}),
 ('R121','0R 0402 DNP (SSD optional 3V3_SB)','R_0402_1005Metric',-1.6,-3.4,0,{'1':'3V3_SB','2':'SSD_3V3_SB_OPT'})]
fps=[pcbnew.FootprintLoad('MP62_BP.pretty',p[2]) for p in parts]
for f,(ref,val,fpn,dx,dy,rot,nets) in zip(fps,parts):
    f.SetFPID(pcbnew.LIB_ID('MP62_BP',fpn)); f.SetReference(ref); f.SetValue(val)
    f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(X+dx),pcbnew.FromMM(Y+dy))); f.SetOrientationDegrees(rot)
    if ref=='R121': f.SetDNP(True); f.SetExcludedFromBOM(True); f.SetExcludedFromPosFiles(True)
    for p in f.Pads():
        n=nets.get(p.GetNumber())
        if n: p.SetNet(net(n))
    b.Add(f)
# schematic no-connect nets for J11 / J12 spare pads
subprocess.run(['kicad-cli','sch','export','netlist','-o','/tmp/n.net','backplane.kicad_sch'],capture_output=True)
s=open('/tmp/n.net').read()
for blk in re.split(r'\n\s*\(net ',s)[1:]:
    nm=re.search(r'\(name "([^"]*)"',blk).group(1)
    if nm.startswith('unconnected-'):
        for r,p in re.findall(r'\(ref "([^"]+)"\) \(pin "([^"]+)"',blk):
            if r in ('J11','J12'):
                for pad in b.FindFootprintByReference(r).Pads():
                    if pad.GetNumber()==p: pad.SetNet(net(nm))
b.Save('backplane.kicad_pcb'); print('ok')
