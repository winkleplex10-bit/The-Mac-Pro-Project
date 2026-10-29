# MacPro6,2 CPU board (CB AM5 v3): NON-FAB rough floorplan draft
2026-10-21 (ET). **NOT FOR FAB. No pin assignments in KiCad; U1 stays a placeholder.** Box only, not pushed.
Basis: `am5-pinmap-table.csv` (from public-domain Wikimedia Commons `Socket_AM5_pinmap.svg`, QuietRub/WikiChip), status map-only unless noted. Orientation below = SVG **top view** (row A at top, column 1 at left). Rotation of U1 on the board is a free choice; all "sides" below are socket-relative.

## Socket region map (from the SVG, top view)
| Region | Balls (approx.) | Socket side |
|---|---|---|
| DDR5 channel A + B (154 + 154) | all rows A-BD, cols 23-40 | **right half** |
| VDDIO_MEM_S3 (23) | rows L-P, cols 19-30 | centre, upper, next to memory |
| PCIe (125 incl. GPP_CLK0-5) | rows J-BD, cols 2-17; lanes 0-7 rows J-Y, 8-15 rows U-AG, 16-23 rows AE-AR, 24-27 rows AJ-AT | **left edge** |
| USB / DisplayPort (+28 split USB-C/DP) | rows A-K, cols 6-23 | **top edge, left of centre** |
| SVI3 (SVC B5, SVT C5, SVD D5) | top-left corner | top-left |
| VDDCR_SOC (24) | rows L-P, cols 8-18 | upper-left of centre |
| VDDCR (203) | rows R-AN, cols 7-30 | large central block |
| Rail sense pins (7) | rows L-AU, cols 21-23 | centre column strip |
| Sideband / GPIO / SPI / eSPI / PROCHOT_L / THERMTRIP_L / PWROK / RESET_L | rows AU-BD, cols 7-22 | **bottom edge, left of centre** |

## Conclusions (rough)
1. **DIMMs (2 total, 1 per channel, per approved power plan):** both slots on the socket's memory (right) side, parallel to the socket edge, A nearest the socket. Channels A and B are interleaved across the same column band, so the two slots stack side by side rather than split left/right. KiCad currently still has **4 UDIMM placeholders, renamed 2026-10-21 to DIMM_A1/DIMM_A2/DIMM_B1/DIMM_B2 (were J6/J7/J9/J10, clashing with backplane MCIO J9/J10)**: drop two (A2/B2) in a later approved pass; power budget's 4-DIMM line should drop to 2.
2. **PCIe x16 to backplane MCIO J9/J10:** lanes leave the left edge. Lanes 0-15 occupy rows J-AG (upper/middle of the left edge), so the CPU-LINK connector J1 / route to BP J9 should sit off the socket's left side, upper half. Lanes 16-27 (GPP/chipset) are lower-left (rows AE-AT) and fan toward BP J10 and PROM21 U2. Lane polarity/reversal unconfirmed.
3. **No boot M.2 J8:** frees the area previously reserved; give it to the VRM output caps or PROM21 breakout. J8 removal is a KiCad change for a later approved pass.
4. **VRM (adopted SI & Fab layout):** VDDCR phases **top-right**, VDDCR_SOC phases **top-left**, SVI3 controller U3 near top-left (SVC/SVD/SVT B5-D5). **No VRM on the left edge: left edge is PCIe only.** Remote-sense Kelvin pairs from the centre sense strip (cols 21-23).
5. **USB/DP** (rows A-K, top edge) escape on an **inner stripline (L3) under the VRM**, with **~5 mm keep-out from switch nodes**, GND planes unbroken above and below.
5a. **PCIe layer split:** lanes 0-15 and lanes 16-27 on separate inner layers (L3 / L8 per `am5-stackup-draft.md`) or separated by a GND via fence.
5b. **Lane reversal and GPP_CLK REFCLK mapping: NOT confirmed by any public source (gap).** Reserve a layer change at the connector (J1) end of each pair.
5c. **Backplate bracket / core nut holes on the bottom layer around the socket: TBD.** They must be placed before left-edge PCIe escape and bottom sideband routing.
6. **PROCHOT backstop:** PROCHOT_L is ball **AW19** (bottom edge, centre-left, next to ALERT_L AU19 and THERMTRIP_L AY18). Plan: backplane RP2350 (INA226/INA228 total 12 V) and/or a fast comparator drive an open-drain N-FET pulling PROCHOT_L low, routed via a spare CPU-LINK pin to the bottom side of the socket. Pull-up rail and level (likely VDD_18/3.3 V domain) is **unconfirmed** – no public electrical spec. Sideband cluster also on the bottom, so RP2350-facing signals (PWROK, RESET_L, SPI/eSPI) group there.


