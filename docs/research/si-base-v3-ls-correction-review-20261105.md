# SI & Fab review: base-v3 LS bounded correction (2026-11-05)

Reviewed read-only for Master Bot / Base Board & Connectors. No PCB edits, no push, no orders.

- **Board:** `/workspace/kicad/macpro62-backplane-v3/backplane.kicad_pcb`
- **SHA-256:** `f584c0938a8c3d5b60c9d0d4c83d0f680c51093463c47b04fd8851f5d0fc159c` (matches claim; identical to `work/handroute/backplane_si_correction_20261105-2215.kicad_pcb`)
- **Pre-correction snapshot:** `work/handroute/backplane_pre_si_correction_20261105-220954.kicad_pcb` SHA `ecf4b683fdefb0ce9fca20bdad544cafd0d83f7089e387e9ed6084f122edc810` (the file SI rejected at 22:04)
- **Journal:** `work/handroute/si_correction_20261105-2215.json`
- **Script:** `work/handroute/si_correction_20261105.py`
- **Report:** `work/handroute/REPORT_ls_handroute_20261105.md` (22:19 EST / America/New_York section)
- **DRC:** `work/handroute/final_drc_20261105-2215.json` (KiCad 9.0.2, 2026-11-05 22:19:40 EST)
- **ERC:** `work/handroute/final_erc_20261105-2215.json` (KiCad 9.0.2, 2026-11-05 22:18:57 EST)
- **Prior reject:** `/workspace/research/si-base-v3-ls-handroute-review-20261105.md`
- **Reviewer method:** independent pcbnew load of the live board, the pre-correction snapshot, and the frozen baseline; UUID delta of every track/via; parse of the DRC/ERC JSON, journal, and `remaining_ls.json`. Not a restatement of the report.

## Verdict

**ACCEPTED WITH CAVEATS** as a bounded correction of the rejected 22:04 draft.

This is **not** completed manual routing and **not** fab-ready. Base Board correctly relabeled the file as a partial algorithmic LS draft plus a specified-geometry cleanup. SI will not treat this pass as converting the A* copper that remains into hand routing.

The correction did what the reject asked for where a short, legal fix existed, and it honestly left the rest open instead of forcing 0.60 mm copper through occupied buck channels or Gen5 boxes. No new clearance, hole-clearance, or short landed on the copper that was written or widened.

## Independent checks (match unless noted)

| Metric | Claimed (after 22:19 correction) | Measured |
| --- | --- | --- |
| SHA-256 | `f584c093…159c` | match (live == snapshot) |
| Footprints / tracks / vias | 221 / 944 / 65 | 221 / 944 / 65 |
| Layer split | L1 605 / L6 339 | L1_SIG_RX 605 / L6_GND_BRK 339 |
| KiCad `GetUnconnectedCount(False)` | 583 (567 → 583) | pre 567, live 583, baseline 992 |
| DRC violations | 284 (274 error / 10 warning) | 284 = 274 + 10 |
| DRC unconnected / schematic parity | 499 / 47 | 499 / 47 (37 `net_conflict` + 10 `footprint_symbol_mismatch`) |
| ERC | 0 error / 142 warning | 0 / 142 (141 dangling labels + 1 `lib_symbol_mismatch`), same composition as 22:04 |
| PCIE_85R tracks | 0 | 0 (length 0 mm) |
| Tracks on L3_SIG_TX_PWR (In2) or L4_SIG_SLOTB (In3) | 0 | 0 |
| True LS still open | 82 nets / 132 airwires | summed from `remaining_ls.json` (`true_ls_open`); taxonomy not re-derived from scratch |
| Unique nets still holding some own-pass tracks | 63 | 63 track-nets; exact match to `unique_committed_nets` |
| Gen5 vias | original 3, unchanged | same three UUIDs and coordinates as the frozen baseline |
| Corridor rip | 467 tracks / 18 vias on 14 nets | pre 467 / 18, live 0 / 0 |
| Journal deletes vs live UUID delta | 518 items | exact match (500 tracks + 18 vias deleted; 3 SYS_INT_N tracks + 1 GND via added) |

