# MacPro6,2 power architecture proposal (draft for Aidan, 2026-10-26)
Status: PROPOSAL. Board figures are teammates' estimates, not measurements.

## 1. Module verification
### Vox Power EIRE600-12 (primary) — datasheet DOC-DTS-036-01
Source: https://www.vox-power.com/wp-content/uploads/EIRE600/DOC-DTS-036-EIRE600-Datasheet.pdf
- Size 5 x 3 x 1.1 in (127 x 76.2 x 27.9 mm); 390 g; M4 pan-head mounting (0.5 N·m). Exact hole pattern: in datasheet drawing (not extracted; read from PDF before layout).
- Output 12 V nominal, adjustable 11.2-13.3 V, 50 A max. 600 W fan/conduction cooled at 115 VAC; 450 W convection (115 VAC). Line derating: 600 W at 115 V linearly to 420 W at 85 V.
- Peak: 750 W (125%) for 3 s, 25% duty, average <= 600 W -> covers the 20-30% short peaks F&S want (exactly 25%; 30% is NOT covered).
- OCP >130% I_rated, auto-restart (hiccup); OVP 135%; OTP 125 C component, auto-restart. 5V bias overload (>12 W) shuts the whole PSU off.
- Standby: 5 V / 2 A bias only (referenced to Vout-). NO 12 V standby variant. Fan output 12 V / 0.5 A (fan-cooled spec).
- Signals: AC_OK (open-collector sink 0.5 mA, >=2 ms warning at 600 W) — meets >=1 ms; Inhibit (remote off, logic low <1.0 V, 10k pulldown); remote sense. NO PWR_OK/DC_OK, NO PMBus/telemetry, NO current share, NO overcurrent warning.
- Hold-up 12 ms min/14 typ at 600 W, 18/20 ms at 400 W (115 V). Turn-on delay 450 ms, rise 3 ms.
- Efficiency up to 96%; 94.7% at 230 V full load; 95.0% average of 25/50/75/100% at 230 V. Per-load 50/75/100% at 115 V: GAP (graph only).
- Input current 6 A max at 600 W/115 V (= our inlet rating, zero margin; input current limit 8 A). Inrush 30 A.
- Safety IEC/UL 62368-1 Ed.3/4, IEC/UL 60601-1 Ed.3.2; EN55032 Class B conducted+radiated; Class I or II.
- Airflow: full-power fan rating references 18.2 CFM (warranty condition) with a specified fan; our ~6 CFM at 40 C is between convection (450 W) and fan rating. Exact derating vs CFM/temperature: GAP (graphs not machine-readable; must read curves / ask Vox). Plan on ~450-500 W sustained until a thermal test or conduction to the case proves more.
- New product (released 15 Oct 2026); availability unverified.

### Backups
| Module | Size (mm) | Fits 28 mm/80 mm? | Cooling | Standby | Signals | Cert | Notes |
|---|---|---|---|---|---|---|---|
| MEAN WELL LOP-600-12 https://www.meanwell.co.uk/power-supplies/medical-grade-power-supplies/lop-600-series | 127x76.2x35 | NO (35 mm) | 400 W convection, 600 W @23 CFM | none | none listed | 62368-1, 60601-1 | 150% peak 3 s; fan 12V/0.5A |
| FORTEC/Cincon? CFM600S120 https://www.fortec.uk/CFM600S/CFM600S | 3x5 in; height GAP | unverified | 510 W natural, 600 W conduction; 26 A open / 32 A covered without fan | +5 V SB | PS On/Off, Power Good, Power Fail | 62368-1, Class B | best backup signal set; height must be checked |
| Bel/Power-One LCC600-12U-9P https://www.components-store.pl/datasheets/6c/LCC600-12U-9P.pdf | enclosed; size GAP (likely too large) | probably NO | conduction, 600 W to 85 C baseplate | 5 V/1.5 A | AC_OK, DC_OK, On/Off, PMBus, current share | Medical+ITE | OCP 105-130%, hiccup then latch after 20 s |
| XP CCH600PS12 | 177.8x101.6x44.5 | NO | baseplate | 5 V/0.5 A | power fail, inhibit, OT, share | 62368 | too big |
Not reached: Advanced Energy/Artesyn, TDK-Lambda, Murata, Delta, SL Power low-profile 600 W parts — GAP, search before committing.
Conclusion: only the EIRE600-12 is verified to fit 28 mm. No candidate offers 12 V standby; only LCC600 has PMBus.

