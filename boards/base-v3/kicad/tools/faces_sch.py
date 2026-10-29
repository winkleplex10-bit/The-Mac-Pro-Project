import uuid,csv,re
U=lambda:str(uuid.uuid4()); ROOT='63abcf95-882c-49fe-b391-c61af6f8ab48'
F='(effects (font (size 1.0 1.0)))'
sch=open('backplane.kicad_sch').read(); assert 'MEG300' not in sch
# J9/J10 off board (MCIO stand-ins superseded by MEG-Array faces)
for r in ('J9','J10'):
    i=sch.find(f'(property "Reference" "{r}"'); j=sch.rfind('(symbol (lib_id',0,i)
    seg=sch[j:i].replace('(on_board yes)','(on_board no)').replace('(dnp no)','(dnp yes)').replace('(in_bom yes)','(in_bom no)')
    sch=sch[:j]+seg+sch[i:]
pos=[f'{r}{c}' for r in 'ABCDEFGHIJ' for c in range(1,31)]
L=pos[:150]; R=pos[150:]
def pins():
    s=''
    for i,p in enumerate(L): s+=f'      (pin passive line (at -12.7 {190.5-2.54*i:.2f} 0) (length 2.54) (name "{p}" {F}) (number "{p}" {F}))\n'
    for i,p in enumerate(R): s+=f'      (pin passive line (at 12.7 {190.5-2.54*i:.2f} 180) (length 2.54) (name "{p}" {F}) (number "{p}" {F}))\n'
    return s
FP='MP62_BP:Amphenol_MegArray_84501_300P_10x30_P1.27mm_UNVERIFIED'
sym=('  (symbol "MEG300" (pin_names (offset 0.508)) (exclude_from_sim no) (in_bom yes) (on_board yes)\n'
 '    (property "Reference" "J" (at 0 194 0) (effects (font (size 1.27 1.27))))\n    (property "Value" "MEG300" (at 0 -194 0) (effects (font (size 1.27 1.27))))\n'
 f'    (property "Footprint" "{FP}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
 '    (property "Datasheet" "https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
 '    (property "Description" "Amphenol MEG-Array 300 pos 10x30 receptacle 84501 (4 mm with 84500)" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))\n'
 '    (symbol "MEG300_0_1" (rectangle (start -10.16 193.04) (end 10.16 -190.5) (stroke (width 0.254) (type default)) (fill (type background))))\n'
 '    (symbol "MEG300_1_1"\n'+pins()+'    )\n  )\n')
lib=open('MP62_BP.kicad_sym').read()
if 'symbol "MEG300"' not in lib:
    k=lib.rstrip().rfind(')'); open('MP62_BP.kicad_sym','w').write(lib[:k]+sym+')\n')
emb='\n'.join('  '+l if l else l for l in sym.replace('(symbol "MEG300"','(symbol "MP62_BP:MEG300"').split('\n'))
k=sch.find('  (lib_symbols\n')+len('  (lib_symbols\n'); sch=sch[:k]+emb+'\n'+sch[k:]
def prop(k,v,x,y,h=False): return f'    (property "{k}" "{v}" (at {x:.2f} {y:.2f} 0) (effects (font (size 1.27 1.27)){" (hide yes)" if h else ""}))\n'
def inst(lib,ref,val,fp,x,y,pl,dnp=False):
    s=f'  (symbol (lib_id "MP62_BP:{lib}") (at {x:.3f} {y:.3f} 0) (unit 1) (exclude_from_sim no) (in_bom {"no" if dnp else "yes"}) (on_board yes) (dnp {"yes" if dnp else "no"}) (uuid "{U()}")\n'
    s+=prop('Reference',ref,x,y-4)+prop('Value',val,x,y+4)+prop('Footprint',fp,x,y,True)+prop('Datasheet','',x,y,True)
    for p in pl: s+=f'    (pin "{p}" (uuid "{U()}"))\n'
    return s+f'    (instances (project "backplane" (path "/{ROOT}" (reference "{ref}") (unit 1))))\n  )\n'
