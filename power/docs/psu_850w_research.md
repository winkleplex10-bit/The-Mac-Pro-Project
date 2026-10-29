# MacPro6,2 custom PSU PCB, 850 W research (Rev C, 2026-10-25 ET)
Builds on `psu_baseline_study.md`. Desk research only: no purchases, pushes or contacts, and /workspace/private was not read.
Tags: [S] = sourced, [E] = engineering estimate, [GAP] = not public, needs measurement or data.
**Safety policy:** this is a requirements and architecture study, not mains construction guidance. The whole primary side (EMI filter, inrush, PFC, bulk, LLC primary, isolation barrier, earthing) must be designed, laid out, tested and certified (IEC/UL 62368-1) by qualified engineers. Nobody should open, probe or modify the stock unit's primary side.

## Decision baseline (Aidan, 2026-10-25)
850 W continuous at 12 V only, original AC inlet reused, no PSU fan (system-fan airflow), scale-back to 650–700 W kept open. Operating point until the core is tested: 142 W Eco CPU plus GPU cap, about 500–520 W.

## 1. Stock Mac Pro 6,1 PSU: what is public
| Item | Finding | Source |
|---|---|---|
| Part numbers | Service APN **661-7542**. PPN 614-0521 / 614-8521, Delta **ADP-450AF**, AcBel **FSD004** (two vendors, interchangeable). The brief's 614-0525 / 661-7563 are **not confirmed** for this unit. | [S] https://beetstech.com/product/mac-pro-a1481-power-supply-450w-661-7542 ; https://www.macpartsdepot.com/661-7542-power-supply-mac-pro-parts-for-mac-pro-late-2013.html |
| Output | 12.1 V @ 37.2 A, single rail. Standby 11 V / 5 W. | [S] iFixit teardown step 22; Apple Service Guide (baseline study) |
| Input label | 100–240 VAC, 50–60 Hz, **6 A** (from a search summary of the iFixit teardown / parts listing, **verify on the label**) | [S, unverified] https://www.ifixit.com/Teardown/Mac+Pro+Late+2013+Teardown/20778 |
| Connections | (a) **DC-Out connector** to the I/O board. (b) Separate **data/signal cable** to the I/O board. (c) **AC inlet cable** from the separate inlet part, latched plug into a socket on the PSU. (d) Bus bars to the CPU riser and GPUs (baseline study). The listing says "11 + 6 pins" (probably DC-Out and signal), **unconfirmed**. | [S] iFixit AC Socket guide steps 22–26 https://www.ifixit.com/Guide/Mac+Pro+Late+2013+AC+Socket+Replacement/21214 ; eBay listing https://www.ebay.nl/itm/188915730679 |
| Mounting | Four **9.0 mm T10** screws on the PSU sides. The PSU+I/O assembly is held by four **5.5 mm T8** screws. The PSU cage has two 3.6 mm T5 screws, and removing it exposes the primary. | [S] iFixit AC Socket guide steps 18–23 |
| AC inlet | Separate part **923-0505**, held to the I/O panel by four T4 screws and wired to the PSU. **Its current rating is not published [GAP].** | [S] https://warriormac.com/shop-online/io-boards-audio/ac-power-inlet-923-0505 ; iFixit steps 31–32 |
| Discharge warning | iFixit: unplug, hold the power button 10 s, and don't touch capacitor leads or the solder side. | [S] iFixit guide intro |
| Pinouts (DC-Out, signal), PS_ON / PG / SMBus/PMBus, OCP/OPP, hold-up, efficiency, PCB outline, dimensions | **[GAP]**, not found publicly. pinoutguide.com's "Apple Mac Pro PSU J1/J2/J3" pages appear to cover the older tower Mac Pro, **not** the 6,1. No public boardview or schematic for the PSU itself was found. The I/O-board (820-xxxx) boardview may show the PSU signal connector names. | https://pinoutguide.com/Power/ |

