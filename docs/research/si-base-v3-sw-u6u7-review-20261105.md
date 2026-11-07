# SI & Fab review: base-v3 U6/U7 coordinated buck rewrite (2026-11-05)

Reviewed read-only for Master Bot / Base Board & Connectors. No PCB edits, no push, no orders.

- **Live board:** `/workspace/kicad/macpro62-backplane-v3/backplane.kicad_pcb`
- **Live SHA-256:** `62392c3c2f03b29e182b74efd5e4b461375822e8f08dcd052dc0cbfbf7f6e196`
- **Claimed SHA-256:** `0e1f4d60910c23988f5bdb1187544dcb24aac99abc2cf6fd8e69245025b0cd22` — **does not match**
- **Snapshot on disk:** `work/handroute/backplane_sw_u6u7_20261105-2251.kicad_pcb` (same SHA as live)
- **Claimed snapshot:** `work/handroute/backplane_sw_u6u7_20261105-2300.kicad_pcb` — **not present**
- **Claimed report:** `work/handroute/REPORT_ls_handroute_20261105.md` — **not present** (so the suggested alternative placements in that report could not be compared)
- **Datasheet:** TI TPS563201 / TPS563208, **SLVSD90B** (December 2015, revised September 2024), fetched from `https://www.ti.com/lit/ds/symlink/tps563201.pdf` and saved at `/workspace/research/ti/tps563201.pdf`
- **Reviewer method:** independent parse of the live PCB (footprints, pads, segments, vias, zones, layer stack) and of `backplane.kicad_sch` / `backplane.kicad_pro`. Not a restatement of the missing report. KiCad DRC/ERC JSON for this batch was not on disk, so DRC identity-match vs 22:35 was not verified.

U6 and U7 are both `TPS563201DDCR` (SOT-23-6 / DDC), not a TPS543x. U6 generates `3V3_SB`; U7 generates `5V_SBY`. Pinout from SLVSD90B Table 4-1: 1 = GND, 2 = SW, 3 = VIN, 4 = VFB, 5 = EN, 6 = VBST. Both sit at rotation 0 on F.Cu, with the matching 4.7 µH inductor to their **right** (FB / VBST side) while SW is on the **left**. That orientation is the root cause of the long switch-node wraps.

## Verdict

**REJECT.** Unsuitable despite the claim that DRC is unchanged. Do not treat the SW nodes as closed, and do not continue LS work on top of this copper.