## Socket mechanism keep-out (replaces the 46.6 × 46.5 mm U1 placeholder; docs only, KiCad unchanged)
Source: `am5-socket-mechanicals.md` (WikiChip: AM5 backplate/stiffener/force-frame/lever envelope 67 × 106 mm). Socket centre (78.4, 73.3) = centre of U1 placeholder x 55.1-101.7, y 50.0-96.5. Board coordinates below are KiCad mm (y down), from `archive/kicad/macpro62-am5-v3/fitcheck_floorplan.txt`.

| Keep-out | Orientation A (106 along x) | Orientation B (106 along y) |
|---|---|---|
| Bracket/backplate envelope 67 × 106, both sides | x 25.4-131.4, y 39.8-106.8 | x 44.9-111.9, y 20.3-126.3 |
| 6 mm inner band (bottom layer: **no copper except GND**) | band x 25.4-31.4 / 125.4-131.4, y 39.8-45.8 / 100.8-106.8 | band x 44.9-50.9 / 105.9-111.9, y 20.3-26.3 / 120.3-126.3 |

- **6,1 core holes:** 69.5 × 55 centred on (78.0, 73.5) → holes at x 43.25 / 112.75, y 46.0 / 101.0 (H1-H4 FIXED). **8 mm dia bottom-layer keep-out** around each.
- **Bracket screw (ILM #6-32 / PEM) positions: GAP.** Custom backplate approved (option 1 in `am5-socket-mechanicals.md` numbering per Master Bot) carrying both ILM nuts and the core's 69.5 × 55 nuts; screw XY to be measured on a retail AM5 board.
- **All must be placed before left-edge PCIe escape and bottom sideband routing.**

### Fit check against current v3 placement
| Item (current position) | Orientation A | Orientation B |
|---|---|---|
| Core holes H1-H4 (8 mm keep-out) | inside envelope; must be integrated into custom backplate | holes 0.85-1.65 mm outside edge, **8 mm keep-out overlaps envelope edge** → custom backplate must absorb them |
| LGA1700 frame seats H5-H8 (x 47.5-53.4 / 103.5-109.4) | inside | inside | 
| → both: H5-H8 are obsolete for AM5; replace with ILM screw positions (GAP) |||
| DIMMs DIMM_A1/A2 (x 3.0-19.3), DIMM_B1/B2 (x 137.0-153.4), back | clear: A1 6.1 mm, B1 5.6 mm from envelope | clear (> 25 mm) |
| VRM inductors L1-L8 (x 18.9-30.1) and COUT1 (x 30.7-36.3), top | **conflict**: L1-L8 overlap by up to 4.7 mm; COUT1 fully inside | clear (COUT1 8.6 mm from edge) |
| CB1 12 V bulk L (back, x 19.7-36.3, y 39.7-70.3) | **conflict** (inside backplate area, bottom) | clear |
| U4-U7 aux rails / CB2 bulk R (x 119.7-148, top & back) | **conflict** (overlap to x 131.4) | clear |
| CAC1 PCIe AC caps (top, y 14.7-23.3) | clear | **conflict** (y 20.3-23.3 overlap) |
| J8 boot M.2 (back, y 13.3-36.3) | clear (3.5 mm) | **conflict** (y 20.3-36.3 overlap) – J8 to be removed later per plan, which clears it |
| U8 VDDIO_MEM, J4 TPM, U10 SPI (top, y 105.7-131.3) | U8 overlaps y ≤ 106.8 (1.1 mm) | **conflict** (inside) |
| BT1 CR2032 holder (DNP): **Keystone 3034** (SMT, nickel-plated phosphor bronze; 3034TR on reel) | bottom | 58.7-81.3 / 119.7-136.3 | **21.5-42.7 / 72.0-95.1** (21.2 × 23.1 body, rotated 90°) | 21.2 × 23.1 | **4.1 (H .160 in, Keystone DS)** | 2.2 mm outside envelope (x 44.9), 2.2 mm from DIMM_A1 (x 19.3), 1.7 mm below CB1; not under backplate; clear of core-hole keep-outs. Bottom-side limits = fillet + back-to-shell gap (M1, open) |
| J1 CPU-LINK (y 1.5-13.0) PCIe exit | clear | clear (7.3 mm) |

**DECISION 2026-10-21 (Master Bot sign-off): Orientation B only. Orientation A is REJECTED.**

**Conclusion (pre-decision):** Orientation A blocks the VRM row and both side power areas, so it would force moving the whole VRM: reject. **Orientation B (long axis along y, toward J1/J3) is the workable one**: DIMMs and VRM stay as placed; to move: CAC1 up/sideways (≥ 3 mm, y ≤ 17), J8 (already planned for removal), U8/J4/U10 and BT1/U14 out of y 20.3-126.3 between x 44.9-111.9 (move below y 126 or out to x > 112 beside U2). Core-hole 8 mm keep-outs touching the envelope edge are only resolvable with the custom backplate. Note the socket-relative "VRM top-right/top-left, PCIe left edge" wording above maps to board coordinates only once U1 rotation is chosen: in the current placement the VRM is at the board's left (x 8-36) and PCIe exits to J1 at the board top (y < 13).

### Relocation plan for the six moved items (orientation B; docs only, KiCad unchanged)
Envelope (both sides): x 44.9-111.9, y 20.3-126.3; 6 mm bottom GND-only band inside it. Core-hole bottom keep-outs: 8 mm dia at (43.25|112.75, 46.0|101.0). **Correction:** the 67.2 mm radius is around the chassis axis on the **base board** (z 1.5-10 mm, MCIO bend, `cpu-baseboard-cable-plan.md` §1.3-1.4), NOT around the CPU core centre; it does not limit BT1/U14. Real limits for CPU-board bottom parts: the fillet at the board's lower edge (pending Aidan's base-ring measurements; U14 stays put) and the back-to-shell gap (measurement M1, open). Heights are **estimates** (typical package for the part class) for Mechanical & Thermal to check.