## 2. High-density 800 W–1 kW 12 V reference designs
| Design | Power / topology | Efficiency | Size / density | Cooling, hold-up, notes |
|---|---|---|---|---|
| **TI TIDA-010062** | 1 kW, 12 V/84 A. GaN CCM totem-pole PFC (LMG341x) plus GaN half-bridge LLC (LMG3422), C2000 digital, QR flyback bias | >95 % at 20–100 % load; PFC >98.8 %, LLC >98.3 % | **160 × 66 × 38 mm** (≈401 cm³), 41 W/in³ | Server PSU with forced air, 0–50 °C ambient, **hold-up 8–10 ms only**, OCP 110–130 %, OVP 13–14.5 V. Reference design, not certified. https://www.ti.com/tool/TIDA-010062 ; https://www.ti.com/lit/ug/tiduet7g/tiduet7g.pdf |
| TI PMP41006 | Same hardware with Si LLC and current-mode (HHC) control | >95 % | 38 × 66 × 165 mm, 39 W/in³ | Better transient response. https://www.ti.com/lit/ug/tidt253/tidt253.pdf |
| **Infineon EVAL-800W-PSU-3P-P7** | 800 W, 12 V (66–83 A), 90–265 VAC. CCM PFC (CoolMOS P7 + CoolSiC diode) plus LLC, OptiMOS SR, CoolSET QR flyback standby, XMC digital | >95 % at 230 VAC, above Platinum | Server form factor, low-cost 4-layer board [dimensions GAP] | Silicon, lower risk, larger. https://www.infineon.com/evaluation-board/EVAL-800W-PSU-3P-P7 |
| Navitas CRPS185 | 3.2 kW, totem-pole plus LLC (GaN) | >96.5 % at 30 % | 40 × 73.5 × 185 mm (544 cc), ≈100 W/in³ | Fan-cooled; shows what the envelope can reach. https://www.eenewseurope.com/en/3-2kw-gan-reference-design-for-data-centre-ai-power/ |
| Navitas LLC module paper | 1.5 kW LLC, planar matrix transformer, >600 kHz | 97.5 % | Module 90 × 30.5 × **11 mm** | Planar magnetics make a low-profile board possible. https://navitassemi.com/wp-content/uploads/2023/06/High-Frequency-High-Efficiency-LLC-Module-with-Planar-Matrix-Transformer-for-CRPS-Application-Using-GaN-Power-IC-paper.pdf |
| CPES (Virginia Tech) | 800 W 380→12 V LLC at 1 MHz, GaN, PCB matrix transformer | 97.6 % peak | 900 W/in³ (DC/DC only) | Research result. https://cpes.vt.edu/library/viewabstract/29461/ |
| Infineon REF_8KW / 12KW | Totem-pole plus FB LLC, SiC/GaN/Si hybrid | 97.5 % | ≈100–113 W/in³ | Uses an **auxiliary hold-up boost** to shrink the bulk capacitor, a useful idea here. https://www.infineon.com/evaluation-board/REF-12KW-HFHD-PSU |
ST, onsemi and Power Integrations: no 800 W 12 V totem-pole + LLC reference design was found this pass [GAP]. Their controllers are listed in §5.
**Every one of these designs assumes forced air from its own fan.** None is fanless at 800 W+.

## 3. Size and fit verdict
- Density anchor: TIDA-010062 at 2.5 W/cm³ gives **≈340 cm³ for 850 W** (at 38 mm height). With planar magnetics and a hold-up boost, ≈250 cm³ might be reachable [E]. The stock bay volume is **[GAP]**.
- At a 92–95 % peak, the heat is 45–74 W at 850 W and ≈27–43 W at the 520 W operating point [E]. With fan airflow, ≈30–45 W is believable in the stock bay. 850 W sustained is **not credible without guaranteed airflow through the PSU**, so the board needs OTP and derating.
- **Verdict:** a 12 V-only GaN design looks plausible if the bay gives ≥ ~300 cm³ with a ≥ ~30–38 mm component height on one side. This is unconfirmed until Aidan's measurements arrive. If the bay is much smaller, 850 W won't fit at certified quality. Then the 650–700 W variant, or keeping part of the load outside the chassis, is the fallback.

