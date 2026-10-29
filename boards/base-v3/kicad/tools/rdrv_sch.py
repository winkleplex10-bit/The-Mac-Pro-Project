import sys,uuid,re
sys.path.insert(0,'tools'); import rdrv_model as M
U=lambda: str(uuid.uuid4())
ROOT='63abcf95-882c-49fe-b391-c61af6f8ab48'
F='(effects (font (size 1.0 1.0)))'
def pin(name,num,x,y,ang,typ='passive'):
    return f'      (pin {typ} line (at {x:.2f} {y:.2f} {ang}) (length 2.54) (name "{name}" {F}) (number "{num}" {F}))\n'
def ballkey(b):
    m=re.match(r'([A-Z]+)(\d+)',b); return (len(m.group(1)),m.group(1),int(m.group(2)))
# ---- build pin lists
hsA=sorted([(b,v[0]) for b,v in M.U20.items() if v[0].startswith('A_PE')],key=lambda t:(int(re.search(r'\d+$',t[1]).group()),t[1]))
hsB=sorted([(b,v[0]) for b,v in M.U20.items() if v[0].startswith('B_PE')],key=lambda t:(int(re.search(r'\d+$',t[1]).group()),t[1]))
rest=sorted([(b,v[0]) for b,v in M.U20.items() if not v[0].startswith(('A_PE','B_PE'))],key=lambda t:(t[1]!='GND',t[1].startswith('VCC')==False,t[1],ballkey(t[0])))
half=(len(rest)+1)//2; restL,restR=rest[:half],rest[half:]
W=27.94
def side_pins(lst,left,top):
    out=[];pos={}
    for i,(num,name) in enumerate(lst):
        y=top-2.54*i; x=-W if left else W
        out.append(pin(name,num,x,y,0 if left else 180)); pos[num]=(x,y)
    return out,pos
geo={}  # (ref,unit)-> {pinnum:(x,y)}
def mk1601():
    s='  (symbol "DS320PR1601" (pin_names (offset 0.508)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
    s+='    (property "Reference" "U" (at 0 2 0) (effects (font (size 1.27 1.27))))\n    (property "Value" "DS320PR1601" (at 0 -2 0) (effects (font (size 1.27 1.27))))\n'
    s+='    (property "Footprint" "MP62_BP:TI_ZDG0354A_nFBGA-354_22.9x8.9mm" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    s+='    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/ds320pr1601.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    s+='    (property "Description" "TI 16-lane PCIe 5.0 linear redriver, nFBGA-354 (SNLS683). Unit A: high-speed, unit B: power/control" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    t1=2.54*32; p1,g1=side_pins(hsA,True,t1); p2,g2=side_pins(hsB,False,t1)
    s+=f'    (symbol "DS320PR1601_1_1" (rectangle (start {-W+2.54} {t1+2.54}) (end {W-2.54} {t1-2.54*64}) (stroke (width 0.254) (type default)) (fill (type background)))\n'+''.join(p1+p2)+'    )\n'
    t2=2.54*57; p3,g3=side_pins(restL,True,t2); p4,g4=side_pins(restR,False,t2)
    s+=f'    (symbol "DS320PR1601_2_1" (rectangle (start {-W+2.54} {t2+2.54}) (end {W-2.54} {t2-2.54*half}) (stroke (width 0.254) (type default)) (fill (type background)))\n'+''.join(p3+p4)+'    )\n  )\n'
    geo[('U20',1)]={**g1,**g2}; geo[('U20',2)]={**g3,**g4}
    return s
