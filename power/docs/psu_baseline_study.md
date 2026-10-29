# MacPro6,2 PSU feasibility study, first pass (AM5 baseline 2026-10-25)

> **Rev B (12:25 ET):** re-centred on Aidan's update: Ryzen 9 class CPU (170 W TDP / 230 W PPT), xx70-class GPU, original AC inlet reused, **PSU PCB replaced by a new custom one in the stock bay**. Mechanical & Thermal's DC budget is now the primary budget. Section 0 supersedes the verdict in §3–4; §1–4 are kept as the record of the earlier 65 W / stock-PSU analysis.
Date: 2026-10-25 (ET). Research and paper analysis only. No hardware, purchases, pushes or contacts.
Tags: [Sourced] = public source or project doc, [Estimate] = engineering estimate, [GAP] = unknown, needs measurement or data.


## 0. Rev B: replacement PSU PCB in the stock bay

### 0.1 Mechanical & Thermal budget (primary; DC estimates, not measured)
GPU ~160 W (RX 9060 XT class); 4× Gen5 SSD 44 W; 2 retimers 6–26 W; chips (ASM4242, chipset, NICs, muxes) ~16 W; USB device power 78 W (2×15 + 4×7.5 + 4×4.5); memory + fan ~20 W; VR losses ~10 %. Totals: CPU 88 W → ~437–457 W; 142 W → ~496–516 W; 230 W → ~593–613 W. M&T targets: ~650 W PSU for 142 W, ~750 W for 230 W; they recommend 88 W CPU + GPU cap. Clearance ≈ 5 mm behind the CPU board; PSU losses add heat to the shared core airflow (core limit unpublished).

**Cross-check against my sources:** RX 9060 XT 16 GB TBP 160 W (8 GB: 150 W) — AMD quick reference guide [confirmed]. Gen5 SSD 4 × 11.55 W = 46 W max (T705 rating) vs M&T 44 W [consistent]. 2.5GbE I226-V ≤ 1.3 W each (Intel ARK) [consistent with 16 W chip lump]. USB 78 W pool is lower than full PD (USB-C ports could each ask 15 W at 5 V/3 A, more with PD) — M&T assumes a capped pool; keep the firmware cap.

### 0.2 Verification of M&T stock-PSU figures
| M&T claim | Status | Source |
|---|---|---|
| 450 W continuous | **Confirmed** | Apple tech specs https://support.apple.com/en-us/112025 |
| 12.1 V @ 37.2 A | **Confirmed** (label; 12.1 × 37.2 = 450.1 W) | iFixit teardown step 22 |
| No own fan | **Confirmed** | iFixit step 22 |
| Apple max ~270 W at wall | **Confirmed**, but only for the D700 / 12-core config (D300/4-core 205 W, D500/6-core 238 W); idle 43–44 W | https://support.apple.com/en-us/102839 |
| ~240 W DC | **Derived, not sourced**: implies ~89 % efficiency; stock PSU efficiency is not published | — |
| Note | AnandTech measured 437 W avg / 463 W peak at the wall under CPU+GPU stress, so Apple's "max" is not the stress ceiling | AnandTech review p.14 |

### 0.3 Budget with the new target parts (12 V DC side)
| Subsystem | Typical | Peak (sustained limit) | Source |
|---|---|---|---|
| CPU Ryzen 9, 170 W TDP | — | PPT 230 W (TDC 160 A, EDC 225 A) → ≈ 256 W at 12 V with 90 % VR | AMD via TechPowerUp / IT之家 |
| GPU RX 9070 | — | TBP 220 W | AMD https://www.amd.com/en/products/graphics/desktops/radeon/9000-series/amd-radeon-rx-9070.html |
| GPU RTX 5070 | — | TGP 250 W | NVIDIA https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5070-family/ |
| SSD 4× Gen5 | ~10 (light) | 44–46 | M&T; T705 rating |
| Retimers ×2 | 6 | 26 | M&T |
| Chips (ASM4242, chipset, NICs, muxes) | — | ~16 | M&T |
| USB device power (capped pool) | — | 78 | M&T |
| Memory + fan | — | ~20 | M&T |
| VR losses on non-CPU loads (~10 %) | — | ~18 | M&T method |
| **Total, RX 9070** | [GAP – no measured typical] | **≈ 653–673 W** (M&T 593–613 + 60) | |
| **Total, RTX 5070** | [GAP] | **≈ 683–703 W** (M&T 593–613 + 90) | |
Vendor system-PSU recommendations for these cards: 650 W (RX 9070, AMD; RTX 5070, NVIDIA, with a Ryzen 9 9950X system). These are ATX recommendations, not a design rating.

