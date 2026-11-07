# SI & Fab review: base-v3 LS routing (2026-11-05)

Reviewed read-only for Master Bot / Base Board & Connectors. No PCB edits, no push, no orders.

- **Board:** `/workspace/kicad/macpro62-backplane-v3/backplane.kicad_pcb`
- **SHA-256:** `ecf4b683fdefb0ce9fca20bdad544cafd0d83f7089e387e9ed6084f122edc810` (matches claim)
- **Report:** `work/handroute/REPORT_ls_handroute_20261105.md`
- **DRC:** `work/handroute/final_drc_20261105-2204.json` (KiCad 9.0.2, 2026-11-05 22:03:44 EST / America/New_York)
- **Context:** `docs/gen5_redriver_segment_lengths_2026-10-28.csv` (stale vs live U21/U22; see below)
- **Reviewer method:** independent pcbnew load of the official board and the frozen baseline, plus parse of the DRC JSON and `remaining_ls.json`. Not a restatement of the report.

## Verdict

**REJECT** for delivery to Aidan as “manual LS routing.”

The official file is a useful partial draft, but it is not finished hand routing and must not be labeled that way. The 21:45 pass used geometric candidates plus bounded A* (`ls_router.py`). The 22:04 clearance pass used scripted coordinate jogs, including 0.03 mm nudges. Base Board already disclosed this; SI agrees and will not treat later jogs as converting the pass into manual routing.

Relabel it as a **partial algorithmic LS draft (A* + scripted repair)** if it is kept as a working copy. Do not send it to Aidan under a manual-routing claim.

## Independent checks (match unless noted)

| Metric | Claimed (after 22:04 repair) | Measured |
| --- | --- | --- |
| SHA-256 | `ecf4b683…c810` | match |
| Footprints / tracks / vias | 221 / 1441 / 82 | 221 / 1441 / 82 |
| KiCad `GetUnconnectedCount` | 567 (992 → 567) | baseline 992, current 567 |
| DRC violations | 288 (278 error / 10 warning) | 288 = 278 + 10 |
| DRC unconnected / schematic parity | 499 / 47 | 499 / 47 (37 `net_conflict` + 10 `footprint_symbol_mismatch`) |
| ERC | 0 error / 142 warning | not re-run; files present and report-consistent |
| PCIE_85R tracks | 0 | 0 (length 0 mm) |
| Tracks on L3_SIG_TX_PWR (In2) or L4_SIG_SLOTB (In3) | 0 | 0 |
| Unique committed pairs / nets | 116 / 79 | taken from `remaining_ls.json` (not independently re-derived) |
| Baseline | 0 tracks, 3 Gen5 vias | 0 tracks, same 3 vias / UUIDs / coordinates |

`.kicad_pro` (mtime 2026-10-29), `.kicad_dru` (2026-10-28), and the schematic (2026-10-29) were not touched this pass. Netclasses are unchanged: PCIE_85R 0.26 / 0.125 mm, PWR 0.60 mm, PWR_HI 1.5 mm, USB2_SATA_90R 0.24 / 0.15 mm.

## Taxonomy: remaining LS vs unconnected counts

These are different questions; all can be true at once.

- **KiCad ratsnest:** 567.
- **analyze_conn `airwires_LS`:** 227. That bucket is *not* “true LS.” It is 108 true-LS airwires + 44 IOB USB3/ASM/LAN PE pairs + 75 `3V3_RDRV` = 227.
- **True LS still open** (`remaining_ls.json` `true_ls_open`): **76 nets / 108 airwires.** `SW_5V_SBY` is not in this list; it is counted as PWR.
- **analyze_conn PWR:** 195 → 197 after the `SW_5V_SBY` revert (+2).
- **DRC `unconnected_items`:** 499. Different pairing than KiCad’s 567. The count staying at 499 across the revert is pair churn, not proof the two switch-node opens are absent — both `C9.2↔U7.2` and `U7.2↔L2.1` are in the 499.

Intentionally unrouted (correct): all PCIE_85R / REFCLK (138 HS_PCIE airwires), the 44 IOB 85 Ω pairs, USB2 90 Ω pairs, and `3V3_RDRV` as a pour rather than skinny traces.

## What is OK

- **Gen5 invariants held.** The only PCIE-ish vias are still:
  - `FS_RX0_P_B` uuid `4be906ad-4cfe-4de7-a5fd-db1002e7b4ec` at (102.000, 82.000)
  - `FS_RX7_N_B` uuid `d640b1d5-9ad4-4ca7-b681-274cb65b989e` at (120.000, 61.000)
  - `FS_TX4_N_B` uuid `cbcf4a94-0daa-4647-9f60-bcda2d00d91b` at (111.000, 67.000)
  Same UUIDs and coordinates as the frozen baseline. Zero tracks on those nets. DRC still flags them as dangling, as expected.
