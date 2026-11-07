# SI & Fab review: base-v3 LS hand-planned batch (2026-11-05)

Reviewed read-only for Master Bot / Base Board & Connectors. No PCB edits, no push, no orders.

- **Board:** `/workspace/kicad/macpro62-backplane-v3/backplane.kicad_pcb`
- **SHA-256:** `0057bf6ac9557c733ddd0d3f0def2bf31178c3e2aac506fc183d37db811c7567` (matches claim; identical to `work/handroute/backplane_ls_handplan_20261105-2235.kicad_pcb`)
- **Pre-batch snapshot:** `work/handroute/backplane_pre_ls_handplan_20261105-222544.kicad_pcb` SHA `f584c0938a8c3d5b60c9d0d4c83d0f680c51093463c47b04fd8851f5d0fc159c` (the file SI accepted-with-caveats at 22:19; identical to `work/handroute/backplane_si_correction_20261105-2215.kicad_pcb`)
- **Ledger:** `work/handroute/ls_handplan_20261105-2235.json`
- **Script:** `work/handroute/ls_handplan_20261105.py`
- **Report:** `work/handroute/REPORT_ls_handroute_20261105.md` (22:35 EST / America/New_York section)
- **DRC:** `work/handroute/final_drc_20261105-2235.json` (KiCad 9.0.2, 2026-11-05 22:35:09 EST)
- **ERC:** `work/handroute/final_erc_20261105-2235.json` (KiCad 9.0.2, 2026-11-05 22:35:06 EST)
- **Prior reviews:** `/workspace/research/si-base-v3-ls-handroute-review-20261105.md` (REJECT of 22:04 as “manual routing”); `/workspace/research/si-base-v3-ls-correction-review-20261105.md` (ACCEPT WITH CAVEATS of 22:19 cleanup)
- **Reviewer method:** independent pcbnew load of the live board, the pre-batch snapshot, and the frozen baseline; UUID delta of every track/via; parse of the DRC/ERC JSON, ledger, script, and `remaining_ls.json`; independent clearance measurements on the new copper. Not a restatement of the report.

## Verdict

**ACCEPTED WITH CAVEATS** as a small, explicitly hand-planned LS batch.

This batch is specified-geometry work: named waypoints, project netclasses loaded, no candidate generation, no A*, no Freerouting, no 0.03 mm DRC-margin nudges. SI will treat these seven items as hand-planned. SI will **not** treat the leftover 21:45 A* copper that remains on the board as hand routing, and will not treat the file as completed LS or as fab-ready.

The copper that was written is safe to keep. No new clearance, hole-clearance, short, or starved-thermal landed on it. Gen5 invariants and corridor occupancy are unchanged.

The unapplied `VIN_F` courtyard rule is **not** approved in the exact form written. See below before anyone takes that text to Aidan.

## Independent checks (match unless noted)

| Metric | Claimed (after 22:35 batch) | Measured |
| --- | --- | --- |
| SHA-256 | `0057bf6a…7567` | match (live == post-batch copy) |
| Pre-batch SHA | `f584c093…159c` | match (pre-backup == 22:19 correction file) |
| Footprints / tracks / vias | 221 / 955 / 67 | 221 / 955 / 67 |
| Layer split | L1 608 / L6 347 | L1_SIG_RX 608 / L6_GND_BRK 347 |
| Widths | 0.15 mm × 953; 0.60 mm × 2 | 953 × 0.15 mm (Default); 2 × 0.60 mm (`VIN_F`, class PWR) |
| KiCad `GetUnconnectedCount(False)` | 579 (583 → 579) | pre 583, live 579, baseline 992 |
| DRC violations | 284 (274 error / 10 warning) | 284 = 274 + 10; **exact identity match** vs 22:19 (0 keys added, 0 removed) |
| DRC unconnected / schematic parity | 499 / 47 | 499 / 47 (37 `net_conflict` + 10 `footprint_symbol_mismatch`) |
| ERC | 0 error / 142 warning | 0 / 142 (141 dangling labels + 1 `lib_symbol_mismatch`); **identity match** vs 22:19 |
| PCIE_85R tracks | 0 | 0 (length 0 mm) |
| Tracks on L3_SIG_TX_PWR (In2) or L4_SIG_SLOTB (In3) | 0 | 0 |
| True LS still open | 80 nets / 128 airwires | summed from `remaining_ls.json` (`true_ls_open`); 247 analyze_conn LS = 128 + 44 IOB 85 Ω pairs + 75 `3V3_RDRV` |
| Unique nets still holding some own-pass tracks | 65 | 65; includes new `TRIP_N` and `FS_PERST1_N` |
| Gen5 vias | original 3, unchanged | same three UUIDs and coordinates as the frozen baseline and the 22:19 file |
| UUID delta vs 22:19 | +17 tracks / +2 vias / −6 tracks | exact match to the ledger (0 extras, 0 missing, 0 modified common UUIDs) |