`.kicad_pro` SHA `afe54ca108ceef2fb7733095f4584dbe4a91d6a7b87017abbc9ef3782656353b`, `.kicad_dru` SHA `b807292e5b82f97e0834cd5e143f8ea9ef6f742713f214902dcdfd8351a0cf30`, and schematic SHA `fa5b47eb6e608e6682b1c893bb9e8354ea2e8d28fbe24361075a27586f702e57` are unchanged. Netclasses still read Default 0.15/0.10, PWR **0.60/0.15**, PWR_FINE 0.40/0.10, PWR_HI 1.50/0.20, PCIE_85R 0.26/0.10, USB2_SATA_90R 0.24/0.10.

Track widths now: **942 × 0.15 mm** and **2 × 0.60 mm** (the kept VIN_F diagonals). That is expected: this pass widened two power segments and added three Default fanout segments; it did not rewrite the leftover A* LS.

DRC `unconnected_items` staying at 499 is pair churn, as before, not proof the new opens are absent. KiCad’s ratsnest rising 567 → 583 is the connectivity number SI trusts here.

## Method (no search / A*)

The correction script is an exact geometry writer: `SetWidth` / `SetStart` / `SetEnd` / `SetPosition` / add named segments / delete listed UUIDs. There is no candidate generation, A*, grid search, or Freerouting in `si_correction_20261105.py`.

It loads `backplane.kicad_pro` first and aborts if PWR is not 0.60 mm or if pcbnew did not assign `VIN_F` / `SW_*` to class PWR. The journal records those loaded classes and pad assignments; live copper matches them (`VIN_F` tracks report class PWR at 0.60 mm; the three `SW_*` nets have zero tracks).

UUID delta versus the rejected `ecf4b683…` file, besides the 518 listed deletes:

- Widened: VIN_F `7c7dd092…` (F1.2–D3.1) and `f7e9fe2c…` (F1.2–R100.1), 0.15 → 0.60 mm, endpoints unchanged.
- Moved: SYS_INT_N via `abdef47c…` (175.75, 131.014) → **(175.75, 133.00)**; L6 segment `24db6225…` endpoint updated to the new via (14.315 mm → 12.864 mm). No new L6 path search.
- Added: three specified L1 SYS_INT_N segments (U5.3 (176.3, 131.0) → (177.50, 131.0) → (177.50, 133.00) → via (175.75, 133.00)) and one GND via `51e657eb…` on U5.2 at (176.3, 130.5), drill 0.25 / pad 0.45, L1–L6.

That is the entire write set. Nothing else appeared or disappeared.

## Reject checklist

From `/workspace/research/si-base-v3-ls-handroute-review-20261105.md`, what had to change before further routing:

1. **Stop calling A* output hand routing.** Done for this file’s labeling. The leftover 0.15 mm copper is still the 21:45 A* draft; it is just smaller.
2. **Load netclasses.** Done for this pass. The two kept VIN_F power segments are 0.60 mm. The switch-node nets were not rewritten at 0.15 mm.
3. **Do not keep 0.03 mm DRC-margin jogs.** **Not in this bound.** Still present: `HALL_A_N` 0.0206 mm at (141.980, 152.594)→(142.000, 152.600); `SYS_INT_N` 0.0398 mm at (165.993, 142.161)→(166.000, 142.200); `HALL_B_N` ~0.050 mm at (134.643, 137.426)→(134.600, 137.400). Rip and redraw later; do not nudge them again.
4. **Pull LS (and new through-vias) out of the U20–J1, U20–J11, and J12 boxes.** Done for the through-channel dumps. See occupancy below.
5. **Fix `SW_5V_SBY`, then `SW_3V3_SB` / `SW_3V3_RDRV` / `VIN_F`, at proper PWR width.** Partial: VIN_F F1–D3–R100 is 0.60 mm; the three switch nodes and the VIN_F U5.10 sense run were reverted and left open rather than forced. That is the safe choice. Closing the switch nodes still needs a buck-channel decision (below).
6. **Restore U5.2 GND spokes** (the `EN_5V` / `SYS_INT_N` via regression). Done. DRC no longer reports U5.2 as a starved thermal. `EN_5V` was left at x=175.20, y=128.00–132.40, as disclosed; the via was moved south and a GND via was placed on the pad instead.
7. **Do not add more L1–L6 through vias in Gen5 channels.** No new via was added inside the three boxes. The new GND via sits on U5.2 at (176.3, 130.5), south of the U20–J1 box (y=100–116). SI had already accepted a U5.2 stitch.
8. **Isolated L3 `3V3_SB` island; `FS_RX7_N_B` vs J12.D23; U21/U22 vs the 2026-10-28 CSV.** Unchanged, and correctly deferred until a Gen5 pass.