## 2. Rails
- 12V_MAIN: module output, 600 W continuous, 750 W/3 s. Sustained target <= 540 W (90%), and lower until airflow derating is known.
- 12V_SB (recommended single standby rail), 1.5-2 A: 
  - Option A (recommended): boost from module 5 V/2 A bias -> 12 V. Max ~10 W in -> ~0.75 A at 12 V at 90% efficiency. Does NOT meet 1.5-2 A; meets real need (I/O 0.17 A + CPU board 2.3-4.2 W ≈ 0.2-0.35 A + EC/SPI). Fully DC-side, no new certification. Must keep bias <12 W or entire PSU trips.
  - Option B: second certified small AC-DC (e.g. 12 V 25-40 W open-frame) in parallel on the mains side for true 1.5-2 A. Needs its own certification-listed part, creepage on carrier, earth bond, and adds inlet current; requires safety review.
  - Option C: derive from 12V_MAIN with module running and Inhibit holding main off — not possible: EIRE600 inhibit kills main output; keeping main always-on at idle defeats standby and is not recommended.
  - Recommendation: Option A, and ask F&S to accept ~0.6-0.75 A 12V_SB (budget shows ~0.35 A used). If they insist on 2 A -> Option B.
- 11V_SB conflict: CPU board wants stock 11V_SB; F&S wants 12V_SB. Recommend 12V_SB everywhere if backplane PS1 accepts 11-12 V input (OPEN for CPU board).
- 5V/3.3V standby: made on the backplane (PS1) from 12V_SB; PSU does not supply them.
- FAN_12V: switched from 12V_MAIN via load switch (1-2 A, eFuse limited), tach readback to EC; the module's 0.5 A fan output is too small for a 1-2 A fan.

## 3. Per-board currents and connectors
| Branch | Cont. | Peak | Connector | Protection |
|---|---|---|---|---|
| CPU/base board 12V | 17.9 A @142 W PPT (215 W); 26.3 A @230 W PPT | VDDCR load steps (AMD data NDA) | Bus bar or 8-10 AWG pair <100 mm, 70 C+, landing on stock LUG1/LUG2 footprint (2x2 PTH per lug) — candidate entry | eFuse ~25 A (TPS259851 on CPU board) + carrier eFuse/fuse 30 A |
| GPU 12V | 13.5-15 A, design 17 A | 25-30 A <1 ms | Micro-Fit 2x4 (4 pwr/4 gnd, HCS terminals) or blade pair, short loop | eFuse/fuse ~30 A with fast trip >35 A; OCW blanking >1 ms |
| I/O board 12V + SB | 11.3 A, budget 15 A | 13 A | Micro-Fit 2x5: 4x12V, 4xGND, 1-2x12V_SB, own harness | 20 A eFuse; SB 1 A polyfuse |
| SSD board | 2.5-5.5 A | 6.5 A | via base board face pins | 8 A on base board |
| Fan | 1-2 A | inrush | 4-pin fan header | load switch w/ 3 A limit |
| CPU board standby | 0.2-0.35 A | | J4 pin1 | |
Note: base board 12V plane checked only to ~15 A — must be re-checked even at 142 W (CPU board item).