`.kicad_pro` SHA `afe54ca108ceef2fb7733095f4584dbe4a91d6a7b87017abbc9ef3782656353b`, `.kicad_dru` SHA `b807292e5b82f97e0834cd5e143f8ea9ef6f742713f214902dcdfd8351a0cf30`, and schematic SHA `fa5b47eb6e608e6682b1c893bb9e8354ea2e8d28fbe24361075a27586f702e57` are unchanged. Netclasses still read Default 0.15/0.10, PWR **0.60/0.15**, PWR_FINE 0.40/0.10, PWR_HI 1.50/0.20, PCIE_85R 0.26/0.10, USB2_SATA_90R 0.24/0.10. No custom `VIN_F` rule was added to `.kicad_dru` (existing rules remain `hs_pour_clearance` and `usb_pour_clearance` only).

DRC `unconnected_items` staying at 499 is pair churn, as before, not proof of connectivity. The four closed airwires show up where they should: KiCad ratsnest 583 → 579; `true_ls_open` 82/132 → 80/128 (`IOB_PLT_RST_N` and `IOB_USB_OC_N_A` left the list; `TRIP_N` 3 → 2; `FS_PERST1_N` 2 → 1). The 22:19 `TRIP_N` pairing `R17.1 ↔ U8.7` is gone; the new tracks now pair against the still-open `D4.3` and `D5.3`. `IOB_PLT_RST_N` / `IOB_USB_OC_N_A` have zero DRC-unconnected rows (those two were already absent from the 499-list at 22:19; the trusted close is the ratsnest / true-LS drop). `VIN_F` U5.10 remains listed against the existing 0.60 mm F1–R100 feed.

## Method (no search / A*)

`ls_handplan_20261105.py` is an exact geometry writer: delete six named stub/next-segment UUIDs after checking live net and endpoints, then `add_track` / `add_via` at hardcoded waypoints. Via insertion aborts if the point sits in a documented Gen5 box. There is no candidate generation, A*, grid search, or Freerouting in the script (those words appear only in the denial comments).

It loads `backplane.kicad_pro` first and aborts unless Default is 0.15/0.10 and PWR is 0.60/0.15, and unless pcbnew assigned Default to the seven touched LS nets and PWR to `VIN_F` / `SW_*`. The ledger records those loaded classes. Live copper matches them (all 17 new tracks are Default 0.15 mm; the two kept `VIN_F` segments remain PWR 0.60 mm; the three `SW_*` nets have zero tracks).

UUID delta versus `f584c093…` is exactly the ledger: 6 tracks deleted, 17 tracks + 2 vias added, nothing else moved or resized.

## Route / stub quality

The three SI-listed pad-snap stubs are gone. They were replaced by real pad-to-next-waypoint segments, not by another micro-jog:

| Net | Old stub | New segment | Length |
| --- | --- | --- | ---: |
| `HALL_A_N` | 0.0206 mm to (142.000, 152.600) | J13.J10 (141.9803, 152.5939) → (141.2, 151.8) | 1.113 mm |
| `HALL_B_N` | 0.0503 mm to (134.600, 137.400) | R14.1 (134.6433, 137.4256) → (137.4, 140.2) | 3.911 mm |
| `SYS_INT_N` | 0.0398 mm to (166.000, 142.200) | J13.B29 (165.9935, 142.1608) → (165.6, 142.6) | 0.590 mm |

