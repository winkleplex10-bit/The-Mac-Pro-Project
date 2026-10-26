# Mac Pro 6,1 Thermal Core Test Plan (MacPro6,2 project)

Owner: Aidan Winkler · Author: Mechanical & Thermal · Date: 2026-10-25 · Status: DRAFT, nothing purchased

**Goal:** measure how much heat the stock 6,1 thermal core and fan can remove from the CPU face and the GPU faces. We'll use that to set firmware CPU (PPT) and GPU (TGP) caps for the AM5 build, which has a 600 W custom PSU with no fan of its own.

**What we know already**
- Apple's measured maximum is 270 W at the wall, about 240 W DC, for the 12-core with D700s ([Apple power spec](https://support.apple.com/en-us/102839)). Apple's ambient spec is 10–35 °C.
- My working ceiling estimate is 300–350 W of CPU plus GPU heat. **This is unverified, and it's what this test checks.**
- Mounting: the CPU-side boss is 7.84 mm and the GPU side 4.75 mm. The CPU hole pattern is 69.5 × 55 mm and the GPU's is 75.2 × 50 mm. The stock GPU uses 2 mm pads on copper strips.
- Candidate caps: CPU 142 W + GPU 160–180 W · 105 + 200 · 88 + 220.

**Gaps (not public, must be measured):** the core's real thermal limit; the fan's voltage, connector pinout, tach type and CFM; the fan's PWM-to-RPM curve; the SMC fan curve; and the AM5 IHS-to-die and GPU die-to-hot-spot deltas through *our* interface.

---

## 1. Methods

### Method A: logged stress run on the stock machine (do this first; low risk)
Reaches only the stock configuration's heat, about 200–250 W (10-core E5 v2 at ~130 W TDP + 2× D300). It **cannot** prove 300+ W, but it calibrates θ (°C/W) for the real interface and fan curve.

1. Room steady at 20–25 °C, machine upright, nothing within 30 cm of the top exhaust. Log room temperature with a thermocouple at the bottom intake.
2. Plug the Mac into a wall power meter (Kill A Watt class).
3. Idle for 15 min and record the baseline.
4. Run the CPU load alone for 30 min, then the GPU load alone for 30 min, then both for 45 min or until steady.
   - **macOS:** `stress-ng --cpu 0 --cpu-method matrixprod` or Prime95 Small FFT for the CPU. GPU: FurMark isn't native on macOS; use a Metal/OpenCL load (gap: pick a tool that loads *both* D300s).
   - **Windows/Boot Camp:** Prime95 Small FFT plus FurMark with one instance per D300 (or CrossFire off, two windows).
5. Logging:
   - **macOS:** `sudo powermetrics --samplers cpu_power,smc,gpu_power -i 2000 > pm.txt` (SMC/GPU fields vary by OS version; gap). Add TG Pro or iStat Menus for SMC temperatures and fan RPM with CSV export. Intel Power Gadget is discontinued by Intel; use it only if you already have it installed.
   - **Boot Camp:** HWiNFO sensors-only, logging to CSV every 2 s (CPU package power, core temps, GPU temps and power where reported, fan RPM).
   - Wall power: read the meter every 1–2 min by hand, or photograph it with a timestamp.
6. Result: θ_CPU ≈ (T_CPU,max − T_amb) / P_package, and the same per GPU. Note that these are **die/junction** readings, not case. Total heat ≈ wall W × PSU efficiency (assume ~0.88; gap).

### Method B: heater blocks on the bare core (proves the ceiling)
Take the boards off the core and clamp heater blocks to the faces using the stock bracket and screw geometry.

