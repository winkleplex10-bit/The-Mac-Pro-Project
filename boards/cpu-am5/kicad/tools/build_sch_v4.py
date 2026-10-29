#!/usr/bin/env python3
"""Generate the MacPro6,2 AM5 CPU board (CB, DRAFT) top-level BLOCK schematic (KiCad 9): a root sheet with hierarchical
sheet symbols + net labels, and one stub file per block holding the matching hierarchical labels, a non-BOM #BLK stub
symbol (passive pins, ERC anchor) and a text description. Same generator pattern as kicad/macpro62-backplane/tools/build_sch.py.
Nets are block-level BUNDLES (e.g. PCIE_GFX_L0_7 = 8 TX + 8 RX pairs); circuits TBD. AMD pin names are NDA -> functional names."""
import os, uuid
PRJ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
U = lambda: str(uuid.uuid4())
ROOT_UUID = "6a1c2d3e-0000-4000-8000-0000000a0005"
VER = '(version 20250114)\n\t(generator "eeschema")\n\t(generator_version "9.0")'
F = '(effects (font (size 1.27 1.27))'
def g(v): return round(v / 1.27) * 1.27
I, O, B, P = "input", "output", "bidirectional", "passive"
SHEETS = [
 ("CPU: Socket AM5 (Ryzen 7000/9000, 142 W PPT cap)", "cpu_am5.kicad_sch", [
   "U1 Socket AM5 LGA1718 (Foxconn PE17181/PE17186 or Lotes AZIFS055), MP62 contact frame on the 69.5 x 55 core holes",
   "Ryzen 7000/9000: 28 PCIe 5.0 lanes / 24 usable [AMD 9950X page; AMD Socket AM5 Quick Reference Guide Nov 2024]; 7000 per-SKU page [GAP-minor]",
   "Lane map (FROZEN): GFX x16 Gen5 -> J1 (GPU) | NVMe x4 Gen5 -> J1 (SSD board A link 0) | GPP x4 Gen5 -> J1 (SSD board A link 1) | x4 Gen4 -> PROM21 uplink",
   "SSD 'x8' = two separate x4 root ports, not one x8 (QRG split). GPP x4 Gen5 on every 7000 SKU [GAP]",
   "USB: 4 x native USB 3.2 Gen2 10G -> J3 C1-C4 (non-USB4) [AMD 9950X page]; 1 x native USB2 -> J1 USB2_SPARE",
   "iGPU display outputs REMOVED (iGPU unused per baseline)",
   "Pin names are functional placeholders: AM5 land map / pin list is AMD NDA [GAP]"],
  [("VDDCR", I), ("VDDCR_SOC", I), ("VDD_MISC", I), ("VDDIO_MEM_S3", I), ("VDD_18_S5", I), ("VDD_33_S5", I), ("VDD_MISC_S5", I),
   ("SVI3_CLK", B), ("SVI3_DAT", B), ("SVI3_ALERT_L", B), ("PROCHOT_L", B),
   ("DDR5_CHA", B), ("DDR5_CHB", B), ("SMB0_SCL", B), ("SMB0_SDA", B), ("FCH_SPI", B),
   ("PCIE_GFX_L0_7", O), ("PCIE_GFX_L8_15", O), ("PCIE_SSDA_LINK0_X4", O), ("PCIE_SSDA_LINK1_X4", O), ("PCIE_PROM21_X4", B),
   ("GPP_CLK_GFX", O), ("GPP_CLK_SSDA0", O), ("GPP_CLK_SSDA1", O), ("GPP_CLK_PROM21", O), ("PCIE_RST_L", O),
   ("USB10G_CPU0_3", O), ("USB2_CPU0", O), ("CLK_48M", I), ("RTC_32K", I), ("VBAT_RTC_CB", I),
   ("PWR_BTN_L", I), ("SYS_RESET_L", I), ("RSMRST_L", I), ("PWR_GOOD", I), ("WAKE_L", B),
   ("SLP_S3_L", O), ("SLP_S5_L", O), ("THERMTRIP_L", O), ("FCH_UART0", B)]),
 ("SVI3 VRM: TI TPS53685 (VDDCR + VDDCR_SOC + VDD_MISC)", "vrm_svi3.kicad_sch", [
   "U3 TI TPS53685 AMD SVI3 multiphase controller (public datasheet: ti.com/product/TPS53685) - replaces RAA229139",
   "Phase plan (unchanged estimate): VDDCR 5 phases, VDDCR_SOC 2, VDD_MISC 1 [rail/phase assignment vs TPS53685 channel limits: check datasheet]",
   "POWER-STAGE PAIRING TBD: SiC654 (current footprint) vs TI NexFET smart stages (e.g. CSD95xxx) - compatibility with TPS53685 current sense not yet checked",
   "Load line / IccMax / TDC / EDC from AMD AM5 VR guide (NDA) [GAP]; 142 W PPT -> VDDCR ~120 A over 5 phases [Estimate]",
   "VR_HOT_L -> PROCHOT_L; PMBus to EC (I2C0). Power limits managed in firmware (Aidan)"],
  [("12V_CB", I), ("VR_EN", I), ("VR_PGOOD", O), ("SVI3_CLK", B), ("SVI3_DAT", B), ("SVI3_ALERT_L", B), ("PROCHOT_L", B),
   ("VDDCR", O), ("VDDCR_SOC", O), ("VDD_MISC", O), ("I2C0_SCL", B), ("I2C0_SDA", B)]),
 ("DDR5 2DPC: 4 x UDIMM vertical (back)", "ddr5.kicad_sch", [
   "J6/J7 (CH-A) and J9/J10 (CH-B): UMAX 90414 short-latch DDR5 UDIMM (unchanged)",
   "Module PMIC from 5V_VIN_BULK; SPD hub on SMBus0 (FCH), 3V3_S5; JEDEC UDIMM pin map not yet netted [open]"],
  [("DDR5_CHA", B), ("DDR5_CHB", B), ("5V_VIN_BULK", I), ("3V3_S5", I), ("SMB0_SCL", B), ("SMB0_SDA", B)]),
 ("PROM21 chipset - PLACEHOLDER - pinout pending datasheet", "prom21.kicad_sch", [
   "*** PLACEHOLDER - pinout pending datasheet *** U2 AMD Promontory 21 (single chip, B650 class), FCBGA 19x19, ~7 W [press: Angstronomics, WePC; not an AMD datasheet]",
   "Ballout, power rails, straps, clocking: AMD NDA -> request via Communications only (no vendor contact) [GAP]",
   "Uplink: PCIe Gen4 x4 from CPU (PCIE_PROM21_X4, GPP_CLK_PROM21)",
   "Downlink #1 Gen4 x4 -> J3 -> ASM4242 USB4 (base side) | Downlink #2 Gen4 x4 SPARE (unrouted; OpenCore boot-drive home is open for Aidan)",
   "Flex x1 #1/#2 -> J3 -> i226-V #1/#2 (2.5 GbE); flex #3/#4 spare",
   "USB 10G -> J3 USB-A hub upstream (hub on base board); USB2 -> J3 base-board USB2 hub; other USB ports spare",
   "REFCLK outputs (ASM, i226A, i226B) + PERST#/CLKREQ# per port: [UNVERIFIED - PROM21 refclk outputs not in public data]",
   "Uplink oversubscription ~1.24x (relayed, not re-derived) [check]. Own SPI flash [Unverified]"],
  [("PCIE_PROM21_X4", B), ("GPP_CLK_PROM21", I), ("PCIE_RST_L", I), ("PROM21_RAILS", I),
   ("PCIE_ASM_X4", O), ("ASM_REFCLK", O), ("ASM_PERST_L", O), ("ASM_CLKREQ_L", B),
   ("PCIE_I226A_X1", O), ("I226A_REFCLK", O), ("I226A_PERST_L", O), ("I226A_CLKREQ_L", B),
   ("PCIE_I226B_X1", O), ("I226B_REFCLK", O), ("I226B_PERST_L", O), ("I226B_CLKREQ_L", B),
   ("USB10G_P21_HUBUP", O), ("USB2_P21_HUB", B)]),
 ("Platform power: 12 V entry (LUG1/LUG2), TPS259851 eFuse, aux + PROM21 rails", "power.kicad_sch", [
   "LUG1/LUG2 12 V entry -> U11 TI TPS259851 eFuse (ILIM ~25 A) -> 12V_CB; U15 INA228 on I2C0, ALERT/FLT# -> PWR_ALERT_N",
   "!! 12 V PLANE MUST CARRY 17.9 A (142 W PPT, est.) / 26.3 A at 230 W - previously checked only to ~15 A -> RE-CHECK on JLC10161H-1080A (inner 0.5 oz) !!",
   "U4 CPU S5 rails from 5V_SBY / 3V3_SB [rail list Unverified, AMD NDA]; U8 VDDIO_MEM_S3; U7 5V_VIN_BULK (DIMM PMICs); U6 PROM21 rails [PLACEHOLDER, NDA]",
   "3V3_S0 load switch; sequencing by EC (RAIL_EN_S5 / RAIL_EN_S0, RAILS_PGOOD)"],
  [("5V_SBY", I), ("3V3_SB", I), ("RAIL_EN_S5", I), ("RAIL_EN_S0", I), ("RAILS_PGOOD", O),
   ("12V_CB", O), ("5V_VIN_BULK", O), ("3V3_S5", O), ("VDD_18_S5", O), ("VDD_33_S5", O), ("VDD_MISC_S5", O),
   ("VDDIO_MEM_S3", O), ("PROM21_RAILS", O), ("I2C0_SCL", B), ("I2C0_SDA", B), ("PWR_ALERT_N", O)]),
 ("EC, firmware, clocks, RTC (on-board CR2032), debug", "ec_fw.kicad_sch", [
   "U9 RP2350 EC: AM5 sequencing RSMRST_L -> PWR_BTN_L -> SLP_S5/S3 -> rails -> PWR_GOOD; VR_EN / VR_PGOOD",
   "Firmware: vendor AGESA UEFI for 7000/9000 via a licensed board maker (ODM) [NDA via ODM]; U10 FCH SPI ROM 32 MB; J4 TPM header (fTPM default)",
   "BT1 CR2032 ON-BOARD (holder footprint MP62_AREA_BT1_CR2032_22x16) -> diode-OR with 3V3_S5 -> VBAT_RTC_CB (VBAT no longer on J3)",
   "Y1 48 MHz [Unverified] + 32.768 kHz; J5 debug (FCH UART, SWD, POST); I2C to base MCU via J3 (LEDs/status)"],
  [("3V3_SB", I), ("PWRBTN_N", I), ("RSTBTN_N", I), ("PWR_BTN_L", O), ("SYS_RESET_L", O), ("RSMRST_L", O), ("PWR_GOOD", O),
   ("SLP_S3_L", I), ("SLP_S5_L", I), ("PCIE_RST_L", I), ("THERMTRIP_L", I), ("VR_EN", O), ("VR_PGOOD", I),
   ("RAIL_EN_S5", O), ("RAIL_EN_S0", O), ("RAILS_PGOOD", I), ("SUS_S3_N", O), ("SUS_S5_N", O), ("RSMRST_OUT_N", O), ("PLTRST_N", O),
   ("THERMTRIP_N", O), ("CARRIER_HOT_N", I), ("PROCHOT_L", B), ("UART0", B), ("I2C0_SCL", B), ("I2C0_SDA", B), ("FAN_PWMOUT", O), ("FAN_TACHIN", I),
   ("FCH_SPI", B), ("FCH_UART0", B), ("CLK_48M", O), ("RTC_32K", O), ("VBAT_RTC_CB", O), ("I2C_BB", B), ("SMB_ALERT_N", I), ("BB_PWR_BTN_N", I)]),
 ("J1 Amphenol ME1022410103011 Mini Cool Edge 224 card edge", "cpu_link.kicad_sch", [
   "J1 = Amphenol Mini Cool Edge 224 (ME1022410103011), 1.1 A/contact [Amphenol datasheet]; 78 GND (keep >= 78 in v4 map)",
   "Carries: GFX x16 Gen5 (GPU) + SSD board A link 0 x4 + link 1 x4 Gen5 + 3 REFCLKs; standby 6 x 5V_SBY + 2 x 3V3_SB; USB2 spare; sideband",
   "Contact-level v4 map (SSD A link0/link1 Gen5 replacing FS slot A/B Gen4, drop SATA0) not yet generated -> cpulink_224_pinout_am5_v4.csv [open]",
   "Gen5 redrivers (DS320PR1601 GPU, 2 x DS320PR810 SSD A) + PT5161L fallback live on the base board, not here"],
  [("5V_SBY", O), ("3V3_SB", O), ("PCIE_GFX_L0_7", I), ("PCIE_GFX_L8_15", I), ("PCIE_SSDA_LINK0_X4", I), ("PCIE_SSDA_LINK1_X4", I),
   ("GPP_CLK_GFX", I), ("GPP_CLK_SSDA0", I), ("GPP_CLK_SSDA1", I), ("USB2_CPU0", I),
   ("PWRBTN_N", O), ("RSTBTN_N", O), ("SUS_S3_N", I), ("SUS_S5_N", I), ("RSMRST_OUT_N", I), ("PLTRST_N", I), ("THERMTRIP_N", I),
   ("CARRIER_HOT_N", O), ("PWR_ALERT_N", I), ("FAN_PWMOUT", I), ("FAN_TACHIN", O), ("UART0", B), ("I2C0_SCL", B), ("I2C0_SDA", B),
   ("SMB0_SCL", B), ("SMB0_SDA", B), ("WAKE_L", B)]),
 ("J3 MCIO-124 to base board (rev 2 pinout)", "iob_hs.kicad_sch", [
   "J3 MCIO 124 RA (SFF-TA-1016) -> base board; contact map = docs/mp62-cb-j3_mcio124_host-end_am5_rev2.csv (67 signal + 57 GND, G-S-S-G)",
   "USB-C C1-C4 (non-USB4) = CPU native USB 10G x4 | USB-A hub upstream = PROM21 10G | USB2 -> base-board USB2 hub",
   "ASM4242 Gen4 x4 (PROM21 DL#1) + 2 x i226 x1 (PROM21 flex) + 3 REFCLKs [Unverified] + PERST#/CLKREQ#",
   "Sideband: SLP_S3#/S5#, 3 PERST#, 3 CLKREQ#, WAKE#, PWR_BTN#, I2C + SMB_ALERT#, BB_HS_PRSNT0#/1#",
   "Removed vs rev 1: iGPU DP (DDIB/DDIC/AUX/HPD), VBAT, USB_OC#, C5/C6, extra USB2"],
  [("USB10G_CPU0_3", I), ("USB10G_P21_HUBUP", I), ("USB2_P21_HUB", B),
   ("PCIE_ASM_X4", I), ("ASM_REFCLK", I), ("ASM_PERST_L", I), ("ASM_CLKREQ_L", B),
   ("PCIE_I226A_X1", I), ("I226A_REFCLK", I), ("I226A_PERST_L", I), ("I226A_CLKREQ_L", B),
   ("PCIE_I226B_X1", I), ("I226B_REFCLK", I), ("I226B_PERST_L", I), ("I226B_CLKREQ_L", B),
   ("SUS_S3_N", I), ("SUS_S5_N", I), ("WAKE_L", B), ("BB_PWR_BTN_N", O), ("I2C_BB", B), ("SMB_ALERT_N", O)]),
]
def text(s, x, y, size=1.27):
    s = s.replace('"', "'")
    return f'\t(text "{s}"\n\t\t(exclude_from_sim no)\n\t\t(at {x:.2f} {y:.2f} 0)\n\t\t(effects (font (size {size} {size})) (justify left bottom))\n\t\t(uuid "{U()}")\n\t)\n'

