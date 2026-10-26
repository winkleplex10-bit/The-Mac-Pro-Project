# Press/compression B2B connectors vs J2 MCIO-74: research only (2026-10-25)

**Baseline:** J2 is an MCIO-74 (8i) right-angle receptacle (Amphenol G97R22332HR) at about 9.0 mm mated height at the latch, with a twinax cable to the IOB (project spec §3/§9). It carries 3 DP links × 4 lanes at HBR3 8.1 Gbps plus AUX and HPD. To check "pins freed": MCIO-74 has 74 contacts. The proposed display-through-board path needs about 55 extra pins on top of the PCIe Gen4 x8 signals. The real question is whether one connector can carry PCIe x8 (about 32 signal pins plus grounds and sideband) together with about 55 display pins, which comes to roughly 120–160 contacts including grounds.

Requirements: HBR3 is 8.1 Gbps NRZ and PCIe Gen4 is 16 GT/s, so any connector rated ≥16 Gbps covers both.

## Candidates

| Part | Pitch / positions | Stack height | Cited SI rating | Covers HBR3 + Gen4? | Mating hardware | Cycles | Fits about 55 display pins + PCIe x8? |
|---|---|---|---|---|---|---|---|
| **Amphenol (ex-FCI) MEG-Array BGA mezzanine** [1][2][3] | 1.27 × 1.27 mm grid. 81/100/200/240/300/320/400/528 pos. The 200-pos part is 10×20 (plug 84516, receptacle 84517/55724/84535) | 4, 5.5, 6, 8, 10, 11.5, 12, 14 mm | "up to 32 Gb/s", documented at 4 mm and 14 mm stacks [1]. An older FCI sheet says 28 Gb/s at 4/6 mm [2][3] | Yes on paper. SI at intermediate heights isn't stated | Two-piece BGA plug and receptacle, push-on, keyed, chamfered lead-in [3]. Bolts aren't intrinsically required. Retention comes from the system (Apple used a clamp and 4 screws on the card [5]) | **Not found** in the public sources I read | **Yes.** 200 pos gives about 145 spare over 55 display pins. 300 pos gives margin for PCIe x8 + DP + GND |
| **Samtec SEARAY 0.8 mm (SEAF8/SEAM8)** [4] | 0.80 mm. Listed mated sets of 60–320+ pos, e.g. 200 (50×4, 20×10) and 240 (30×8, 40×6) | 7 or 10 mm | 28 Gbps NRZ / 56 Gbps PAM4. Samtec lists PCIe 4.0 as "Capable" [4] | Yes | Two-piece open-pin-field, SMT solder charge. Friction retention. Samtec's page lists no mandatory screws | Not on the page I read | **Yes.** 200–240 pos works as a backup (see below) |
| **Samtec Z-Ray ZA8/ZA8H compression interposer** [6][7] | 0.80 mm (ZA1 1.00 mm). Up to 50×50 dual-compression. Standard parts about 400 contacts | about 1.0 mm interposer (custom 0.5–4 mm) | Datasheet: "up to 14 Gbps (ZAX)" [6]. Press release: "28+ Gb/s" [7]. These conflict | HBR3 yes. Gen4 only on the 28 Gb/s claim | **Needs screw-down and alignment hardware** [7] and compression across the board pair, so in practice also a stiffener or backer (mechanical downside) | Press release: "increased cycle life", no number | Yes on pin count. Mechanically the worst fit (bolts, stiffener, flatness) |
| **Hirose FX23** [8][9] | 0.5 mm. 20–120 signal + 4 power | 8–30 mm (stacking); right-angle versions exist | 16 Gbps, PCIe Gen4 [8] | Yes, with no margin above Gen4 | Floating ±0.6 mm X/Y, guide posts | **100** [9] | Only marginal. 120 signal pins minus 55 leaves 65 for PCIe x8 + GND, so it's tight and would need ground planning |
| **Hirose IT3 / IT5** [10][11] | 1.5 mm staggered BGA. 100/200/300 | IT3: 17–42 mm | IT3 10+ Gbps (−2 dB to 12 GHz). IT5 25+ Gbps | IT3 **no** for Gen4 and is "not recommended for new design" [10]. IT5 possibly yes | 3-piece with interposer | 100 [10] | Pin count yes, but the 17 mm+ height is likely too tall. IT3 should be dropped |
| **Molex Mirror Mezz** [12] | Hermaphroditic, 4.0 × 1.5 mm pair pitch. Up to 270 pairs | 5, 8, 11 mm | up to 224 Gbps | Yes (overkill) | BGA, self-/cross-mate | not read | Yes. Server/OCP-class part, probably costly and BGA |
| **Molex NeoScale** [13][14] | 2.80 mm triad. e.g. 216 circuits (4×18) | 12–42 mm | up to 56 Gbps | Yes | 2-piece | **100** [14] | Yes on pins. Too tall at 12 mm minimum |
| **TE Free Height** (search synthesis only) | 0.5 / 0.8 mm | 5–20 mm | 25+ / 32 Gbps | Probably | not verified | not verified | **Unverified.** No TE datasheet was opened |

**Pins freed vs MCIO-74:** none of these "frees" pins by itself. A single 200–300 pos array (MEG-Array, SEARAY, Mirror Mezz) replaces J_PCIE (MCIO-124) and J_DISP (MCIO-74), 198 contacts in total, with one connector. That leaves room for about 55 display pins next to PCIe x8. A 120-signal FX23 can't replace both.

