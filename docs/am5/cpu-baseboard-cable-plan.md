# MacPro6,2 v3 face interconnect plan: CB → BP → Face P / Face S
Written 2026-10-21 (ET). Target approved by Aidan on 2026-10-21: Ryzen 7000/9000 with GFX x16 (an 8000G still drops in at x8), stock 450 W PSU with firmware limits, and the BP v3 changes (INA226, J7 DNP, storage-face deviations).
Sources: `boards/base-v3/kicad/backplane.kicad_pcb` (read with pcbnew; not modified), `fitcheck_mcio_o10.txt`, ICD v3 §5/§14/§20, and the vendor datasheets cited below. Nothing has been ordered or submitted.

## 1. Interconnect per lane group

### 1.1 Connector positions (BP v3 PCB, KiCad sheet coordinates in mm, F side)
| Ref | Part | KiCad X, Y | Rot | BP frame (ICD fp6) | Function |
|---|---|---|---|---|---|
| J1 | Amphenol ME1022410103011 Mini Cool Edge 224, vertical (LCSC C4941560, 0 stock / pre-order) | 150.000, 112.600 | 180° | – | CPU-LINK from the CB tab |
| J9 | MCIO 124P RA, G97R24332HR class (LCSC C4867471, 0 stock) | 164.679, 78.249 | −45° | (14.68, 21.75), s = +5.0 | Face P x16 |
| J10 | MCIO 124P RA, same part | 130.724, 87.795 | +45° | (−19.28, 12.20), s = +5.0 | Face S slot A x4 + slot B x4 |
| J3 | JST BM15B-GHS-TBT GH15 (C5305069) | 192.5, 86.5 | 45° | (42.5, 13.5) | Face P AUX |
| J4 | JST BM15B-GHS-TBT GH15 | 147.5, 56.5 | 45° | (−2.5, 43.5) | Face S AUX |
| J7 | M.2 M-key (C841661) | 130.0, 130.0 | 90° | – | **DNP (approved)** |

### 1.2 Lane groups
| Group | CPU source (CB AM5 v3) | Path | BP connector → cable → module connector | REFCLK / PERST# | Width (7000/9000) | Width (8000G) |
|---|---|---|---|---|---|---|
| Face P | GFX x16 (Gen5-capable; the BP is budgeted for Gen4 with redrivers removed) | CB J1 fingers → BP J1 → BP L1/L3 → **J9** | MCIO-124 straight ↔ straight, crossed (P1 B-n ↔ P2 A-n), ≈ 55 mm → Face P J_PCIE (module X 47.0) | REFCLK0 = CPU GPP_CLK; PERST0# = PLTRST# ∧ FACE_P_RDY | x16 | x8 (lanes 8-15 idle) |
| Face S slot A | GPP#1 x4 → FS 0-3 | J1 → **J10 set A** | same cable part → Face S J_PCIE | REFCLK0; PERST0# = PLTRST# ∧ FACE_S_RDY | x4 | x4 |
| Face S slot B | GPP#2 x4 → FS 4-7 (CPU-LINK v3 pins) | J1 → L1/In2/In3/B.Cu → **J10 set B** (A/B 20-36) | same cable (one 124P cable carries both slots) | REFCLK1 (J10 A29/30); PERST1# B29 (R64/Q12); CLKREQ1# pulled up (R65) | x4 | x4 (GPP#2 exists on 8000G) [Inference, confirm against the AMD 8000G lane map] |
| Face P display | Face GPU DP → J_DISP | not on the BP | MCIO-74 to IOB J2 (DISPLAY-LINK) | – | – | – |
| Face AUX | BP MCU sideband | J3 / J4 | GH15 cables, ≈ 56 / 64 mm lateral run | – | – | – |

