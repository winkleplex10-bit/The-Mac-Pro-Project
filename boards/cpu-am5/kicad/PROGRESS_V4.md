# AM5 CB v3 work log
Copy of kicad/macpro62-am5 (original untouched; checksums /workspace/scratch/v2_baseline/am5_original.sha256).
Goal: PROM21 free Gen4 x4 downstream port -> CPU-LINK ex-RSVD pins (slot B x2), slot A on CPU GPP x4 unchanged.

## 19:49 ET: v3 copy made from kicad/macpro62-am5

## 20:2x-20:45 ET: retargeted to Ryzen 7000/9000 (Raphael / Granite Ridge), slot B on CPU GPP#2 (CPU-LINK v3, 4 lanes)
- tools/build_sch.py / build_pcb.py: target text, lane blocks (GFX x16 live, GPP#1 -> FS 0-3, GPP#2 -> FS 4-7 + GPP_CLK_FSB -> FS_REFCLK1,
  PROM21 x4 chipset link, J8 M.2 boot -> PROM21 free Gen4 x4 via PCIE_PROM21_M2_X4 / PROM21_CLK_M2). Placeholder footprints unchanged.
- tools/make_pinouts_v3.py -> docs/cpulink_224_pinout_am5_v3.csv (21 contacts re-pinned per CPU-LINK v3; v1 CSVs untouched).
- Rebuilt (README sequence): DRC 0 violations / 0 unconnected / 0 footprint errors; ERC 0 (same as v1). floorplan.png + schematic_blockdiagram.pdf regenerated.
- docs/v3_lane_cpu_research.md: lanes, Phoenix vs Raphael, TDP/VRM/PSU budget, display plan, CPU prices.

## 21:15 ET: BP v3 went 6L / slot B x4 (Aidan 20:43)
- docs/cpulink_224_pinout_am5_v3.csv regenerated from the BP v3 draft CSV: RX7 polarity B54 = FS_PER7_N, B55 = FS_PER7_P (BP-side route choice; CPU-LINK v3 is a new pinout); lanes 6-7 no longer "NC on BP v3".
- CB board/schematic unaffected (J1 is block-level; the CSV is documentation). research doc lane table: slot B x4.

## 2026-10-09 15:04 ET: snapshot before netlist work: /workspace/backups/iob_am5v3_pre_netpush_20261009-1457.tgz

## 2026-10-09 15:10 ET: connector nets on the PCB + real J3 (exec subagent)
- Finding: the CB schematic is block-level only (10 stub sheets, 0 BOM symbols) -> no netlist exists to push. A real component-level
  AM5 schematic is blocked at its core by NDA data (AM5 LGA1718 land map, PROM21 ballout, SVI3 controller config) - U1/U2/U3 stay stand-ins.
- tools/assign_connector_nets.py (new; run after build_pcb.py + postprocess.py): J1 CPU-LINK 224/224 pads netted from
  docs/cpulink_224_pinout_am5_v3.csv; J3 AREA -> real MCIO 124P RA (MP62_AM5_Real.pretty, same footprint as IOB J1), 124/124 pads netted
  from docs/mp62-cb-j3_mcio124_host-end_am5.csv, B side, mating face to the top edge, body centred on the old area (+1 mm).
- DRC 0 violations / 0 footprint errors (131 unconnected = netted connector pads, nothing routed). ERC unchanged (block schematic).
- Still AREA/PLACEHOLDER: U1 (NDA), U2 (NDA), U3 (SVI3, NDA tools), U4-U8 rail areas, CIN1/COUT1, CAC1, J4 TPM, U16 VL822 area, Y1, U9/U10,
  J8 M.2 (placeholder pads, standard M-key pinout not yet netted), DIMMs J6/J7/J9/J10 (real UMAX 290-pad footprint, JEDEC DDR5 UDIMM pin map not netted).
- snapshot backups/am5v3_connnets_20261009-1505.tgz

## 2026-10-28 15:05 ET: v4 frozen-config schematic pass (Aidan: "draw it out, leaving a placeholder for the chipset.")
- Backup: /workspace/backups/am5v3_pre_kicadpass_20261028-1459. Generator: tools/build_sch_v4.py (build_sch.py kept as v3 history).
- 8 block sheets: lane map x16/x4/x4 Gen5 to J1 + x4 Gen4 PROM21; PROM21 = PLACEHOLDER (pinout pending datasheet); TPS53685 (stages TBD);
  J1 Mini Cool Edge 224; J3 rev2; iGPU DP removed; BT1 CR2032 -> VBAT_RTC_CB; LUG1/LUG2 + TPS259851, 17.9 A plane re-check flag.
- Removed sheets usb_hub (hub on base board) and m2_boot (no chipset boot NVMe). PCB not touched. ERC 0/0. PDF /workspace/docs/am5-cpu-board-schematic.pdf

## 2026-10-29 Migrated to v4
Copied from /workspace/kicad/macpro62-am5-v3 (kept intact for the archive). Project renamed macpro62_am5_v4. Includes the Oct 28 schematic pass (PROM21 placeholder, TPS53685, J3 rev2, CR2032) and the J1 v4 DRAFT pinout (docs/cpulink_224_pinout_am5_v4_DRAFT.csv, not pinned; P12V fed ahead of the CB eFuse). The PCB has not been updated yet (still old J3 rev1 nets, VL822, J8).