### 0.4 Required rating and transients
- Steady-state worst ≈ 700 W. Add ~15–20 % design margin for derating at the hot in-core ambient and ageing → **continuous rating ≈ 800–850 W at 12 V**.
- Transients: GPU boost excursions and CPU EDC (225 A on the core rail for ms) exceed the steady figures. ATX 3.x / PCIe CEM 5.x define short-duration power-excursion tolerance (order of 2× PSU rating for ~100 µs; GPU up to ~3× its rating for ~100 µs) [**verify exact numbers against the Intel ATX 3.1 design guide before setting requirements**]. Recommendation: the new PSU must ride through ≥ 1.5–2× rated for ≥ 100 µs without OCP trip and hold 12 V within ±5 % ; put OCP/OPP with a time delay (e.g. ≥ 1 ms) above the excursion profile. Add 12 V bulk capacitance on GPU and CPU boards.
- Hold-up ≥ 16 ms at full load (typical for ATX-class; RSP-750 example: 16 ms) → large bulk capacitor, which competes for volume.

### 0.5 Topology options for a custom 12 V-only PCB
| Option | Typical peak efficiency | Notes |
|---|---|---|
| A. Interleaved/bridgeless (totem-pole, GaN/SiC) PFC + LLC half/full-bridge + synchronous rectification, 12 V only | 80 PLUS Titanium-class: 90/92/94/90 % at 10/20/50/100 % load (115 V internal) [verify current CLEAResult table] | Highest density; standard for 800 W+ server/SFX PSUs. GaN raises switching frequency → smaller magnetics. **Recommended topology.** |
| B. Boost CCM PFC (Si) + LLC, 12 V only | Platinum-class ~92 % at 50 % | Lower risk, larger heatsinks/magnetics. |
| C. Phase-shifted full bridge | ~90–93 % | Older, more common at kW+; less attractive here. |
| D. Keep stock PSU and add a 2nd certified supply (external brick) for the GPU face | — | Avoids mains design; loses "single inlet". Fallback. |
Standby: separate flyback (5–11 V SB) — must keep the 11 V / 5 W standby behaviour (or redesign BP/IOB standby).

### 0.6 Heat dissipated in the core airflow
Loss = P_out × (1/η − 1):
| Output | η 90 % | η 92 % | η 94 % |
|---|---|---|---|
| 450 W (stock rating) | 50 W | 39 W | 29 W |
| 700 W (target worst) | 78 W | 61 W | 45 W |
| 850 W (rated) | 94 W | 74 W | 54 W |
Stock PSU loss at 450 W: unknown (efficiency not published) [GAP]. Plus the **system load itself rises from ~450 W to ~700 W into the same thermal core**; that is the dominant thermal issue for M&T, not the PSU loss alone. The stock PSU has no fan; a fanless 800 W+ in the shared airflow is unproven.

