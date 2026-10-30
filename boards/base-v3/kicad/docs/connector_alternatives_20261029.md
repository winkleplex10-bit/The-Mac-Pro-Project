# J1 / J3-J14 connector alternatives (research only, 2026-10-29)
Nothing in KiCad, the CSVs or the pin maps was changed. Nobody was contacted.

## Required counts (taken from the project files)
- **J3/J14 (MCIO-124)**, mp62-cb-j3_mcio124_host-end_am5_rev2.csv: 124 positions = **67 signals + 57 GND, 0 power, 0 spare**.
  - 26 high-speed differential pairs (52 pins): USB3 C1, C2, C5, C6 and HUBUP (20 pins), PCIe ASM4242 x4 (16), I226A and I226B x1 (8), three REFCLKs (6), USB2_HUB (2).
  - 15 single-ended pins: CLKREQ# ×3, PERST# ×3, SLP_S3#, SLP_S5#, WAKE#, I2C_BB ×2, SMB_ALERT#, PWR_BTN#, BB_HS_PRSNT0#/1#.
- **J1 (CPU-LINK, footprint "MiniCoolEdge_224P_Vertical_SMT_PLACEHOLDER")**: 224 = 124 signals + 80 GND + 20 power (12 P12V, 2 3V3_SB, 6 5V_SBY), 0 spare.
- **J1 + J3 combined**: 191 signals + 20 power = 211 non-GND pins. With a GSSG ground pattern on the new pairs, the merged connector needs about 290–300 positions. The absolute floor with no extra grounds is 224 + 67 = 291.

## A. Smaller cable connector in place of MCIO-124 (ranked)
| # | Option | Positions | Pairs it can carry | Fit for 26 pairs + 15 SE | Notes |
|---|---|---|---|---|---|
| 1 | Keep MCIO-124 (SFF-TA-1016), 0.6 mm | 124 | 16X + sidebands, or 20X | Fits now, 0 spare | Baseline |
| 2 | MCIO 74 + MCIO 50 (two connectors) | 124 total | 8X/12X + 8X | Would need a custom pinout; little or no gain | Two parts, two cables, larger total area: **no** |
| 3 | MCIO 74 alone | 74 | 8X + sidebands / 12X | **Does not fit**: short by about 14 pairs | |
| 4 | MCIO 38 | 38 | 4X + sidebands / 6X | **Does not fit**, even ×2 | |
| 5 | SlimSAS 4i/8i (SFF-8654, 0.6 mm, 38/74 pin) | 38/74 | 4/8 lanes | Same limits as MCIO 38/74; **does not fit** | GAP: no datasheet fetched |
| 6 | Samtec ECDP/HSEC8-DP twinax, 0.8 mm | 16–112 | up to 32 pairs | 112 positions could hold 26 pairs + SE, but with **0.8 mm pitch the footprint is longer than MCIO-124** | Gen4/5; |

MCIO positions and channel options (38/50/74/100/124/148), 0.6 mm pitch, Gen5, 0.5 A per contact: Amphenol AssembleTech MCIO overview https://www.amphenol-ast.com/v3/en/overview.aspx?classId=231, cable datasheet https://www.amphenol-ast.com/V3/UpLoadFiles/20180527/MCIO_CA_Tech_Datasheet.pdf, 38-pos product page https://www.amphenol-ast.com/v3/en/product_view.aspx?id=368.

**Verdict A:** a smaller connector doesn't work unless the signal set shrinks. Ways to shrink it, all of which affect performance and need Aidan's decision:
- Move the USB3 C1/C2/C5/C6 ports behind the VL822 hub (frees 16 pins).
- Drop to an ASM4242 x2 link.

Without the four USB3 ports and with ASM x4, about 18 pairs remain, which still exceeds what MCIO-74 can carry.

