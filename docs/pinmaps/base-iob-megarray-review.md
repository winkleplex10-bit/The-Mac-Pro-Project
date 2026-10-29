# Review: base-iob-megarray.csv (Base Board & Connectors, 2026-10-26)
Reviewer: Base Board & Connectors. Source files were read, not edited.
Inputs: docs/pinmaps/base-iob-megarray.csv (168 rows), docs/macpro62-io-board-am5-plan.md §2–4, docs/am5-cpu-board-frozen-config.md (Option C, J3), macpro62-interface-control-rev4.md (I-2, I-3, I-7, I-8), kicad/macpro62-backplane-v3/docs/loss_budget_A1.md.

## Verdict
**Connector choice: OK (200-pos 10×20 at 4 mm exists and is rated for the speeds here). Pin map: NOT ready.** The ground pattern is a 1-D list, not a 10×20 grid assignment. The base-end column is empty. J3 can't carry everything this map expects from it.

## 1. Connector size, stack height, rating (public sources)
- The 200-position (10×20) part at 4.0 mm mated height is plug **84516** with receptacle **84517**. The same plug works at 6 mm (with 55724) and 8 mm (with 84535). [A1][A2][A3]
- Current rating: **0.45 A/contact with all contacts energized, 2.0 A with a single contact**, at ≤30 °C rise. [A2][A4 §6.4]
- Data rate: the current Amphenol page and datasheet say up to 32 Gb/s, documented for 4 mm and 14 mm stacks. The older FCI GS-20-033 says 4/6 mm were "tested to 28 Gb/s". [A1][A3][A5] Propagation delay is ≤35 ps at 4 mm. [A4 §6.6]
- Signals that cross this connector: PCIe Gen4 at 16 GT/s (ASM4242 uplink), Gen3/2.5G (i226), USB 10G, USB2, and optionally DP into the ASM4242 (HBR3 8.1 Gb/s, or UHBR10/20 at 10/20 Gb/s). **USB4 Gen3 at 20 Gb/s/lane does NOT cross the Meg-Array.** The ASM4242 sits on the IOB, so USB4 PHY traffic stays IOB-local. Every signal is under the 28 Gb/s figure. UHBR20 is the only one near it, and it is untested here. Per-signal-type margin at 4 mm has to come from Amphenol's S-parameter files: **[GAP]**, since the files are public but SI & Fab hasn't run them.
- Spare/power: 200 − 168 = **32 spare**. No power pins are needed because the IOB gets power from the PSU directly (ICD I-7/I-8) and 12 V isn't carried. If the 10 DP-in pairs are dropped, it's 136 pins and 64 spare.
- **Problem P1 – ground count is too low for a BGA grid.** 48 GND for 48 pairs means 1 per pair. In a 1.27 mm 10×20 array, a pair whose neighbour on every side is another signal won't stay isolated. Typical Meg-Array differential layouts put GND around each pair (in a row-pair/ground-row or checkerboard pattern), and that needs roughly 1.5–2 GND per pair. Rough estimate: 48 pairs × 2 = 96 pins, + 96 GND, + 24 sideband = 216 > 200. **So 200 positions only work if (a) the DP-in pairs are dropped (38 pairs → 76 + ~70 GND + 24 ≈ 170) or (b) low-speed USB2 and sideband pins are used as part of the shielding.** Otherwise go to the **300-position (84500/84501, 4 mm)**. [A1][A2] Amphenol's recommended pin pattern for 4 mm: **[GAP]**. It's in the SI report on amphenol-cs.com, which isn't cited here yet.

## 2. Ground pattern / return paths
- The CSV puts "GND after pair X" in a linear list. That says nothing about physical neighbours in the 10×20 grid. **P2: the map has no row/column (A1…K20) assignment**, so shielding on both sides can't be verified. As written, each pair has GND on one side only, after it in the list.
- Recommended pattern: put each pair in-row with its own GND, and stagger adjacent rows so every pair has GND on both sides in-row and a GND or quiet signal above and below. Keep TX and RX in separate column blocks (avoids NEXT). Keep ASM Gen4 and any DP/UHBR pairs on the outer rows nearest the via fan-out, or at least separated from USB2 and sideband by a GND row.
- Return path: GND vias at every GND ball on both boards, stitched to the adjacent reference planes on the base and the IOB. Sideband/USB2 don't count as shield. The IOB and base GND are also tied through the Micro-Fit pass-through (I-8). Make sure that loop doesn't become the high-speed return (low-impedance GND bank inside the Meg-Array: at least 30% of balls).
- USB4 Gen3 20 Gb/s doesn't apply here (see §1). DP HBR3/UHBR on the optional DP-in pairs: AUX shouldn't be counted as a shielded HS pair, and HPD needs a pull-down on the sink side.
- REFCLK pairs (3) have one GND each. They need GND on both sides because of the jitter budget.