# ---------- sub-sheet stub files ----------
SHEET_UUIDS = [U() for _ in SHEETS]

def stub_lib(sym, pins):
    n = len(pins)
    yb = -(n - 1) * 2.54 - 1.27
    o = f'\t\t(symbol "MP62:{sym}"\n\t\t\t(pin_names (offset 1.016))\n\t\t\t(exclude_from_sim yes)\n\t\t\t(in_bom no)\n\t\t\t(on_board no)\n'
    for k, v, yy, hide in (("Reference", "#BLK", 2.54, ""), ("Value", sym, 3.81, ""), ("Footprint", "", 0, " (hide yes)"), ("Datasheet", "", 0, " (hide yes)"),
                           ("Description", "Non-BOM block stub: one passive pin per hierarchical label (ERC anchor)", 0, " (hide yes)")):
        o += f'\t\t\t(property "{k}" "{v}"\n\t\t\t\t(at 2.54 {yy:.2f} 0)\n\t\t\t\t(effects (font (size 1.27 1.27)) (justify left){hide})\n\t\t\t)\n'
    o += f'\t\t\t(symbol "{sym}_0_1"\n\t\t\t\t(rectangle (start 2.54 1.27) (end 25.4 {yb:.2f})\n\t\t\t\t\t(stroke (width 0.254) (type default))\n\t\t\t\t\t(fill (type background))\n\t\t\t\t)\n\t\t\t)\n'
    o += f'\t\t\t(symbol "{sym}_1_1"\n'
    for i, (pn, pt) in enumerate(pins):
        o += f'\t\t\t\t(pin passive line\n\t\t\t\t\t(at 0 {-i * 2.54:.2f} 0)\n\t\t\t\t\t(length 2.54)\n\t\t\t\t\t(name "{pn}" (effects (font (size 1.0 1.0))))\n\t\t\t\t\t(number "{i + 1}" (effects (font (size 1.0 1.0))))\n\t\t\t\t)\n'
    o += '\t\t\t)\n\t\t)\n'
    return o