### Mac Pro 6,1 Meg-Array claim: verified in part
- **Verified:** iFixit's teardown, step 11, says "This FCI Meg-Array connector … looks to be a fully custom way of hooking up PCI-E, with many pins in a pressed-in connector". The connectors were pried out with a spudger, and ribbon cables connect to the interconnect board (step 15) [5]. Apple sells the graphics-board cable and the interposer flex cable as separate service parts (923-0500, 923-0496) [15][16].
- **Verified:** 1.27 mm pitch, up to 32 Gb/s, 4–14 mm stack heights, and a 200-pos size exist [1].
- **Not verified:** that Apple's part is the 200-pos size, that the flex has a Meg-Array at *each* end, and anything from the Apple service manual (I didn't open it). "No bolts" holds for the connector itself, but the GPU card is held by a clamp and 4 screws [5].
- **Caveat:** 32 Gb/s is documented only at 4 mm and 14 mm stacks [1]. An older FCI spec (GS-20-033) says the taller stacks support 10 Gb/s and that the 4/6 mm stacks were tested to 28 Gb/s [3]. That's still well above HBR3 and Gen4, but heights of 8–12 mm need SI & Fab to check the S-parameters.

### SEARAY 0.8 mm at 200–240 pins as the backup
It works on paper. Standard mated pairs exist at 200 pos (SEAF8-50-05.0-S-04 / -20-…-10, 7 mm) and 240 pos (7 mm and 10 mm variants). It's rated 28 Gbps NRZ and Samtec lists it as PCIe 4.0 capable [4]. It's a press-fit, push-on board-to-board part with no screws listed, so it avoids Z-Ray's bolts and stiffener. It's board-to-board only, so a cable or flex version would be a separate product line (not researched).

## Ranked shortlist
1. **Amphenol MEG-Array 200/300 pos.** Proven in the Mac Pro 6,1 [5], push-on, 32 Gb/s [1], 4–14 mm heights, and enough pins for PCIe x8 + 3× DP + GND.
2. **Samtec SEARAY 0.8 mm 200–240 pos.** Backup with a smaller footprint, 28 Gbps / PCIe 4.0 capable [4], 7/10 mm stacks, no bolts.
3. **Molex Mirror Mezz.** Big SI margin and 5 mm stack, but a server-class part whose cost and availability are unverified.
4. **Hirose FX23 120 pos.** Gen4-rated and floating (tolerant of misalignment), but the pin count is tight and it's rated for only 100 cycles.
5. **Samtec Z-Ray.** Lowest profile, but it needs bolts and a stiffener, and its data-rate figures conflict (14 vs 28+ Gbps).

Ruled out: Hirose IT3 (NRND, 10 Gbps), Molex NeoScale (≥12 mm, 2.8 mm pitch).

## Gaps (not verified, so no guesses)
- Distributor stock and pricing for every part. I checked none, and requested no quotes.
- Mating-cycle ratings for MEG-Array, SEARAY 0.8, Z-Ray and Mirror Mezz.
- Exact footprint dimensions (mm × mm) for each candidate. Datasheet drawings weren't extracted.
- Apple's Meg-Array position count, the connector at each end of the flex, and the Apple service manual content.
- MEG-Array SI at 6–12 mm stacks, and whether its retention force is enough without a clamp.
- TE Free Height and any TE compression part. No datasheet was read.
- Whether a flex/cable version exists for MEG-Array or SEARAY 0.8 (the Mac Pro used custom flex).
- JLC/LCSC availability, which matters for the project's cost rule (§1.6). MEG-Array, SEARAY and Mirror Mezz are BGA or solder-charge arrays and may need X-ray inspection.
- Whether the MCIO-74 contact count (74) is all signal or includes ground. I took it from the part name and spec, not a re-read of SFF-TA-1016.

## Sources
1. Amphenol MEG-Array datasheet: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf
2. Amphenol MEG-Array series page: https://www.amphenol-cs.com/product-series/meg-array.html
3. FCI/Amphenol GS-20-033 application spec: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/gs-20-033.pdf ; older FCI sheet: https://www.farnell.com/datasheets/2357990.pdf
4. Samtec SEAF8: https://www.samtec.com/products/seaf8
5. iFixit Mac Pro Late 2013 teardown (steps 11, 12, 15): https://www.ifixit.com/Teardown/Mac+Pro+Late+2013+Teardown/20778
6. Samtec Z-Ray ZA8/ZA8H catalog page: https://media.ic-find.com/datasheets/e57ed03c88110c576a2d22b13342f92b.pdf
7. Connector Supplier, Samtec Z-Ray: https://connectorsupplier.com/samtec-z-ray-ultra-low-profile-ultra-high-density-interposers/
8. Hirose FX23: https://www.hirose.com/en/product/series/FX23
9. Hirose FX23 part list: https://www.hirose.com/en/product/c/FX23
10. Hirose IT3 part list: https://www.hirose.com/en/product/c/IT3
11. Hirose IT3 catalog: https://www.hirose.com/en/product/document?clcode=&documentid=en_IT3_CAT&documenttype=Catalog&lang=en&productname=&series=IT3
12. Molex Mirror Mezz: https://www.molex.com/en-us/products/connectors/board-to-board-connectors/mirror-mezz-mirror-mezz-pro-connectors
13. Molex NeoScale brief: https://www.molex.com/content/dam/molex/molex-dot-com/en_us/pdf/application-briefs/987651-6791.pdf
14. Molex 170807 series chart: https://www.molex.com/en-us/products/series-chart/170807
15. Graphics board cable 923-0500: http://www.powerbookmedic.com/Mac-Pro-Graphics-Board-Cable-Late-2013-p-161470.html
16. Interposer flex 923-0496: https://www.macpartstore.com/product/923-0496-cable-flex-interposer-board-mac-pro-late-2013/
