# MacPro6,2 inter-board link and bandwidth map (AM5), rev 7b
Base Board & Connectors, 2026-10-26 ≈18:00 EDT (rev 4 ≈17:50, rev 3 ≈17:40, rev 2 ≈17:30). Draft, nothing approved. No other files edited, nothing pushed.
Inputs: research/connector-bandwidth-options.md (M&T), docs/pinmaps/base-iob-megarray-review.md, docs/am5-cpu-board-frozen-config.md, macpro62-interface-control-rev4.md, boards/base-v3/kicad/docs/loss_budget_A1.md, plus public vendor pages below.
Tags: [Sourced] = public page (URL in Sources); [Estimate]; [GAP].


## Rev 7: Gen5 public TI redrivers placed on the base board (Aidan decision via Master Bot, 2026-10-28; placed ≈15:10 EDT)
Base Board & Connectors. Board A only (Board B on hold). Draft, nothing pushed, ordered, or sent to vendors. Backups: /workspace/backups/bp-v3-redrivers-20261028/.
- **Parts (public datasheets):**
  - **U20 DS320PR1601** (GPU x16, J1 ↔ GPU face): ZDG0354A nFBGA-354, 22.8 × 8.9 mm, 1.4 mm max, ball Ø0.37, NSMD land Ø0.30 (TI SNLS683, Jun 2023: pin table pp.6–14, P_ACT 5.8 W typ / 7.0 W max at EQ 5–19 and θJA 17.4 / θJC(top) 6.5 °C/W p.16, power/decoupling/layout p.34, outline p.40, land pattern p.41, stencil p.42). AC caps internal, no refclk/sideband. SMBus/I²C only: MODE = L2 target via 6.2 k (6.225 k ±10 %, Tbl 5-1).
  - **U21/U22 DS320PR810** (SSD board x8 = 2 × x4, FS lanes 0–3 / 4–7): NJX0064A WQFN-64, 5.5 × 10 mm, 0.4 mm pitch, EP 4.1 × 8.6 (TI SNLS668, Aug 2022: pins pp.4–6, P_ACT 1.41 typ / 1.75 W max p.8, 5-level straps Tbl 7-4 and addresses Tbl 7-5 p.17, decoupling p.28, outline p.34, land p.35). MODE = L2 (24.9 k); U21 ADDR1/0 = L0/L0 → 0x18/0x19, U22 L0/L1 → 0x1A/0x1B. RSVD2–5 → GND per p.6.
  - **U23 PT5161L fallback: separate alternate footprint, DNP, no pads.** Package and pinout are NDA-gated; TI publishes no cross-map, so pin compatibility with DS320PR1601 is **unverified and not assumed**.
- **Decoupling (per datasheet), on B.Cu directly under each IC:** U20 16 × 100 nF + 4 × 1 µF + 2 × 10 µF (30 VCC balls); U21/U22 4 × 100 nF + 1 × 1 µF each, plus one shared 10 µF for the bus.
- **Placement (board coords, mm; board centre (150,100), r 61):** U20 (182.2, 102.9) rot 0, the free band between J1 and the J9 Face-P connector, toward the outer edge. U21 (153.5, 102.9) and U22 (160.5, 102.9), rot 0. U23 ALT is a reservation at U20's site. Heatsink keep-out is drawn on Dwgs.User at 24 × 10.6 mm. The band is only 11.6 mm wide (J9 courtyard y 97.1 to J1 y 108.8), and H2 (199,100) and U3 bound it.
- **Per-segment Manhattan estimate, connector pad → redriver centre → face pad** (full table: boards/base-v3/kicad/docs/gen5_redriver_segment_lengths_2026-10-28.csv; J9 MCIO = proxy for the not-yet-placed GPU MEG-Array):

| Link | Redriver | J1 → redriver (mm) | redriver → face (mm) | Pairs over 40 mm |
|---|---|---|---|---|
| GPU x16 (FP lanes 0–15, TX+RX) | U20 | 8.8–36.9 | 17.1–68.1 | 16 (lanes 0–7, face side 40.3–68.1) |
| SSD x4 #1 (FS 0–3) | U21 | 15.0–23.0 | 32.9–37.1 | 0 |
| SSD x4 #2 (FS 4–7, slot-B pins) | U22 | 16.2–53.8 | 39.9–44.1 | 6 (FS4–6 both sides up to 53.8; FS7 RX B 44.1) |

