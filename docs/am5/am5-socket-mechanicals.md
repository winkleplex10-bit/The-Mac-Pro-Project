# AM5 (LGA1718) socket mechanicals vs Mac Pro 6,1 core — public sources only
Status: research note, non-fab. No board files edited. 2026-10-21.

## AM5 public data
| Item | Value | Source |
|---|---|---|
| Package / IHS outline | 40 x 40 mm lidded package | https://en.wikichip.org/wiki/amd/packages/socket_am5 ; https://en.wikipedia.org/wiki/Socket_AM5 |
| Seated lid-top height above PCB top | 7.98 ± 0.60 mm (AMD drawing, as reported) | https://www.igorslab.de/en/amds-socket-am5-mounting-technical-data-and-the-fitting-boxed-coolers/ ; WikiChip (above) |
| Socket mechanism footprint (backplate/stiffener/force frame/lever) | 67 x 106 mm | WikiChip (above) |
| Stiffener-frame (ILM) attachment | 4 captive #6-32 Torx T20 screws into PEM nuts on backplate, through PCB | WikiChip; Thermalright ASF manual https://eu.manuals.plus/asin/B0CYQ3LDML |
| ILM screw torque | 12 in-lbf (~1.36 N·m) recommended | ASUS install guide https://dlcdnets.asus.com/pub/ASUS/mb/13MANUAL/E_MB_Installation_Guide_EM_WEB.pdf |
| Backplate | fixed to board on AM5, not removable; variants per PCB thickness | Noctua FAQ https://www.noctua.at/en/support/faqs/does-my-amd-motherboard-come-with-a-backplate-and-how-do-i-proceed-with-the-installation ; WikiChip |
| Frame material | 1.2 mm stainless force + stiffener frames, 2 x 0.18 mm insulators | WikiChip |
| ILM screw X/Y positions vs socket center | **GAP** (AMD mechanical drawing is partner-only; no public dimensioned drawing found) | — |
| Lotes/Foxconn public socket drawing | **GAP** (none found) | — |
| AMD recommended / max heatsink static load on lid | **GAP** (in AMD thermal design guide, not public) | — |

## Mac Pro 6,1 reference (Xeon E5 v2, LGA2011-0)
| Item | Value | Source |
|---|---|---|
| Intel LGA2011-0 package+ILM lid-top height | 8.014 ± 0.34 mm | Intel TMDG figure quoted at https://www.overclock.net/threads/lga-2011-vs-lga-2011-v3-mounting-holes-the-same.1603137/ (secondary; primary = Intel Xeon E5-2600 v2 Thermal/Mechanical Design Guide — confirm) |
| Apple's 6,1 CPU board actual socket stack / PCB thickness | **GAP** (Apple uses its own retention; not published — measure on Aidan's board) |
| Core heatsink spring preload on CPU | **GAP** (Apple does not publish; measure) |
| Intel LGA2011 heatsink static load | **GAP** in this note (pull from the Intel TMDG if used) |

## Z-height comparison
- AM5 7.98 nominal vs LGA2011-0 8.014 nominal → AM5 lid sits **~0.03 mm lower** — effectively identical.
- Tolerances: AM5 ±0.60, LGA2011 ±0.34 → worst-case spread ≈ −0.97 to +0.91 mm.
- Conclusion: **no shim or different standoff length is needed nominally**, provided (a) our AM5 v3 PCB is the same thickness as Apple's CPU board and (b) the board-to-core standoffs match Apple's. If PCB thickness differs, change standoff length by the difference. The core's spring screws take up ±0.6 mm; verify by measuring stock 6,1 stack, then a pressure-film (e.g. Fujifilm Prescale) check on first article.

## ILM vs core-hole clearance (core holes 69.5 x 55 at (78.0,73.5) → holes at x 43.25/112.75, y 46.0/101.0)
- AM5 mechanism footprint 67 x 106 mm about socket center (78.4,73.3):
  - 106 mm along x: spans x 25.4–131.4, y 39.8–106.8 → **all four core holes fall inside the footprint**.
  - 106 mm along y: spans x 44.9–111.9 → core holes at x 43.25/112.75 are only **~0.85–1.65 mm outside the edge** (< 3 mm rule).
- Either orientation: **conflict / under 3 mm.** Exact ILM screw positions are a GAP, so a direct screw-to-hole distance can't be stated, but the stock AM5 stiffener/backplate cannot be assumed clear.
- Our socket placeholder (46.6 x 46.5 mm) is far smaller than the real 67 x 106 mm mechanism — placeholder under-reserves space.
- Options: (1) replace stock ILM with an aftermarket-style AM5 contact frame (Thermalright ASF type, same 4 ILM screws) — still needs ILM screw positions; (2) custom combined backplate/frame that carries both the ILM nuts and the core's 69.5 x 55 nuts, after measuring a real AM5 board; (3) small socket offset if one hole only grazes.

## Can a frame clamped to the core holes deliver the lid load?
- Socket contact load on AM5 is applied by the ILM force frame on the lid flanges, independent of the heatsink. The core only needs to supply heatsink/TIM pressure, like any AM4/AM5 cooler.
- AMD's allowed heatsink load: GAP. Practical public reference: AM4/AM5 coolers mount on the 54 x 90 pattern with spring screws; no AMD number published.
- Core clamping to the 69.5 x 55 holes gives a load path similar to Apple's on LGA2011; with matched z-height it should deliver comparable pressure. Verify with pressure film and compare to the 6,1 stock reading.

## Actions / gaps
1. Measure a retail AM5 board: ILM screw XY vs socket center, backplate outline, PCB thickness.
2. Measure stock Mac Pro 6,1: CPU board thickness, standoff height, lid-to-core gap, spring preload.
3. Get Intel E5 v2 TMDG primary citation for 8.014 mm.
4. Find a public AMD heatsink load limit (none found).
5. Enlarge socket keep-out placeholder to the true 67 x 106 mm mechanism.