The leftover staircase weaves on `HALL_A_N` / `HALL_B_N` after those waypoints were correctly left alone (a full 45° pad-to-resistor cut of the J13 diagonal pin field would have been worse). `HALL_B_N` R14.1–Q6.1 and the `SYS_INT_N` ~52 mm J13/U5 vs R47/U1 island remain open, as logged.

Closed paths:

1. **`TRIP_N` R17.1–U8.7** — L1 Manhattan 5.511 mm: south at R17.1 x=165.7931 to y=121.025, then east into U8.7. R17.1 at y=116.926 sits 0.926 mm south of the U20–J1 box (y=116); the vertical does not clip the box. An east-then-south at U8.7 x=167.205 would have run through U8.8 (`3V3_SB`). Copper-edge to U8.8 / U8.6 pads is 0.25 mm (Default 0.10). Copper-edge to the `LATCH_CLR_N` via at (166.308, 121.449) is **0.124 mm vs Default 0.10**. That is legal and it is not a scripted 0.03 mm nudge — the jog is pad-defined Manhattan — but the extra margin is only 0.024 mm. Keep it; do not shave it further. `D4.3` and `D5.3` correctly remain open (`D5.3` sits near the U20–J1 box edge).

2. **`FS_PERST1_N` Q12.3–R64.2** — L1 5.128 mm: west at y=105.4125 from x=102.50 to 97.81, then south into R64.2. Outside J12 (y=105 > 95) and U20–J1 (x≈100 < 155). J12.A7 was correctly left open inside the J12 box. Copper-edge to R64.1 (`CB_PLTRST_N`) is 0.675 mm; to R65.1 (`FS_CLKREQ1_N`) about 0.19 mm. The report’s “BOOTSEL_N V at (98.145, 106.995)” is actually pad **R61.2** `BOOTSEL_N`, not a via — a labeling slip. Centerline to the new westbound run is 1.58 mm, as claimed, so the clearance claim still holds.

3. **`IOB_PLT_RST_N` J13.B30–R127.1** — L1 fanout 1.137 mm to via (168.40, 142.1464) drill 0.25 / pad 0.45, then L6 south / west / north / west, 33.381 mm of new track. The via is east of J13, outside every Gen5 box. Existing same-net L6 from R127.1 toward U27.4 was reused, not ripped. Closest foreign L6 copper: `IOB_SLP_S3_N` via at (166.093, 150.500), copper-edge 0.400 mm to the y=151.20 highway.

4. **`IOB_USB_OC_N_A` J13.D30–R128.1** — L1 fanout 2.708 mm to via (170.00, 144.6862), then L6 parallel highway at y=152.00 / x=156.20, 34.112 mm of new track. Centerline separation from the new `IOB_PLT_RST_N` path is 0.80 mm (highways) and 1.00 mm (drops); copper-edge 0.65 mm and 0.85 mm vs Default 0.10. Existing same-net L6 from R128.1 toward U27.5 was reused.

Both new vias are L1–L6 through (they punch In2/In3), which SI already allowed **outside** the three boxes. They are at y≈142–145, x=168.4 / 170.0 — well south/east of U20–J1 (y=100–116), U20–J11 (y=65–103), and J12 (x=95–160). The long L6 go-arounds are electrically fine for a reset and an overcurrent sideband.

No written geometry had to be reverted. Paths they probed and rejected were never added. That is the right habit.

Other leftover A* pad-snaps **under 0.06 mm** still exist on untouched nets (for example `CB_I2C0_SDA` 0.017 mm, `CB_PWRBTN_N` 0.034 mm, `FS_SMB_ALERT_N` 0.045 mm). They are not part of this batch. Rip and redraw them the same way when those nets are next touched; do not nudge them.

