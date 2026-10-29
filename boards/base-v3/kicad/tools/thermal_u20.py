# rev 7c: U26 TMP1075 @0x4A + C83, U20 heatsink keep-outs (text edit; pcbnew unavailable on box)
import re,uuid
U=lambda:str(uuid.uuid4())
def newu(t): return re.sub(r'\(uuid "[^"]+"\)',lambda m:f'(uuid "{U()}")',t)
def shift(t,dy): return re.sub(r'\(at ([\d.]+) ([\d.]+)',lambda m:f'(at {m[1]} {float(m[2])+dy:.2f}',t)
sch=open('backplane.kicad_sch').read(); L=sch.split('\n')
u3=L[3900:3925]; t='\n'.join(u3)
t=shift(t,25.4).replace('"U3"','"U26"').replace('TMP1075DGKR @0x48 core side','TMP1075DGKR @0x4A U20 redriver temp, A1=V+')
t=newu(t)
t=t.replace('(global_label "GND" (shape passive) (at 981.71 67.31','(global_label "3V3_SB" (shape passive) (at 981.71 67.31')
i=sch.find('(symbol (lib_id "MP62_BP:C") (at 802.640 350.520'); j=sch.find('\n  (symbol',i+10)
c=sch[i:j].replace('"C24"','"C83"')
c=re.sub(r'\(at ([\d.]+) ([\d.]+)',lambda m:f'(at {float(m[1])+170.18:.2f} {float(m[2])-284.48:.2f}',c)
c=newu(c)
k=sch.rfind('\n  (sheet_instances')
if k<0: k=sch.rfind('\n)')
sch=sch[:k]+'\n  '+t.strip()+'\n  '+c.strip()+sch[k:]
open('backplane.kicad_sch','w').write(sch)
pcb=open('backplane.kicad_pcb').read()
def blk(ref):
  i=pcb.find(f'(property "Reference" "{ref}"'); j=pcb.rfind('\t(footprint ',0,i); d=0;k=j
  while True:
    if pcb[k]=='(':d+=1
    elif pcb[k]==')':
      d-=1
      if d==0:break
    k+=1
  return pcb[j:k+1]
b=blk('U3').replace('"U3"','"U26"').replace('(at 197.5 107)','(at 173.7 111)',1).replace('0x48','0x4A')
# pad 6 -> 3V3_SB
b=re.sub(r'(\(pad "6"[\s\S]*?\(net )\d+ "GND"\)',r'\g<1>115 "3V3_SB")',b,1)
b=newu(b)
cb=blk('C24').replace('"C24"','"C83"'); cb=re.sub(r'\(at 151.135 123.585',r'(at 177.2 111',cb,1); cb=newu(cb)
# keep-out graphics + channel rule area
def rect(x1,y1,x2,y2,lay='Dwgs.User'): return f'\t(gr_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width 0.15) (type dash)) (fill no) (layer "{lay}") (uuid "{U()}"))\n'
def txt(s,x,y): return f'\t(gr_text "{s}" (at {x} {y} 0) (layer "Dwgs.User") (uuid "{U()}") (effects (font (size 0.8 0.8) (thickness 0.12)) (justify left)))\n'
g=rect(161.7,97.6,185.7,108.2)+txt('U20 HS PEDESTAL 24x10.6 + soft pad',161.7,96.8)
g+=rect(153.7,85.4,193.7,120.4)+txt('U20 FIN OVERHANG 40x35: parts <=3mm only',153.7,84.6)
g+=rect(185.7,97.6,208.0,108.2)+txt('U20 RADIAL AIR CHANNEL rim->U20: no tall/upstream parts',186,96.8)
g+=f'''\t(zone (net 0) (net_name "") (layer "F.Cu") (uuid "{U()}") (name "KO_U20_RADIAL_CHANNEL") (hatch edge 0.5)
\t\t(connect_pads (clearance 0)) (min_thickness 0.25) (filled_areas_thickness no)
\t\t(keepout (tracks allowed) (vias allowed) (pads allowed) (copperpour allowed) (footprints not_allowed))
\t\t(fill (thermal_gap 0.5) (thermal_bridge_width 0.5))
\t\t(polygon (pts (xy 185.7 97.6) (xy 208.0 97.6) (xy 208.0 108.2) (xy 185.7 108.2))))
'''
k=pcb.rfind('\n)')
pcb=pcb[:k]+'\n'+b+'\n'+cb+'\n'+g+pcb[k:]
open('backplane.kicad_pcb','w').write(pcb)