def lab(n,x,y,right): return f'  (global_label "{n}" (shape passive) (at {x:.2f} {y:.2f} {0 if right else 180}) (fields_autoplaced yes) (effects (font (size 1.0 1.0)) (justify {"left" if right else "right"})) (uuid "{U()}"))\n'
def nc(x,y): return f'  (no_connect (at {x:.2f} {y:.2f}) (uuid "{U()}"))\n'
NETS={r['position']:r['base_net'] for r in csv.DictReader(open('/workspace/docs/pinmaps/base-ssd-megarray.csv'))}
out=[]
for ref,val,X,nets in (('J11','MEG300 84501 GPU face (pinout pending GPU Board)',899.16,{}),('J12','MEG300 84501 SSD face',1066.8,NETS)):
    Y=647.7; s=inst('MEG300',ref,val,FP,X,Y,pos)
    for i,p in enumerate(L):
        x,y=X-12.7,Y-(190.5-2.54*i); n=nets.get(p); s+=lab(n,x,y,False) if n else nc(x,y)
    for i,p in enumerate(R):
        x,y=X+12.7,Y-(190.5-2.54*i); n=nets.get(p); s+=lab(n,x,y,True) if n else nc(x,y)
    out.append(s)
# 12 V -> 3V3_RDRV buck (TI TPS565208, SLVSE72B), same pinout as TPS563201 symbol
bx,by=599.44,670.56
s=inst('TPS563201','U24','TPS565208DDCR','MP62_BP:SOT-23-6',bx,by,['1','2','3','4','5','6'])
for (px,py,n) in ((-7.62,2.54,'12V_MAIN_IN'),(-7.62,0,'RDRV_BUCK_EN'),(-7.62,-2.54,'GND'),(7.62,2.54,'SW_3V3_RDRV'),(7.62,0,'BST_3V3_RDRV'),(7.62,-2.54,'FB_3V3_RDRV')):
    s+=lab(n,bx+px,by-py,px>0)
out.append(s)
P=[('C73','10uF 25V X5R 0805','MP62_BP:C_0805_2012Metric','12V_MAIN_IN','GND'),('C74','10uF 25V X5R 0805','MP62_BP:C_0805_2012Metric','12V_MAIN_IN','GND'),('C75','100nF 25V X7R 0402','MP62_BP:C_0402_1005Metric','12V_MAIN_IN','GND'),
   ('C76','100nF 16V X7R 0402 (VBST)','MP62_BP:C_0402_1005Metric','BST_3V3_RDRV','SW_3V3_RDRV'),
   ('C77','22uF 10V X5R 0805','MP62_BP:C_0805_2012Metric','3V3_RDRV','GND'),('C78','22uF 10V X5R 0805','MP62_BP:C_0805_2012Metric','3V3_RDRV','GND'),('C79','22uF 10V X5R 0805','MP62_BP:C_0805_2012Metric','3V3_RDRV','GND'),
   ('R118','33.2k 1% 0402 (FB top, SLVSE72B Tbl 2)','MP62_BP:R_0402_1005Metric','3V3_RDRV','FB_3V3_RDRV'),('R119','10k 1% 0402 (FB bottom)','MP62_BP:R_0402_1005Metric','FB_3V3_RDRV','GND'),
   ('R120','100k 1% 0402 (EN pull-up, always on)','MP62_BP:R_0402_1005Metric','12V_MAIN_IN','RDRV_BUCK_EN'),
   ('R121','0R 0402 DNP (SSD optional 3V3_SB)','MP62_BP:R_0402_1005Metric','3V3_SB','SSD_3V3_SB_OPT'),
   ('L5','2.2uH Isat>=7A (part TBD; 4x4 fp placeholder)','MP62_BP:L_Changjiang_FNR4030S','SW_3V3_RDRV','3V3_RDRV')]
for k,(ref,val,fp,n1,n2) in enumerate(P):
    x=624.84+(k%6)*25.4; y=662.94+(k//6)*15.24; lid={'C':'C','R':'R','L':'L'}[ref[0]]
    out.append(inst(lid,ref,val,fp,x,y,['1','2'],dnp=ref=='R121')+lab(n1,x-3.81,y,False)+lab(n2,x+3.81,y,True))
out.append(f'  (text "Rev 7b (Aidan 2026-10-28): PSU is 12 V only; base fed only via J1. U24 TPS565208 (5 A) 12V_MAIN_IN -> 3V3_RDRV for U20-U22 (~10.5 W). J9/J10 MCIO stand-ins set off-board; J11 GPU / J12 SSD MEG-Array faces. NOTE: J1 has no 12 V pins yet (12V_MAIN_IN still enters on J2)." (exclude_from_sim no) (at 599.44 640.08 0) (effects (font (size 2 2)) (justify left)) (uuid "{U()}"))\n')
j=sch.rfind('  (sheet_instances'); sch=sch[:j]+''.join(out)+sch[j:]
open('backplane.kicad_sch','w').write(sch); print('ok')