## 4. Sequencing and signals (carrier MCU-less; logic on carrier + backplane MCU)
- AC applied -> module bias 5 V up -> boost 12V_SB -> SB_GOOD (open-drain supervisor) -> backplane MCU.
- PS_ON# (active low from backplane MCU, J4 pin3) -> drives EIRE600 Inhibit (inverted) -> 12V_MAIN up (450 ms delay + 3 ms rise).
- PWR_OK (J4 pin4): generated on carrier by a voltage supervisor on 12V_MAIN (window ~11.4-12.6 V) + 100-500 ms delay, AND-ed with AC_OK so it drops on AC_OK (>=2 ms warning) before 12 V falls — satisfies ">=1 ms before loss".
- AC_OK forwarded separately to EC (SPI-write protect).
- Telemetry: module has none -> carrier INA228/INA238-class monitor(s) on the main bus (shunt) and per-branch eFuse IMON; plus NTC on module. PMBus-compatible address on EC SMBus 100 kHz. CPU board already has INA228 @0x45 — avoid address clash.
- OCW: fast comparator on main shunt (~600 W = 50 A threshold, ~10-50 µs) -> open-drain PWR_ALERT#, OR-ed (diodes) into PROCHOT_L and GPU throttle; CARRIER_HOT# from module NTC.
- J4 pinout so far: 1 11V/12V_SB, 3 PS_ON#, 4 PWR_OK; add AC_OK, SB_GOOD, PWR_ALERT#, CARRIER_HOT#, SMBCLK/SDA, GND.

## 5. Three-layer limiting
1. Static: BIOS PPT/TDC/EDC, GPU VBIOS TBP, USB PD 100 W total; sum <= 540 W.
2. Slow (~100 ms) EC loop on INA telemetry; lowers CPU limit (AGESA runtime change = GAP) and PD contracts.
3. Fast hardware OCW -> PROCHOT_L/GPU throttle in µs, inside the module's 750 W/3 s window (before 130% OCP hiccup).

## 6. Budget (12 V, W)
| Config | CPU board | GPU | I/O | SSD | Fan | Total |
|---|---|---|---|---|---|---|
| Earlier estimate, Navi23 | 120-160 | 160-180 | 135 | 65 | 24 | 505-565 |
| CPU board figure 142 W PPT, Navi23 | 215 | 160-180 | 135 | 30-65 | 24 | 565-620 (AT/OVER 600) |
| Capped: 105 W PPT (~165 W board, Power Supply estimate), GPU 160, I/O with PD 100 W (~120), SSD 2 drives 30, fan 24 | 165 | 160 | ~120 | 30 | 24 | ~500 (<=540 OK) |
| Capped w/ 4 SSD | 165 | 160 | ~120 | 65 | 24 | ~535 (borderline) |
| xx70 GPU 220-250 W, 105 W PPT | 165 | 220-250 | ~120 | 30-65 | 24 | ~560-625 — conflicts with 6 A inlet |
| xx70 at earlier CPU estimate | | | | | | 625-640 — over |
At 600 W out / ~94% / 115 V the module draws its full 6 A rated input; 108 V mains sag pushes above 6 A, so sustained ~540 W is the real ceiling. Thermal: the ~6 CFM may further limit to ~450-500 W until tested.

## 7. Decisions for Aidan
1. Accept sustained cap ~540 W (105 W PPT CPU, GPU 160 W, PD 100 W) — or accept xx70 only with a new >=10 A inlet.
2. Navi23 vs xx70 GPU (xx70 not compatible with stock inlet at full caps).
3. 12V_SB at ~0.75 A via DC-side boost (no new cert) vs 1.5-2 A via a second certified mains module.
4. Approve EIRE600-12 as primary (new part; confirm availability/derating with Vox).
5. SSD 2 vs 4 drives.

## 8. Open items per teammate
- CPU & Base Board: does PS1 accept 12V_SB (11-12 V)? 12V plane/lug re-check at 18-26 A; PS_ON# polarity/PWR_OK timing (U-2); feed pair (U-3); INA228 address coordination.
- GPU Board: throttle pin; confirm 2x4 Micro-Fit vs blade; real spike data.
- I/O & Storage: accept PD 100 W firmware budget; SB pins; SSD count.
- Firmware & Software: accept 12V_SB <1 A; no PMBus in module -> INA-based telemetry; AGESA runtime limit (GAP); AC_OK 2 ms.
- Mechanical & Thermal: EIRE600 derating at ~6 CFM/40 C, conduction path to case (module is conduction-rated), 5 mm clearance to CPU board, M4 hole pattern vs stock 6 holes.
- Power Supply (me): read EIRE600 derating curves/hole drawing, verify CFM600S height, check other vendors listed as GAP.