| Item | Side | Old (x / y) | New (x / y) | Size | Height (est.) | Clearances |
|---|---|---|---|---|---|---|
| CAC1 PCIe AC caps (TX only, 24 lanes through J1 = 48 caps) | top | 44.7-115.3 / 14.7-23.3 | **44.7-115.3 / 14.5-17.0** (single row, 0402 oriented along signal flow, 24 pairs at ~1.1 mm cap pitch ≈ 53 mm used) | 70.6 × 2.5 | 0.55 (0402) | **1.5 mm from J1 gold fingers (J1 ends y 13.0) per SI & Fab**; 3.3 mm outside envelope (y 20.3) |
| U8 VDDIO_MEM_S3 1.1 V | top | 54.7-69.3 / 105.7-114.3 | **74.0-88.6 / 127.0-135.6** | 14.6 × 8.6 | ~3.0 (buck inductor) | 0.7 mm below envelope; 1.1 mm above Y1; clear of U9 (x ≤ 73.3). Longer VDDIO feed to socket: wide plane on L5/L6 |
| U10 FCH SPI 32 MB | top | 76.7-87.3 / 122.7-131.3 | **88.9-99.5 / 127.0-135.6** | 10.6 × 8.6 | ~2.2 (SOIC-8 208 mil) | 0.5 mm from U2 (x ≥ 100); clear of Y1 (y ≥ 136.7) |
| J4 SPI TPM header (opt.) | top | 61.7-72.3 / 122.7-129.3 | **112.5-119.1 / 108.5-119.1** (rotated 90°) | 6.6 × 10.6 | ~4-8.5 (1.27 vs 2.54 mm 2×7 header; prefer 1.27 SMD) | 0.6 mm outside envelope (x 111.9); 2.5 mm below H4 screw seat; 0.6 mm from U4-U7 column (x 119.7); U2 starts y 123 |
| BT1 CR2032 holder (DNP) | bottom | 58.7-81.3 / 119.7-136.3 | **24.0-40.6 / 72.0-94.6** (rotated 90°) | 16.6 × 22.6 | ~4.2-5.6 (SMD CR2032 holder) | 4.3 mm outside envelope; 6.9 mm from core-hole (43.25, 101) centre → 2.9 mm clear of its 8 mm keep-out; between CB1 (ends y 70.3) and U14; 4.7 mm from DIMM_A1; max r 58.0 < 67.2 → **not in base-ring keep-out, not under backplate** |
| U14 ALC897 (DNP) | bottom | 40.7-51.3 / 114.7-125.3 | **27.0-37.6 / 105.5-116.1** | 10.6 × 10.6 | ~1.6 (LQFP-48) | 7.3 mm outside envelope; 7.2 mm from core-hole (43.25, 101) centre → 3.2 mm clear of its keep-out; not under backplate; position kept pending fillet measurement (base-ring r 67.2 does not apply). Audio routing to J3 becomes ~50 mm longer (low-speed, OK) |