### 1.3 Cable spec (one part number for both faces)
- **Type (DECIDED 2026-10-21): 32 AWG, 85 Ω twinax, ribbon**. Shielding and drain wire are the same as the 30 AWG part (pair shield + drain, polyester jacket, per the Amphenol AST spec). Gen5-rated. **Narrow plug (no anti-skew flanges)** is mandatory at the module end: the J_PCIE/J_DISP plug gap is 1.30 mm, and a flanged plug overlaps by 1.45 mm. Latch type is thumb release or pull tab; check the latch envelope (z 10.0 at the BP end). The ≈ 55 mm length makes 32 AWG insertion loss negligible (well under 1 dB at 16 GHz).
- **Length:** mating face ↔ mating face is 52.8 mm (J9) / 56.3 mm (J10) at a GPU-edge height M1 = 15 mm, and 61.3 / 64.8 mm at 23.5 mm. **Order 55 mm ± 2.** If the M1c / C-16 measurement comes back at 23.5 mm, use **63 mm ± 2**. The free cable between plug rears is 26.4 / 29.9 mm (M1 15).
- **RFQ must-haves (U-21, not sent):**
  1. Written confirmation that the 32 AWG 85 Ω ribbon cable's **minimum bend radius is ≤ 3.6 mm**.
  2. For the receptacle, Amphenol's written **PCIe Gen5 (32 GT/s) rating for G97R24332HR**, with its customer drawing including the peg PTH and solder-ring dimensions.
- **Vendor:** a custom length is needed because the catalogue minimum is 150 mm. Candidates:
  - Amphenol AssembleTech, MCIO-124ST plug family (DS-0002).
  - Molex 216610 series; 2166101121/-1125/-1135 are the 150 mm references and fine as a **fit sample**.
  - ACES "MCIO_124P_16i_ST_85ohm" (29 AWG, pull tab, ≤ 1 m).
  - TE.
  - RFQ is U-21. It is **not sent**.
- **Minimum bend radius, 32 AWG 85 Ω (Amphenol AssembleTech MCIO cable datasheet):**
  - Ribbon thickness: 0.71 mm.
  - 2.5 × thickness rule: R ≥ **1.78 mm**.
  - One-layer ribbon table (2018-05-29 sheet): R ≥ **3.55 mm**. This is the governing value.
  - Discrete 32 AWG for reference: 0.65 mm thickness, 2.5× rule = 1.63 mm, table value 3.25 mm.
  - Molex 216610 gives no value; ask for it in the RFQ.
- **Design bend radius: R_c 3.6 mm**, the value already used by the BP fit check. It is ≥ 3.55 mm, so it passes, but with only 0.05 mm margin. **The RFQ must state "32 AWG 85 Ω ribbon, min bend radius ≤ 3.6 mm, written".**
- *Rejected alternative (30 AWG):* 0.85 mm thick, one-layer bend radius 4.25 mm. That pushes the bend outer face to about r 66.5 and needs a keep-out of r ≤ 67.2 mm, which is +0.7 mm on the fillet.

### 1.4 Clearances for Mechanical & Thermal at the filleted bottom (base ring)
These come from `fitcheck_mcio_o10.txt`. n is radial from the BP centre, z is height above the BP top surface, and BP rim r = 61.0.

| Item | J9 (Face P) | J10 (Face S) |
|---|---|---|
| BP plug body, radial span | n 31.78 – 44.98 | n 28.29 – 41.49 |
| Plug latch height | z 10.0 | z 10.0 |
| Ribbon top in the straight run | z 4.5 | z 4.5 |
| Clearance ribbon → GPU board bottom edge | 10.4 mm (edge z 15) / 18.9 mm (edge z 23.5) | same |
| Face board plane | n 55.0 – 56.6 from z 15 | same |
| **Bend outer face (32 AWG, R_c 3.6, thickness 0.71)** | **n 61.1, r ≤ 65.8 over z 1.5 – 8.2 → 0.1 mm beyond the BP rim** | same |
| Ribbon corridor width | s +5.0 ± 19.3 (≈ 38.6 mm), free of parts (nearest J3 2.91 mm) | nearest J4 6.45 mm |

**Ask to Mechanical (M1b), 32 AWG:**
- Keep the base-ring / fillet inner surface out of **r ≤ 66.5 mm for z 1.5 – 8.5 mm**. That is the bend outer face (r ≤ 65.8 at R_c 3.6) plus a 0.7 mm margin.
- The thinner 0.71 mm ribbon only reduces the outer face, so the 65.8 mm bound is conservative.
- The keep-out covers the ≈ 38.6 mm-wide sector at each MCIO (J9 at −45°, J10 at +45°).
- Stock hole S5 (18.49, 50.72) sits under the J9 ribbon. Keep the surface flat there: no screw head, ≤ z 1.5 (CR-BP-1).

**Thermal:**
- The ribbon is a ≈ 38.6 × ≤ 4.5 mm obstruction across the bottom intake at each face.
- MCIO cable operating range is 0 – 80 °C (Amphenol). Keep local air ≤ 70 °C.