written = set()
for idx, (name, fname, desc, pins) in enumerate(SHEETS):
    if fname in written:
        continue
    written.add(fname)
    s = f'(kicad_sch\n\t{VER}\n\t(uuid "{U()}")\n\t(paper "A4")\n'
    sym = "STUB_" + fname.replace(".kicad_sch", "").upper()
    insts = [(SHEET_UUIDS[k], k) for k, sh in enumerate(SHEETS) if sh[1] == fname]
    s += f'\t(title_block\n\t\t(title "MP62 AM5 CPU board: {name}")\n\t\t(date "2026-10-28")\n\t\t(rev "A-am5-v4")\n\t\t(comment 1 "Block stub: hierarchical labels + one non-BOM stub symbol (#BLKn, passive pins) so ERC sees the nets; circuit TBD")\n\t)\n\t(lib_symbols\n' + stub_lib(sym, pins) + '\t)\n'
    y = 30.48
    for (pn, pt) in pins:
        s += f'\t(hierarchical_label "{pn}"\n\t\t(shape {pt})\n\t\t(at 38.1 {y:.2f} 180)\n\t\t{F} (justify right))\n\t\t(uuid "{U()}")\n\t)\n'
        y += 2.54
    s += f'\t(symbol\n\t\t(lib_id "MP62:{sym}")\n\t\t(at 38.1 30.48 0)\n\t\t(unit 1)\n\t\t(exclude_from_sim yes)\n\t\t(in_bom no)\n\t\t(on_board no)\n\t\t(dnp no)\n\t\t(uuid "{U()}")\n'
    s += f'\t\t(property "Reference" "#BLK{insts[0][1] + 1}"\n\t\t\t(at 40.64 27.94 0)\n\t\t\t(effects (font (size 1.27 1.27)) (justify left) (hide yes))\n\t\t)\n'
    s += f'\t\t(property "Value" "{sym}"\n\t\t\t(at 40.64 26.67 0)\n\t\t\t(effects (font (size 1.27 1.27)) (justify left) (hide yes))\n\t\t)\n'
    for i in range(len(pins)):
        s += f'\t\t(pin "{i + 1}"\n\t\t\t(uuid "{U()}")\n\t\t)\n'
    s += '\t\t(instances\n\t\t\t(project "macpro62_am5"\n'
    for su, k in insts:
        s += f'\t\t\t\t(path "/{ROOT_UUID}/{su}"\n\t\t\t\t\t(reference "#BLK{k + 1}")\n\t\t\t\t\t(unit 1)\n\t\t\t\t)\n'
    s += '\t\t\t)\n\t\t)\n\t)\n'
    s += text("BLOCK STUB (rev A block diagram). Contents planned:", 76.2, 30.48, 1.5)
    for i, d in enumerate(desc):
        s += text("- " + d, 76.2, 35.56 + i * 3.81)
    s += ')\n'
    open(os.path.join(PRJ, fname), "w").write(s)