- **No new Gen5 copper, so no new length or 85 Ω geometry to pass or fail.** In2 stripline 0.24 / 0.127 and F.Cu microstrip 0.26 / 0.125 are still the documented targets in `docs/impedance_v3_6L.json`. There is nothing routed to measure against them.
- **LS stayed off In2/In3.** All 1441 tracks are on L1_SIG_RX (900) or L6_GND_BRK (541). That preserves the In2/In3 reference-plane rule from the earlier SI note.
- **Clearance repair did what it claimed for new-track DRC.** Remaining 12 clearances and 2 hole-clearances are pad/via/footprint hits (U21/U22 BGA-to-GND 0.0207 mm, U25 PWR_HI 0.0377 mm, J11 vs J3, J12.D23 vs the `FS_RX7_N_B` via, H3 vs J14 NPTH). No remaining new-track clearance, hole-clearance, or short showed up in the 22:04 DRC.
- IOB 85 Ω pairs and USB2 90 Ω pairs were left alone. Good.

Gen5 *routed* lengths are still not measurable. The 2026-10-28 CSV remains estimate-only, and it is also stale versus this file: live U20 is at (173.70, 102.90) as accepted, but live U21 / U22 are at **(129.00, 90.00)** and **(136.00, 90.00)**, not the SI-accepted (158.6, 102.9) / (152.5, 102.9). Those two positions are already present on the frozen baseline, so this LS pass did not move them — but the CSV must not be used as the current budget until Base Board reconciles placement and remeasures.

## What must change before further routing (process + geometry)

1. **Stop calling A* output hand routing.** Next LS work has to be drawn in pcbnew (or equivalently specified segment-by-segment by a person looking at the nearby copper), with the project netclasses loaded. No geometric search, no bounded A*, no Freerouting.
2. **Load netclasses.** The 21:45 router wrote every track at 0.15 mm. That includes all 34 PWR-class segments (required width 0.60 mm).
3. **Do not keep 0.03 mm DRC-margin jogs.** These are visible on the board:
   - `HALL_A_N` 0.0206 mm stub at (141.980, 152.594) → (142.000, 152.600)
   - `SYS_INT_N` 0.0398 mm stub at (165.994, 142.161) → (166.000, 142.200)
   - `HALL_B_N` has no separate 0.03 mm segment; the nudge landed as a ~0.05 mm odd-angle piece, which is the same class of fix.
   If a path only clears by 0.03 mm, rip it and choose a real corridor.
4. **The A* signature is obvious and will fight Gen5 later:** 594 of 1441 segments are 45°, 232 are off-grid odd angles, plus stair-stepped 45° chains (for example `CB_PWRBTN_N`). That copper meanders through future 85 Ω space (next section).
5. **Do not add more L1–L6 through vias in Gen5 channels.** All 82 vias are 0.25 mm drill and span L1_SIG_RX to L6_GND_BRK, so the 79 new vias punch In2 and In3. Several already sit in face/SSD corridors (below).
6. **UUID membership is not a substitute for a completed baseline DRC.** The pre-route DRC jobs were still stalled at report time. SI accepts the “new vs preexisting” split only where it was also checked against the 21:45 → 22:04 violation delta (24 new-copper hits gone, one new starved thermal). Anything still classified only by UUID should be treated as unverified if it matters electrically.

## Thermal / power regressions — fix these first

These are ahead of any further LS.

1. **`SW_5V_SBY` is open.** Pads still present, zero tracks:
   - U7.2 (181.863, 126.500) — TPS563201 switch node
   - C9.2 (179.635, 126.105) — bootstrap cap
   - L2.1 (187.000, 126.500) — inductor
   DRC lists both missing pairs. The 5V-standby buck cannot switch like this. Re-route as a **short, wide (0.60 mm minimum, preferably a small pour)** switch-node, not another 0.15 mm A* run. `BST_5V_SBY` is still present (11 segments, 6.07 mm at 0.15 mm) with the switch node deleted; that leftover should be rebuilt with the node, not left as an orphan bootstrap trace.
2. **The other switch nodes that did stay connected are still wrong electrically.** All at 0.15 mm on L1:
   - `SW_3V3_SB` — 12 segments, 9.63 mm (PWR class, should be 0.60 mm and short)
   - `SW_3V3_RDRV` — 13 segments, 11.59 mm (same)
   - `VIN_F` — 9 segments, 16.08 mm (PWR class, should be 0.60 mm)
   - `BST_3V3_SB`, `BST_3V3_RDRV`, `BST_5V_SBY`, and the `FB_*` nets are Default-class 0.15 mm as well.
   Rip these and hand-draw short wide copper at the inductor/IC, after netclasses are loaded.