## 2. Second sources for the J9/J10 receptacle (G97R24332HR)
Web check on 2026-10-21, read-only. Stock figures are whatever the pages showed and should be confirmed before ordering.

| Part | Mfr | Type | Pin/footprint compatible? | Stock seen |
|---|---|---|---|---|
| **G97R24332HR** (current) | Amphenol | MCIO 124P RA, 85 Ω, 30 µ" | – | **LCSC C4867471: 0.** Newark/Farnell (30AK6208): 20 pcs, ≈ CA$11.73. Heilind: call. **Not listed** at Mouser or Digikey in search results |
| **Molex 2173463021** | Molex | MCIO RA 16x Gen5 124P, 30 µ" Au, 1.50 mm peg | **Pin- and peg-compatible (see §2.1)** | RADIOMAG: on order, 120 pcs, 10-14 days, €26.81 @1. Chinese brokers claim stock (unverified). Mouser/Digikey: not confirmed |
| Molex 2173463011 / -3022…-3026 | Molex | same, 15 µ" or other peg lengths | Yes. Prefer the **1.50 mm peg** (-3011 / -3021) for a 1.6 mm BP | not checked |
| ACES 52730-1247D-021 (expected PN) | ACES | MCIO Gen5 R/A 85 Ω 124P | SFF-TA-1016, so probably compatible; **no datasheet confirmed** | **Not found** at Digikey. Digikey stocks only the ACES 124P **vertical** 52729-1247D-021 (200 pcs) and the RA 38P/74P |
| Amphenol G97V24332HR | Amphenol | 124P **vertical** | **No.** A vertical part would need a BP re-layout and a different cable exit | Newark 184 / 1715 pcs |

### 2.1 Molex 2173463021 vs Amphenol G97R24332HR (datasheet check, read-only)
| Item | Molex 2173463021 (sales drawing 2173463021_sd, product page) | Amphenol G97R24332HR | Our footprint `MP62_MCIO_124P_RA_SFF-TA-1016` |
|---|---|---|---|
| Rating | **PCIe Gen5, 32.0 Gbps data rate**, 85 Ω, SFF-TA-1016 MCIO, 200 cycles, 1.1 A/contact | MCIO R/A 85 Ω 124P 30 µ" (distributors), 0.5 A, card 1.57 mm. **Gen rating not confirmed:** the Amphenol drawing PDF is behind a Cloudflare block, so it could not be read | – |
| Contact pitch / rows | 0.60 / pad rows 0.575 and 3.525 from datum | 0.60 / SFF-TA-1016 land | 0.60 / 0.575, 3.525 |
| NPTH locating pegs | 2 × Ø1.10 ± 0.05 at **40.645** spacing (housing posts) | SFF Table A-2 [Inference: same, not read from the Amphenol drawing] | 2 × Ø1.1 at ±20.3225 (= 40.645) ✔ |
| Shell solder pegs (PTH) | 4 × at **41.70** spacing, y **1.775 / 4.325**; peg length 1.50 (‑3021); drawing shows 1.10 / 1.50 PTH dims with a 2.00 solder ring | SFF Table A-2 [Inference] | 4 × oval drill 0.6 × 1.5, pad 1.0 × 1.9 at ±20.85, y 1.775 / 4.325 ✔ positions |
| Min board edge | 6.025 | SFF | 6.025 used for the mating-face calculation ✔ |

**Verdict:**
- All peg and pad positions match, so the Molex part drops onto the current footprint.
- **One open check:** the Molex PTH drill/slot size and solder ring (1.10 / 1.50 / 2.00 on the drawing) against our 0.6 × 1.5 oval drill with a 1.0 × 1.9 pad. The ring may need enlarging to 2.0 mm. That would be a footprint change, which is not made here.
- Amphenol's Gen5 rating needs its drawing or datasheet, retrieved manually.

**Recommendation:**
1. Qualify **Molex 2173463021** as the alternate on the BP BOM. Order through Farnell/Newark/Mouser and confirm the footprint pegs.
2. Buy the 20 G97R24332HR at Newark for the prototype.
3. JLC assembly will need consigned parts, because LCSC shows 0 stock.

## 3. Doc lines that conflicted with the approved 7000/9000 x16 target
Snapshot taken before the edits in §4.