- **Flags:** 22 of 48 pairs exceed the ~40 mm/side budget on the Manhattan estimate. Octilinear routing is shorter (×≈0.8–0.85), but GPU lanes 0–7 face-side still land at about 34–58 mm. A final answer needs the real MEG-Array position (Aidan's stock-base measurements). The fixes would be to move J1 lanes 0–7 or the face connector, or to swap U20's site.
- **Open issues:**
  1. **3V3_RDRV is a NEW rail with its source TBD.** Max load ≈ 7.0 + 2 × 1.75 = 10.5 W (3.2 A). The existing 3V3_SB TPS563201 (3 A, standby) is not suitable. Needs Aidan's decision (../power/docs).
  2. **U20 ball coordinates aren't transcribed.** The staggered grid on SNLS683 p.41 is ambiguous from text, so the footprint is an outline placeholder until TI CAD or a full transcription is available.
  3. **The high-speed nets are not yet spliced.** The *_A/*_B labels are placed, but the J1→J9/J10 copper is still direct, so a net split plus reroute is needed.
  4. **U20 straps (8 address pins) are TBD** (SNLS683 Tbl 7-3/8-1), and I²C address collisions haven't been checked yet.
  5. **Heatsink:** at 7 W with θJC 6.5 °C/W and Tj ≤ 120 °C, a 24 × 10.6 mm footprint sink needs θSA ≲ 4–5 °C/W. That is unlikely without height or ducting, so it goes to M&T.
  6. **B-side passives make assembly double-sided** (it was F-only).
  7. **DRC is no longer clean after placement** (see the BP README note). That's expected until the reroute.
  8. **SSD-side PT5081L/PT5161L fallback: none placed** (the brief covered the GPU only).

### Rev 7a (2026-10-28 ≈16:00 EDT, SI & Fab review): moves, angled lengths, real ZDG0354A ball map
Backup: /workspace/backups/bp-v3-rdrv-move-20261028/. The nets are not split and nothing is rerouted (waiting on Aidan for the 3V3_RDRV source).
- **New placement (mm, rot 0, F.Cu):**
  - U20 DS320PR1601 moves 182.2 → **173.7**, y 102.9 (8.5 mm toward J9). U23 ALT moves with it.
  - U22 moves 160.5 → **152.5** (8 mm toward J10). U21 moves 153.5 → **158.6**. The B.Cu passives move with their ICs.
  - **Blockers:** the band is y 97.1–108.8 (J9/J1). An 810 can't go left of x = 152.5 because of J10's courtyard. Both 810s have to sit left of U20, since no other free site exists toward J10 (a polygon search of the whole board found none). That caps U20's left edge at about 161.7. Placing U20 at x ≤ 170 (all face-side pairs ≤ 45) forces an 810 to the right of U20 (x ≈ 184), which puts SSD lanes 0–3 at 60–67 mm. Rejected.
- **Angled (octilinear) estimates, max(dx,dy) + 0.414·min(dx,dy), pad → IC centre** (CSV updated):

| Redriver | CPU side (J1) | Face side | Over 45 mm |
|---|---|---|---|
| U20 GPU x16 | 8.3–21.9 | 10.1–46.4 | FP_RX0, FP_TX0 (46.4, face side) |
| U21 SSD FS0–3 | 15.3–21.6 | 34.5–41.1 | none |
| U22 SSD FS4–7 | 8.3–40.8 | 23.9–30.6 | none |

- **ZDG0354A:** all 354 balls come from the vector drawing on SNLS683 p.41: 354 Ø0.30 land circles, labels matched one-to-one and cross-checked against the pin table, pp.6–14. The check gives 35 distinct X and 129 distinct Y positions, monotonic in column number. Nearest-neighbour pitch is 0.6 (206 balls), 0.5, 0.75, 0.8 and 0.7, matching the drawing's 0.6/0.5/0.8 TYP. Spans are 7.88 × 21.94 (drawing: 7.88 / 21.9). The footprint is now TI_ZDG0354A_nFBGA-354_22.9x8.9mm (placeholder removed).
- **Routing layers (stackup JLC06161H-2116, 1.6 mm):** host RX on L1_SIG_RX (F.Cu microstrip referenced to In1 GND, w 0.26 / gap 0.125, 85.5 Ω). Host TX on L3_SIG_TX_PWR (In2 stripline between In1 and In3, w 0.24 / gap 0.127, 84.5–85.7 Ω; legacy TX pairs at 0.21/0.127 come to 88.7–89.7 Ω). L4_SIG_SLOTB (In3) is the second inner signal layer. No GND plane separates In2 and In3, so the broadside rule applies. Through vias are 0.45/0.25 with no backdrill. Approximate stubs: from In2 about 1.0 mm, from In3 about 0.6 mm (SI to rule on backdrill or layer choice).

### Rev 7b (2026-10-28 ≈18:30 EDT): SSD face pinout, real face connectors, 12 V buck (Aidan: 12 V-only PSU, base fed only via J1)
Backup: /workspace/backups/bp-v3-faces-20261028/. Nets still not split, nothing rerouted or pushed.
- **SSD face MEG-Array 300 pinout:** docs/pinmaps/base-ssd-megarray.csv (10 × 30, GSSG: pairs at columns 3k+1/3k+2, GND at 3k; full GND rows B/D/F/H/I fence the pair rows). Also has base_end and base_net columns.
  - Row C: 8 TX pairs (2 × x4) + 2 REFCLK.
  - Row E: 8 RX pairs + 2 spare pair slots (board B).
  - Row G: 10 spare pair slots (board B).
  - Row A: PERST#/CLKREQ#/PEWAKE# × 2 + SMB CLK/DAT, alternating with GND.
  - Row J: **12 × P12V** (J1–J12) + **12 × GND return** (J13–J24) + optional P3V3_SB (J25, via R121 0 Ω DNP).
  - **Counts: 18 pairs = 36 pins, 9 single-ended (8 sideband + 1 optional 3V3), 12 × 12 V, 210 GND (incl. 12 returns), 33 spare = 300.**
  - **12 V power is APPROVED** (Aidan): 2.5 A / 12 = 0.21 A/pin vs 0.45 A rating, 2.1× margin.
  - The pinout is our own and only mirrors the stock GPU-face position, not Apple's pin map.
- **Face connectors placed** (per docs/stock-base-connector-positions.md; KiCad y = 100 − Y_stock):
  - **J11 GPU** at (115.0, 66.0), rotation +45°. GPU pinout is pending GPU Board, so all its pads are currently no-connect.
  - **J12 SSD** at (185.0, 66.0), rotation −45°. Nets come from the CSV.
  - Both use the footprint Amphenol_MegArray_84501_300P_10x30_P1.27mm_UNVERIFIED (1.27 mm grid, Ø0.64 pads and A1/key location are not in a public dimensioned land pattern; housing 44.1 × 17.34 from mezz_megarray.pdf).
  - J9/J10 MCIO stand-ins are removed from the PCB and set off-board/DNP in the schematic. MCIO_RIBBON rule areas are deleted.
  - **Fit:** outer pads reach r 57.8 mm, inside the 58 mm ring keep-out. The housing corners reach r ≈ 61.6 mm, past the 61 mm board edge, within the scan's ±2 mm accuracy, so the position needs a calliper check.
- **Lengths (octilinear, pad → redriver centre; GPU face = J11 centre until its pinout exists):**

| Redriver | J1 side | Face side | Over 45 mm |
|---|---|---|---|
| U20 → J11 (GPU, left) | 8.3–21.9 | 74.0 | all 32 pairs |
| U21 → J12 (SSD 0–3) | 15.3–21.6 | 51.4–58.6 | all 8 |
| U22 → J12 (SSD 4–7) | 8.3–40.8 | 50.3–54.9 | all 8 |

  **Root cause:** J1 puts the GPU lanes on its +x (right) half and the SSD lanes on the −x half, so the GPU face on the left forces the two groups to cross. The fix is either swap faces (GPU right / SSD left, which the positions doc marks provisional) or remap J1 (CPU Board). Swapping with the redrivers left as they are gives U20 face-side ≈ 41.6 mm (centre estimate), with the SSD redrivers then moved left toward the SSD face. The redrivers would need re-placing either way (Aidan to pick left/right).
- **12 V → 3V3_RDRV buck:**
  - Part: **U24 TI TPS565208DDCR** (SLVSE72B: 4.5–17 V in, 5 A, SOT-23-6 DDC, VFB 0.76 V, pins GND1/SW2/VIN3/VFB4/EN5/VBST6 p.4). The 5 A rating is ≥ 4 A and gives 1.56× over 3.2 A.
  - Values per Tbl 2 p.14 (3.3 V): R118 33.2 k / R119 10 k, L 2.2 µH, Cout 3 × 22 µF (in the 20–68 µF range). Cin 2 × 10 µF 25 V + 100 nF. VBST 100 nF. EN 100 k pull-up to 12 V (always on).
  - Placed at (118, 96), about 56 mm from U20. The L5 part is TBD: it needs ≥ 7 A Isat, and the 4 × 4 footprint is a placeholder.
- **J1 12 V: there are 0 pins today.** J1 carries only 5V_SBY × 6 and 3V3_SB × 2; 12V_MAIN_IN still enters on J2 (Micro-Fit), which Aidan's decision makes obsolete. **Base 12 V load:** SSD 2.5 A + buck input ≈ 10.5 W / (12 V × 0.88) ≈ 1.0 A + MCU/sensors ≈ 0.1 A, about **3.6 A**. Fan power [GAP] is not included, and GPU power is not counted (it must not come through J1). At 1.1 A/contact (Mini Cool Edge, frozen-config doc) with 2× margin, that needs **≥ 7 × 12 V + 7 GND on J1** (8 + 8 if fans draw 12 V from the base). It's a CPU Board pinout change. The base's own U6/U7 standby bucks fed by 11V_SB_IN on J2 also become redundant or need a new source.
- **Base 12 V eFuse at J1 (Aidan: base 12 V is taken ahead of the CB eFuse):**
  - Part: **U25 TI TPS259824LNRGE** (SLVSEI3D, rev May 2026): 2.7–24 V, 15 A, 2.7 mΩ, RGE VQFN-24 4 × 4 with 2 exposed pads. 16.9 V OVLO, active current limit (Device Comparison Table p.4). Pins p.5. ILIM points p.9 (300 Ω → 4.98 A, 182 Ω → 8.13 A). Outline p.55, land pattern p.56.
  - Values: **R122 249 Ω → ILIM ≈ 6.0 A typ** (interpolated; verify against the ILIM equation). EN/UVLO 100 k/13 k ≈ 10.4 V (verify V_EN, p.8). dVdt 22 nF (TBD). IMON 1.5 k → BP_12V_IMON. PG → BP_12V_PG (10 k to 3V3_SB). RETRY_DLY/NRETRY/LDSTRT to GND. Cin 1 µF, Cout 10 µF.
  - Placed at (111, 104) next to the J1 left end. EFUSE_IN = J1 v4 P12V (A103–B106, ×8 at 0.75 A derated = 6 A). Output feeds 12V_MAIN_IN.
  - **The J1 symbol and footprint nets are still v3.** Applying the v4 draft remaps sideband/FS pins too, so it waits for the v4 freeze (CPU Board).
- **Base 12 V budget (from J1):** SSD face 2.5 A (I/O & Storage figure) + U24 input 10.5 W / (12 V × 0.88 est.; SLVSE72B Fig 12 not read numerically) = 0.99 A + eFuse/buck quiescent < 0.01 A → **≈ 3.5 A, within the 6 A J1 allocation and the 6.0 A ILIM**. Not included: fan power [GAP]. GPU power must not come via J1.
- **Base standby (v4: CB → base):**
  - **5V_SBY: ≈ 0 A of base load.** Its only base consumer was the U7 buck output. **U7 (and U6 for 3V3_SB) now back-feed CB-supplied rails and must be DNP/removed**, along with J2 / 11V_SB_IN.
  - **3V3_SB: ≈ 0.07 A base-own worst case** (estimate: RP2350B MCU ~30–40 mA, W25Q128 ~15 mA active, INA226/TMP1075 ×2/LVC1G74 < 1 mA, LED D10 ~2 mA, 2.2 k I²C pull-ups ≤ 6 mA, 10 k pull-ups ≤ 8 mA; RP2350/W25Q datasheets not re-opened this turn) **+ IOB 3V3_SB via J6 [GAP] + optional SSD 3V3_SB (J12 J25, R121 DNP, ≤ 0.45 A)**. J1 v4 3V3_SB = 2 pins × 1.1 A.

## Rev 6: reuse of Apple Mac Pro 6,1 interconnects (Aidan goal, 2026-10-26 ≈17:45 EDT)
**GPU pair count (corrected, GPU Board):** 32 PCIe + 1 REFCLK + 16 display + 4 AUX = **53 pairs** → 106 S + 106 GND (2/pair, GSSG) + 16 SE = **228 of 300 → 72 spare**. Fits MEG-Array 300.

### Stock connectors found (public sources)
| Link | Apple part | Connector | Positions / grid | Stack | Amphenol PN | Public pinout |
|---|---|---|---|---|---|---|
| GPU board ↔ interconnect board | Graphics board flex **821-1880 / 923-0500** | FCI (Amphenol) **MEG-Array** mezzanine at both flex ends (iFixit step 11; Apple service manual: "mezzanine connectors", flex) | **10 × 30 = 300** (ground map rows 1–10 × cols A0–C9: **95 GND / 205 signal**) [MacRumors #25986811, dwdrummer959; see docs/stock-pinouts-macrumors.md] → same size as **84500/84501** | **[GAP]** (measure on Aidan's boards) | **[GAP]** (markings not public) | **Ground positions only**; no signal names, lanes or rails |
| CPU riser ↔ logic board | CPU riser card | **Edge connector** into a logic-board slot (Apple service manual "CPU Check") | [GAP] | card edge | [GAP] | none (CodeJingle: ~20 PCIe pairs, mapped "by look") |
| Interconnect board ↔ logic board | PCIe interposer **923-0496** | high-density slot, lifted "straight up" (iFixit interconnect guide; TekDep) | [GAP] | [GAP] | [GAP] | none |
| I/O board ↔ interconnect | I/O board flex **923-0501** | mezzanine (MEG-Array-type) both ends (service manual) | [GAP] | [GAP] | [GAP] | none |
| I/O wall flex | 821-2222 | 14P 0.5 mm FPC | 14 | – | – | partial (pins 3+6 = power button) |
| GPU boards | 820-3532 (D700) / 820-3533 (D500) / 820-3627 (D300) | – | – | – | – | no schematic/boardview public (docs/gpu-board-prior-art.md §3.1) |

### Compatibility assessment
**(a) Mechanical only (Apple footprint + stack, our pinout): feasible, recommended.** Our MEG-Array 300 (10×30) is the same size as Apple's GPU connector. Match Apple's stack height once measured (4 mm parts 84500/84501 if it matches; 5.5/8 mm variants exist). Free choice of pinout lets us place the 53 pairs in GSSG rows. Conflicts: (1) if the **stock flex 923-0500** is reused, that is a cable (conflicts "no cables") and a 2013-era PCIe 3.0 flex with unknown loss at 16 GHz; it would almost certainly fail Gen5 and UHBR20 → usable only as a PCIe 3/4 bring-up aid; (2) Apple's fixed 95-GND pattern gives ~1.8 GND/pair for 53 pairs, but the positions are Apple's, not GSSG-adjacent → don't inherit it.
**(b) Electrical (Apple pinout, stock FirePro D-series at PCIe 3.0): not recommended.** Pinout isn't public (ground map only) → needs reverse engineering on Aidan's boards; stock GPUs are GCN1 (no macOS driver after Monterey, out of scope per prior art); their display goes to Thunderbolt 2 controllers on the stock I/O path, which our AM5 IOB doesn't have; power/SMC sideband via interlock relays (CodeJingle warning). Pin-sharing Apple's map with Gen5 + UHBR20 forces Apple's ground layout onto 32 GT/s pairs → conflicts with GSSG. A stock **I/O board** (TB2/Falcon Ridge, PCIe 2.0) is likewise incompatible with the AM5 lane plan.
**Recommendation (decision for Aidan):** (a) — reuse Apple's mechanical arrangement and the 300-pos MEG-Array size/stack, with our own Gen5 GSSG pinout, board-to-board, no stock flex in the shipping design. Keep (b) out of scope.
Gaps: Apple MEG-Array stack heights and Amphenol PNs (measure/read markings), 923-0496 slot type and count, 923-0501 position count, any signal pinout.

## Decisions recorded (Aidan, 2026-10-26 ≈17:42 EDT)
- **GPU face ↔ base: MEG-Array 300-position at 4.0 mm (plug 84500 / receptacle 84501), parallel mezzanine.** (Supersedes the rev 5 400-pos suggestion; at 300 use 2 GND/pair → 228 pins, 72 spare.)
- **SI & Fab GPU-side loss: 12–23 dB** (vs 36 dB Gen5 budget). **Design for Gen5 with a firmware Gen4 fallback** (`pcie_gen_max`).
- **Display: full UHBR20**, with a **UHBR20 retimer near the ports on the I/O board**.

### DP 2.1 UHBR20 retimer / redriver candidates (IOB, near ports) [Sourced, public pages]
| Part | Type | Key data | Link |
|---|---|---|---|
| Parade **PS8483** | DP 2.1 **retimer** (LTTPR, jitter cleaning), dual mode | RBR…UHBR20, up to 80 Gb/s, adaptive CTLE+DFE, also FRL to 12 Gb/s; 3.3 V + 0.9 V; 4.4×9.7 mm QFN-66 | https://www.paradetech.com/products/ps8483-20gbps-displayport-dual-mode-retimer/ |
| TI **TDP2004** | 4-ch **linear redriver** (not a retimer) | DP 2.1 to 20 Gb/s + HDMI 2.1 source 12 Gb/s; 19 dB EQ; 160 mW/ch; 4×6 mm WQFN-40 | https://www.ti.com/lit/ds/symlink/tdp2004.pdf |
| Diodes **PI2DPX2063A / PI2DPX2023A** | 4-to-4 linear redriver | UHBR20, AUX listener, 1.8 V, 2.85×4.5 mm LGA | https://www.diodes.com/assets/Product-showcases/1.8V-20Gbps-DP-2.1-UHBR20-Linear-ReDriver-with-AUX-Listener-for-High-Resolution-Video-Connectivity.pdf |
| Analogix / Kandou UHBR20 retimers | – | **[GAP]** not found in public datasheets this run | – |
Recommend PS8483 (true retimer; also covers FRL). Redrivers are fallbacks if loss is small enough.

### HDMI 2.1 FRL retimer (replaces TDP158)
| Part | Type | Key data | Link |
|---|---|---|---|
| Parade **PS8419** | HDMI 2.1 **retimer**, jitter cleaning | FRL to 12 Gb/s, TMDS 6 Gb/s, auto FRL link training, DDC/SCDC interception, crystal-free; 3.3 V + 1.1 V; 4.5×6.5 mm QFN-46 | https://www.paradetech.com/products/ps8419/ |
| Parade PS8483 (dual mode) | DP retimer with FRL 12G | one part for DP++/HDMI port | above |
| TI TDP2004 | linear redriver, HDMI 2.1 source 12G | not a retimer | above |

## Changes in rev 5 (Aidan, 2026-10-26)
1. Aidan pointed to Amphenol MEG-Array (https://www.amphenol-cs.com/product-series/meg-array.html) as Apple's 6,1 connector → **MEG-Array, parallel mezzanine, is now the leading GPU-face candidate** (§3e). Rev 4's APF6-RA pick becomes fallback F2.
2. Recommended size: **400 positions (10×40), plug 84740 + receptacle 74221 at 4.0 mm**; 300 (84500/84501) is the minimum.
3. Gen5 sits at the 32 Gb/s rating (0 % headroom); insertion loss is fine with the base retimer, crosstalk/return loss is the risk → SI sim gate, with Gen4 and UHBR13.5 caps as pre-agreed fallbacks (decisions for Aidan).

## Changes in rev 4 (Aidan, 2026-10-26)
1. **Edge connectors only on the CPU board.** Mini Cool Edge 168 (rev 3 J2 pick) and **MCE-280 (PCIe + display) are REJECTED** for the GPU face. HSEC8 also out (edge card).
2. **No cables.** J9 MCIO (GPU PCIe) and J2 are replaced by **one two-part board-to-board connector, GPU face → base**, carrying Gen5 x16 + 4 display streams + sideband (§3c).
3. **GPU now RTX 5070-class** (likely): Gen5 x16 32 GT/s NRZ; 4 streams, possibly DP 2.1 UHBR20 (20 Gb/s/lane) and HDMI 2.1 FRL 12G. Navi23 numbers in rev 3 superseded.
4. **Recommendation (decision for Aidan): Samtec AcceleRate HP, APF6-RA right-angle socket on the GPU face + APM6 vertical terminal on the base, 4 rows × 70–80 (280–320 pos).** Runner-up: Amphenol ExaMAX2 backplane-style (RA receptacle on face, vertical header on base).
5. MEG-Array to the IOB at UHBR20: connector margin only ~1.4–1.6×; needs SI sim and likely a DP 2.1 retimer on the base or a UHBR rate cap (§3d).
6. Apple Mac Pro 6,1 reference arrangement added (§3c).

## Changes in rev 3 (Aidan, 2026-10-26)
1. **J2 (GPU display → base) is no longer MCIO** (not enough pins). New J2 candidates compared in §3b; recommendation = Amphenol Mini Cool Edge 0.60 mm, 168 positions, same family and orientation as J1 (**decision for Aidan**).
2. Display defined as **Navi23, 4 streams max**: 4× DP HBR3, or 3× DP + 1× HDMI. No UHBR. HDMI 2.1 FRL only if a FRL-capable retimer replaces the TDP158 [part GAP].
3. MEG-Array to the IOB re-checked for 4 streams (§3): **still needs 300 positions**; 200 fails at ≥1.5 GND/pair.

## Changes in rev 2 (Aidan decisions 2026-10-26)
1. **All inter-board signals via the base board; no side flex/cable paths.** GPU display (4× DP + HDMI) and ASM4242 DP-in now go GPU board → base → MEG-Array → IOB. **J2 DISPLAY-LINK re-targets to the base board** (was Face P → IOB, ICD I-3). MEG-Array must grow to **300 positions**.
2. **USB from the CPU's integrated controller**: AM5 CPU = **4× USB 3.2 Gen2 10G + 1× USB 2.0** [Sourced: AMD Ryzen 9 9950X spec page; same AM5 I/O die on Ryzen 7000/9000 – confirm the chosen SKU page]. USB-A moves off PROM21.
3. **Hubs and PCIe switches allowed.** VL822 hub for USB-A; Gen5 switch for SSD version B; placements chosen to cut J3/MEG-Array pins.
4. Supersedes rev 1 link rows L6–L8 and the oversubscription table.

## 0. Rate basis
Gen5 3.94 GB/s/lane each way (≈3.4 usable); Gen4 1.97 (≈1.7); USB 10G ≈1.21 GB/s line (~1.0 real); DP HBR3 x4 = 25.9 Gb/s payload; HDMI 2.1 FRL 4×12 Gb/s. ASM4242 PCIe tunnel capped by its Gen4 x4 uplink [Sourced ASMedia].

## 1. USB port sourcing (baseline: 6× USB-C, 4× USB-A)
| Port | Data source | SS lanes | USB2 leg | Path |
|---|---|---|---|---|
| USB-C 1–2 (USB4 40G) | ASM4242 (Gen4 x4 from PROM21) + DP-in from GPU | USB4 PHY local to IOB | ASM4242 [GAP: integrated USB2 vs external] | ASM uplink J3 → base → MEG; DP-in GPU → J2 → base → MEG |
| USB-C 3–4 (DP-Alt) | **CPU USB 10G #1, #2**; DP from GPU into IOB DP-Alt muxes | 2 pairs each | PROM21 USB2 | J3 → base → MEG |
| USB-C 5 (USB 3.2) | **CPU USB 10G #3** | 2 pairs | CPU USB2 #1 | J3 → base → MEG |
| USB-C 6 (USB 3.2) | PROM21 USB 10G #1 (CPU has only 4 ports) | 2 pairs | PROM21 USB2 | J3 → base → MEG |
| USB-A 1–4 | **CPU USB 10G #4 → VL822 hub on the IOB**, 4× 10G downstream | 2 pairs upstream | VL822 built-in USB2 hub (upstream USB2 from PROM21) | J3 → base → MEG → hub at the ports |
Result: PROM21 USB load drops to one 10G port + USB2. USB-A 4 ports share 10 Gb/s (VL822 uplink).

## 2. Link table (source → destination)
| # | Link | Protocol / gen | Lanes | Raw each way | Effective | Connector / pins | Rating → headroom | Retimer / redriver | Owner bot |
|---|---|---|---|---|---|---|---|---|---|
| L1 | CPU → base (GPU) | PCIe 5.0 | x16 | 64 GB/s | ~54–63 | J1 Mini Cool Edge 224: 64 pins + REFCLK + sideband | MCE 32G NRZ / 64G PAM4 [Sourced]: Gen5 at NRZ rating | see L4 | CPU Board / Base Board |
| L2 | CPU → base (SSD A + B) | PCIe 5.0 | 2× x4 (NVMe root + GPP root) | 2×15.75 | ~27–31.5 | J1: 32 pins + 2 REFCLK | as L1. J1 total ≈134–138 used of 224, 86–90 GND (Option C) | see L5 | CPU Board / Base Board |
| L4 | Base → GPU board, rev 4 | PCIe 5.0 | x16 + REFCLK = 33 pairs | 64 GB/s | ~54–63 | **APF6-RA (face) ↔ APM6 vertical (base)**, shared with display; J9 MCIO cable deleted (no cables) | 56G NRZ / 112G PAM4 → 1.75× Gen5 | **Retimer still expected** on the base (loss budget 18–35 dB vs 36 dB, minus the cable segment ~0.6–1.2 dB) [GAP S-params] | Base Board / GPU Board |
| L5 | Base → SSD board | PCIe 5.0 | 2× x4 (ver. A); ver. B: switch, see §5 | 2×15.75 | ~27–31.5 | BP J10 MCIO 124 (~82 pins, ~34 % spare); x16 downstream if the switch sits on the base | at rating | Likely needed (ver. A). Ver. B with switch on base: switch re-times, no separate retimer | Base Board / I/O & Storage |
| L6 | CPU → base (USB/PROM21 domain) | Gen4 x4 (ASM4242), Gen3 x1 ×2 (i226), CPU USB 10G ×4, PROM21 USB 10G ×1, USB2 | 22 HS pairs + USB2 | ~14.3 GB/s | ~12.5 | **J3 MCIO 124** (CB → base, Option C) | 2× rate margin | None at Gen4 (9.5–16.8 vs 28 dB) | CPU Board / Base Board |
| L8 | **GPU → base (display)**, rev 4 | DP 2.1 up to UHBR20 (20 Gb/s/lane) ×4 streams, or 3 DP + HDMI FRL 12G | 16 main + 4 AUX pairs + HPD/DDC/CEC/config | 4×4×20 = 320 Gb/s raw ≈ 38.7 GB/s (128b/132b) one way | – | **Same B2B as L4: APF6-RA / APM6 (recommended, §3c)** | 56G NRZ: UHBR20 2.8×, FRL 4.7× | UHBR20 across 2 connectors + base: retimer likely [GAP, SI sim]; HDMI FRL retimer [GAP part] | GPU Board / Base Board |
| L7 | **Base → IOB** | L6 set + L8 display (4 streams) | 50 pairs incl. 3 REFCLK + ~37 SE | ~27 GB/s | – | **MEG-Array 300-pos 4 mm (84500/84501)** | 28–32 Gb/s [Sourced]: Gen4 ~1.75–2×, USB 10G ~3×, HBR3 ~3.5×, FRL ~2.3×; 0.45 A/contact → no power | None at these rates [Estimate; GAP Amphenol S-params] | I/O & Storage / Base Board / SI & Fab |
| P1 | PSU → boards, 12 V | power | – | 450–520 W, ~50 A (CPU ≤17.9 A) | – | Bus bars / lugs (I-9), IOB stock 12P (I-7). Never MCIO (0.5 A) or MEG (0.45 A) | – | – | Power Supply / M&T |

## 3. MEG-Array to the IOB, re-check with 4 display streams
| Group | Pairs |
|---|---|
| ASM4242 Gen4 x4 | 8 |
| i226 ×2 | 4 |
| USB 10G SS (CPU #1–4, PROM21 #1) | 10 |
| USB2 | 5 |
| REFCLK | 3 |
| Display: 4 streams × 4 main | 16 |
| Display AUX ×4 | 4 |
| **Total** | **50 pairs = 100 pins** (rev 2 counted 5 streams = 54) |
Single-ended ≈ 37: rev 2 base set ~24 + HPD ×4, DDC ×2, CEC, config/CAD ×4, retimer I²C ×2.
| GND ratio | Total pins | 200-pos | 300-pos (84500/84501) |
|---|---|---|---|
| 1.0/pair | 187 | fits, 13 spare, rejected pattern | – |
| 1.5/pair | **212** | **fails** | 88 spare |
| 2.0/pair | **237** | **fails** | 63 spare |
Verdict: **300-position MEG-Array at 4 mm still required.** Routing: two of the four streams go to the ASM4242 DP-in, two to the DP-Alt muxes (or one to HDMI).

## 3b. J2 replacement (GPU face → base), Navi23 4 streams
Requirement: 20 pairs (40 pins) + ~14 SE (HPD ×4, DDC SCL/SDA, CEC, config/CAD ×4, retimer I²C ×2, retimer EN) = 54 signal; + GND 1.5–2/pair = 30–40 → **84–94**; +20 % spare → **~101–113**; growth room (5th stream or a later UHBR GPU, ~+20) → **target ≈120–140 positions**.

| Option | Positions | Rating | Pitch / footprint | Height / card | Face-to-base like J1? | Fit | Source |
|---|---|---|---|---|---|---|---|
| **Amphenol Mini Cool Edge 0.60 mm, 168** (140 alt.) | 168 (140) | 32G NRZ / 64G PAM4 (Gen6) | 0.60 mm, 2 rows; length ≈63 mm (140 ≈55 mm) [Estimate from 224 = 79.89 mm card] | 1.6 mm card; vertical or RA receptacle | **Yes: same family, same card-edge into base receptacle**, same tooling and footprint rules as J1 | 168: 55–84 spare / growth; 140: 27–56 | amphenol-cs.com Mini Cool Edge page; flyer PDF; farnell 3212940 |
| Samtec **HSEC8-DV**, e.g. HSEC8-175-01-L-DV (150) | up to 200 (100/row); 150 chosen | 28 Gb/s NRZ (31 Gb/s diff de-embedded, 21 Gb/s with PCB) | 0.80 mm; length = n/row × 0.8 + 4.6 → 64.6 mm at 75/row | 7.98 mm vertical; 1.60 mm card (2.36 opt.); 2.8 A/pin | Yes, card edge | 150: 37–66 spare. HBR3 ~2.6–3.8× | samtec.com/products/hsec8-dv; HSEC8 SI report; datasheet |
| Samtec **ERM8-RA / ERF8-DV** (Edge Rate) | up to 200 | 28 Gb/s NRZ RA-to-DV; 56G PAM4 marketing | 0.80 mm, 2 rows; footprint [GAP] | 7–18 mm vertical; RA header on the face → perpendicular; 1,000 cycles, 2.2 A | Yes with RA header (not a card edge; two-part) | 140–160 fits | samtec.com/products/erf8; ERF8/ERM8 spec (digikey PDF) |
| Second **Amphenol MEG-Array** (e.g. 160/200, 4–14 mm) | 81–528 | 28–32 Gb/s | 1.27 mm BGA array | 4–14 mm, **parallel mezzanine only** | **No** (needs the face parallel to the base) | pins fit; orientation doesn't | Amphenol MEG-Array datasheet |
| Other: **one Mini Cool Edge 280** for PCIe x16 + display (replaces J9 MCIO cable and J2) | 280 | 32G NRZ / Gen6 | ~94 mm (M&T) | 1.6 mm card | Yes (as J1) | 52 pairs → 104 + 78 GND + ~30 SE ≈ 212 → 68 spare; removes a cable; Gen5 x16 retimer still on base | M&T study, Amphenol |
| SEARAY 0.8 | 40–500 | 28G NRZ | 0.80 mm array | 7/10 mm mezzanine | No (parallel) | – | samtec.com/products/seaf8 |

**Recommendation (decision for Aidan):** **Mini Cool Edge 0.60 mm, 168 positions** for J2: same family and card-edge orientation as J1, highest rating (Gen6-class), 55–84 spare pins for growth, mounts the GPU face to the base the same way the CPU board does. Runner-up: HSEC8-DV 150 (cheaper, distributor stock, 28 Gb/s still ≥2.6× HBR3). Worth considering: MCE 280 combining GPU PCIe + display, which also removes the J9 MCIO cable (fits "minimise cables").

## 3c. GPU face ↔ base board two-part connector (rev 4)
**Requirement:** 33 PCIe pairs (x16 TX/RX + REFCLK) + 16 display main + 4 AUX = **53 pairs (106 pins)**; SE ≈16 (PERST, CLKREQ, PRSNT, WAKE, SMBus ×2, HPD ×4, DDC ×2, CEC, config ×3); GSSG at 1.5–2 GND/pair = 80–106 → **202–228**; +20 % spare → **≈245–275**; growth → **target 280–320 positions**. Rate: ≥32 Gb/s NRZ with margin (UHBR20 = 20 Gb/s/lane, Gen5 = 32 GT/s). Geometry: faces sit 120° apart on the core and stand **perpendicular to the base** → RA on the face + vertical on the base is the natural mate; mezzanine/parallel needs a bracket or flex (excluded). Power stays on bus bars.

| Option | Rating | Positions | Pitch | Footprint length (for ~280–320) | Mated orientation / height | Cycles | A/pin | Perpendicular fit | Source |
|---|---|---|---|---|---|---|---|---|---|
| **Samtec AcceleRate HP APF6-RA + APM6** (recommended) | 56G NRZ / 112G PAM4, PCIe 6.0 | 4 rows × 10–100 (40–400; 800 for APM6 vertical) | 0.635 mm | ≈ 70–80 × 0.635 + ends ≈ **50–57 mm** [Estimate] | RA socket on face, vertical terminal on base; perpendicular. Vertical-to-vertical 5/10 mm also offered | **[GAP]** (Samtec E.L.P. range 250–2,500; series value not stated) | 1.2 A | **Yes** | samtec.com/products/apf6-ra ; high-density arrays page |
| Samtec AcceleRate HD ADM6/ADF6 | 64G PAM4 / 32G NRZ, PCIe 6.0 | 40–400 (4 × 10–100) | 0.635 mm | 300 pos ≈ 50 mm, 5 mm wide | **Parallel only**, 5–16 mm | [GAP] | 1.34 A | No (good for base ↔ IOB, §3d) | samtec.com/products/adm6 , /adf6 |
| Samtec NovaRay NVAM/NVAF | 112–128G PAM4, PCIe 7.0 | 8–64 pairs (2 banks × 16 pairs max per row set) | 0.80 mm | 32 pairs ≈ 37.75 × 11.40 mm (design guide); 64 pairs ≈ 2× | Parallel, 7–12 mm (RA mate listed is APF6-RA) | [GAP] | 2.1 A sig / 9.6 A GND | No; 64 pairs max is tight for 53 + SE | samtec.com/products/nvaf , /nvam ; samtec B2B design guide |
| **Amphenol ExaMAX2** (runner-up) | 112G PAM4, PCIe 6.0 (85 Ω version) | 12–96 pairs, wafers; integrated LS pins | 2.0 mm (3.0 opt.) | e.g. 6–8 pair × 8–10 columns; 4-pair × 8-col RA header = 23.9 mm (A dim) → ~30–40 mm [Estimate] | Backplane style: RA receptacle on face + vertical header on base (perpendicular); also coplanar, mezzanine | 200 | 0.5 A | **Yes** | amphenol-cs.com ExaMAX page; bpl_examax_backplane.pdf; GS-12-1096 |
| Amphenol Paladin | 112G PAM4 [not re-verified] | [GAP] | [GAP] | [GAP] | Backplane/orthogonal | [GAP] | [GAP] | Yes (backplane) | [GAP: datasheet not opened] |
| TE STRADA Whisper | up to 112G | 4/6/8/12 pair per column, up to 52 DP/in | 3.9 mm column, 2.5 mm row | 53 pairs ≈ 9 cols × 6 pr ≈ 35 mm [Estimate] | RA receptacle + vertical header (backplane), coplanar, orthogonal; press-fit | 200 | 0.25–0.8 A | Yes; press-fit needs thick boards [GAP min thickness] | TE STRADA Whisper page; DS 1654263-1; spec 108-32112 |
| Molex Mirror Mezz / Mirror Mezz Pro | 112G PAM4 | up to 270 pairs, hermaphroditic | 4.00 × 1.50 mm pair pitch | [GAP] | **Parallel only**, 5/8/11 mm | 100 | 1.0 A | No | Molex 987652-0673 |
| Molex Impel / Impel Plus | 40G / 56G NRZ | up to 80 DP/in | [GAP] | [GAP] | Backplane RA/vertical | [GAP] | [GAP] | Yes, but older; Impel 40G borderline | Molex AS-171320-992-001 |
| Samtec ERM8-RA / ERF8 | 28G NRZ (RA-to-DV) | ≤200 | 0.80 mm | [GAP] | RA + vertical | 1,000 | 2.2 A | Yes, but **<32 Gb/s → rejected** | samtec.com/products/erf8 |
| Samtec HSEC8 / MCE edge parts | 28–32G | – | – | – | edge card | – | – | **Rejected (edge only on CPU board)** | – |
| **Apple Mac Pro 6,1 reference: FCI (now Amphenol) MEG-Array** | Original PCIe 3.0 era (8 GT/s); today's MEG-Array 28–32 Gb/s | **Part number and pin count: [GAP]** | 1.27 mm BGA | [GAP] | Apple used **a flex cable with MEG-Array mezzanine ends** (GPU data "flips up"), GPU boards on the core; CPU riser is an **edge** connector into the logic board | 50–200 | 0.45 A | Needs flex (cable) → conflicts with "no cables"; at 32 Gb/s gives **0 % Gen5 headroom** | iFixit Mac Pro Late 2013 teardown step 11; iFixit interconnect-board guide; Apple service manual (mezzanine connectors, flex) |

Apple arrangement verdict: Apple's own connector family (MEG-Array) survives at 32 Gb/s, but it is mezzanine-only and Apple bridged the 90°/120° geometry with flex cables; reusing it mechanically means cables, and electrically Gen5 sits exactly at its rating. A current successor in the same "array mezzanine" style is AcceleRate HP (APM6/APF6) — and its **right-angle socket** removes the flex, which is why it's recommended.

**Recommendation (decision for Aidan): Samtec AcceleRate HP APF6-RA (GPU face) + APM6 vertical (base), ~4 × 75 = 300 positions, ~50–55 mm long.** Why: SMT both sides (thin face board OK), open pin field for GSSG, 1.75× Gen5 and 2.8× UHBR20 margin, fits well inside the 122.25 mm base. Runner-up: ExaMAX2 backplane-style (more rugged guidance, 200 cycles, but 0.5 A, press-fit and larger body).

## 3e. MEG-Array as the GPU-face ↔ base mezzanine (rev 5, leading candidate)
**Apple precedent (confirmed, public):** iFixit's Mac Pro Late 2013 teardown (step 11) identifies the graphics-card data connectors as **FCI Meg-Array**, "the same type used for the G4 & G5 PowerPC processor daughtercards". Apple's service manual calls the GPU and I/O-board links **mezzanine connectors on a flex cable** needing a special removal tool; the CPU riser uses an **edge connector** into the logic board. So Apple ran MEG-Array **at both ends of a flex**, not board-to-board direct. Apple part numbers/pin count: **[GAP]** (not in public teardowns). Era: PCIe 3.0 (8 GT/s).
**Geometry flag:** a direct parallel mezzanine needs the face's connector area parallel to the base. With faces perpendicular to the base and 120° apart, that needs a face-board tab/foot or a stand-off bracket (M&T to confirm). Apple solved it with flex, which "no cables" excludes.

**Rating vs stack height** [Sourced: Amphenol mezz_megarray.pdf; GS-20-033]
- Current datasheet: **32 Gb/s documented at 4 mm and 14 mm**. An older DigiKey-hosted revision says 4 and 6 mm. GS-20-033: "4mm and 6mm stack heights tested to 28Gb/s"; taller stacks quoted at 10 Gb/s.
- So only **4.0 mm** is consistently rated 32 Gb/s → use 4 mm. (14 mm 32 Gb/s claim is in one document only.)
- 300 and 400 positions are both offered at 4.0 mm: 300 = 84500 / 84501; 400 = 84740 / 74221. 0.45 A/contact all energized; 50–200 cycles.

**Positions (GSSG)**
| Item | Pins |
|---|---|
| PCIe Gen5 x16 TX+RX (32 pairs) + REFCLK (1) | 66 |
| Display 4 streams × 4 main (16 pairs) | 32 |
| AUX ×4 | 8 |
| **Signal pairs 53 (Aidan's ~49 + 4 AUX)** | **106** |
| SE: PERST, CLKREQ, PRSNT, WAKE, SMBus ×2, HPD ×4, DDC ×2, CEC, config ×3 | 16 |
| GND at 2/pair (GSSG in-row + ground row between TX and RX blocks) | 106 |
| GND at 3/pair (fully shielded pair: in-row + row above/below; advised for Gen5 at 0 % margin) | 159 |
| **Total at 2/pair / 3/pair** | **228 / 281** |
| 300-pos | 72 / 19 spare |
| **400-pos** | **172 / 119 spare** |
**Recommendation: 400 (84740/74221, 4 mm).** At 0 % rate headroom the extra grounds are worth more than the space; 300 works only at 2 G/pair with ~24 % spare. Body ≈ 10 × 40 grid → ≈ 13 × 51 mm array, ≈ 60 mm housing [Estimate; GAP drawing]. Fits within 122.25 mm with margin.

**Loss with the base retimer mid-channel (Gen5, 36 dB @ 16 GHz per segment)** [Estimate; scaled from loss_budget_A1.md Gen4 numbers ×~1.8 at 16 GHz]
| Segment | Root → retimer | Retimer → GPU |
|---|---|---|
| Package(s) | CPU pkg + CB traces 9–15 | GPU pkg 3–5 |
| Connector | J1 MCE ~1 | MEG-Array 4 mm ~1–1.5 [GAP S-params] |
| Base traces | ~50 mm ≈ 2 | ~30–50 mm ≈ 1.2–2 |
| Face/GPU board traces | – | 50–100 mm ≈ 2–4 |
| Retimer pkg | ~1 | ~1 |
| **Total** | **≈ 13–19 dB** | **≈ 8–13.5 dB** |
Insertion loss is comfortable on both sides. The risk is the **connector itself at its rated edge** (crosstalk, return loss, ILD at 16 GHz) → **must be proven with Amphenol's public S-parameter files** (SI & Fab) before freeze. Retimer candidates: previous DS320PR810 is a redriver; a true Gen5 retimer part is **[GAP]**. Placement on the base board's outer edge in intake air (M&T), 3–5 W.

**UHBR20 on the MEG-Array:** 20 Gb/s vs 32 → 1.6× connector margin; the display path then crosses **two** MEG-Arrays (face→base, base→IOB). Margin is marginal without a DP retimer on the base.

**Caps (decisions for Aidan, not picks)**
- **Gen4 cap on the GPU:** 2× rate margin on the MEG; x16 Gen4 = 31.5 GB/s. Typical published GPU scaling shows low single-digit % loss at Gen4 x16 for RTX 50-class [Estimate; GAP cite]. Suggest designing for Gen5 with firmware fallback to Gen4 (as BP-G4 did, `pcie_gen_max`), decided after SI sim.
- **UHBR13.5 cap:** 2.4× margin per MEG; still drives 4K high refresh with DSC [Estimate]. Or keep UHBR20 with a DP 2.1 retimer on the base [part GAP].

**Fallbacks if MEG-Array fails SI** (same parallel orientation unless noted)
| Fallback | Rating | Positions | Pitch / size | Stack | Cycles | A/pin | Notes | Source |
|---|---|---|---|---|---|---|---|---|
| F1 Samtec AcceleRate HP APM6/APF6 vertical | 56G NRZ / 112G PAM4 | 80–800 | 0.635 mm, 4 rows | 5 / 10 mm | [GAP] | 1.2 A | 1.75× Gen5, 2.8× UHBR20; best electrical upgrade in the same orientation | samtec.com/products/apf6-ra ; arrays overview |
| F2 Samtec APF6-RA (face) + APM6 (base), perpendicular | same | 40–400 | 0.635 mm; ~50–57 mm for 300 | RA | [GAP] | 1.2 A | Rev 4 pick; avoids the parallel-tab geometry | as above |
| F3 Samtec NovaRay NVAM/NVAF | 112–128G PAM4, PCIe 7.0 | ≤64 pairs per part (32 pairs ≈ 37.75 × 11.40 mm) | 0.80 mm | 7–12 mm | [GAP] | 2.1 A | Fully shielded pairs; needs 2 parts or 1 × 64-pair with SE elsewhere | samtec.com/products/nvaf ; B2B design guide |
| F4 Samtec AcceleRate HD ADM6/ADF6 | 32G NRZ / 64G PAM4 | 40–400 | 0.635 mm, 5 mm wide | 5–16 mm | [GAP] | 1.34 A | Same NRZ rating as MEG → density gain only | samtec.com/products/adm6 |
| F5 Caps above (Gen4 / UHBR13.5) on MEG-Array | – | – | – | – | – | – | Cheapest fallback; no layout change | – |

## 3d. MEG-Array (base → IOB) at UHBR20
- Pin count unchanged vs rev 3 (4 streams = 20 pairs): still **300-pos (84500/84501)**.
- Rate: UHBR20 is 20 Gb/s NRZ (10 GHz Nyquist) against MEG-Array 32 Gb/s (Amphenol, 4/14 mm) or 28 Gb/s (older FCI GS-20-033, 4/6 mm) → **1.4–1.6× connector margin only**, and UHBR20 has the tightest loss budget of DP 2.1. The display path crosses two separable interfaces (APF6/APM6 + MEG) plus base and IOB traces.
- Verdict: **marginal; not sign-off-able without SI sim.** Options for Aidan: (a) DP 2.1 UHBR20 retimer on the base before the MEG [part GAP]; (b) cap display at UHBR13.5/UHBR10 (MEG margin 2.4–3.2×); (c) replace base↔IOB MEG with Samtec AcceleRate HP APM6/APF6 vertical, 56G NRZ, 5 or 10 mm stack (stack height must match the current 4 mm MEG gap → mechanical change); AcceleRate HD ADM6/ADF6 (32G NRZ, 5 mm) gives no margin gain over MEG.
- HDMI FRL 12G on the MEG: 2.3–2.7× → OK.

## 4. J3 pin budget (MCIO 124, ~80 signal)
| Item | Pins |
|---|---|
| ASM4242 Gen4 x4 | 16 |
| i226 ×2 | 8 |
| CPU USB 10G ×4 | 16 |
| PROM21 USB 10G ×1 | 4 |
| USB2 ×5 | 10 |
| REFCLK ×3 | 6 |
| Sideband (PERST/CLKREQ ×3, WAKE, SMBus, OC, PWR_BTN, SLP_S3/S5, PLT_RST, LED) | ~19 |
| **Total** | **~79 of ~80** (rev 1 was ~95) |
Display no longer touches J3. Margin is ~1 pin, so either:
- base MCU re-derives LED/SLP/PLT_RST from J1 sideband (saves ~6 → ~73), and/or
- **USB2 hub on the base board** (e.g. a 4-port USB2 hub such as Microchip USB2514B [GAP: datasheet not opened]) so J3 carries 1–2 USB2 pairs (saves ~6–8).
Moving VL822 onto the CPU board would also save pins on J3 (one upstream instead of 4 downstream), but the CPU USB 10G #4 is already a single upstream, so no gain.

## 5. Switches and hubs (public parts)
| Part | Role | Key data | Power | Placement | Source |
|---|---|---|---|---|---|
| VIA Labs **VL822-Q8** | USB-A hub, 1 up / 4 down, all 10G | QFN-88 10×10, 3.3 V + 1.05 V, 25 MHz xtal, BC1.2 | **[GAP]** datasheet says TBD; ~1–2 W class [Estimate] | IOB, near USB-A | via-labs.com id=99; VL822 datasheet PDF |
| Broadcom **PEX89024** | SSD ver. B Gen5 switch | 24 lanes / 24 ports, 115 ns, 29×29 mm, multi-partition | **14 W typ** | SSD board, or base board (see below) | broadcom.com PEX89024; BC00-0445EN |
| Microchip **PM50028** (Switchtec PFX 28xG5) | alt. Gen5 switch | 28 lanes, 16 ports, 8 partitions, x1–x16 bifurcation | **[GAP]** | same | Microchip 00003776 |

**Upstream x8 check (SSD ver. B): fails as a single x8.** The two SSD x4s come from two separate CPU root ports (NVMe x4 and GPP x4; AMD QRG), so they can't bond into one x8 upstream. Workable versions:
- B1: switch in **2 partitions**, each x4 up → 2× x4 down (4 drives, 24 lanes total = PEX89024/PM50028). Same 31.5 GB/s to the CPU, 2 drives share each x4.
- B2: a true x8 upstream only if the GPU drops to x8 (CPU x16 → 2×8) [Aidan decision, GPU perf].
- B3: switch on **one** CPU x4 upstream → 4× x4 (20 lanes), freeing the GPP x4 Gen5 for the ASM4242 (fixes PROM21; see §6 O-1).
Placement: on the **base board** the switch re-times the Gen5 path (likely removes the SSD retimer) but then J10 must carry x16 (MCIO 124 is enough) and 14 W lands on the base (outer edge, intake air, heatsink <5 mm: M&T). On the **SSD board** J10 stays at 2× x4 but the base still needs a retimer. Decision for Aidan.

## 6. PROM21 uplink oversubscription (Gen4 x4 = 7.88 GB/s raw, ~6.9 usable)
| Load on PROM21 | rev 1 | rev 2 (CPU USB + hub) |
|---|---|---|
| ASM4242 USB4 | 7.88 | 7.88 |
| 2× i226 | 0.63 | 0.63 |
| USB-A ×4 | 5.0 direct / 1.25 hub | **0** (CPU USB #4) |
| USB-C 3.2 / DP-Alt data | 0–2.5 | **1.25** (one port) |
| Boot NVMe J8 (Gen4 x4) | 7.88 | 7.88 if kept |
| **Ratio, no boot NVMe** | 1.24–2.03× | **9.76 → 1.24×** |
| **Ratio, with boot NVMe** | up to 2.71× | **17.6 → 2.24×** |
M&T's ~2.4× drops to **1.24×** if the boot NVMe leaves PROM21, else 2.24×. USB4 alone saturates the uplink, so it's the main remaining load.

Options (decisions for Aidan, not picks):
- O-1: ASM4242 on CPU GPP x4 Gen5 (runs Gen4 x4) + SSD board via a switch on the CPU NVMe x4 (version B3). PROM21 → 1.9 GB/s (**0.24×**); SSD total drops to 15.75 GB/s.
- O-2: Drop or move the boot NVMe (boot from the SSD board) → 1.24×.
- O-3: Sixth USB-C onto the VL822 (5 downstream not available, VL822 is 4-port) or a second hub → 1.08×.
- O-4: GPU to Gen5 x8, freeing x8 for ASM4242 + SSD x8 switch upstream (B2) [perf GAP].
- O-5: Accept 1.24× (no boot NVMe) – real-world contention only under simultaneous USB4 + net + USB load.

## 7. Gaps
Rev 5: Apple 6,1 MEG-Array part numbers/pin count; MEG-Array 4 mm S-params and recommended Gen5 pin pattern; 400-pos footprint drawing; face-tab/bracket geometry for a parallel mezzanine at 120° faces (M&T); Gen5 retimer part; DP 2.1 UHBR20 retimer part; Gen4 vs Gen5 perf figure for RTX 5070-class; which stack heights the 32 Gb/s claim covers (4/14 vs 4/6 mm — documents disagree).
Rev 4: APF6-RA/APM6 mating cycles, exact RA footprint and body depth on the face edge; ExaMAX2 85 Ω wafer config for 53 pairs + LS; Paladin data; STRADA min board thickness; Mac Pro 6,1 MEG-Array part number and pin count; UHBR20 retimer part; RTX 5070-class board details (PCB display count, FRL retimer); clearance at the 120° face joints and the 12–13 mm base ends (M&T).
Rev 3: MCE 140/168 exact lengths and part numbers (Amphenol custom/standard), FRL retimer part to replace TDP158, ERF8 footprint, GPU-face/base clearance for a second card edge (M&T), whether MCE 168 is a standard part (study lists 140/168 as SFF-TA-1002 4C/4C+ options).
MCE/MCIO/MEG S-parameters and 1080A loss; MEG 4 mm pin pattern; VL822 and PM50028 power; ASM4242 USB2 legs and power; per-SKU USB/GPP confirmation for the chosen CPU (AMD page cited is 9950X); PROM21 port counts (press only); GPU display count/UHBR; ICD I-3 must be revised (owner action); USB2514B datasheet not opened.

## Sources
Rev 6: graphics flex 821-1880/923-0500 https://www.macsology.com/product/923-0500-cable-flex-graphics-board-mac-pro-late-2013-821-1880/ · TekDep teardown (923-0496, 923-0501) https://tekdep.com/mac-pro-2013-a1481-teardown · MacRumors ground map https://forums.macrumors.com/threads/nvme-with-st-ngff2013-c-vega-internal-gpu-mac-pro-2013-6-1.2085886/page-19 · Apple service manual (iFixit) https://www.ifixit.com/Document/XMlFgdGGPKXQ1IdB/2013-MP-Repair-Manual.pdf
Rev 5: MEG-Array series https://www.amphenol-cs.com/product-series/meg-array.html (Cloudflare blocked direct fetch; content via search) · datasheet https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf · older rev https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6257/mezz_megarray.pdf · GS-20-033 https://www.amphenol-cs.com/media/wysiwyg/files/documentation/gs-20-033.pdf
Rev 4: APF6-RA https://www.samtec.com/products/apf6-ra · ADM6/ADF6 https://www.samtec.com/products/adm6 , https://www.samtec.com/products/adf6 · NovaRay https://www.samtec.com/products/nvaf , https://suddendocs.samtec.com/literature/samtec-high-speed-b2b-design-guide.pdf · Samtec arrays overview https://www.samtec.com/high-speed-board-to-board/high-density-arrays/ · ExaMAX/ExaMAX2 https://www.amphenol-cs.com/product-series/examax.html , https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/backplane/bpl_examax_backplane.pdf , https://www.amphenol-cs.com/media/wysiwyg/files/documentation/gs-12-1096.pdf · STRADA Whisper https://www.te.com/en/products/connectors/pcb-connectors/backplane-connectors/high-speed-backplane-connectors/strada-whisper.html , https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=108-32112&DocType=Specification+Or+Standard&PartCntxt=2187626-1 · Molex Impel https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/applicationspecificationspdf/171/171320/AS-171320-992-001.pdf · Mac Pro 2013: https://www.ifixit.com/Teardown/Mac+Pro+Late+2013+Teardown/20778 , https://www.ifixit.com/Guide/Mac+Pro+Late+2013+Interconnect+Board+Replacement/21209 , https://www.ifixit.com/Document/XMlFgdGGPKXQ1IdB/2013-MP-Repair-Manual.pdf
HSEC8-DV: https://www.samtec.com/products/hsec8-dv , https://suddendocs.samtec.com/testreports/connector-speed-sma_hsec8-dv_web.pdf , https://datasheet.octopart.com/HSEC8-150-01-SM-DV-A-Samtec-datasheet-41340256.pdf · ERF8/ERM8: https://www.samtec.com/products/erf8 , https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6239/erm8-erf8.pdf · Mini Cool Edge flyer: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/general/mini-cool-edge-flyer.pdf · SEARAY: https://www.samtec.com/products/seaf8 · AMD Ryzen 9 9950X spec (4× USB 10G, 1× USB2, 24 usable lanes): https://www.amd.com/en/products/processors/desktops/ryzen/9000-series/amd-ryzen-9-9950x.html · AMD AM5 QRG: https://www.amd.com/content/dam/amd/en/documents/partner-hub/ryzen/amd-socket-am5-quick-reference-guide.pdf · VL822: https://www.via-labs.com/product_show.php?id=99 , http://www.usbtech.net/upload/portal/20210129/273a4e5ddf8b65a319765aa6eb529a1d.pdf · PEX89024: https://www.broadcom.com/products/pcie-switches-retimers/expressfabric/gen5/pex89024 , https://docs.broadcom.com/doc/BC00-0445EN · Switchtec PFX Gen5: https://ww1.microchip.com/downloads/en/DeviceDoc/00003776.pdf · MEG-Array: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf · Mini Cool Edge: https://www.amphenol-cs.com/product-series/mini-cool-edge-0-60mm.html · MCIO: https://www.amphenol-ast.com/v3/en/product_view.aspx?id=370 · ASM4242: https://www.asmedia.com.tw/product/e20zx49yU0SZBUH5/363Zx80yu6sY3XH2.html

## Rev 6a decisions (2026-10-26, Aidan)
- C1/C2 DP-Alt: Parade PS8838 retimer (approved).
- C3/C4 USB4: Parade PS8830 retimers at the ports (approved). It is a retimer, not a host; host stays ASM4242 on PROM21 downlink 1 (Aidan confirmed). Note ASM4242 DP-in is HBR3 only. Datasheets gated; routed to Communications under NDA rule.

## Rev 7c (2026-10-28): U20 heatsink keep-outs and temperature sensor
- Dwgs.User: pedestal band 24×10.6 mm (x 161.7–185.7, y 97.6–108.2), centred on U20 (173.7,102.9); fin overhang 40×35 mm (x 153.7–193.7, y 85.4–120.4), parts ≤3 mm only; radial air channel from U20 to the rim (x 185.7–208, same y band). The channel is also an F.Cu rule area (KO_U20_RADIAL_CHANNEL, footprints not allowed), so DRC will flag what is in it.
- Conflicts (not moved; this needs a mechanical decision): **H2 mounting hole/standoff (199,100) is inside the radial channel, directly upstream.** U3 (197.5,107) and R25 (202.1,108.6) are low parts in the channel and can stay or move. **J3 JST GH top-entry (192.5,86.5), about 4.25 mm tall (GAP: confirm height), reaches the fin overhang corner.** Clearance from the H2 pad edge (r 2) to the fin edge is 3.3 mm, below the 4 mm target. The screw has a straight driver path (not under the fins). H1 (101,100) is clear: nearest part U25 is about 10.8 mm away. H3 (172,130) is outside the fin footprint (fin edge y 120.4).
- U26 TMP1075DGKR (same part as U3, LCSC C2864807; GAP: confirm the address table in the TI TMP1075 datasheet) on I2C_SYS at **0x4A** (A1=V+, A0=A2=GND); ALERT goes to the shared BP_OTEMP_N; it sits at (173.7,111) just below the pedestal band, with C83 100 nF.
- Mated heights: Meg-Array 84500+84501 = 4.0 mm stack (Amphenol Meg-Array product family). J1 Mini Cool Edge: body ≈6 mm (earlier estimate; GAP: drawing CME102241010301X gives no height, so the card seating height still has to be measured).
- KiCad is no longer installed on the box and the Debian mirror returns HTTP 500, so the rev 7c edits were made as text and DRC/ERC have not been rerun.

## Rev 7d (2026-10-28, 19:15 EDT): faces swapped (Aidan's decision)
- GPU face J11 is upper-right at (185.63,67.74), rotation −46.7; SSD face J12 is upper-left at (114.24,68.11), rotation +46.5. This was placed by the concurrent tools/stock_align.py from stock measurements.
- U21/U22 and their B.Cu passives (C62–C72, R111–R117) moved by (−21,−6): U21 is now (137.6,96.9), U22 (131.5,96.9). U20 did not move, so its heatsink keep-outs stay where they were.
- Octilinear lengths (tools/swap_lengths.py → CSV): U20 A 8.3–21.9, B 39.3 (to the J11 centre; GPU pinout pending). U21 A 15.8–21.0, B 37.8–44.8. U22 A 14.6–28.4, B 34.3–41.9. **0 pairs over 45 mm** (worst 44.8).
- Meg-Array fab body corners: r 61.50 (J11) and 61.54 (J12) from the true disc centre, still past the 61.035 edge. Pads are at r ≤57.8.
- ERC rev 7d: 0 errors, 162 warnings (global_label_dangling). DRC: drc_report_rev7d_20261028.txt (running in the background).