## Gen5 corridor occupancy

Unchanged vs 22:19, including the three original Gen5 dangling vias:

| Box | What remains |
| --- | --- |
| U20–J1 (155–195, 100–116) | `GPU_RDRV_PD` only: two ~0.60 mm U20 pin ties (1.203 mm total) |
| U20–J11 (165–210, 65–103) | `GPU_RDRV_PD` only: one of those same ties clips the overlap |
| J12 (95–160, 55–95) | `SSD_3V3_SB_OPT` J12.J25–R121.2 (4.305 mm); `SSD_RDRV_PD` two 0.40 mm U21/U22 PD ties; `BST_3V3_RDRV` U24.6–C76.1 (2.457 mm, C76 at y=93.2); plus the original three Gen5 dangling vias |

Gen5 invariants still hold:

- `FS_RX0_P_B` uuid `4be906ad-4cfe-4de7-a5fd-db1002e7b4ec` at (102.000, 82.000)
- `FS_RX7_N_B` uuid `d640b1d5-9ad4-4ca7-b681-274cb65b989e` at (120.000, 61.000)
- `FS_TX4_N_B` uuid `cbcf4a94-0daa-4647-9f60-bcda2d00d91b` at (111.000, 67.000)

Zero tracks on those nets. Those are still the only FS_RX/FS_TX vias. DRC still flags them as dangling, as expected. The `FS_RX7_N_B` vs J12.D23 hit was correctly left alone.

Live U20 remains at (173.70, 102.90). Live U21 / U22 remain at (129.00, 90.00) / (136.00, 90.00), not the SI-accepted (158.6, 102.9) / (152.5, 102.9). The 2026-10-28 length CSV is still not valid for this file’s U21/U22.

There is still no routed Gen5 copper to score against the 20–22 dB/side budget, and no 85 Ω geometry to pass or fail.

## Power / thermal

**`VIN_F` fused feed — unchanged and still accepted.** Live copper is only:

- F1.2 (176.400, 138.500) → D3.1 (178.500, 141.500), 3.662 mm at 0.60 mm, class PWR
- F1.2 (176.400, 138.500) → R100.1 (174.3875, 135.050), 3.994 mm at 0.60 mm, class PWR

U5.10 (180.70, 130.00, 1.45×0.30, net `VIN_F` / PWR) is still open. R100 is the shunt: R100.1 `VIN_F`, R100.2 `VIN`. U5.9 is `VIN` (INA226 IN−) 0.50 mm north of U5.10 (IN+). Pad gap 0.20 mm. A 0.60 mm trace plus PWR 0.15 mm clearance cannot enter U5.10 next to U5.9. Leaving that pin open this pass was correct.

**Three switch nodes — still openly open, and they still need a buck-channel decision.** Zero tracks on `SW_5V_SBY`, `SW_3V3_SB`, and `SW_3V3_RDRV`. Pads unchanged from 22:19 (U7.2/C9.2/L2.1, U6.2/C5.2/L1.1, U24.2/C76.2/L5.1). `BST_5V_SBY` remains an orphan bootstrap on an open switch node. Do not send a thin Default detour through those nests.

**U5.2 thermal — still restored.** DRC does not report U5.2 as a starved thermal. The SI-accepted GND via `51e657eb-46f6-4596-ade6-837cdde29c0f` is still on the pad at (176.3, 130.5), drill 0.25 / pad 0.45.

**U21.56 / U22.64 — still 1-spoke, correctly left alone.** DRC still reports both (and U21/U22 pads 21, 24, 56, 64) as `starved_thermal` on L1, min 2 / actual 1. Independent inspect: **no tracks or vias within 1.6 mm** of U21.56 (130.60, 85.40) or U22.64 (134.40, 85.40). Both sit inside the J12 box. A new GND via there would be a new via in a documented HS corridor. Same class as the other ~90 BGA thermals. Do not “fix” them with corridor copper.