# ---------- project symbol library for the stub symbols (keeps ERC free of lib_symbol_issues) ----------
_lib = '(kicad_symbol_lib\n\t(version 20241209)\n\t(generator "mp62_build_sch")\n\t(generator_version "9.0")\n'
_done = set()
for (name, fname, desc, pins) in SHEETS:
    if fname in _done:
        continue
    _done.add(fname)
    _lib += stub_lib("STUB_" + fname.replace(".kicad_sch", "").upper(), pins).replace('(symbol "MP62:', '(symbol "')
_lib += ')\n'
open(os.path.join(PRJ, "MP62_AM5_Stubs.kicad_sym"), "w").write(_lib)
open(os.path.join(PRJ, "sym-lib-table"), "w").write('(sym_lib_table\n  (version 7)\n  (lib (name "MP62")(type "KiCad")(uri "${KIPRJMOD}/MP62_AM5_Stubs.kicad_sym")(options "")(descr "MP62 AM5 CB block-stub symbols (non-BOM)"))\n)\n')


# ---------- root sheet ----------
s = f'(kicad_sch\n\t{VER}\n\t(uuid "{ROOT_UUID}")\n\t(paper "A2")\n'
s += '\t(title_block\n\t\t(title "MacPro6,2 AM5 CPU board (CB) DRAFT - top-level block diagram")\n\t\t(date "2026-10-28")\n\t\t(rev "A-am5-v4")\n\t\t(company "MacPro6,2 / Aidan Winkler")\n'
s += '\t\t(comment 1 "v4 frozen config: Ryzen 7000/9000 142 W, PROM21 PLACEHOLDER, TPS53685 SVI3, J3 rev2, no iGPU DP, on-board CR2032")\n\t\t(comment 2 "See /workspace/docs/am5-cpu-board-frozen-config.md; nets are block-level bundles")\n\t)\n\t(lib_symbols)\n'
s += text("MP62 AM5 CPU BOARD rev A-am5 DRAFT - BLOCK DIAGRAM. Sheets are stubs (labels only). Same label name = same net (bundle).", 25.4, 20.32, 2.0)
s += text("Off-board: J1 Mini Cool Edge 224 (card edge) | J3 MCIO 124 -> base board | LUG1/LUG2 12 V | J5 debug | J4 TPM. AMD pin names (NDA) replaced by functional names.", 25.4, 25.4, 1.6)
W = 60.96
XS = [38.1, 165.1, 292.1, 419.1]
hs = [g(5.08 + 2.54 * len(sh[3])) for sh in SHEETS]
RY = [38.1]
for r in range(1, 3):
    RY.append(g(RY[-1] + max(hs[(r - 1) * 4:r * 4]) + 22.86))