| File:line | Conflicting text (abridged) |
|---|---|
| archive/kicad/macpro62-am5-v3/README.md:8 | Target Ryzen 5 8600G / 7 8700G (Phoenix) at cTDP 45 W; 7000/9000 "later option" |
| macpro62-am5-board-plan.md:13-14 | CPU = 8600G/8700G; power cTDP 45 W, PPT ≈ 61 W |
| macpro62-am5-board-plan.md:19 | "8000G GFX x8 → Face P" as the design case |
| macpro62-am5-board-plan.md:48, 135-136, 167-168 | DXIO GFX x8; lane table x8 live, lanes 8-15 unused |
| macpro62-am5-board-plan.md (lane map) | GPP x4 → M.2 boot (v3 moved it to the PROM21 free x4) |
| macpro62-am5-board-plan.md:65, 318, 349 | fixed cTDP 45 W fallback / decision D-A3 |
| macpro62-am5-board-plan.md:315, 320 | R-A2 "keep the LGA1700 CB as the parallel path"; R-A7 "8000G caps Face P at x8" |
| macpro62-architecture-spec-v0.2.md:126 | "LGA1700 CB unchanged and still primary" |
| macpro62-architecture-spec-v0.2.md:128-129 | Platform 8600G/8700G cTDP 45 W; GFX x8 → Face P; GPP x4 → M.2 boot |
| macpro62-architecture-spec-v0.2.md:274 | "Own LGA1700 board CB (primary since 2026-10-01)" |
| macpro62-architecture-spec-v0.2.md:1037 / ICD v3:402 | LPT actuator = Intel PL1/PL2 via SMM MSR (AM5 = PPT/TDC/EDC via SMU) |
| macpro62-interface-control-v3.md:54-55 | FP/FS_REFCLK = PCH SRCn (U-12); SATA0 = PCH HSIO (U-13) |
| macpro62-interface-control-v3.md:348-360 | §12 lane map = Z790 PCH table |
| macpro62-interface-control-v3.md:466 | O-7 PECI on Raptor Lake |
| macpro62-interface-control-v3.md:487-488 | U-12 / U-13 Z790-specific |
| macpro62-interface-control-v3.md:546-564 | §19 "8000G… FP 8-15 not driven… GPP x4 → CB M.2… cTDP 45 W" |
| macpro62-interface-control-v3.md:613 | 447 W > 445 W ceiling "LPT caps PPT or 45 W Eco" (now covered by the approved firmware limits) |

## 4. Edits made after approval
See the change log in the agent summary. Backup: `/workspace/backups/docs_pre_am5x16_20261021-144031.tgz`.

### Change log (2026-10-21 ≈ 14:41 ET; no KiCad boards touched)
- `archive/kicad/macpro62-am5-v3/README.md`: added a banner with the approved target and rewrote the Target line (x16; 8000G as an x8 drop-in).
- `macpro62-am5-board-plan.md`: added a banner and updated the CPU bullet, the Face P lane bullet, and the two GFX rows in the lane table.
- `macpro62-architecture-spec-v0.2.md`: marked change 35 as superseded, added **change 36** (AM5 v3 is the board of record, plus the lane map, power and BP approvals), and updated the LGA1700 table row to "parked".
- `macpro62-interface-control-v3.md`:
  - Added a header note with the approvals.
  - FP/FS_REFCLK row: U-12 closed on AM5.
  - §12: added an AM5 note, rewrote the CPU rows (GFX x16, GPP#1, GPP#2) and added rows for PROM21 x4 and J8 M.2 on PROM21.
  - O-7 struck through as moot.
  - U-12 and U-13 reworded for AM5.
- Not changed (history only): the PCH HSIO rows in §12, §19 (8000G draft), and the 8000G detail sections in the board plan (§2 table, R-A/D-A items).

### Peg solder-ring change (2026-10-21 ≈ 14:45 ET): attempted, then reverted
- Tried pad 1.1 × 2.0, then 1.0 × 2.0 (was 1.0 × 1.9) on the 4 MP pegs in the library footprint and on J9/J10.
- Both sizes gave **1 DRC clearance error**: J10 MP peg (GND) at (148.53, 76.11) against the routed track FP_TX1_N on L3, at 0.083 mm and 0.097 mm vs the 0.1 mm rule.
- The fix needs the Face P TX1 pair moved. That is not trivial, so both files were restored from `backups/backplane-v3_pre_pegring_20261021-144326.tgz`. After the restore, DRC is back to 0 / 0 / 0 and ERC is 0.
- J9 had no conflict.
- The Molex part still fits the current 1.0 × 1.9 pad by position. The ring size is a solderability margin item to confirm with the drawing.