## 4. Requirements (transients, hold-up, protections, safety, EMC, inlet)
**ATX 3.1 PSU excursion** (PSU >450 W with 12V-2x6) [S]: **200 % for 100 µs, 180 % for 1 ms, 160 % for 10 ms, 120 % for 100 ms** of rated power. https://www.infobytes.de/pages/atx3.1powerrev2.1.pdf ; https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/2.0/2.01/psu-power-excursion/
**PCIe CEM 5.1 card:** up to **3× sustained for ≤100 µs**, falling at longer intervals; sustained power is a 1 s moving average [S] (same guide and https://pcisig.com/PCIExpress/Specs/CEM/CardElectromechanical_5.1_1.0). Our GPU is fed through bus bars, not 12V-2x6, but the card's behaviour is the same, so design to the ATX 3.1 table.
- For 850 W, that means about 1.7 kW for 100 µs, which is mostly handled by 12 V output and bus-bar capacitance. 1.36 kW for 10 ms has to come from the LLC itself, so the **OCP must not trip inside the table**.
- Recommended for the scale-back: rate the PSU at 700 W but meet the excursion table against the real ~520–700 W load.

**Hold-up** (ATX 3.1 Table 4-8) [S]: required **12 ms at 100 %**, recommended **17 ms at 80 %**. TIDA-010062 only meets 8–10 ms, so it needs more bulk capacitance.
- Bulk estimate [E], using E = P·t/η and a 390 → 310 V window. At 850 W: 12 ms/100 % ≈ 10.7 J and 17 ms/80 % ≈ 12.2 J, so **≈440–470 µF / 450 V**. At 700 W: ≈360–390 µF. At 650 W: ≈330 µF.
- The bulk capacitors are the tallest parts (≈30–50 mm snap-ins). An auxiliary hold-up boost (Infineon approach) cuts this by about 30–50 % [E].

**Protections:** OCP (≈110–130 % sustained, with a time-qualified curve so the excursion table passes), OVP (13–14.5 V latch, per TIDA spec), UVP, short circuit, OTP with a derating curve, brown-in/brown-out, input fuse, inrush limiting, surge (MOV/GDT) on the primary, and PG/PS_ON timing. Also preserve the **Hall-interlock 12 V disable** and the >240 VA bus-bar hazard handling. Standby must stay ≥ 11 V / 5 W or match the new I/O board.
**Safety (IEC/UL 62368-1):**
- Reinforced insulation primary↔secondary, hipot ≈3 kVAC for class I (RSP-750 example).
- Creepage and clearance from the standard's tables for working voltage (≈420 V peak on the PFC bus), PD2 and altitude, **taken from the standard by the certifying engineer**.
- Safety-rated transformer, isolator and Y-caps, protective earth bonding to the chassis, touch-current limits, and component ratings at in-core temperature.
- A planar transformer needs certified insulation, for example the triple-insulated or solid-insulation rules for PCB-winding constructions.

**EMC:** CISPR 32 / EN 55032 Class B conducted and radiated emissions, plus EN 55035 immunity and IEC 61000-3-2 harmonics (PFC is mandatory above 75 W input), and 61000-3-3 flicker. Typical filter: a 2-stage common-mode/differential-mode filter, which takes significant volume. GaN fast edges make the layout and filter harder.
**Inlet current** [E, PF 0.99, η 0.94]:
| Pout | 90 VAC | 100 VAC | 115 VAC | 230 VAC |
|---|---|---|---|---|
| 850 W | **10.1 A** | 9.1 A | 7.9 A | 4.0 A |
| 700 W | 8.4 A | 7.5 A | 6.5 A | 3.3 A |
| 650 W | 7.8 A | 7.0 A | 6.1 A | 3.0 A |
| 520 W op. | 6.2 A | 5.6 A | 4.9 A | 2.4 A |
- The stock label reads about **6 A** (to be verified). Inlet 923-0505 and the internal inlet cable/connector ratings are **[GAP]**. A typical IEC 60320 C14-style inlet is 10 A (IEC) / 15 A (UL), but the internal cable and latch connector may be lower.
- **850 W at low line likely exceeds the inlet and wiring.** Options: low-line power derating (for example 850 W only at ≥180 VAC and ≈650–700 W at 100–127 V, as many server PSUs do), or a certified replacement inlet and cable.
- Inrush: NTC plus bypass relay or an active (relay-less) limiter. Size the bulk capacitance with the cold-start inrush in mind against the inlet and fuse I²t.

## 5. Preliminary block diagram and key parts shortlist (no purchases; verify all against datasheets)
```
AC inlet 923-0505 -> fuse/MOV -> 2-stage EMI filter -> inrush (NTC+relay / active)
  -> GaN CCM totem-pole PFC (fast GaN leg + slow Si/SiC line leg) -> 390 V bulk (+ opt. hold-up boost)
  -> GaN half-bridge LLC (planar or matrix transformer, reinforced isolation)
  -> synchronous rectifier (parallel 40 V Si FETs) -> output caps + OR-ing/eFuse -> 12 V bus bars + DC-Out
  standby: QR flyback (separate, reinforced) -> 11 V/5 V SB -> I/O board
  control: digital MCU(s) for PFC+LLC, digital isolator across barrier, PS_ON/PG/(PMBus telemetry), OTP NTCs, Hall-interlock input
```
| Function | Candidates | Links |
|---|---|---|
| PFC GaN | TI LMG3422R030 / LMG3522R030 (600–650 V, integrated driver); Infineon CoolGaN 650 V (e.g. IGT65R025D2); Navitas GaNSense ICs | https://www.ti.com/product/LMG3422R030 ; https://www.ti.com/product/LMG3522R030-Q1 ; https://www.infineon.com/cms/en/product/power/gan-hemt-gallium-nitride-transistor/ |
| Digital control | TI C2000 F28003x (as in TIDA-010062); Infineon XMC4200/1400 (as in EVAL-800W) | https://www.ti.com/product/TMS320F280039C |
| Analog alternative | onsemi NCP1680 (CrM totem-pole PFC), NCP13992 (LLC), NCP4307 (SR); TI UCC256404 (LLC), UCC24624 (SR) | https://www.onsemi.com/products/power-management/ac-dc-power-conversion/power-factor-correction-controllers/ncp1680 ; https://www.ti.com/product/UCC256404 ; https://www.ti.com/product/UCC24624 |
| SR FETs | Infineon OptiMOS 40 V (e.g. ISC014N08NM6 class) / TI CSD 40 V, several in parallel for ≈71 A | https://www.infineon.com/cms/en/product/power/mosfet/n-channel/ |
| Standby | Power Integrations InnoSwitch3/4 (integrated reinforced isolation); Infineon CoolSET QR | https://www.power.com/products/innoswitch |
| Isolation | TI ISO77xx reinforced digital isolators | https://www.ti.com/isolation/digital-isolators/overview.html |
| Magnetics | Planar or PCB matrix transformer (Navitas/CPES approach) for a low profile; PFC inductor is a low-profile PQ/RM or coupled design; custom from a magnetics house with a safety file | see §2 papers |
Status: these are candidates from reference designs and are not verified for availability or price.

## 6. Scaled-back variant (650–700 W)
- Same topology and certification effort, so NRE (design house, safety and EMC testing) is about the same and probably dominates total cost [E, GAP: no quotes].
- Hardware deltas [E]: ≈20–25 % less bulk capacitance (330–390 µF), ≈15–20 % smaller magnetics, fewer SR FETs, a smaller heatsink, and ≈15–20 % less volume (≈270–290 cm³ at TIDA density). Total BOM roughly 10–20 % lower.
- **Main real benefit: the inlet.** 700 W at 90 V is ≈8.4 A, under a likely 10 A inlet, so the stock inlet and cable stay reusable without low-line derating. 700 W still covers the 520 W operating point and the ~650–700 W worst case, though without margin.
- Suggested plan: one PCB layout with 850 W-capable silicon, built in a "700 W" population (smaller bulk, firmware OCP/OPP limit) or an "850 W at high line" build. **One certification would cover the highest rating** [E, the certifier must confirm].

## 7. Data for Mechanical & Thermal (preliminary, [E] until a layout exists)
- Outline: target ≤ ~160 × 66 mm board (TIDA-like), 38 mm max height. **The real outline is pending the stock bay measurements.**
- Hot spots: (1) PFC GaN pair and line-leg FETs, (2) LLC GaN + transformer, (3) SR FETs + output bus (≈71 A at 850 W), (4) inrush NTC (when hot) / relay, (5) PFC inductor, (6) bulk caps, which run cool but are temperature-limited (life halves per ~10 °C).
- Loss: 45–74 W at 850 W, ≈30–45 W at 520 W.
- Parts taller than 4.5 mm: bulk caps (30–50 mm), PFC inductor, transformer (11–20 mm planar, more if wound), EMI chokes, X/Y caps, relay, and heatsinks. **Proposal:** put every tall part on the side away from the CPU board. Keep the CPU-facing side to SMD parts ≤ 3 mm plus an insulating barrier (Formex-type) with the required safety distance. The ≈5 mm gap cannot hold any primary parts; that is the certifier's call. Airflow must go through the tall-parts side.
- Required from M&T: guaranteed airflow (CFM or m/s) through the PSU zone, and the inlet-air temperature at the PSU.

## 8. Remaining measurements and data for Aidan (unplugged, sat ≥15 min, power button held 10 s; no probing of the primary side or capacitors)
1. PSU envelope L × W × H with the cage, plus free bay volume and height on each side, including the gap to the CPU board.
2. PSU label photo: input A rating, vendor (Delta or AcBel), model.
3. AC inlet 923-0505 markings (A/V rating, approval marks), plus the inlet cable gauge and connector type at the PSU.
4. DC-Out and data connectors: pin count, pitch and markings (photos). Pin functions should come later from I/O-board-side tracing, done by a qualified person.
5. Bus-bar cross-section, length and attach points (≈71 A at 850 W).
6. Mounting-hole positions (the four T10 sides), board outline, and a scaled photo of both sides **from outside the cage, no touching**.
7. Airflow path to and from the PSU.
8. Decision: is a low-line derating (e.g. 650–700 W at 100–127 V) acceptable, or does he want 850 W at 100 V? The latter likely means a new inlet and cable.
9. Who is the qualified mains designer/certifier (in-house or design house)?

## 9. Gaps (not guessed)
Stock pinouts, signals and PMBus; OCP and hold-up; dimensions; inlet rating; I/O-board-side standby needs; an ST/onsemi/PI 800 W reference design; Infineon EVAL-800W dimensions; cost quotes; core airflow figures.

## Thermal design inputs from Mechanical & Thermal (2026-10-25, 12:37 PM ET; calculated, not measured)
- Inlet air: design for 40 C. That's Apple's 35 C maximum ambient (https://support.apple.com/en-us/112025) plus some heat picked up from the CPU board. The PSU sits in the bottom intake stream.
- Airflow needed through the PSU, for a 15 C air rise: about 3.5-5.3 CFM at the 520W point and 5.3-8.7 CFM at 850W. Design for at least 9 CFM at 850W.
- Requirements: put the GaN transistors and rectifiers on a heat spreader along the board's long axis, with low-pressure fin spacing; add thermal sensors with power derating at the hot spots; provide for a fan-speed or tachometer signal.
- Still unknown: the 6,1 fan's CFM and how its airflow splits between the core and the PSU. The fan may need upsizing.

## DECISION 2026-10-25 1:02 PM ET (Aidan): 600W continuous on the stock inlet
- The stock AC inlet is rated 100-250V at 6A. At 120V that is about 720W of input, so at roughly 93% efficiency the continuous output rating becomes 600W (about 5.4A input at 120V). This supersedes the 850W target.
- Short spikes per the ATX 3.1 table are still required, above the 600W rating, as brief transients only. Firmware power limits for the CPU, GPU and USB pool keep the sustained load at or below 600W.
- Operating point: 142W Eco CPU plus a capped GPU, about 500-520W, which fits within 600W.
- Heat loss at 600W and 93% efficiency is about 45W. The board should shrink by roughly 25-30% compared with the 850W layout.
- The mains side must still be designed and certified by qualified people, and the earth path still has to be confirmed.