## Power / thermal geometry

**VIN_F power path — accepted.** Live copper is only:

- F1.2 (176.400, 138.500) → D3.1 (178.500, 141.500), 3.662 mm at 0.60 mm, class PWR
- F1.2 (176.400, 138.500) → R100.1 (174.387, 135.050), 3.994 mm at 0.60 mm, class PWR

Combined 7.656 mm. Those pads are large enough for 0.60 mm (F1.2 1.25×1.75, D3.1 2.5×1.8, R100.1 1.125×1.75). No 2215 DRC item mentions `VIN_F`.

**VIN_F U5.10 Kelvin sense — openly open, but not a placement blocker.** Seven 0.15 mm sense segments were removed. U5.10 (180.70, 130.00, 1.45×0.30) cannot take 0.60 mm copper: U5.9 VIN is 0.50 mm north, pad gap 0.20 mm vs 0.45 mm needed for a 0.60 mm trace plus PWR clearance. Refusing to force 0.60 mm onto that pin is correct.

The sense pin should not wait on a footprint move. VIN_F is doing two jobs: the fused feed (needs 0.60 mm) and a Kelvin input (should neck down). A short Default 0.15 mm or PWR_FINE 0.40 mm stub into U5.10 is the right electrical answer, and the deleted 0.15 mm run already proved a narrow path can exist outside the Gen5 boxes. Restore it as specified geometry, not as another 0.60 mm PWR run.

**Three switch nodes — openly open, and these do need a buck-channel decision.**

| Net | Pads still present | Live tracks |
| --- | --- | --- |
| `SW_5V_SBY` | U7.2 (181.863, 126.500), C9.2 (179.635, 126.105), L2.1 (187.000, 126.500) | 0 (already open since 22:04) |
| `SW_3V3_SB` | U6.2 (181.863, 134.000), C5.2 (184.565, 131.135), L1.1 (187.000, 134.000) | 0 (12 segments reverted) |
| `SW_3V3_RDRV` | U24.2 (116.862, 96.000), C76.2 (118.480, 93.200), L5.1 (121.100, 96.000) | 0 (13 segments reverted) |

The cited crossings are real: `BST_3V3_SB` (183.605, 131.135)–(184.137, 133.050) crosses a north bus at y=132.20 near x=183.90; `BST_3V3_RDRV` (119.138, 95.050)–(117.520, 93.200) crosses a north bus at y=94.30 near x=118.48 and sits in the J12 box because C76 is at y=93.2. `SW_5V_SBY` is still boxed in by leftover `BST_5V_SBY` (11 segments, 6.066 mm at 0.15 mm), `AUXP_EN_N`, `EN_5V` at y=128.0, and `FB_5V_SBY`. Do not send another thin A* run through those nests, and do not drag a long 0.60 mm detour across the board.

`BST_5V_SBY` remains an orphan bootstrap on an open switch node, as SI noted last time. Leave it documented until the node is rebuilt with it.