Starved-thermal count stays 94. Clearance (12), hole-clearance (2), and shorting (124) sets are identity-identical to 22:19. No 22:35 violation item mentions the new HALL stubs, `TRIP_N`, `FS_PERST1_N`, `IOB_PLT_RST_N`, `IOB_USB_OC_N_A`, or the two new vias. The only DRC rows that name new UUIDs are two `unconnected_items` pairings of the new `TRIP_N` tracks against still-open `D4.3` / `D5.3` — expected leftover airwires, not new faults.

The isolated L3 `3V3_SB` island is unchanged (still one `isolated_copper` DRC item; L3 still has GND and `3V3_SB` zones and zero tracks).

## Proposed `VIN_F` U5.10 rule — do not apply as written

U5 is INA226AIDGSR (VSSOP-10_3x3mm_P0.5mm) at (178.50, 131.00). Public TI SBOS547C §8.4.1 wants a Kelvin / 4-wire connection to the shunt. The shunt is R100. Distance R100.1 → U5.10 is **8.084 mm**. U5 courtyard (F.Courtyard shapes) is an irregular ~6.4 × 3.5 mm outline, roughly x=175.32–181.68, y=129.25–132.75. U5.10 is inside that courtyard; R100.1 is not.

The proposed, **unapplied** rule:

```
(rule "VIN_F_U5_10_Kelvin_neck"
  (constraint track_width (min 0.15mm))
  (constraint clearance (min 0.10mm))
  (condition "A.NetName == 'VIN_F' && A.insideCourtyard('U5')")
)
```

| Question | SI answer |
| --- | --- |
| Geographically bounded? | **Yes.** The courtyard is package-local. It will not relax the whole `VIN_F` net, and it will not legalize a skinny A* power run elsewhere. That part is the right instinct. |
| Appropriate as a pad-entry width exception? | **Partly.** U5.10 cannot take 0.60 mm copper. A 0.15 mm neck into that pad is the right local exception. Keep netclass PWR (0.60/0.15) for F1–D3–R100. Do not reclass the whole net to PWR_FINE or Default. |
| Sufficient for a datasheet-correct Kelvin run? | **No.** A proper IN+ sense path starts on **R100.1**, not as a tee from mid-span of the high-current F1.2–R100.1 0.60 mm segment, and it runs ~8 mm to U5.10. Most of that path is outside the courtyard, so this rule would not cover it. `A.insideCourtyard('U5')` also typically requires the item to be fully inside, so a 0.15 mm segment that *crosses* the courtyard boundary may not match either. |
| Is the clearance relaxation needed? | **No.** A 0.15 mm trace entering U5.10 from east or north (along the pad, not between U5.10 and U5.9) has ~0.275 mm copper-edge to the U5.9 pad — already above PWR 0.15 mm. Relaxing courtyard clearance to 0.10 mm would also apply if any 0.60 mm `VIN_F` copper ever entered the courtyard. Drop the clearance constraint; make this a width-only exception. |
| Would `intersectsCourtyard` be better? | **No.** A long skinny `VIN_F` segment that merely clipped the courtyard could then inherit the width exception for the whole segment. |

Do **not** send this exact rule to Aidan for a yes/no. It is too tight to do the job they described (“restore a short 0.15 mm stub from the 0.60 mm feed to U5.10”) and the clearance half is unnecessary. Refine it first.

**In-scope geometry + rule (no Aidan required, FYI only):**

1. Keep the 0.60 mm F1–D3–R100 feed as it is.
2. Start a dedicated 0.15 mm sense trace **on the R100.1 pad** (shunt Kelvin tap). Do not tee the middle of F1.2–R100.1.
3. Route that trace to U5.10 from the east or north, not between U5.10 and U5.9, and stay out of the Gen5 boxes.
4. Legalize it with a small rule *area* covering only that sense path (R100.1 to U5 courtyard / U5.10), for example:

```
(rule "VIN_F_U5_10_Kelvin_neck"
  (constraint track_width (min 0.15mm))
  (condition "A.NetName == 'VIN_F' && A.insideArea('VIN_F_Kelvin_U5')")
)
```

