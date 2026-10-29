# MacPro6,2 connector bandwidth and options (AM5 locked baseline), 2026-10-25
Read-only study for Mechanical & Thermal. No project files changed.
**Caveat:** vendor figures below are typical published specs. The URLs are vendor series and spec pages that were **not re-fetched this run**. Check every number against the datasheet before any choice is made. Anything unconfirmed is marked GAP.

## 1. Worst-case requirements (+20% headroom)
Rates: Gen5 32 GT/s is 3.94 GB/s per lane each way. Gen4 is 1.97. HBR3 is 8.1 Gb/s. HDMI 2.1 FRL is 4 × 12 Gb/s. Ground ratio is about 1 GND per pair (G-S-S-G shared).

| Interface | Signals | GB/s each way | Diff pairs (incl. REFCLK) | Sideband | Power | Pins est. | +20% |
|---|---|---|---|---|---|---|---|
| A. CPU card edge J1 (if GPU and SSD both go through the backplane) | Gen5 x16 + Gen5 x8 (24 CPU lanes) | 94.5 | 48 + 3–5 REFCLK = 53 | PERST/CLKREQ ×5, SMBus, WAKE, PRSNT, ~14 | Standby only (6.6 A 5VSB, 2.2 A 3V3SB today); main 12 V stays on lugs (CPU at 230 W is ~25 A, ~30 pins) | 106 S + ~56 G + 14 SB + 8 PWR ≈ 184 | **~220** (current J1: 224, fully used at Gen4) |
| B. Backplane → GPU face (J9), with display through the backplane | Gen5 x16 + 4 DP ×4 HBR3 (2 USB4 DP-in, 2 DP Alt) + HDMI 2.1 FRL ×4 | 63 PCIe; display ~22 one way | 32 + 1 REFCLK + 16 DP + 4 HDMI + 4 AUX = 57 | HPD ×5, DDC, PERST, CLKREQ, SMBus, PRSNT ~14 | GPU 220–250 W is ~21 A at 12 V. Needs ~26 pins at 1 A derated, or blades. GAP: is GPU 12 V on lugs or on the connector? | 114 S + ~60 G + 14 SB ≈ 188 (+26 PWR) | **~225** (~255 with power) |
| C. Backplane → SSD face (J10) | Gen5 x8, bifurcated 2×4 or 4×2 | 31.5 | 16 + 4 REFCLK = 20 | PERST/CLKREQ ×4, SMBus, PRSNT ~12 | 4 Gen5 NVMe at ~12–14 W ≈ 56 W ≈ 5 A at 12 V, ~6–8 pins | 40 S + ~22 G + 12 + 8 ≈ 82 | **~100** |
| D. CPU board → I/O board (J3) | ASM4242 needs Gen4 x4 (8 pairs) + 2 DP-in (8 pairs, sourced from the GPU, so they may live on E instead); 2 × USB 3.2 Gen2x2 (8); USB-A via a hub uplink (2), or 4 direct 5G (8); 2 × i226 Gen3 x1 (4); USB2 ×10; REFCLK 3 | ~15 (7.9 USB4 + 5 Gen2x2 + 1.25 hub + 1 ETH) | ~38 HS + 10 USB2 ≈ 48 | PERST/CLKREQ, USB-C CC/SBU via the I/O board, ~16 | Low (USB-C PD comes from the I/O board's own feed; GAP) | 96 S + ~48 G + 16 ≈ 160 | **~190**. One MCIO-124 isn't enough |
| E. GPU display → I/O (only if not through the backplane) | 4 DP ×4 HBR3 + HDMI FRL ×4 (+AUX) | ~22 one way (UHBR on RDNA4 would be more; GAP) | 20 + 4 AUX = 24 | HPD ×5, DDC ×2 | none | 48 S + ~26 G + 8 ≈ 82 | **~100**. MCIO-74 is too small; MCIO-124 fits |

Notes: the PROM21 chipset uplink (Gen4 x4, 7.9 GB/s) still feeds most of D. ASM4242 on the chipset makes it worse. That is a lane-plan problem, and no connector fixes it. The SI budget from CPU & Base Board: a Gen5 backplane path is 18–35 dB against a 36 dB budget, so **any Gen5 path through the backplane needs a retimer** whatever connector we use. Cabled (Flyover-type) paths are the way to avoid one.

## 2. Candidate connectors (VERIFIED REV, 2026-10-25 12:45 EDT)
**What changed:** values are now cited from vendor pages and datasheets, either fetched directly or quoted by search. Items marked [CHG] differ from the earlier from-memory table. The Amphenol PDFs couldn't be downloaded with curl (the server returned HTML), so their values come from the datasheet text quoted in search results at the cited URL.

**J1 CSV re-check** (archive/kicad/macpro62-am5-v3/docs/cpulink_224_pinout_am5_v3.csv): 224 pins = 96 PCIe data (48 pairs; the AM5 column already labels x16 as Gen5 to Face P) + 78 GND + 8 standby power (6 × 5V_SBY, 2 × 3V3_SB) + 7 REFCLK lines + 4 reserved + 31 other (SATA, USB2, sideband). This confirms the earlier CPU & Base Board counts. The slot is full.

| Connector | Max rate | Positions / pitch | Height / card | A per contact | Cycles | Retention | Source |
|---|---|---|---|---|---|---|---|
| Amphenol Mini Cool Edge 0.60 mm | 32G NRZ / 56G / 64G PAM4 (PCIe Gen6); 112G PAM4 per the flyer [CHG: Gen6 confirmed] | Signal-pin options 56, 84, 140, 168, 280 (+ custom; our 224 is one); **largest standard is 280** [CHG] | 1.6 mm mating card standard; 1.97 / 2.36 mm on request [CHG: a ~2.0 mm card is possible on request]. RA seating 3.05–7.05 mm | 1.1 A signal; up to 12 power pins at up to 25 A each in the hybrid version [CHG] | 200; 10k high-cycle option [CHG] | Card edge; optional latch and metal key | https://www.amphenol-cs.com/product-series/mini-cool-edge-0-60mm.html ; https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/general/mini-cool-edge-flyer.pdf ; https://www.farnell.com/datasheets/3212940.pdf |
| SFF-TA-1002 (EDSFF/OCP 3.0) | Implemented by Mini Cool Edge (above), so same ratings | 4C = 140, 4C+ = 168 (MCE options) | 1.57/1.6 mm | 1.1 A | 200 | Card edge | Same as above. GAP: SNIA spec text not opened |
| MCIO (SFF-TA-1016) | Gen5 32 GT/s; Gen6 on current Amphenol cable parts | 38/50/74/100/124/148 pos, 0.6 mm [CHG: 148-pos 24X exists] | Plug paddle 1.57 mm | **0.5 A** on current listings (an older sheet says 1 A) [CHG] | 250 min | Active latch | https://www.amphenol-ast.com/v3/en/product_view.aspx?id=370 ; https://www.amphenol-ast.com/V3/UpLoadFiles/20180527/MCIO_CA_Tech_Datasheet.pdf |
| Molex NearStack PCIe | Gen5 32G NRZ, roadmap Gen6 | x8: 18 pairs + 16 SE (72-pin) | Low profile | 0.65 A per mated pair; 0.30 A single-ended [CHG] | 200 (product spec) vs 100 min (datasheet) | Metal shroud + positive latch; 65 N rip-out | https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/208/208021/2080210001-PS-000.pdf |
| Molex NearStack HD | **Gen6 64G PAM4** [new] | 56 circuits (18 pairs); x16 needs two | 9.50 mm high; cable 110 mm–1 m | 0.65 A | 100 min | Latch | https://www.molex.com/content/dam/molex/molex-dot-com/en_us/pdf/datasheets/987652-6741.pdf |
| Samtec AcceleRate HD | 64G PAM4 / 32G NRZ, PCIe 6.0 capable [CHG] | Up to 400, 0.635 mm, 4 rows × 10–100 | 5–16 mm stack [CHG], 5 mm wide | 1.34 A [CHG] | GAP (described as "high-cycle") | Friction; optional guide-post standoffs | https://www.samtec.com/connectors/high-speed-board-to-board/high-density-arrays/accelerate-hd |
| Samtec SEARAY 0.8 (SEAF8/SEAM8) | 28G NRZ / 56G PAM4. Not marketed as Gen6 | 40–500, 0.80 mm (≤10 rows × 50) | 7 or 10 mm only | 1.3 A | GAP | Friction, solder charge | https://www.samtec.com/products/seaf8 ; https://www.samtec.com/high-speed-board-to-board/high-density-arrays/searay-8mm/ |
| Samtec Flyover ExaMAX cable | 112G PAM4, PCIe 6.0 capable | 16–96 pairs, 2.00 mm | Cable | GAP | 200 | Guide / latch | https://www.samtec.com/high-speed-cable/flyover/examax/ |
| Samtec NovaRay I/O | 128G PAM4, PCIe 7.0 capable | GAP | Panel-mount cable (external I/O, not internal) | GAP | GAP | – | https://www.samtec.com/high-speed-cable/flyover/novaray-io/ |
| Molex Mirror Mezz Pro (218910/218916) | 112 Gbps | Up to 270 pairs; 4.00 × 1.50 mm pair pitch, hermaphroditic | Stacks 5 / 8 / 11 mm (2.5 + 2.5, etc.) | 1.0 A (0.75 A on 1 oz Cu, 1.2 A on 2 oz) | **100** | Friction; 1.0–1.2 mm gatherability | https://www.molex.com/content/dam/molex/molex-dot-com/en_us/pdf/datasheets/987652-0673.pdf ; https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/202/202828/2028280001-000.pdf |
| Amphenol MEG-Array | 32 Gb/s (at 4 and 14 mm stacks) | 81–528, 1.27 mm | 4–14 mm | **0.45 A all contacts energized** (2 A single contact) [CHG] | 50/100/200 options (the GS-12-100 spec says 50) [CHG] | System clamp | https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf |
| PCIe CEM x16, Amphenol ExaMAX/Paladin, SlimSAS | Not re-verified this run. Kept as background only | | | | | | GAP |

## 3. Ranking per interface (quality first). Changes after verification:
- [CHG] AcceleRate HD is confirmed Gen6-capable with a 5 mm minimum stack and 1.34 A. It is now the first-choice board-to-board part on the faces, ahead of Mirror Mezz Pro, which has only 100 cycles and a coarse 4 mm pair pitch.
- [CHG] SEARAY 0.8 drops: it isn't marketed for Gen6, and 7 mm is its lowest stack.
- [CHG] MEG-Array is ruled out for Gen5 power and signal use: 32 Gb/s, 0.45 A, as few as 50 cycles.
- [CHG] A 280-pin Mini Cool Edge exists and its hybrid version carries power at up to 25 A per pin. A 280-pin J1 would cover A (~220) with ~27% headroom and could even carry 12 V. GAP: does a 280 receptacle (~25% longer) fit Apple's base-connector area?
- [CHG] For cables, MCIO is 0.5 A per pin, so it carries signals only. NearStack HD (Gen6) or Flyover ExaMAX (Gen6) are the cable picks.

**A. CPU card edge**
1. **Take the GPU x16 off the card edge** with a Gen5/Gen6 cable (Samtec Flyover or Molex NearStack x16, or MCIO-124 Gen5) from beside the socket to the GPU face. This saves the backplane loss and likely the retimer. J1 then carries only SSD x8 + sidebands (~100 pins of 224), and the existing MCE 224 fits Apple's slot. GAP: is there cable routing room past the core and brackets?
2. Keep everything on the edge with a Gen6-rated Mini Cool Edge 224 (or larger, if Amphenol makes one that fits Apple's footprint; GAP). That's ~220 needed against 224, with no headroom, and a Gen5 retimer is required on the CPU side.
3. SFF-TA-1002 4C+ (168) plus a second 2C connector. Positions are short with one connector, and two may not fit Apple's footprint (GAP: footprint length).
Card thickness: every card-edge option needs 1.57 mm. Our 1.6 mm board is fine; a 2.0 mm card isn't accepted.

**B. Backplane → GPU face**
1. Direct Flyover/NearStack cable from the CPU board (as A1), with display on a separate MCIO-124 Gen5 cable. Retimer likely not needed.
2. Samtec AcceleRate HD or Molex Mirror Mezz Pro (~250+ pos), with low stack and Gen6 margin, replacing MEG-Array (32 Gb/s has no Gen5 margin). It fits the 5 mm-class stack. Retimer still needed via the backplane.
3. SEARAY 0.8 (300–400 pos): proven, but the rating is borderline for Gen5 (28 NRZ).
Power: keep GPU 12 V on lugs or blades, not signal contacts.

**C. Backplane → SSD face:** 1) MCIO-124 Gen5 (one connector carries x8 + 4 REFCLK + sidebands), 2) AcceleRate HD ~120 pos, 3) SFF-TA-1002 2C card edge. A retimer is likely needed if it runs through the backplane (a Gen5 x8 retimer, or a switch on the SSD board).

**D. CPU/base → I/O:** 1) two cables, MCIO-124 + MCIO-74 (Gen5-rated parts even though the traffic is Gen4), 2) a NearStack x16 + x8 pair, 3) one AcceleRate HD mezzanine if the I/O board is rigid-mounted (GAP: mechanics). No retimer at Gen4.

**E. GPU display → I/O:** 1) through the backplane, inside B's connector (preferred), 2) MCIO-124 cable (MCIO-74 is too small for 4 DP + HDMI FRL), 3) a Y-split flex.

## 4. Decisions for Aidan
1. Allow the GPU x16 (and maybe the SSD x8) to leave the CPU board by cable instead of the card edge and backplane? This is the best SI result and frees J1.
2. If not, accept Gen5 retimers on the backplane paths (cost, power ~5–10 W, heat).
3. Replace MEG-Array (32 Gb/s) on the faces with a Gen5/Gen6-rated mezzanine (AcceleRate HD / Mirror Mezz Pro).
4. Move ASM4242 to CPU lanes (SSD to Gen5 x4) or accept the chipset oversubscription. A connector can't fix this.
5. Measurements needed: the length of Apple's base connector footprint, and cable routing room around the core.