**U5.2 thermal regression — gone.** 22:04 DRC reported L1 GND zone vs U5.2 (spoke count 1 vs min 2). 22:19 does not. Independent pad check: GND via centered on U5.2 at (176.3, 130.5). Copper-edge gap from that via (0.45 mm pad) to U5.3 SYS_INT_N (0.30 mm pad, 0.50 mm pitch) is 0.125 mm vs Default 0.10; DRC did not flag it. The moved SYS_INT_N via at (175.75, 133.00) is south of the `EN_5V` vertical (ends at y=132.40) and is no longer between `EN_5V` at x=175.20 and U5.2.

**Zone-fill thermal churn (caveat, not a new-track hit).** Starved thermals went 98 → 94. Besides U5.2, DRC dropped reports on C31.2, SW2.2, U22.35, U22.44, and U20.B19, and added 1-spoke reports on **U21.56** (130.60, 85.40) and **U22.64** (134.40, 85.40). Those two are preexisting U21/U22 GND pads plus the same baseline L1 GND zone UUID, inside the J12 box, after nearby FS_* / I2C copper was ripped and the zone refilled. Same class as the other ~90 BGA thermals; no new-track clearance or short. Watch them on the next refill; do not treat the −4 as “four electrical fixes.”

Clearance (12), hole-clearance (2), and shorting (124) sets are unchanged. The 12/2 remain the preexisting pad/via hits (U21/U22 BGA-to-GND, U25 PWR_HI, J11 vs J3, H3 vs J14 NPTH, J12.D23 vs `FS_RX7_N_B`). Short pad-description and UUID sets are identical to 22:04.

No 22:19 violation item mentions the new VIN_F 0.60 mm diagonals, the SYS_INT_N package-channel fanout, the moved SYS_INT_N via, or the U5.2 GND via.

## Gen5 corridor occupancy

Through-corridor nets are empty on the live board (14 nets, 467 tracks + 18 vias removed; no automatic replacement). The six pair-field vias SI called out are gone:

- `BP_OTEMP_N` (171.038, 111.335)
- `FP_PWR_GOOD` (191.873, 90.142)
- `FP_SMB_SDA` (194.520, 87.488)
- `FP_THERM_ALERT_N` (196.345, 85.745)
- `FP_MOD_LED_N` (199.811, 82.179)
- `FS_CLKREQ1_N` (104.952, 71.271)

Live box occupancy, same clip-window as last time:

| Box | What remains |
| --- | --- |
| U20–J1 (155–195, 100–116) | `GPU_RDRV_PD` only: two ~0.60 mm U20 pin ties (1.203 mm total) |
| U20–J11 (165–210, 65–103) | `GPU_RDRV_PD` only: one of those same ties clips the overlap |
| J12 (95–160, 55–95) | `SSD_3V3_SB_OPT` J12.J25–R121.2 (4.305 mm); `SSD_RDRV_PD` two 0.40 mm U21/U22 PD ties at y=94.6; `BST_3V3_RDRV` U24.6–C76.1 (2.457 mm, C76 at y=93.2); plus the original three Gen5 dangling vias |

Those four kept nets are local pad ties whose pads sit in or on a box, not through-channel highways. SI accepts leaving them.

Gen5 invariants still hold:

- `FS_RX0_P_B` uuid `4be906ad-4cfe-4de7-a5fd-db1002e7b4ec` at (102.000, 82.000)
- `FS_RX7_N_B` uuid `d640b1d5-9ad4-4ca7-b681-274cb65b989e` at (120.000, 61.000)
- `FS_TX4_N_B` uuid `cbcf4a94-0daa-4647-9f60-bcda2d00d91b` at (111.000, 67.000)

Zero tracks on those nets. Those are still the only FS_RX/FS_TX vias. DRC still flags them as dangling, as expected. The `FS_RX7_N_B` vs J12.D23 hit (0.0031 mm vs PCIE_85R 0.100 mm; hole 0.103 vs 0.200) was correctly left alone and still has to move before any SSD-side Gen5 fanout.

The isolated L3 `3V3_SB` island is still at about (91.96, 117.61). Stitch or delete it before Gen5 work.