def mk810():
    items=sorted(M.U21.items(),key=lambda t:int(t[0]))
    L=[(n,v[0]) for n,v in items if v[0].startswith('RX') or v[0] in('MODE','EQ0/ADDR0','EQ1/ADDR1','GAIN0/SDA','RX_DET/SCL','PD0','PD1','READ_EN_N','ALL_DONE_N') ]
    R_=[(n,v[0]) for n,v in items if (n,v[0]) not in L]
    t=2.54*17; p1,g1=side_pins(L,True,t); p2,g2=side_pins(R_,False,t)
    s='  (symbol "DS320PR810" (pin_names (offset 0.508)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
    s+='    (property "Reference" "U" (at 0 2 0) (effects (font (size 1.27 1.27))))\n    (property "Value" "DS320PR810" (at 0 -2 0) (effects (font (size 1.27 1.27))))\n'
    s+='    (property "Footprint" "MP62_BP:TI_NJX0064A_WQFN-64_5.5x10mm_P0.4mm_EP4.1x8.6mm" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    s+='    (property "Datasheet" "https://www.ti.com/lit/ds/symlink/ds320pr810.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    s+='    (property "Description" "TI 8-channel PCIe 5.0 linear redriver, WQFN-64 NJX (SNLS668)" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
    s+=f'    (symbol "DS320PR810_1_1" (rectangle (start {-W+2.54} {t+2.54}) (end {W-2.54} {t-2.54*max(len(L),len(R_))}) (stroke (width 0.254) (type default)) (fill (type background)))\n'+''.join(p1+p2)+'    )\n  )\n'
    geo['810']={**g1,**g2}; return s
def mkpt():
    return ('  (symbol "PT5161L_ALT" (pin_names (offset 0.508)) (exclude_from_sim no) (in_bom no) (on_board yes)\n'
      '    (property "Reference" "U" (at 0 7 0) (effects (font (size 1.27 1.27))))\n    (property "Value" "PT5161L_ALT_DNP" (at 0 -7 0) (effects (font (size 1.27 1.27))))\n'
      '    (property "Footprint" "MP62_BP:Astera_PT5161L_ALT_DNP_PLACEHOLDER" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
      '    (property "Datasheet" "NDA (Astera Labs)" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
      '    (property "Description" "Fallback Gen5 x16 retimer reservation, DNP. No pins: pinout NDA-gated, no compatibility with DS320PR1601 assumed" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
      '    (symbol "PT5161L_ALT_0_1" (rectangle (start -12.7 5.08) (end 12.7 -5.08) (stroke (width 0.254) (type dash)) (fill (type none))))\n  )\n')
libsyms=mk1601()+mk810()+mkpt()
# ---- library file
lib=open('MP62_BP.kicad_sym').read()
if 'symbol "DS320PR1601"' not in lib:
    i=lib.rstrip().rfind(')'); lib=lib[:i]+libsyms+')\n'; open('MP62_BP.kicad_sym','w').write(lib)
# ---- schematic
sch=open('backplane.kicad_sch').read()
assert 'DS320PR1601' not in sch, 'already applied'
emb=libsyms.replace('(symbol "DS320PR1601"','(symbol "MP62_BP:DS320PR1601"').replace('(symbol "DS320PR810"','(symbol "MP62_BP:DS320PR810"').replace('(symbol "PT5161L_ALT"','(symbol "MP62_BP:PT5161L_ALT"')
emb='\n'.join('  '+l if l else l for l in emb.split('\n'))
i=sch.find('  (lib_symbols\n')+len('  (lib_symbols\n'); sch=sch[:i]+emb+'\n'+sch[i:]
out=[]
def prop(k,v,x,y,hide=False): return f'    (property "{k}" "{v}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)){" (hide yes)" if hide else ""}))\n'
def inst(lib,ref,val,fp,x,y,unit,pins,dnp=False,extra=''):
    s=f'  (symbol (lib_id "MP62_BP:{lib}") (at {x:.3f} {y:.3f} 0) (unit {unit}) (exclude_from_sim no) (in_bom {"no" if dnp else "yes"}) (on_board yes) (dnp {"yes" if dnp else "no"}) (uuid "{U()}")\n'
    s+=prop('Reference',ref,x,y-4)+prop('Value',val,x,y+4)+prop('Footprint',fp,x,y,True)+prop('Datasheet','',x,y,True)+extra
    for p in pins: s+=f'    (pin "{p}" (uuid "{U()}"))\n'
    s+=f'    (instances (project "backplane" (path "/{ROOT}" (reference "{ref}") (unit {unit}))))\n  )\n'
    return s
def lab(net,x,y,right):
    return f'  (global_label "{net}" (shape passive) (at {x:.2f} {y:.2f} {0 if right else 180}) (fields_autoplaced yes) (effects (font (size 1.0 1.0)) (justify {"left" if right else "right"})) (uuid "{U()}"))\n'
def nc(x,y): return f'  (no_connect (at {x:.2f} {y:.2f}) (uuid "{U()}"))\n'
def connect(g,X,Y,netmap):
    s=''
    for num,(px,py) in g.items():
        n=netmap[num][1]; ax,ay=X+px,Y-py
        s+= lab(n,ax,ay,px>0) if n else nc(ax,ay)
    return s
fp1601='MP62_BP:TI_ZDG0354A_nFBGA-354_22.9x8.9mm'; fp810='MP62_BP:TI_NJX0064A_WQFN-64_5.5x10mm_P0.4mm_EP4.1x8.6mm'
X1,Y1=76.2,571.5; X2,Y2=218.44,629.92
mpn=lambda m: f'    (property "MPN" "{m}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
out.append(inst('DS320PR1601','U20','DS320PR1601ZDGR',fp1601,X1,Y1,1,list(geo[('U20',1)]),extra=mpn('DS320PR1601ZDGR'))+connect(geo[('U20',1)],X1,Y1,M.U20))
out.append(inst('DS320PR1601','U20','DS320PR1601ZDGR',fp1601,X2,Y2,2,list(geo[('U20',2)]),extra=mpn('DS320PR1601ZDGR'))+connect(geo[('U20',2)],X2,Y2,M.U20))
for ref,X,netm in (("U21",360.68,M.U21),("U22",482.6,M.U22)):
    out.append(inst('DS320PR810',ref,'DS320PR810NJXR',fp810,X,530.86,1,list(geo['810']),extra=mpn('DS320PR810NJXR'))+connect(geo["810"],X,530.86,netm))
out.append(inst('PT5161L_ALT','U23','PT5161L_ALT_DNP','MP62_BP:Astera_PT5161L_ALT_DNP_PLACEHOLDER',599.44,500.38,1,[],dnp=True))
for k,(ref,val,fp,n1,n2,grp) in enumerate(M.P):
    x=599.44+(k%10)*25.4; y=541.02+(k//10)*15.24
    lid='C' if ref[0]=='C' else 'R'
    out.append(inst(lid,ref,val,fp,x,y,1,['1','2'])+lab(n1,x-3.81,y,False)+lab(n2,x+3.81,y,True))
note=f'  (text "Gen5 redrivers (Aidan 2026-10-28): U20 DS320PR1601 GPU x16 (A side = J1/CPU, B side = GPU face), U21/U22 DS320PR810 SSD x8 (FS lanes 0-3 / 4-7), U23 PT5161L fallback DNP (no pins, NDA, NOT pin-compatible-assumed).\\nHigh-speed nets *_A / *_B are NOT yet spliced into FP_*/FS_* (J1->J9/J10 copper still direct): net split + reroute pending.\\n3V3_RDRV is a NEW rail, source TBD (~10.5 W max = 3.2 A @3.3 V; 3V3_SB buck is 3 A standby, not used).\\nU20 address straps TBD per SNLS683 Tbl 7-3/8-1. U21 0x18/0x19, U22 0x1A/0x1B (SNLS668 Tbl 7-5)." (exclude_from_sim no) (at 360 470 0) (effects (font (size 2 2)) (justify left)) (uuid "{U()}"))\n'
out.append(note)
j=sch.rfind('  (sheet_instances'); sch=sch[:j]+''.join(out)+sch[j:]
open('backplane.kicad_sch','w').write(sch); print('sch ok')
