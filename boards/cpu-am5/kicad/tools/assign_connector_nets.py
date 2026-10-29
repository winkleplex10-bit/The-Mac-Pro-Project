#!/usr/bin/env python3
"""2026-10-09 (AM5 v3): the CB schematic is still block-level (no component symbols), so connector nets are pushed to the PCB
straight from the ICD pin-map CSVs (source of truth): J1 CPU-LINK <- docs/cpulink_224_pinout_am5_v3.csv (pin, signal),
J3 IOB-HS MCIO 124 <- docs/mp62-cb-j3_mcio124_host-end_am5.csv (cb_contact, signal). Also swaps the J3 AREA for the real
MCIO 124P RA footprint (MP62_AM5_Real, copied from MP62_IO, same part as IOB J1). Run after build_pcb.py/postprocess.py."""
import csv, os, pcbnew
PRJ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); PCB = os.path.join(PRJ, "macpro62_am5_v4.kicad_pcb")
b = pcbnew.LoadBoard(PCB)
def net(n):
    ni = b.FindNet(n)
    if not ni: ni = pcbnew.NETINFO_ITEM(b, n); b.Add(ni)
    return ni
# J3 AREA -> real MCIO 124 RA (B side, mating face toward the top edge, body centred on the old area)
old = b.FindFootprintByReference("J3")
if "AREA" in old.GetFPIDAsString():
    pos = old.GetPosition(); val = old.GetValue()
    f = pcbnew.FootprintLoad(os.path.join(PRJ, "MP62_AM5_Real.pretty"), "MP62_MCIO_124P_RA_SFF-TA-1016")
    f.SetFPID(pcbnew.LIB_ID("MP62_AM5_Real", "MP62_MCIO_124P_RA_SFF-TA-1016")); f.SetReference("J3"); f.SetValue(val)
    b.Remove(old); b.Add(f); f.Flip(f.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
    f.SetPosition(pcbnew.VECTOR2I(pos.x, pos.y + pcbnew.FromMM(1.0)))
def push(ref, rows, pin_key):
    f = b.FindFootprintByReference(ref); pads = {}
    for p in f.Pads(): pads.setdefault(p.GetNumber(), []).append(p)
    ok = miss = 0
    for r in rows:
        sig = r["signal"].strip()
        if not sig or sig.upper() in ("NC", "-"): continue
        for p in pads.get(r[pin_key].strip(), []): p.SetNet(net(sig)); ok += 1
        if r[pin_key].strip() not in pads: miss += 1
    if "MP" in pads:
        for p in pads["MP"]: p.SetNet(net("GND"))
    print(ref, "pads netted", ok, "csv pins without pad", miss)
push("J1", list(csv.DictReader(open(os.path.join(PRJ, "docs", "cpulink_224_pinout_am5_v3.csv")))), "pin")
push("J3", list(csv.DictReader(open(os.path.join(PRJ, "docs", "mp62-cb-j3_mcio124_host-end_am5.csv")))), "cb_contact")
b.Save(PCB)