## Thermal control inputs from Mechanical & Thermal (2026-10-26 5:04 PM ET, estimates)
- Plan around 450W sustained; 500W is a target to prove in the thermal test. Heat is about 29-32W; the air rise is about 9C at 6 CFM. The risk is the baseplate temperature.
- Margin options: bolt the baseplate through a thermal pad to a spreader tied to the chassis or core fins; add a shroud or baffle; use a fan curve driven by PSU temperature. Get the derating curve from Vox (needs Aidan's OK before contacting them).
- Sensors: S1 on the module baseplate (warn 90C, derate 100C, hard throttle 110C); S2 at the carrier hot spot and S3 at the 12V connector or lug (warn 85C, derate 95C, hard throttle 105C); S4 at the inlet air. Warn and derate go to the EC; hard throttle and module faults go to PROCHOT_L and the GPU slowdown through a hardware OR.
- Fan: a separate switched 12V rail with board PWM; the module's fan output at most as a diode-OR backup. The curve takes the highest of CPU Tctl, GPU hotspot, S1 and inlet; S1 at 85C forces 100%; a tach alarm if the fan stops.
- Thermal test: log about once per second; steps at 300/400/450/500/550/600W, each held until flat for 10 minutes, at 25C and 40C intake. Cap = the highest step with S1 at 90C or below at 40C intake, minus 10%.
- Measured on the stock machine: CPU alone 100W at 67C; CPU plus both GPUs about 90C; fan at 100% is 1900 RPM; room about 22C.

## Base-board PSU input (Aidan's decision 2026-10-29 10:39 AM ET, relayed by I/O & Storage)
The I/O board no longer gets a direct PSU lead; its 12V goes PSU -> base-board input -> I/O connector. The SSD board 12V already goes through the base board. The GPU feed is undecided.
Load through the base input at 12V:
- CPU board: 17.9A at 142W PPT, 26.3A at 230W
- I/O: 15A budget
- SSD: 6.5A peak
- Base retimer: about 1A
- Fan: up to 2A
- Total: about 42A at 142W, about 51A at 230W
- Adding the GPU (RTX 5070 at 250W, 21A plus 25-30A spikes) would bring it to about 72A.
Proposal:
- Rate the base input for 60A continuous without the GPU, or 80A if the GPU is fed through the base board.
- Use the bus bar or lug pair on the stock LUG footprint (2x2 PTH per lug; one 12V lug pair and one GND lug pair), or two crimped 8 AWG pairs under 100mm, rated 105C.
- Put an eFuse or fuse per downstream branch on the base board.
- Recommend a separate direct GPU feed from the PSU to keep the base-board current lower; the decision is open.
- CORRECTION (10:40 AM ET, from Base Board & Connectors): Aidan's decision only covers the I/O 12V through the base input. The CPU board keeps its own LUG1/LUG2 feed, because J1 v4 has only 8 P12V pins. Baseline is Scenario A: a base input for I/O + SSD + fan + retimer, about 25A, rated about 30A. The 60A CPU-through-base version (B) is not decided and is Aidan's call. Agreed: a direct PSU-to-GPU feed and per-branch eFuses. PSU outputs: (1) CPU lugs about 18-26A, (2) base input about 30A rating, (3) GPU direct about 21A plus spikes.
- UPDATE (11:48 AM ET, Aidan decision as relayed by Base Board & Connectors): no base PSU input. The base runs from the CPU board over J1 (12 P12V pins, about 3.5A). PSU 12V outputs: (1) CPU lugs about 18-26A plus about 3.5A base pass-through, (2) I/O board direct about 15A, (3) SSD board direct (the stock second-D700 feed) about 3A without the switch or about 7A with PEX, (4) GPU direct about 21A plus spikes. Supersedes the base-input notes above.