**Heater blocks**
- **CPU face:** an aluminium or copper block (copper preferred, ≥10 mm thick) with a contact area matching an AM5 IHS (~40 × 40 mm centre), drilled for the 69.5 × 55 mm pattern or clamped by the stock bracket. The spacer height must reproduce the 7.84 mm boss stack.
- **GPU faces (×2):** a block with a contact area of about one GPU die plus memory footprint, on the 75.2 × 50 pattern with 4.75 mm bosses. Put paste on the die area. Replicate the 2 mm pads on the copper strips where memory would sit, or leave the strips bare and note it.
- **Heat sources:** cartridge heaters in drilled bores (snug fit with heater compound), or thick-film power resistors (Ohmite TGH, TO-247/TO-220 class) screwed to the back of the block with paste. 100 W aluminium-clad resistors also work. Budget **≥1.5× the target power per face** so no resistor runs near its rating.
- **Thermocouples:** K-type in a 1 mm hole drilled to the block centre, 1 mm behind the contact face ("simulated case/IHS"). Add one on the core face beside the block, one at the fin exit, and one at the intake.
- **Power:** a DC bench supply (preferred, since P = V·I is read directly and there's no mains on the bench), one channel per face. Use AC through a variac or SSR only with an isolated, enclosed and fused heater circuit.
- **Fan:** with the boards removed there's no SMC, so **drive the fan externally** from a bench supply at its rated voltage (gap: read the fan label, measure the connector pinout, and confirm it's 12 V with a tach line. Don't guess; check with a multimeter on the running stock machine first). Read the tach with the Arduino (pulse count; gap: pulses per revolution, assume 2) and log the fan V and I. Test at **full speed** and again at the Method A observed RPM.
- **Interface:** use the same paste (Arctic MX-4 or a known paste) at the same thickness and the stock screw torque. Note the torque if you can measure it (gap: Apple's spec).

---

## 2. Safety (read before Method B)
- **Mains isolation:** no exposed mains anywhere. DC heaters are strongly preferred. If you use AC heaters, put them in an enclosed, earthed, fused box, with the variac/SSR fed from an RCD/GFCI outlet.
- **Thermal cutoffs:** one thermal fuse or bimetal cutoff per block (≈130 °C), wired in series with that block's heater.
- **Never run a heater without the fan running.** Start the fan first and stop it last. If the tach reads 0, cut the heaters immediately (by hand, or with an Arduino-controlled relay).
- **Maximum block temperature: 110 °C.** Abort any step that exceeds it. A real CPU fails long before that anyway.
- **Emergency stop:** one switch or power strip within reach that kills all heater power, with the fan on a separate supply.
- **Fire:** a non-flammable surface (ceramic tile or metal tray), a CO₂ or ABC extinguisher nearby, no paper or plastic near the blocks, and Kapton tape and fibreglass-braid thermocouples only.
- **Burns:** blocks and the core exceed 80 °C. Use gloves, and leave 30 min to cool before touching anything.
- **Thermocouple fixing:** fix the bead with high-temperature epoxy or Kapton plus a crimped retainer. A loose thermocouple reads low, and that's the most dangerous failure here.
- **Supervised:** never leave a step unattended, and have a second person present for anything above 250 W.

---

## 3. Power steps (Method B)
Start at **100 W total**, then step up in **25 W** increments. Hold each step **20–30 min, or until steady (<0.5 °C change per 5 min on every channel)**.

Run three split profiles. The GPU share is divided equally across the two GPU faces unless we pick a single-GPU AM5 layout (gap: the final design has one GPU face, so also run Profile "1-GPU" with all GPU heat on one face).

| Profile | CPU : GPU ratio | Example at 300 W total |
|---|---|---|
| P1 (142 + 160–180) | ~45 : 55 | CPU 135 W, GPU 165 W |
| P2 (105 + 200) | ~34 : 66 | CPU 102 W, GPU 198 W |
| P3 (88 + 220) | ~29 : 71 | CPU 87 W, GPU 213 W |
| 1-GPU | same ratios, GPU heat on one face | — |

Stop a profile at the first fail (Section 5) and record the last passing step. Expected range: 100 → ~350 W, about 11 steps, so ~5–6 h per profile.

---

## 4. What to log and how
Sample every **1–5 s (2 s recommended)** to **CSV** with an ISO timestamp.

| Channel | Sensor | Notes |
|---|---|---|
| T_CPU_block | K-type, 1 mm behind face | simulated IHS/case |
| T_GPU1_block, T_GPU2_block | K-type | simulated hot spot |
| T_core_CPU, T_core_GPU1/2 | K-type on core face next to block | gives the interface ΔT |
| T_exhaust | K-type at fin exit (top) | also check it's safe to touch |
| T_intake | K-type at bottom intake | ambient |
| Fan V, I, RPM | bench supply readback + Arduino tach | |
| Heater V, I per face | bench supply readback, or a DMM | P = V·I |
| Wall power | Kill A Watt | Method A, and total Method B input |
| Noise | phone SPL app at 1 m | note per step |

**Logger options:** Pico TC-08 (8 channels, USB, logs to CSV out of the box), or an Arduino Uno with one MAX31855 breakout per channel (~6 channels) running a serial-to-CSV script on the laptop.

---

## 5. Pass/fail limits (per step)
Correct to the hot ambient: **T@35 = T_measured + (35 − T_intake)**.

| Item | Pass at 25 °C intake | Pass corrected to 35 °C |
|---|---|---|
| CPU block (sim. IHS) | ≤ 80 °C | ≤ 90 °C (AM5 Tctl max 95 °C; IHS-to-die margin) |
| GPU block (sim. hot spot) | ≤ 90 °C | ≤ 100 °C (junction limit ~100–110 °C) |
| Exhaust air / top surface | ≤ 60 °C / touch-safe | note |
| Any block absolute | < 110 °C (abort) | — |
| Fan | steady RPM; noise noted | — |

**Derived values**
- θ_CPU = (T_CPU_block − T_intake) / P_CPU (°C/W), and θ_GPU in the same way per face.
- θ_interface = (T_block − T_core_face) / P, which separates paste/pad from the core itself.
- **Combined capacity** = the highest total W where every channel passes at the 35 °C correction. Report it per profile.

---

## 6. Mapping results to firmware caps
θ from the block is case-referenced. The die runs hotter by an **IHS-to-die delta**, which is a gap: AMD doesn't publish it for our interface. Assume ~10–15 °C at 140 W for AM5 (soldered IHS, chiplet hot spot) until we measure it on the real board.

**CPU:** P_max = (T_case,limit − T_amb) / θ_CPU, with T_case,limit = 95 − Δ_IHS-die.

**Worked example (made-up numbers):**
- Measured θ_CPU = 0.42 °C/W at the P1 split. Ambient design 35 °C, Δ_IHS-die 12 °C → T_case limit 83 °C.
- P_max = (83 − 35) / 0.42 = **114 W**.
- Apply a 10–15 % margin → **PPT ≈ 97–103 W**. Set a custom PPT of ~100 W, or use the 88 W PPT (65 W TDP Eco) preset. The 142 W PPT preset would be too high for this result.
- **GPU:** θ_GPU = 0.25 °C/W, hot-spot limit 100 °C, design hot spot ≤ 90 °C → (90 − 35) / 0.25 = 220 W → ×0.85–0.90 → **TGP ≈ 187–198 W**.
- Then check that the *total* (e.g. 88 + 190 = 278 W) is under the measured combined capacity for that profile minus 10 %. If it isn't, scale both down along the profile ratio.

**Choosing values:** set the AMD PPT (with matching TDC/EDC) and the GPU TGP/power limit at the computed value minus 10–15 %. Then validate on the real AM5 hardware with a Method A–style logged run before calling it final. PSU loss (~30–45 W at 520 W) adds core-adjacent heat; gap: whether the PSU's heat crosses the core. Run one Method B step with an extra ~40 W on a dummy block in the PSU bay if possible.

---

## 7. Parts list (links only; nothing bought; all links checked 2026-10-25)

| Item | Link | Qty / note |
|---|---|---|
| Wall power meter (Kill A Watt P4400) | https://www.p3international.com/products/p4400.html | 1 |
| K-type thermocouple, fibreglass braid | https://www.adafruit.com/product/270 | 8–10 |
| MAX31855 thermocouple amplifier | https://www.adafruit.com/product/269 | 1 per channel (Arduino option) |
| Arduino Uno R3 | https://store.arduino.cc/products/arduino-uno-rev3 | 1 (logger + fan tach) |
| Pico TC-08 thermocouple logger (alternative) | https://www.picotech.com/data-logger/tc-08/thermocouple-data-logger | 1 |
| Thick-film power resistors (Ohmite TGH series) | https://www.ohmite.com/catalog/tgh-series/ | 2–3 per face |
| Cartridge heaters (alternative) | https://www.mcmaster.com/cartridge-heaters/ | 1–2 per block |
| Thermal cutoffs | https://www.mcmaster.com/thermal-cutoffs/ | 1 per block |
| Aluminium bar stock | https://www.mcmaster.com/aluminum-bars/ | blocks |
| Copper bar stock (preferred for the CPU block) | https://www.mcmaster.com/copper-bars/ | blocks |
| Bench DC supply (Rigol DP800 series) | https://www.rigolna.com/products/dc-power-loads/dp800/ | 1–2 (3 channels: heaters + fan); check that the current per channel covers the target W |
| Thermal paste (Arctic MX-4) | https://www.arctic.de/en/MX-4/ACTCP00002B | 1 |
| Prime95 | https://www.mersenne.org/download/ | software |
| stress-ng | https://github.com/ColinIanKing/stress-ng | software |
| FurMark | https://geeks3d.com/furmark/ | software (Windows) |
| HWiNFO | https://www.hwinfo.com/ | software (Boot Camp) |
| TG Pro | https://www.tunabellysoftware.com/tgpro/ | software (macOS) |
| iStat Menus | https://bjango.com/mac/istatmenus/ | software (macOS) |
| Mac Pro Late 2013 teardown guides | https://www.ifixit.com/Device/Mac_Pro_Late_2013 | reference for board removal |

Gaps in the list: high-temperature thermocouple epoxy, Kapton tape, the 2 mm GPU pads (match the stock pad spec, which is a gap), an RCD/GFCI strip and a relay module. These are generic items; pick them at purchase time.

**Note:** a single-channel bench supply is usually limited to ~100–200 W per channel. A 350 W test needs either several channels or a larger 24–48 V supply plus the resistors in series. Size this before buying (gap).

---

## 8. Blank results table

| Profile | Step total W | P_CPU | P_GPU1 | P_GPU2 | T_intake | T_CPU blk | T_GPU1 blk | T_GPU2 blk | T_exhaust | Fan V / A / RPM | Wall W | Steady? (min) | CPU@35 | GPU@35 | Pass? | Noise dB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | |
| | | | | | | | | | | | | | | | | |

**Summary per profile:** θ_CPU ___ °C/W · θ_GPU ___ °C/W · combined capacity ___ W · recommended PPT ___ W · TGP ___ W