## B. Larger card edge to absorb J3 (ranked)
| # | Option | Positions | Pitch | Gen5 | Per-pin current | Fit vs. ~291–300 needed |
|---|---|---|---|---|---|---|
| 1 | **Amphenol Mini Cool Edge 0.60 mm, 280-pin vertical SMT, ME1028040101011** (the same family as the current J1) | 280 | 0.60 mm | Family spec 32–56 GT/s; Gen5 part codes exist for RA sizes; GAP: Gen5 rating of the 280V part not confirmed | 1.1 A | **Short by ≥11 even with zero added GND**; does not fit as-is |
| 2 | Keep 224-pin J1, plus a **second Mini Cool Edge on the CPU-board edge** (140-pin ME1014010101011 or 84-pin ME1008410101011) in place of J3/J14 | 224 + 140 | 0.60 mm | as above | 1.1 A | **Fits.** GSSG needs about 94 positions (52 HS + about 27 GND + 15 SE), leaving about 46 spare out of 140. The 84-pin part is too small. |
| 3 | Samtec HSEC8-DV | 18–200 | 0.80 mm | **No, Gen4 only (28 Gbps NRZ)** | 2.8 A (2 pins) | Smaller than 224 |
| 4 | Samtec HSEC8-DP | 16–112 | 0.80 mm | Gen5 | 2.7 A | Too small |
| 5 | PCIe CEM x16 (Samtec PCIE-G5 etc.) | 164 | 1.0 mm | Gen5 | ~1.1 A (CEM) | Smaller than the current 224 |
| 6 | SFF-TA-1002 / OCP 3.0 4C+ (Amphenol MCE, TE Sliver, Samtec HSEC6) | 168 | 0.60 mm | Gen5 | 1.1 A | Smaller than the current 224 |

Sources:
- Mini Cool Edge 0.60 mm datasheet, which lists 48/56/84/140/168/196/224/280 vertical sizes, 1.1 A, and 32–56 GT/s: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/ssio/ssio_mini_cooledge_0_60mm.pdf
- Samtec 0.80 mm edge-card page (HSEC8-DP 56G PAM4, 2.7 A; HSEC8-DV 28G, 20–100 per row): https://www.samtec.com/rugged-power/high-speed/080mm/
- HSEC8-DV product page (PCIe 5.0 "No"): https://www.samtec.com/products/hsec8-dv
- Samtec edge card guide (PCIE-G5, HSEC6 SFF-TA-1002): https://suddendocs.samtec.com/literature/samtec_edge_card_application_design_guide.pdf

## Base-board length near J1 (from backplane.kicad_pcb)
- J1 sits at (150, 112.6), rotated 180°.
- Pads span ±42.2 mm, and the courtyard is ±43.2 mm, so it is **86.4 mm** long.
- The Ø122.07 disc is centred at about (150, 100), so the chord at y = 112.6 is about **119 mm**, roughly 16 mm of free length on each side. The mounting holes S1–S6 (Ø6 keep-outs) and the J11/J12 Meg-Arrays at about ±46.6° crowd the ends.
- A 280-pin part, estimated at about 103 mm by scaling 56 extra positions × 0.6 mm / 2 rows (GAP: not datasheet-dimensioned), would just fit geometrically. A second 140-pin part (estimated at about 50 mm) needs its own edge segment on the CPU board, which is a Mechanical & Thermal question.

## Recommendation
1. **Keep MCIO-124 for J14.** No smaller connector carries 26 pairs plus 15 sideband signals.
2. If Aidan wants the cable gone, the only fitting edge option found is **a second Mini Cool Edge 140 on the CPU-board edge** (same family and pitch as J1, 1.1 A). It needs CPU Board and Mechanical & Thermal to confirm edge length and alignment.
3. A single 280-pin J1 is about 11+ pins short, so it only works if the J3 signal set is also cut (see the performance options under A, which are Aidan's call).

## Gaps and URL check
- Gen5 rating for the vertical 140/224/280 MCE parts was not confirmed (GAP).
- Housing lengths come from estimates, not drawings (GAP).
- No SlimSAS datasheet was opened (GAP).
- **URL check (curl, 2026-10-29):**
  - samtec.com/rugged-power/high-speed/080mm returned 200.
  - The Amphenol CS PDF and the Samtec guide returned 403, and samtec.com/products/hsec8-dv returned 429. All three are bot blocks.
  - amphenol-ast.com timed out from the box.
  - All of these pages were indexed and returned content through web search today, but they need a browser check.
