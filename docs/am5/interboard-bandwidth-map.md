# MacPro6,2 inter-board link and bandwidth map (AM5), rev 6
Base Board & Connectors, 2026-10-26 ≈18:00 EDT (rev 4 ≈17:50, rev 3 ≈17:40, rev 2 ≈17:30). Draft, nothing approved. No other files edited, nothing pushed.
Inputs: research/connector-bandwidth-options.md (M&T), docs/pinmaps/base-iob-megarray-review.md, docs/am5-cpu-board-frozen-config.md, macpro62-interface-control-rev4.md, kicad/macpro62-backplane-v3/docs/loss_budget_A1.md, plus public vendor pages below.
Tags: [Sourced] = public page (URL in Sources); [Estimate]; [GAP].

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