3. **U5.2 starved GND thermal (regression).** DRC: L1 GND zone vs U5.2 at (176.30, 130.50), 1 spoke vs min 2. Caused by the `EN_5V` Manhattan repair: vertical at **x=175.20**, y=128.00–132.40 (4.4 mm), 1.1 mm west of U5.2, plus a `SYS_INT_N` via at **(175.75, 131.01)** between that trace and the pad. `FP_PERST_N` already occupies x=174.80 (vertical y=126.20–132.60), so the corridor is tight — but leaving a current-sense amp ground with one spoke is not acceptable. Move `EN_5V` and/or that via, and restore at least two thermal spokes (a GND via on U5.2 is fine).
4. **Isolated L3 `3V3_SB` island** at about (91.96, 117.61) on L3_SIG_TX_PWR (In2). Unchanged this pass, but it is floating copper on the future TX layer. Stitch it or delete it before Gen5 work. In2 also carries both an `L3_GND` pour and an `L3_3V3_SB` pour; any split on that layer has to be planned around TX pairs, not left as a leftover fill.

## Gen5 corridor encroachment (must change before more LS, and before any Gen5 routing)

No Gen5 traces exist, so this is occupancy, not a measured loss failure. A* dumped long sidebands onto L1_SIG_RX (the RX microstrip layer) through the channels U20 / J1 / J11 / J12 will need.

- **U20–J1 box** (155–195, 100–116): 105 segments, ~265 mm, 10 nets. Heaviest: `TRIP_N` (53), `FP_THERM_ALERT_N`, `I2C_SYS_SCL`, `FP_THERM_TRIP_N`. Via: `BP_OTEMP_N` at (171.04, 111.34), in the J1 pad row.
- **U20–J11 face box** (165–210, 65–103): 81 segments, ~198 mm. Mostly `FP_THERM_ALERT_N`. Four new L1–L6 vias: `FP_PWR_GOOD` (191.87, 90.14), `FP_SMB_SDA` (194.52, 87.49), `FP_THERM_ALERT_N` (196.35, 85.75), `FP_MOD_LED_N` (199.81, 82.18).
- **J12 / U21 / U22 box** (95–160, 55–95): 104 segments, ~186 mm (`FS_SMB_SDA`, `FS_PERST1_N`, `FS_THERM_TRIP_N`, `SW_3V3_RDRV`, …). New via `FS_CLKREQ1_N` at (104.95, 71.27) in the J12 field, on top of the three preserved Gen5 dangling vias.

Pull this LS out of those boxes, or at least squeeze it to board edges / L6 breakout **outside** the pair channels, before adding more copper. Do not add further through-vias there.

Preexisting, but blocking Gen5 later: the preserved `FS_RX7_N_B` via at (120.000, 61.000) has **0.0031 mm** clearance to J12.D23 GND (PCIE_85R 0.100 mm required) and hole clearance 0.103 mm vs 0.200 mm. That via has to move before any SSD-side Gen5 fanout.

## Remaining DRC (not introduced as new-track hits)

- 124 pad–pad shorts (H3/J14, U26/J1, J11/J3 class — placement).
- 98 starved thermals (97 preexisting-style + the U5.2 regression).
- 33 solder-mask bridges (fine-pitch / BGA).
- 12 clearances and 2 hole-clearances, as above.
- 6 keepout violations (H2, R25, U3 in `KO_U20_RADIAL_CHANNEL`; J11, J12, J13 vs other keepouts).
- 3 dangling Gen5 vias, 3 courtyard overlaps, silk/lib warnings.

None of that is fab-ready. Placement clashes (H3 vs J14 especially) remain Aidan/Mechanical questions, unchanged here.

## Next steps for Base Board & Connectors

1. Relabel this file as a partial algorithmic LS draft. Do not deliver it to Aidan as completed manual routing.
2. Fix the power/thermal regressions first: `SW_5V_SBY` switch-node, then `SW_3V3_SB` / `SW_3V3_RDRV` / `VIN_F` at proper PWR width, then U5.2 GND spokes / `EN_5V` + `SYS_INT_N` via.
3. Rip LS (and new through-vias) out of the U20–J1, U20–J11, and J12 Gen5 boxes listed above. Keep future LS vias out of those channels; prefer not punching L1–L6 through In2/In3 there.
4. Continue remaining true LS (76 nets / 108 airwires) as real hand routing, project netclasses loaded, LS only on L1/L6, no 0.03 mm nudges. Congested leftovers (J1↔U1 UART/FAN/RSMRST/PWR_OK, J14 I2C, QSPI SD0/SD2/SD3/SS, U20/U21/U22 MODE/ADDR and PD straps, `I2C_SYS_SDA`/`SCL`) need room or part moves, not a clearance-rule change.
5. Before any Gen5 pass: move the `FS_RX7_N_B` via off J12.D23; stitch or delete the isolated L3 `3V3_SB` island; confirm U21/U22 coordinates against the 2026-10-28 SI placement and remeasure segment lengths (the Oct 28 CSV is not valid for this file’s U21/U22); then route In2 at 0.24 / 0.127 (widen any leftover 0.21 mm pairs to 0.24) and F.Cu at 0.26 / 0.125.
6. Hold the 3V3_RDRV rail decision before splitting redriver nets, as before.

SI can re-review after the switch-node / U5.2 fixes and after LS is cleared from the Gen5 channels — or when there are actual routed Gen5 lengths to score against the 20–22 dB/side budget.