## 3. Base-end column vs CPU Board J3
- **P3: `base_end_pin` is empty for all 168 rows.** That makes the map unreviewable for routing.
- **P4: J3 is over budget.** The frozen config gives J3 (MCIO 124) as having "80 signal today". The CSV expects these from J3 (Option C): ASM Gen4 x4 (8 pairs) + 2× i226 (4) + 4 CPU USB 10G (8) + 4 PROM21 USB 10G (8) + USB2 ×7 (7) = **35 pairs = 70 pins + 3 refclks (6) = 76**, plus about 19 sideband (PERST/CLKREQ ×3, WAKE, SMBus ×3, PWR_BTN, LEDs, SLP_S3/S5, PLT_RST, OC ×2, PRSNT). That's **≈95 > 80**. Either some sideband moves to the base board (the base MCU re-derives LEDs, SLP and PLT_RST from J1 sideband, which already carries SUS_S3/S5/PLTRST/PWRBTN), or USB2/USB-A has to take another path. That needs a decision from CPU Board and Aidan.
- **P5: frozen config and CSV disagree on the hub.** Frozen config §3 says "USB 10G #1 → VL822" (a hub). The CSV and IOB plan say USB-A A1–A4 are "PROM21 direct, no hub" (4 PROM21 10G ports). The PROM21 USB 10G port count isn't confirmed from public AMD docs here: **[GAP]**.
- **P6: ASM DP-in (10 rows) has no source.** None of it comes from J3, and the GPU display goes to the IOB over J2 (ICD I-3). If DP-in comes from the GPU, it would go through the face → base → Meg-Array, which is a new base route not in the backplane v3. Recommend **dropping DP-in from the Meg-Array** and feeding it over J2 or a dedicated cable, or leaving the ASM4242 DP-in unpopulated.
- P7: the USB2 count (7) vs 10 ports depends on the IOB hub. USB2_7 says "CPU, hub upstream", which is OK.
- P8: VBAT row: OK to delete, consistent with the frozen config §RTC (CB CR2032). But ICD rev4 still shows VBAT_RTC IOB→CB on J3 A26 (Z790-era). ICD needs an update.
- P9: rev4 ICD and backplane v3 are still the LGA1700/Z790 revision (I-2 = CB J3 → IOB J1 direct). Option C (J3 → base → Meg-Array → IOB) isn't in the ICD or backplane v3 yet. That adds a new MCIO receptacle and the Meg-Array to the base board, and its loss sits in the Gen4 budget (28 dB @ 8 GHz, loss_budget_A1.md, a 4-layer number). Cable + base trace + Meg-Array + IOB to ASM4242 needs a recheck: **[GAP]**.

## Decisions for Aidan
1. ASM4242 DP-in: drop it from the Meg-Array (recommended), or route GPU DP through the base board.
2. If DP-in stays: 300-position Meg-Array, or 200-position with proper ground.
3. J3 overflow: move derived sideband to the base board (recommended), or cut USB2/USB-A from J3.
4. USB-A topology: VL822 hub vs PROM21 direct (the frozen config and IOB plan conflict).

## Next actions (no files changed)
- I/O & Storage + SI & Fab: produce the 10×20 grid assignment with GND on both sides of every pair.
- CPU Board: new J3 pin table (Option C), then I fill in base_end_pin.
- Update ICD to rev5 (I-2 re-targeted, new Meg-Array interface).

## Sources
[A1] https://www.amphenol-cs.com/product-series/meg-array.html
[A2] https://www.farnell.com/datasheets/3946610.pdf (FCI MEG-Array datasheet: current rating, P/N selector)
[A3] https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf
[A4] FCI GS-12-100 product spec: https://www.manuallib.com/download/pdf10/FCI-MEG-ARRAY-81-100-200-240-300-400-528-POSITIONS-GS-12-100.PDF
[A5] Amphenol GS-20-033 application spec: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/gs-20-033.pdf
Gaps: Amphenol pin-pattern/SI report for 4 mm; PROM21 USB 10G count (public); ASM4242 USB2 & DP-in details (NDA); 1080A loss; end-to-end Gen4 channel budget for Option C.