Two of the new connections are DC shorts (U7 bootstrap cap pads crossed; U6 feedback landed on R2's GND pad). Even if those two landings were swapped to the correct pads, the 11.26 mm and 11.36 mm switch-node runs — and U6's two-via hop across B.Cu (`L6_GND_BRK`) beside/under the device — violate SLVSD90B §7.4.1 items 2, 4, 5 and 8 and §7.2.2.5. This needs a placement move or a 180° rotate of U6/U7 (Aidan decision), not another thin detour.

## Independent checks (match unless noted)

| Metric | Claimed | Measured on live `62392c3c…` |
| --- | --- | --- |
| SHA-256 | `0e1f4d60…0cd22` | **`62392c3c…f7f6e196` (mismatch)** |
| Snapshot filename | `backplane_sw_u6u7_20261105-2300.kicad_pcb` | **`…-2251.kicad_pcb` only; SHA equals live** |
| Report / DRC / ERC JSON | `REPORT_ls_handroute_20261105.md`; DRC 284 identity-match vs 22:35; ERC 0/142 | **report and DRC/ERC JSON not on disk** |
| Footprints / tracks / vias | 221 / 956 / 73 | 221 / **955** / **69** |
| Layer split | (not separately claimed) | F.Cu (`L1_SIG_RX`) 606, B.Cu (`L6_GND_BRK`) 349, In1–In4 **0 tracks** |
| `SW_5V_SBY` U7 pad 2 → L2 pad 1 | 0.60 mm, L1 north bus, 11.36 mm | **match:** 11.363 mm, all F.Cu, width 0.60 mm |
| `SW_3V3_SB` U6 pad 2 → L1 pad 1 | 0.60 mm, L6 north-of-device hop, 2 vias, 11.26 mm | **match:** 11.263 mm; vias at (180.600, 134.000) and (185.500, 132.200), 0.45/0.25, F.Cu↔B.Cu |
| C5 SW pad → L1 pad 1 | 5.30 mm | **match:** 5.300 mm |
| BST 2 vias / L6; EN 2 vias / L6 | claimed for this rewrite | **not present:** `BST_3V3_SB`, `BST_5V_SBY`, `EN_3V3`, `EN_5V` all have **0 vias**. U6 BST is a 1.988 mm F.Cu stub; U7 BST is a 10.713 mm F.Cu wrap; both EN nets are F.Cu only |
| Footprint / rule / schematic changes; C76 | none; C76 untouched | **match:** C76 still at (118.000, 93.200) on `BST_3V3_RDRV` / `SW_3V3_RDRV`; `.kicad_pro` PWR still 0.60/0.15; no new `.kicad_dru` inspected as changed |
| PCIE / Gen5 lane tracks | 0 | **0** (192 `FP_/FS_ TXn/RXn` lane nets; zero segments) |
| In2 (`L3_SIG_TX_PWR`) / In3 (`L4_SIG_SLOTB`) tracks | 0 | **0** |
| Original 3 Gen5 vias | invariant | **match:** `FS_RX0_P_B` (102, 82), `FS_RX7_N_B` (120, 61), `FS_TX4_N_B` (111, 67) |
| Suggested alternative placements | not applied | cannot compare to the missing report; SI's own placement recommendation is below |

Netclasses loaded on the written copper: `SW_3V3_SB` and `SW_5V_SBY` are 0.60 mm (PWR); BST / FB / EN runs are 0.15 mm (Default). That part is consistent with the project file.

The SHA / count / BST-via / EN-via mismatches mean this file is not exactly the state described in the review request. The switch-node lengths that *were* claimed do match the copper that is here, so the electrical verdict is against this live geometry, not against a missing 23:00 snapshot.

## Parts and placement (as found)

| Ref | Function | Location (mm) | Notes |
| --- | --- | --- | --- |
| U6 | TPS563201 → `3V3_SB` | (183.000, 134.000) rot 0 | SW pad 2 at (181.863, 134.000) **left**; VBST pad 6 at (184.137, 133.050) **right** |
| L1 | 4.7 µH 2 A (SWPA4030S4R7MT) | (188.500, 134.000) | SW pad at (187.000, 134.000), 5.137 mm east of U6 SW — on the opposite side of the IC |
| C5 | 100 nF bootstrap | (184.085, 131.135) | pad 1 `BST_3V3_SB`, pad 2 `SW_3V3_SB`; 1.99 mm from U6 VBST |
| R1 / R2 | 33 k / 10 k FB divider | (183.105, 137.145) / (180.645, 137.605) | Table 7-2 3.3 V values (33.2 k / 10 k typ.) |
| R5 | 100 k EN pull-up to VIN | (179.645, 134.605) | “always on” |
| U7 | TPS563201 → `5V_SBY` | (183.000, 126.500) rot 0 | same pin orientation as U6 |
| L2 | 4.7 µH 2 A | (188.500, 126.500) | SW pad 5.137 mm east of U7 SW |
| C9 | 100 nF bootstrap | (179.635, 126.585) rot 90 | **left** of U7 (SW side), 4.54 mm from U7 VBST |
| R3 / R4 | 56 k / 10 k FB divider | (187.105, 130.145) / (190.105, 130.145) | Table 7-2 5 V uses 54.9 k / 10 k; 56 k is the common E96 stand-in |
| R6 | 100 k EN pull-down to GND | (171.645, 141.605) | “off until MCU enables `5V_SBY`” |
| C3 | 22 µF VIN | (183.608, 129.542) | shared, in the gap between U6 and U7 (2.72 mm from U7 VIN, 5.68 mm from U6 VIN) |
| C10 / C11 | 22 µF `5V_SBY` | (192.655, 134.875) / (193.155, 130.375) | 9.35 mm and 6.06 mm from L2 |
| C6 / C7 | 22 µF `3V3_SB` | (153.800, 107.133) / (147.902, 104.556) | **43.9 mm and 50.2 mm from L1** |

L1/L2 are specified at 2 A Irms, below the IC's 3 A rating. SLVSD90B Table 7-2 allows 4.7 µH as the *max* for both 3.3 V and 5 V (typ. 2.2 µH / 3.3 µH). That is a pre-existing schematic choice, not introduced by this routing, but it already caps each rail at about 2 A.

SLVSD90B layout rules used below (§7.4.1 and §7.2.2.5):

1. VIN and GND traces as wide as possible.
2. Input and output capacitors as close to the device as possible.
3. Sufficient vias for CIN / COUT.
4. **Keep the SW trace as physically short and wide as practical** (to minimize radiated emissions).
5. **Do not allow switching current to flow under the device.**
6. A separate VOUT path to the upper feedback resistor.
7. Kelvin GND for the feedback path.
8. Voltage feedback loop away from the high-voltage switching trace, preferably ground-shielded.
9. VFB node as small as possible.
10. GND between COUT and the GND pin as wide as possible.

Bootstrap: “A 0.1-µF ceramic capacitor **must be connected between the VBST to SW pin**.” Figure 7-18 places the boost cap next to pin 6, the inductor next to pin 2, and any internal/bottom SW pour only as a *local* pour under that short SW node — not as a board-level hop.

## Critical defects (reject items)

### 1. U7 C9 pads are crossed — DC short of `SW_5V_SBY` to `BST_5V_SBY`

C9 (rot 90) at (179.635, 126.585):

- pad 1, net `BST_5V_SBY`, absolute (179.635, 126.105)
- pad 2, net `SW_5V_SBY`, absolute (179.635, 127.065)

Drawn copper:

- `SW_5V_SBY` 0.60 mm segment `(181.8625, 126.5) → (179.635, 126.105)` lands on **pad 1 (BST)**
- `BST_5V_SBY` 0.15 mm segment `(179.635, 127.065) → (179.635, 128.15)` starts on **pad 2 (SW)**

That is a copper short of VBST to SW, bypassing the 100 nF cap. VBST-to-SW would sit at ~0 V instead of the ~5 V the high-side gate drive needs (abs max VBST vs SW is only 6 V per §5.1). U7 would not switch the high-side FET correctly. Swap the two landings so SW copper meets pad 2 and BST copper meets pad 1. Then still move C9 — see item 4.

### 2. U6 `FB_3V3_SB` landed on R2 pad 2 (GND) — DC short of FB to GND

R2 (rot 90) at (180.645, 137.605):

- pad 1, net `FB_3V3_SB`, absolute (180.645, 137.095)
- pad 2, net `GND`, absolute (180.645, 138.115)

Drawn copper on net 175 (`FB_3V3_SB`):

- `(184.137, 134.950) → (183.615, 137.145)` — U6 pin 4 to R1 pad 2: correct
- `(183.615, 138.115) → (183.615, 137.145)` — down to R1 pad 2
- `(180.645, 138.115) → (183.615, 138.115)` — **starts on R2 pad 2 (GND)**

There is no `FB_3V3_SB` segment to R2 pad 1. Feedback is shorted into the GND pad (and into `L1_GND` once that pour connects). U6 would read VOUT = 0, run to current limit, and hiccup. Move the west end of that run from (180.645, 138.115) to R2 pad 1 at (180.645, 137.095).

### 3. 11+ mm switch nodes, and a B.Cu hop under U6, violate §7.4.1 #4 and #5

Straight pad-to-pad SW distance is only 5.137 mm on both rails. The ICs face the wrong way, so the routes wrap around the package:

**`SW_3V3_SB` (11.263 mm, 0.60 mm):**
U6.2 (181.863, 134.000) → west 1.263 mm to via (180.600, 134.000) → B.Cu south 1.800 mm to (180.600, 132.200) → B.Cu east **4.900 mm** to via (185.500, 132.200) → F.Cu east 1.500 mm to (187.000, 132.200) → north 1.800 mm into L1.1 (187.000, 134.000).

The B.Cu east-west run at y = 132.200 crosses the IC's x-extent (U6 body ≈ x 182.2–183.8, y 132.55–135.45). The 0.60 mm trace occupies y ≈ 131.90–132.50, i.e. along the pin-1/6 edge and under the courtyard. Switching current therefore flows across the device on `L6_GND_BRK`, which is exactly what §7.4.1 item 5 forbids.

That same B.Cu copper slots the `L6_GND` pour (B.Cu user name is `L6_GND_BRK`). Return current on L6 has to walk around a ~4.9 × 0.60 mm cut plus clearance, beside the IC. In4 (`L5_GND`) is still adjacent, so the board is not without a reference, but the interruption is unnecessary and noisy.

**`SW_5V_SBY` (11.363 mm, 0.60 mm, all F.Cu):**
U7.2 (181.863, 126.500) → west to (180.600, 126.500) → south to (180.600, 124.650) → east 6.400 mm to (187.000, 124.650) → north into L2.1 (187.000, 126.500), plus a 2.262 mm stub from U7.2 to C9 pad 1 (the wrong pad, item 1).

This north bus does not via-hop and stays just outside the molded body, so it is better than U6's B.Cu underpass — but 11.36 mm is still not “as physically short as practical.” The geometric minimum same-layer wrap around the package, without moving parts, is about 8.5 mm. Anything with two through-vias and an inner/bottom hop is longer and worse.

### 4. Bootstrap loops are not local

- **U6 / C5:** the BST side is fine (1.988 mm F.Cu from C5 pad 1 to U6 pin 6). The SW side of C5 joins the *east* via at (185.500, 132.200), on the inductor end of the hop. The capacitor therefore closes through ~10 mm of SW copper and both vias back to U6 pin 2, not through a tight pin-6-to-pin-2 loop. Gate-drive current sees that inductance on every edge; SLVSD90B abs max VBST vs SW is 6 V.
- **U7 / C9:** after (and in addition to) the pad crossing, BST is a 10.713 mm, 0.15 mm F.Cu wrap at y = 128.150 — through the gap between U6 and U7 — to reach pin 6 on the far side of the IC. That is not “connected between the VBST to SW pin.”

### 5. `3V3_SB` has no local COUT (§7.4.1 #2)

C6/C7, the only 22 µF parts on `3V3_SB`, sit 44 mm and 50 mm from L1. There is no `3V3_SB` track or via in this file (distribution is an In2 pour, `L3_3V3_SB`, which L1's F.Cu pad cannot reach without a via). `5V_SBY` likewise has 0 tracks and 0 vias; C10/C11 are at least in the neighborhood of L2 (6–9 mm) but still not next to L2's VOUT pad. `VIN` also has 0 tracks / 0 vias; C3 is a reasonable shared bulk for U7 and only a fair one for U6. These output-cap distances are placement issues that this routing did not fix and cannot fix with more trace.

## Other electrical notes (not independently reject-worthy, but must change with the fix)

**Current capacity of 0.60 mm SW (1 oz outer, stackup 0.035 mm F.Cu / B.Cu):** IPC-2221 gives about 1.65 A at 10 °C rise, 2.24 A at 20 °C, 2.68 A at 30 °C. That is matched to the 2 A inductor, not to the IC's 3 A rating, and is acceptable for a short SW run if the standby load stays ≤ ~1.5–2 A. It is **not** a reason to keep an 11 mm SW. Two 0.45/0.25 through-vias in the U6 hop are a weak via count for a 2 A switch node (~1 A class per via); do not “fix” the hop by adding vias — remove the hop.

Inner 0.5 oz (0.0152 mm) at 0.60 mm would be only ~0.45–0.73 A. They did not put SW on In1–In4, which is correct.

**`EN_3V3`:** 6.092 mm F.Cu from U6 pin 5 to R5. Functionally fine for a DC pull-up. It does walk across the package centerline; keep EN off the SW/BST copper in the rewrite.

**`EN_5V`:** 30.393 mm F.Cu from U7 pin 5, east to x = 186.100, then a 10.900 mm run at **y = 128.500** toward R6. `BST_5V_SBY` runs at **y = 128.150** for 5.765 mm. Those two 0.15 mm traces are parallel ~0.35 mm apart in the U6–U7 gap. After C9 is moved, pull `EN_5V` out of that alley so BST/SW edges do not couple into enable (U1 / RP2350 also owns `EN_5V`; the route toward R6 is only a partial run). Claimed “EN 2 vias/L6” is not on the board; EN does not need vias, it needs separation from the switch node.

**`FB_5V_SBY`:** 8.153 mm F.Cu correctly joins U7 pin 4, R3 pad 2, and R4 pad 1. Keep it. Once a local `5V_SBY` pour exists, Kelvin R3 pad 1 from the local COUT (§7.4.1 #6), not from a long plane neck. This path sits south of U7, away from the north SW bus — acceptable after the SW wrap is shortened.

**`FB_3V3_SB`:** after fixing the R2 short, the divider is on the VIN/FB (south) side of U6, away from the B.Cu SW hop. Length of the VFB node is larger than “as small as possible” but can stay once it only touches R1 pad 2 and R2 pad 1. Kelvin R1 pad 1 from a *local* COUT, which does not yet exist.

**`VIN_F`:** two existing 0.60 mm F.Cu segments (F1/D3/R100 neighborhood) were not part of this buck rewrite and were not re-reviewed here.

## What must change before this copper can be accepted

Routing-only fixes (do these even if Aidan later approves a move; they are not sufficient by themselves):

1. Re-land C9 so `SW_5V_SBY` meets pad 2 and `BST_5V_SBY` meets pad 1. Then move C9 next to U7 pins 6 and 2 so the BST loop is a few millimetres, not 10.7 mm.
2. Move the `FB_3V3_SB` west end from R2 pad 2 (GND) to R2 pad 1 (FB) at (180.645, 137.095).
3. Delete the U6 `SW_3V3_SB` B.Cu hop and both vias at (180.600, 134.000) and (185.500, 132.200). Do not replace them with another L6 (or In2/In3) hop.
4. Tie C5's SW pad to a short local stub at U6 pin 2, not to the inductor-side via.
5. Keep `EN_5V` out of the y ≈ 128.2 alley between the two converters.

Placement decisions for **Aidan** (required to satisfy “SW as physically short as practical”):

1. **Rotate U6 and U7 180°** at the same centers, *or* move L1/L2 to the SW (left) side of each IC. Rotation is the smaller change: SW pad-to-inductor pad drops from a 5.14 mm wrap-around to about 2.86 mm straight on F.Cu. Target SW length **< ~3 mm**, width 0.60 mm or wider, no vias. Figure 7-18 is this orientation.
2. **Add or move a ≥ 10–22 µF ceramic COUT next to L1** (and preferably slide C10/C11 next to L2's VOUT pad). C6/C7 44–50 mm away do not count as the converter's output capacitors.
3. Confirm the `3V3_SB` / `5V_SBY` budget is ≤ ~1.5–2 A (inductor and 0.60 mm limited). If either rail can see more than that, the inductor and the SW/VOUT width have to be upsized — that is schematic/BOM, not another route.

If rotation or inductor relocation is refused, the shortest remaining same-layer north wrap (~8.5 mm, no vias, BST cap at the VBST/SW corner) is still against §7.4.1 item 4. SI would still **REJECT** any via hop or 11 mm class SW on these parts.

Do not close `SW_3V3_SB` / `SW_5V_SBY` again by forcing a path through a blocked channel. The three switch nodes needed a coordinated rewrite; this one closed the airwires by violating the datasheet and by landing on the wrong pads.

## Gen5 / other invariants

No Gen5 lane copper was added. The original three dangling Gen5 vias are unchanged. There are still zero tracks on In2 and In3. C76 and the `SW_3V3_RDRV` net were not touched. Those invariants hold, and they do not make the buck rewrite acceptable.

## Note for Base Board → Master Bot

**REJECT** the U6/U7 coordinated buck rewrite on live SHA `62392c3c…` (claimed SHA `0e1f4d60…` and the 23:00 snapshot / report were not on disk). Claimed SW lengths (U7→L2 11.36 mm, U6→L1 11.26 mm, C5→L1 5.30 mm) and 0.60 mm widths match; claimed BST/EN L6 vias do not (zero vias on those nets). Two new landings are DC shorts: U7 C9 has `SW_5V_SBY` on the BST pad and `BST_5V_SBY` on the SW pad; U6 `FB_3V3_SB` ends on R2 pad 2 (GND) instead of pad 1. Even after those are swapped, 11+ mm SW runs and U6's two-via B.Cu hop across `L6_GND_BRK` beside the device violate TI SLVSD90B §7.4.1 (SW short and wide; no switching current under the device) and §7.2.2.5 (bootstrap cap between VBST and SW). Gen5 is untouched (0 lane tracks, original 3 vias). Required Aidan placement decision: rotate U6/U7 180° or move L1/L2 to the SW side so SW can be a short F.Cu run (~3 mm), and place a local ≥10–22 µF COUT next to L1. No further SW detours. Nothing edited or pushed.