Do not set a board-wide `VIN_F` minimum width of 0.15 mm.

**Aidan / schematic, if they would rather avoid a PWR-class exception:** add a net-tie at R100.1 (`VIN_F` PWR 0.60 / `VIN_F_SNS` Default 0.15 to U5.10). That is the textbook Kelvin implementation. Also worth checking later: IN− from R100.2 to U5.9, if that path is not already a dedicated sense trace.

## Exact decisions

### In-scope for Base Board (no Aidan)

- Continue remaining true LS (80 nets / 128 airwires) as real hand routing: project netclasses loaded, L1/L6 only, no geometric search, no A*, no Freerouting, no 0.03 mm nudges. Keep new LS and new L1–L6 vias out of the three Gen5 boxes.
- Leave `FS_PERST1_N` J12.A7 open until a path exists that does not dump copper through the J12 pair field.
- Coordinated BST / FB / EN rewrite of **`SW_5V_SBY`** around U7 and **`SW_3V3_SB`** around U6, as a short 0.60 mm node or small pour, rebuilt together with each bootstrap. Retire the orphan `BST_5V_SBY` leftover as part of that. No thin detour, no long 0.60 mm wander across the board.
- A coordinated BST / FB / EN rewrite of **`SW_3V3_RDRV` around U24 that does not move C76 further into the J12 pair field**. C76 already sits at y=93.2 inside the J12 box; SI previously accepted that local `BST_3V3_RDRV` pad tie. Do not grow it.
- `VIN_F` Kelvin stub using the SI-specified geometry and rule-area exception above. Do not apply the exact courtyard+clearance text from the 22:35 report.
- Same-style redraw of other leftover A* pad-snaps when those nets are next touched.
- Watch U5.2 (≥2 spokes) and U21.56 / U22.64 (still 1-spoke) on the next zone refill.

### Needs Aidan

- **Moving C76 (or U24 / L5)** out of the J12 box to make a short wide `SW_3V3_RDRV` node without occupying the SSD pair field. That is a placement / keepout question.
- **Schematic net-tie** at R100 for `VIN_F` / `VIN_F_SNS`, if they prefer that over a local DRC exception.
- Unchanged, and not this batch: U21/U22 live coordinates vs the SI-accepted placement; `FS_RX7_N_B` vs J12.D23; the isolated L3 `3V3_SB` island; the `3V3_RDRV` rail decision before splitting redriver nets; any Gen5 routing.

### Do not

- Deliver this board to Aidan as completed hand routing or as fab-ready. 284 DRC violations remain (124 pad–pad shorts, 94 starved thermals, 33 solder-mask bridges, 12 clearances, 6 keepouts, 3 dangling Gen5 vias, 3 courtyard overlaps, plus silk/lib). Placement clashes (H3 vs J14, U26 vs J1, H2/U3/R25 vs the U20 radial keepout) are unchanged.
- Call the leftover 21:45 A* copper hand routing.
- Force 0.60 mm onto U5.10, or reclass all of `VIN_F` to Default / PWR_FINE.
- Add a GND via on U21.56 or U22.64 inside the J12 box.
- Thin-stitch the three switch nodes.

## Next steps for Base Board & Connectors

1. Keep the current label: leftover algorithmic LS draft, plus the 22:19 SI correction, plus this 7-item hand-planned batch. Do not collapse those into “the board is hand-routed.”
2. Continue remaining true LS under the rules above.
3. Treat the three open switch nodes as a buck-channel rewrite (or, for `SW_3V3_RDRV` / C76, an Aidan placement change), not as ordinary LS.
4. Do not apply the exact proposed `VIN_F` courtyard rule. If you write the Kelvin stub this cycle, use a dedicated 0.15 mm run from R100.1 and a rule *area* (width only), or ask Aidan for a net-tie.
5. SI can look again when the switch nodes are rebuilt at width, when there is a specified Kelvin stub on U5.10 under a bounded rule, or when there are actual routed Gen5 lengths to score.

SI & Fab: `f8cb7986-a918-45d3-8985-d543184b5211`.