**BT1 holder choice:** a CR2032 cell is 3.2 mm thick, so ~3 mm total is not feasible for any surface holder (only a PCB cut-out/sunk holder, not recommended). Lowest reputable SMT options found:
- **Keystone 3034: 4.1 mm** (selected). Datasheet table: https://static.distyparts.com/disty-files/datasheets/36/-3/03/36-3034DKR-ND.pdf ; product https://www.keyelco.com/product.cfm/product_id/798 ; TME lists H 4.06 mm. LCSC **C5199422**, search index showed 61 in stock at $0.355 (live page returned 404 to our fetch, so **stock unverified**; JLC assembly-library status not checked).
- Linx BAT-HLD-001: 4.2 mm, 15.5 × 22.9 mm (smaller footprint; fits the earlier 16.6 mm-wide spot): https://www.micro-processor.sg/parts-file/8e-bat-hld-001.pdf . LCSC availability not checked.
- MPD BU2032SM family: 5.2-5.33 mm (taller, rejected). Keystone 1058: 5 mm.
(Linx BAT-HLD-002-SMT is 2.8 mm but fits CR2016 only.)

**CAC1 SI rules (SI & Fab):** both caps of each pair side by side at equal distance from the fingers; L2 GND void under every cap pad.
**CAC1 count reconciliation:** lanes through J1 per `cpu-baseboard-status.md` = GFX x16 (→ BP J9) + GPP#1 x4 + GPP#2 x4 (→ BP J10) = **24 lanes**. PCIe AC caps sit only on each link's TX side, so the CPU board carries caps on the 24 CPU-TX pairs only (CPU-RX caps are at the GPU/SSD transmitters) → **48 caps**. My earlier 40 omitted GPP#2; SI's 64 equals TX+RX of a x16 alone (16 × 2 × 2) and double-counts RX. **48 is right** (PROM21's x4 uplink stays on-board and its caps belong near U2, not in CAC1).
No item lacks a legal spot. Tight items: CAC1 3.3 mm below envelope with 1.5 mm finger gap, U8 0.7 mm and U10/J4 ~0.5 mm from neighbours. All positions depend on the ILM screw XY (GAP) not landing in these zones.

## Open gaps (unchanged)
- ILM/bracket screw XY positions (custom backplate), PCB thickness.
- PCIe lane reversal/polarity and GPP_CLK REFCLK assignment.
- Backplate bracket / thermal-core nut hole positions.
- Socket mechanical drawing / real LGA1718 footprint (pad size, keep-outs, ILM holes).
- PROM21 ballout.
- Electrical spec of PROCHOT_L (pull-up voltage, timing) and all CPU-side ballout except names: all map-only.
