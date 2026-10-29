# Gen5 redriver model (Aidan decision 2026-10-28): pin -> net for U20 (DS320PR1601), U21/U22 (DS320PR810),
# U23 (PT5161L ALT, DNP, no pins) plus decoupling and straps. Shared by schematic and PCB scripts.
import json,re
PWR='3V3_RDRV'   # NEW rail, source TBD (3V3_SB TPS563201 is 3 A standby: not adequate)
p1601=json.load(open('/workspace/research/ti/ds320pr1601_pins.json'))
def hs1601(name):
    m=re.match(r'([AB])_PE([TR])([pn])(\d+)',name)
    side,tr,pol,ch=m.groups(); ch=int(ch); pol='P' if pol=='p' else 'N'
    # side A = CPU (J1) side, side B = GPU-face side. A_PER <- CPU TX ; B_PET -> GPU ; B_PER <- GPU TX ; A_PET -> CPU RX
    if side=='A': return f'FP_{"TX" if tr=="R" else "RX"}{ch}_{pol}_A'
    return f'FP_{"TX" if tr=="T" else "RX"}{ch}_{pol}_B'
U20={}
ctr={'addr':0}
for ball,name in p1601.items():
    if name=='GND': n='GND'
    elif name.startswith('VCC'): n=PWR
    elif name.startswith(('A_PE','B_PE')): n=hs1601(name)
    elif name=='SDA': n='I2C_SYS_SDA'
    elif name=='SCL': n='I2C_SYS_SCL'
    elif name=='MODE': n='U20_MODE'
    elif 'ADDR' in name: n='U20_'+name.replace('-','_')
    elif name.startswith('PD_'): n='GPU_RDRV_PD'
    else: n=None   # N/C, RSVD*, READ_EN_# (unused in target mode), ALL_DONE# (unused in target mode) -> no-connect
    U20[ball]=(name,n)
def u810(lanebase):
    d={}
    for p in [9,12,21,24,32,41,44,53,56,64,65]: d[str(p)]=('GND','GND')
    for p in [6,18,38,50]: d[str(p)]=('VCC',PWR)
    for p,nm in [(3,'RSVD2'),(15,'RSVD3'),(35,'RSVD4'),(47,'RSVD5')]: d[str(p)]=(nm,'GND')  # SNLS668 p.6: connect RSVD2-5 to GND
    for p,nm in [(58,'RSVD0'),(30,'RSVD1'),(57,'READ_EN_N'),(31,'ALL_DONE_N'),(27,'EQ0_1'),(29,'EQ1_1'),(28,'GAIN1')]: d[str(p)]=(nm,None)
    d['61']=('MODE',None); d['59']=('EQ0/ADDR0',None); d['60']=('EQ1/ADDR1',None)
    d['63']=('GAIN0/SDA','I2C_SYS_SDA'); d['62']=('RX_DET/SCL','I2C_SYS_SCL')
    d['25']=('PD0','SSD_RDRV_PD'); d['26']=('PD1','SSD_RDRV_PD')
    rx={0:(1,2),1:(4,5),2:(7,8),3:(10,11),4:(13,14),5:(16,17),6:(19,20),7:(22,23)}
    tx={0:(55,54),1:(52,51),2:(49,48),3:(46,45),4:(43,42),5:(40,39),6:(37,36),7:(34,33)}
    for ch in range(8):
        l=lanebase+(ch%4)
        if ch<4: rn,tn=f'FS_TX{l}_%s_A',f'FS_TX{l}_%s_B'   # CPU TX -> RX ch0-3 -> TX ch0-3 -> SSD
        else:    rn,tn=f'FS_RX{l}_%s_B',f'FS_RX{l}_%s_A'   # SSD TX -> RX ch4-7 -> TX ch4-7 -> CPU RX
        d[str(rx[ch][0])]=(f'RX{ch}P',rn%'P'); d[str(rx[ch][1])]=(f'RX{ch}N',rn%'N')
        d[str(tx[ch][0])]=(f'TX{ch}P',tn%'P'); d[str(tx[ch][1])]=(f'TX{ch}N',tn%'N')
    return d
U21=u810(0); U22=u810(4)
for U,r in ((U21,'U21'),(U22,'U22')):
    U['61']=('MODE',f'{r}_MODE'); U['59']=('EQ0/ADDR0',f'{r}_ADDR0'); U['60']=('EQ1/ADDR1',f'{r}_ADDR1')
# passives: ref, value, footprint, net1, net2, side, note
fp04c='MP62_BP:C_0402_1005Metric'; fp08c='MP62_BP:C_0805_2012Metric'; fp04r='MP62_BP:R_0402_1005Metric'
P=[]; cn=[40]; rn=[101]
def C(v,fp,grp):
    P.append((f'C{cn[0]}',v,fp,PWR,'GND',grp)); cn[0]+=1
def R(v,n1,n2,grp):
    P.append((f'R{rn[0]}',v,fp04r,n1,n2,grp)); rn[0]+=1
for i in range(16): C('100nF 16V X7R 0402',fp04c,'U20')
for i in range(4): C('1uF 10V X5R 0402',fp04c,'U20')
for i in range(2): C('10uF 10V X5R 0805',fp08c,'U20')
for U in ('U21','U22'):
    for i in range(4): C('100nF 16V X7R 0402',fp04c,U)
    C('1uF 10V X5R 0402',fp04c,U)
C('10uF 10V X5R 0805',fp08c,'U21')   # one 10 uF per power bus feeding the DS320PR810s (SNLS668 p.28)
R('6.2k 1% 0402 (MODE=L2 target, SNLS683 Tbl 5-1: 6.225k)','U20_MODE','GND','U20')
for a in ['A_ADDR0_7_0','A_ADDR1_7_0','B_ADDR0_7_0','B_ADDR1_7_0','A_ADDR0_15_8','A_ADDR1_15_8','B_ADDR0_15_8','B_ADDR1_15_8']:
    R('TBD strap (SNLS683 Tbl 7-3/8-1)',f'U20_{a}','GND','U20')
R('10k 1% 0402 (PD pull-down, GPU redriver on)','GPU_RDRV_PD','GND','U20')
R('24.9k 1% 0402 (MODE=L2 secondary, SNLS668 Tbl 7-4)','U21_MODE','GND','U21')
R('1k 1% 0402 (ADDR0=L0)','U21_ADDR0','GND','U21'); R('1k 1% 0402 (ADDR1=L0 -> 0x18/0x19)','U21_ADDR1','GND','U21')
R('24.9k 1% 0402 (MODE=L2 secondary)','U22_MODE','GND','U22')
R('8.25k 1% 0402 (ADDR0=L1)','U22_ADDR0','GND','U22'); R('1k 1% 0402 (ADDR1=L0 -> 0x1A/0x1B)','U22_ADDR1','GND','U22')
R('10k 1% 0402 (PD pull-down, SSD redrivers on)','SSD_RDRV_PD','GND','U21')
ICS=[('U20','DS320PR1601ZDGR','MP62_BP:TI_ZDG0354A_nFBGA-354_22.9x8.9mm',U20,False),
     ('U21','DS320PR810NJXR','MP62_BP:TI_NJX0064A_WQFN-64_5.5x10mm_P0.4mm_EP4.1x8.6mm',U21,False),
     ('U22','DS320PR810NJXR','MP62_BP:TI_NJX0064A_WQFN-64_5.5x10mm_P0.4mm_EP4.1x8.6mm',U22,False),
     ('U23','PT5161L_ALT_DNP','MP62_BP:Astera_PT5161L_ALT_DNP_PLACEHOLDER',{},True)]