Live U20 remains at (173.70, 102.90). Live U21 / U22 remain at (129.00, 90.00) / (136.00, 90.00), not the SI-accepted (158.6, 102.9) / (152.5, 102.9). The 2026-10-28 length CSV is still not valid for this file’s U21/U22.

There is still no routed Gen5 copper to score against the 20–22 dB/side budget, and no 85 Ω geometry to pass or fail. In2 0.24/0.127 and F.Cu 0.26/0.125 remain the documented targets.

## What continuing requires

Split, because these are different kinds of work:

1. **Permitted in-scope manual rework (remaining true LS and cleanup).** 82 nets / 132 airwires, including the six corridor nets that are now fully open (`FP_MOD_LED_N`, `FP_THERM_TRIP_N`, `FS_CLKREQ1_N`, `FS_PERST1_N`, `FS_THERM_TRIP_N`, `TRIP_N`) and the extra airwires on `I2C_SYS_SCL` (11), `BP_OTEMP_N` (4), `FS_SMB_SDA` (3), and the other ripped sidebands. Draw this in pcbnew, project netclasses loaded, L1/L6 only, no geometric search, no A*, no Freerouting, no 0.03 mm nudges. Keep new LS and new L1–L6 vias out of the three Gen5 boxes. The leftover 0.03 mm stubs listed above are in this bucket: rip and choose a real corridor. Congested leftovers (J1↔U1 UART/FAN/RSMRST, J14 I2C, QSPI, U20/U21/U22 straps) still need room or part moves, not a rule change.

2. **Buck channel / placement decisions (the three SW nodes).** A short 0.60 mm (or small pour) node is the right electrical answer, and it will not fit without rewriting the existing `BST_*` / `FB_*` / `EN_*` copper that already crosses the only short slots — or without moving those footprints. That rewrite is allowed as coordinated, specified-geometry work around U6/U7/U24. It is not “more LS.” Long detours and another 0.15 mm stitch are not acceptable. Footprint moves are an Aidan/placement question if keepouts or the J12 box are involved (`SW_3V3_RDRV` / C76 already sit in that box).

3. **VIN_F U5.10 sense** is in-scope as a specified narrow Kelvin neck-down (see above), not a buck-placement hold.

4. **Before any Gen5 pass, unchanged:** move `FS_RX7_N_B` off J12.D23; stitch or delete the L3 `3V3_SB` island; reconcile U21/U22 with the SI-accepted placement and remeasure; then route In2 at 0.24/0.127 and F.Cu at 0.26/0.125. Hold the 3V3_RDRV rail decision before splitting redriver nets.

5. **Do not deliver this board to Aidan as completed hand routing or as fab-ready.** 284 DRC violations remain (124 pad–pad shorts, 94 starved thermals, 33 solder-mask bridges, 12 clearances, 6 keepouts, 3 dangling Gen5 vias, 3 courtyard overlaps, plus silk/lib). Placement clashes (H3 vs J14, U26 vs J1, H2/U3/R25 vs the U20 radial keepout) are unchanged.

## Next steps for Base Board & Connectors

1. Keep the current label: partial algorithmic LS draft plus a bounded SI correction. Do not call the leftover A* copper hand routing.
2. Continue remaining true LS and the 0.03 mm stub cleanup as real hand routing under the rules above.
3. Treat the three open switch nodes as a buck-channel rewrite (or a placement change), not as ordinary LS. Rebuild each node short and wide together with its bootstrap, and retire the orphan `BST_5V_SBY` leftover as part of that.
4. Put a short narrow Kelvin stub back on VIN_F to U5.10; leave the 0.60 mm F1–D3–R100 feed as it is.
5. On the next zone refill, confirm U21.56 / U22.64 spoke counts and that U5.2 stays at two or more spokes.
6. SI can look again when the switch nodes are rebuilt at width, when there is a specified Kelvin stub on U5.10, or when there are actual routed Gen5 lengths to score.

SI & Fab: `f8cb7986-a918-45d3-8985-d543184b5211`.