### 0.7 Does 800 W+ fit the stock volume?
- Stock PSU dimensions/volume: **not public [GAP]** → must be measured.
- Reference densities (certified commercial units, for comparison only): Mean Well RSP-750-12: 750 W, 12 V 62.5 A, 87 % typ, **250 × 127 × 41 mm (≈ 1.30 L)**, own fan, hold-up 16 ms (datasheet https://www.meanwell.com/Upload/PDF/RSP-750/RSP-750-SPEC.PDF). Server CRPS-format modules reach 800 W–2 kW Titanium in ≈ 185 × 73.5 × 40 mm (≈ 0.54 L) with a fan [verify vendor datasheet before use].
- Implication: 800 W in the stock bay needs ≳ 0.5–0.6 L of real volume at CRPS-class density **with forced air**; at fanless densities it is unlikely. Verdict: **fit is unknown until the bay is measured; plausible only with GaN Titanium-class design and guaranteed system-fan airflow through the PSU.**

### 0.8 Safety / certification (mandatory)
- **All mains-side (primary) design, layout, and testing must be done or verified by qualified power-electronics engineers and certified (IEC/UL/EN 62368-1).** This study does not provide a mains design and nobody should build or probe the primary side without that.
- Requirements to plan for: reinforced insulation primary↔secondary (3 kVAC hipot typical for 62368-1 class I units, e.g. RSP-750 I/P-O/P 3 kVAC); creepage/clearance per 62368-1 tables for 250 VAC working voltage, altitude and pollution degree 2 (reinforced creepage typically ≈ 5–6.4 mm — **look up the table, do not use this number as a design value**); safety-rated transformer/optocoupler/Y-caps; earth bond from the inlet; input fuse, MOV/inrush limit; leakage current limits; EMC (CISPR 32 class B, EN 61000-3-2 harmonics → PFC mandatory above 75 W); OCP/OVP/OTP/SCP; X-cap discharge.
- The reused AC inlet: confirm its type and current rating. Input current at 850 W out / 0.92 at 100 VAC ≈ 9.2 A; at 90 VAC ≈ 10.3 A — **may exceed a 10 A IEC rating at low line** [check inlet rating; consider derating to 115 VAC minimum or a lower rating].
- Housing interlock (Hall) and >240 VA bus-bar hazard must be preserved.

### 0.9 Measurements for Aidan to take (power off, unplugged, ≥ 15 min, spare/removed PSU preferred; no live mains probing)
1. Stock PSU outer envelope L × W × H and any curved/cut-outs; usable bay volume after removing the PSU (incl. clearance to CPU board, housing, I/O board).
2. PCB outline, mounting holes (4× T10 ball screws), keep-outs, max component height each side.
3. Bus-bar attachment points (4× T8 at PSU), bar cross-section (width × thickness) and length — for ~60 A capability.
4. AC inlet: type (IEC C14/C8?), markings for current/voltage rating, how it connects to the PSU PCB, earth path.
5. DC cable and signal cable to I/O board: connector type, pin count (pinout later, by qualified probing).
6. Airflow path: where system-fan air enters/leaves the PSU, free area, distance to fan.
7. Photos of both sides of the stock PCB with a scale (bulk cap size, transformer size) to estimate achievable density.
8. Weight of the stock PSU (thermal mass reference).

### 0.10 Rev B verdict
- Stock 450 W PSU: **cannot** support Ryzen 9 (230 W PPT) + xx70 GPU: shortfall ≈ 200–250 W.
- Required: ≈ 700 W worst-case 12 V, **design for 800–850 W continuous**, Titanium-class (≥ 92–94 % at 50 %), with ATX 3.x-style excursion tolerance.
- Top recommendation: proceed with the custom PSU PCB only as a professionally designed / certified effort (GaN totem-pole PFC + LLC, 12 V only + standby flyback), **after** the bay measurements show ≥ ~0.5 L and M&T confirms the core can remove ~700 W system + 45–75 W PSU loss. Interim/bring-up: a certified external 12 V supply (e.g. 750 W class module outside the chassis) — no opened mains units. Alternative if thermals fail: Ryzen 9 at Eco 105 W / 142 W PPT + GPU power cap (~500–520 W system, M&T's 650 W target).

## 1. Existing project budget (found in /workspace; /workspace/private not read)
Sources: `specs/MacPro62_Technical_Specification_2026-10-22.md` §1.1, `macpro62-interface-control-rev4.md` §13, `docs/cpu-board-power-budget.md` (2026-10-21), `../archive/docs/macpro62-storage-board-plan.md` §4.4, `macpro61-stock-hardware-reference.md` §3–4.
- Approved direction (Aidan, 2026-10-21): **stock 450 W PSU + firmware power limits**. System ceiling **445 W**, held by the BP MCU live power target (LPT, 10 Hz, target 430 W) with a hardware fast path (CARRIER_HOT#/PROCHOT, USB-C pool drop to 45 W).
- Spec v10-22 table (12 V side, worst / sustained): CB 138 / 128 W (65 W Ryzen, PPT 88 W); Face P (GPU) 130 W cap, 150 W after thermal test P3; Face S 40 / 35 W; BP 10 W (Gen4) / 17 W (Gen5); fan ≤ 10 / 3–5 W; IOB incl. ports 99 / 75 W (USB-C pool 45 W). **System ≈ 427 W (P 130) / ≈ 447 W (P 150)**.
- `docs/cpu-board-power-budget.md`: at PPT 130 W the CB rises to **201 W worst / 169 W typ**; at 138 W to 210 / 178 W. That is +63–72 W over the spec figure and conflicts with the "PPT ≤ 88 W, no X parts" rule in `v3_lane_cpu_research.md` §3.
- Storage: SM-1 face declared 40 W Class 1 (2-drive build); the 4-drive build "still uses the old 40 W allowance and needs a re-budget" (team/HANDOFF.md). Its 4×M.2 line assumed Gen3 drives (7 W each).
- Open items already logged: U-20 stock PSU behaviour at 445 W > 1 s (OCP/OPP point) unmeasured; O-8 PD renegotiation timing; PSU signal/DC pinouts unknown.
- No separate Mechanical & Thermal "power/thermal budget" file beyond the above was found; thermal limits live in the stock reference §4.2 and the face spec.

## 2. Public research
| Item | Value | Source |
|---|---|---|
| Stock PSU part | Apple 661-7542; Delta ADP-450AF | Beetstech listing [S17 in stock ref]: https://beetstech.com/product/mac-pro-a1481-power-supply-450w-661-7542 |
| Rating | 450 W continuous, 100–120 / 200–240 V AC | Apple tech specs https://support.apple.com/en-us/112025 |
| Main rail | **12.1 V @ 37.2 A** (single rail) | iFixit teardown step 22 https://www.ifixit.com/Teardown/Mac+Pro+Late+2013+Teardown/20778 |
| Standby | **11 V, 5 W** | Apple Service Guide p.22 (public copy via MacRumors) |
| Delivery | Bus bars to CPU riser and GPU A/B; DC + signal cable to I/O board; >240 VA hazardous energy on bus bars; Hall interlock disables 12 V with housing off | Apple Service Guide pp.20–22, 164, 298–299 |
| Cooling | No own fan; system fan airflow | iFixit step 22 |
| Stock wall power | 43–44 W idle; 205 / 238 / 270 W max by config | Apple https://support.apple.com/en-us/102839 |
| Stock stress | 437 W avg / 463 W peak at the wall, CPU throttled, GPUs 97 °C | AnandTech Mac Pro review p.14 (archived) |
| PSU efficiency, dimensions, OCP/OPP point, hold-up, pinout | **[GAP]** not public | — |
| AM5 power tiers | TDP 65 → PPT 88 W (TDC 75 A, EDC 150 A); 105 → 142 W (110/170 A); 170 → 230 W (160/225 A); 120 W TDP ≈ 162 W PPT by AMD's 1.35× rule | TechPowerUp https://www.techpowerup.com/295301/ ; IT之家 https://www.ithome.com/0/655/229.htm ; HWCooling https://www.hwcooling.net/en/more-ryzen-7000-details-tdp-and-ppt-igpu-features-and-more/ |
| Gen5 NVMe | Crucial T705: 3.5 A @ 3.3 V ≈ **11.55 W max**; >10 W sustained sequential; ~2.4 W light use | Tom's Hardware review https://www.tomshardware.com/pc-components/ssds/crucial-t705-2tb-ssd-review ; jisakuhibi.jp |
| M.2 connector | 3.3 V, 2.5 A/pin-group limit used in project (8.25 W) — note Gen5 drives like T705 spec 3.5 A | project CB budget; PCI-SIG M.2 [verify] |
| 2.5GbE (Intel I226-V) | 0.91 W active / 0.76 W idle / 0.6 W EEE (3 m, 25 °C); 1.185 W at 100 m/55 °C; TDP 1.3 W | Intel I225/I226 DS 596659 rev2.6; Intel ARK https://www.intel.com/content/www/us/en/products/sku/210599/ |
| USB-A 3.x | 900 mA @ 5 V = 4.5 W per port | USB 3.x spec [standard value; verify cite] |
| USB-C | 5 V/3 A = 15 W default; PD SPR up to 100 W (20 V/5 A, EPR to 240 W) | USB-IF PD spec [standard values; verify cite] |
| USB4 per-port minimum source power | **[GAP]** – not confirmed this pass | — |
| GPU in thermal core | No public core rating; project envelope ≈ 100–130 W per GPU face (inference from wall data); Face P cap 130 W, 150 W after P3 | stock ref §4.2; face spec §6.2 |
| Fan | Stock fan current unmeasured (M-IOC1); project allocation ≤ 10 W | IOB plan |

## 3. Power budget (12 V side, after board-level conversion losses)
"Idle" figures are not measured for any MP62 board; shown only where sourced, otherwise [GAP].

| Subsystem | Idle | Typical sustained | Peak / worst | Basis |
|---|---|---|---|---|
| CB, 65 W TDP (PPT 88) | [GAP] | 128 | 138 | ICD §20.4 |
| CB, 105 W TDP (PPT 142) | [GAP] | ≈ 182 [Estimate, scaled] | ≈ 215 [Estimate, scaled from 138 W case: 210 + 4/0.87] | cpu-board-power-budget.md |
| CB, 120 W TDP (PPT ≈ 162) | [GAP] | — | ≈ 238 [Estimate] | same method |
| CB, 170 W TDP (PPT 230) | [GAP] | — | ≈ 316 [Estimate] | same method |
| Face P GPU (PCIe 5.0 x16) | [GAP] | 130 | 130 cap / 150 after P3 | face spec §6.2 |
| Face S, 2× Gen5 NVMe | ≈ 5–8 [Estimate] | ≈ 20 | ≈ 2×11.55 + bucks/eFuse ≈ 26–28 | T705 rating |
| Face S, 4× Gen5 NVMe + Gen5 switch | [GAP] | [GAP] | ≈ 46 drives + switch [GAP, Gen5 switch power unknown] + ≈ 4 loss → **≥ 55–60, exceeds 40 W Class 1** | T705 rating; storage plan |
| Backplane (Gen5 redrivers) | — | 10 | 17 | arch §4.4 |
| Fan | — | 3–5 | ≤ 10 | M-IOC1 open |
| IOB incl. ports (6× USB-C pool 45 W capped, 4× USB-A, 2× 2.5GbE, HDMI 2.1b) | ≥ 0.6 W per idle 2.5GbE (EEE) | 75 | 99 (pool cap 45 W mandatory; uncapped ≈ 11.7 A > eFuse) | IOB plan §7 |
| 2.5GbE ×2 (inside IOB) | 1.2 | 1.8 | 2.6 | Intel DS / ARK |
| USB-A ×4 VBUS (inside IOB) | 0 | — | 18 | 4×4.5 W |

### Totals vs stock PSU (450 W rated, 445 W project ceiling, LPT target 430 W)
| Case | Total | Margin to 445 W |
|---|---|---|
| A: 65 W CPU, P 130, S 2× Gen5 (40 W alloc), BP 17, fan 10, IOB 99 | ≈ 434 W | +11 W |
| A sustained | ≈ 382 W | +63 W |
| B: 65 W CPU, P 150 | ≈ 454 W | **−9 W** (LPT) |
| C: 105 W CPU, P 130 | ≈ 511 W | **−66 W** |
| D: 105 W CPU, P 150, S 4× Gen5 (~60) | ≈ 551 W | **−106 W** |
| E: 170 W CPU, P 130 | ≈ 612 W | **−167 W** |

**Transients:** AM5 EDC (150 A on a 65 W part, 225 A on 170 W) and GPU boost excursions are ms-scale and exceed PPT/board caps briefly; LPT acts at 10 Hz (100 ms), the fast path in < ~2 ms. Stock PSU OCP/OPP trip level and transient tolerance are **unknown (U-20)** — this is the biggest risk to "stock PSU with limits". Bus-bar 12 V bulk capacitance on each new board must ride out GPU/CPU load steps; ATX 3.x-style 2–3× excursion behaviour of this Delta unit is undocumented.

**Verdict:** stock 450 W supply is feasible **only** with a 65 W-TDP CPU (PPT 88, or 105 W parts locked to ≤ 88 W / Eco), GPU face capped at 130 W, 2-drive or power-state-limited storage, the USB-C 45 W pool cap, and the LPT. Headroom ≈ 11 W worst, ≈ 63 W sustained. Any 105/120/170 W-class unlocked CPU, a 150 W GPU face plus full ports, or 4× Gen5 drives → shortfall of 10–170 W.

## 4. Options
| Option | Fit | Thermals | Efficiency | Safety | Notes |
|---|---|---|---|---|---|
| 1. Keep stock PSU + limits (current plan) | Perfect, uses bus bars/mounts | Proven airflow path; core heat also budget-limited (~450 W system historically throttled) | Unknown [GAP]; likely 80 Plus-class era unit | No mains work; Hall interlock must be emulated by IOB (low-voltage side only) | Need: OCP/OPP + transient measurement on a spare unit (U-20), signal pinout. **Recommended.** |
| 2. Modify stock PSU (re-rate, change OCP, add capacity) | Same | Higher dissipation in a fanless unit | — | **Mains-side work: NOT recommended. Any change to the primary side requires certified design and qualified handling; voids safety approvals.** | Reject for a first pass. |
| 3. Custom/compact internal PSU (e.g. ~600 W 12 V-only open-frame/1U module) | **[GAP]** PSU bay dimensions not measured; must reuse bus bars and IOB cable | Must be cooled by system fan; core thermals still cap ~450 W | Modern Platinum/Titanium units 92–94 % (product-specific [GAP]) | Use only a certified (IEC/UL 62368-1) off-the-shelf module; no self-built mains stage; creepage/earthing per module's guide | Only worth it if Aidan wants >65 W-class CPUs; but thermal core is likely the binding limit anyway. |
| 4. External supply (e.g. certified 12 V brick or 240 W USB-PD EPR/DC barrel input) | Loses stock IEC look; cable entry through I/O panel | Moves PSU heat out of chassis (+ ~30–40 W headroom inside) | Certified brick efficiency (DoE Level VI) | Certified external unit keeps all mains outside the build; DC-only inside | Good as bring-up/bench supply; could be a "Pro" variant or supplement (e.g. feed USB-C pool). |
Bench/bring-up: use a certified lab DC supply or certified 12 V module on the bus bars, never an opened mains unit.

## 5. Open questions for Aidan
1. CPU class: confirm 65 W TDP / PPT 88 (or 105 W parts locked to Eco). The 10-21 CB budget assumed PPT 130–138 W which does not fit.
2. Face P: is 130 W final, or is 150 W after P3 a goal (needs ~9 W more from elsewhere)?
3. Storage: 2 or 4 drives, Gen4 or Gen5? 4× Gen5 needs a new allocation (≥ 55–60 W) or NVMe power-state caps.
4. USB-C: is 45 W pool acceptable, and do USB4 ports need a guaranteed per-port minimum (e.g. 15 W)?
5. Can a spare 661-7542 be bought (when he OKs purchases) for OCP/OPP/transient tests and pinout?
6. Acceptable to offer an external-supply variant?

## 6. Escalate to Master Bot
- Conflict: CB budget (PPT 130–138 W) vs spec/ICD (PPT ≤ 88 W). Needs one owner decision; affects CB, LPT firmware, thermal M-AM5-1.
- Face S 4× Gen5 exceeds its 40 W Class 1 declaration → storage-face re-budget.
- U-20 (stock PSU OCP/OPP/transient) is a gating risk for the whole power plan; schedule measurement on a spare unit.
- Mechanical & Thermal: need PSU bay dimensions/clearances and thermal-core total capacity before any replacement-PSU option.
- Policy: any PSU mains-side modification is out of scope unless a certified design and qualified handling are arranged.

## 7. Gaps not filled (not guessed)
Stock PSU efficiency curve, dimensions, OCP/OPP, hold-up time, connector pinouts; Gen5 PCIe switch power; USB4 minimum per-port source power; all MP62 idle figures; stock fan current; HDMI 2.1b retimer/level-shifter power (assumed inside IOB 99 W).

## 8. Rev B open questions / escalations
- Aidan: confirm GPU (RX 9070 220 W vs RTX 5070 250 W); accept firmware caps (CPU Eco/PPT, GPU power limit, USB pool) if the thermal core can't take ~700 W; who will do/verify the mains design and certification (in-house qualified engineer or contracted design house)?
- Master Bot: (1) project direction changed from "stock 450 W + limits" (10-21) to "custom PSU PCB"; spec §1.1, ICD §13 and LPT 445 W ceiling need updating; (2) thermal-core capacity for ~700–770 W total heat is the gating item for M&T; (3) mains safety policy: no build/probing of primary side without qualified/certified design.