cols = [(XS[i % 4], RY[i // 4]) for i in range(len(SHEETS))]
page = 2
for idx, (name, fname, desc, pins) in enumerate(SHEETS):
    x, y = cols[idx]
    h = hs[idx]
    s += f'\t(sheet\n\t\t(at {x:.2f} {y:.2f})\n\t\t(size {W:.2f} {h:.2f})\n\t\t(exclude_from_sim no)\n\t\t(in_bom yes)\n\t\t(on_board yes)\n\t\t(dnp no)\n\t\t(fields_autoplaced yes)\n'
    s += '\t\t(stroke (width 0.1524) (type solid))\n\t\t(fill (color 0 0 0 0.0000))\n'
    s += f'\t\t(uuid "{SHEET_UUIDS[idx]}")\n'
    s += f'\t\t(property "Sheetname" "{name}"\n\t\t\t(at {x:.2f} {y - 0.71:.2f} 0)\n\t\t\t{F} (justify left bottom))\n\t\t)\n'
    s += f'\t\t(property "Sheetfile" "{fname}"\n\t\t\t(at {x:.2f} {y + h + 0.59:.2f} 0)\n\t\t\t{F} (justify left top))\n\t\t)\n'
    py = y + 2.54
    labels = ""
    for (pn, pt) in pins:
        left = (pt == "input")
        px = x if left else x + W
        ang = 180 if left else 0
        just = "left" if left else "right"
        s += f'\t\t(pin "{pn}" {pt}\n\t\t\t(at {px:.2f} {py:.2f} {ang})\n\t\t\t(uuid "{U()}")\n\t\t\t{F} (justify {just}))\n\t\t)\n'
        lx = px - 10.16 if left else px + 10.16
        labels += f'\t(wire\n\t\t(pts (xy {px:.2f} {py:.2f}) (xy {lx:.2f} {py:.2f}))\n\t\t(stroke (width 0) (type default))\n\t\t(uuid "{U()}")\n\t)\n'
        lang = 0 if not left else 180
        ljust = "left" if not left else "right"
        labels += f'\t(label "{pn}"\n\t\t(at {lx:.2f} {py:.2f} {lang})\n\t\t(fields_autoplaced yes)\n\t\t{F} (justify {ljust} bottom))\n\t\t(uuid "{U()}")\n\t)\n'
        py += 2.54
    s += f'\t\t(instances\n\t\t\t(project "macpro62_am5"\n\t\t\t\t(path "/{ROOT_UUID}"\n\t\t\t\t\t(page "{page}")\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)\n'
    s += labels
    page += 1
s += '\t(sheet_instances\n\t\t(path "/"\n\t\t\t(page "1")\n\t\t)\n\t)\n)\n'
open(os.path.join(PRJ, "macpro62_am5_v4.kicad_sch"), "w").write(s)
# net sanity: every bundle on >= 2 sheets
from collections import Counter
c = Counter(pn for sh in SHEETS for pn, pt in set(sh[3]))
single = [k for k, v in c.items() if v < 2]
print("schematic written: %d sheets, %d nets, single-sheet nets: %s" % (len(SHEETS), len(c), single or "none"))
