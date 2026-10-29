# MacPro6,2 AM5 v3 CPU board: 12 V input power budget
Date: 2026-10-21 (ET). Research only; no KiCad files changed.

**Basis:**
- Ryzen 7000/9000 with **PPT 130 W** as the main case and 138 W for comparison.
- PPT is socket power and covers VDDCR + SOC + MISC.
- Board parts are from `archive/kicad/macpro62-am5-v3/placeholders_flagged.txt`: SiC654 ×8 + FP4, PROM21, 4 × DDR5 **UDIMM**, J8 M.2, U16 VL822, U9 RP2350.
- Worst = every load at its maximum at the same time. Typical = PPT-limited sustained load with typical peripherals.
- Tags: [Sourced] datasheet/vendor, [Estimate].

## PPT 130 W

| Load | Out worst (W) | Out typ (W) | η worst / typ | 12 V in worst (W) | 12 V in typ (W) | Converter | Source |
|---|---|---|---|---|---|---|---|
| CPU (VDDCR ×5 + VDDCR_SOC ×2 + VDD_MISC ×1), at the PPT | 130.00 | 130.00 | 87 / 90 % | 149.4 | 144.4 | SVI3 VRM, 8 × SiC654 + FP4 150 nH | PPT per brief; η from Vishay SiC654 DS Fig. 6/9 (12→1.05 V, ≈ 91–94 % stage-only at 10–25 A/phase, 300–500 kHz) minus inductor DCR, PCB and controller losses → system 87 % worst / 90 % typ [Estimate] |
| PROM21 chipset (core + PHY rails) | 7.00 | 4.00 | 88 / 90 % | 8.0 | 4.4 | U6 bucks | Max ≈ 7 W per chip: AMD/ASMedia PROM21 figures (Tom's Hardware, WePC, Notebookcheck); typical 4 W [Estimate] |
| DDR5 UDIMM ×4 (J6/J7/J9/J10, UMAX C-90414 = UDIMM, on-module PMIC) | 20.00 | 10.00 | 81 / 85 % | 24.7 | 11.8 | on-module PMIC (from 5 V VIN_BULK) × U7 5 V buck | Module type: UDIMM per placeholders_flagged.txt (not SODIMM). PMIC η from JEDEC PMIC5100 limits / Richtek RTQ5132 (85–93 %). Per-module 5 W worst / 2.5 W typ for 32 GB 2R at 2DPC DDR5-3600 [Estimate]. PMIC capability ceiling 10.6 W/module (SWA+SWB 2 × 4 A × 1.1 V + SWC 1 A × 1.8 V) |
| VDDIO_MEM_S3 1.1 V (CPU memory PHY, U8) | 3.00 | 1.50 | 88 / 90 % | 3.4 | 1.7 | U8 buck | AMD rail list under NDA (A-11) [Estimate] |
| M.2 boot SSD on PROM21 Gen4 x4 (J8) | 8.25 | 3.00 | 90 / 92 % | 9.2 | 3.3 | 3V3 buck | Worst = M.2 3.3 V connector limit 2.5 A (PCI-SIG M.2). Reference drive Samsung 990 PRO: 5.5–6.5 W average read (DS rev 2.0). Typical 3 W mixed [Estimate] |
| VL822-Q7 USB 10G hub U16 (+ crystal, flash) | 1.50 | 0.80 | 88 / 90 % | 1.7 | 0.9 | 3V3 + 1.05 V bucks | VIA VL822 DS: power dissipation 'TBD'. Comparable Gen2 hubs ≈ 1 W [Estimate] |
| RP2350 EC U9 + QSPI flash | 0.20 | 0.10 | 85 / 88 % | 0.2 | 0.1 | 3V3_SB LDO/buck | RP2350 DS ≈ 20–30 mA at 3.3 V for both cores at 150 MHz [Estimate from DS typical figures] |
| CPU S5/aux rails U4/U5 (VDD_18/33_S5, MISC_S5), TPM, SPI ROMs, clocks, sequencing | 2.00 | 1.00 | 85 / 88 % | 2.4 | 1.1 | U4 bucks/LDOs | Rail list NDA (A-11) [Estimate] |
| CB 5V_SBY standby share (S0 overhead) | 1.50 | 1.00 | 100 / 100 % | 1.5 | 1.0 | from the BP 5V_SBY | ICD v3 §13: CB 5V_SBY 1–3 W [Estimate]; counted once |
| Input path: U11 TPS259851 eFuse (≈ 0.6 mΩ) + RS1 0.5 mΩ shunt (INA226) |  |  |  | 0.3 | 0.2 |  | TI TPS25985 R_ON ≈ 0.59 mΩ (DS); I²R at the input current |
| **Total CB 12 V input** | | | | **200.8 W (16.7 A)** | **169.0 W (14.1 A)** | | |

## PPT 138 W

| Load | Out worst (W) | Out typ (W) | η worst / typ | 12 V in worst (W) | 12 V in typ (W) | Converter | Source |
|---|---|---|---|---|---|---|---|
| CPU (VDDCR ×5 + VDDCR_SOC ×2 + VDD_MISC ×1), at the PPT | 138.00 | 138.00 | 87 / 90 % | 158.6 | 153.3 | SVI3 VRM, 8 × SiC654 + FP4 150 nH | PPT per brief; η from Vishay SiC654 DS Fig. 6/9 (12→1.05 V, ≈ 91–94 % stage-only at 10–25 A/phase, 300–500 kHz) minus inductor DCR, PCB and controller losses → system 87 % worst / 90 % typ [Estimate] |
| PROM21 chipset (core + PHY rails) | 7.00 | 4.00 | 88 / 90 % | 8.0 | 4.4 | U6 bucks | Max ≈ 7 W per chip: AMD/ASMedia PROM21 figures (Tom's Hardware, WePC, Notebookcheck); typical 4 W [Estimate] |
| DDR5 UDIMM ×4 (J6/J7/J9/J10, UMAX C-90414 = UDIMM, on-module PMIC) | 20.00 | 10.00 | 81 / 85 % | 24.7 | 11.8 | on-module PMIC (from 5 V VIN_BULK) × U7 5 V buck | Module type: UDIMM per placeholders_flagged.txt (not SODIMM). PMIC η from JEDEC PMIC5100 limits / Richtek RTQ5132 (85–93 %). Per-module 5 W worst / 2.5 W typ for 32 GB 2R at 2DPC DDR5-3600 [Estimate]. PMIC capability ceiling 10.6 W/module (SWA+SWB 2 × 4 A × 1.1 V + SWC 1 A × 1.8 V) |
| VDDIO_MEM_S3 1.1 V (CPU memory PHY, U8) | 3.00 | 1.50 | 88 / 90 % | 3.4 | 1.7 | U8 buck | AMD rail list under NDA (A-11) [Estimate] |
| M.2 boot SSD on PROM21 Gen4 x4 (J8) | 8.25 | 3.00 | 90 / 92 % | 9.2 | 3.3 | 3V3 buck | Worst = M.2 3.3 V connector limit 2.5 A (PCI-SIG M.2). Reference drive Samsung 990 PRO: 5.5–6.5 W average read (DS rev 2.0). Typical 3 W mixed [Estimate] |
| VL822-Q7 USB 10G hub U16 (+ crystal, flash) | 1.50 | 0.80 | 88 / 90 % | 1.7 | 0.9 | 3V3 + 1.05 V bucks | VIA VL822 DS: power dissipation 'TBD'. Comparable Gen2 hubs ≈ 1 W [Estimate] |
| RP2350 EC U9 + QSPI flash | 0.20 | 0.10 | 85 / 88 % | 0.2 | 0.1 | 3V3_SB LDO/buck | RP2350 DS ≈ 20–30 mA at 3.3 V for both cores at 150 MHz [Estimate from DS typical figures] |
| CPU S5/aux rails U4/U5 (VDD_18/33_S5, MISC_S5), TPM, SPI ROMs, clocks, sequencing | 2.00 | 1.00 | 85 / 88 % | 2.4 | 1.1 | U4 bucks/LDOs | Rail list NDA (A-11) [Estimate] |
| CB 5V_SBY standby share (S0 overhead) | 1.50 | 1.00 | 100 / 100 % | 1.5 | 1.0 | from the BP 5V_SBY | ICD v3 §13: CB 5V_SBY 1–3 W [Estimate]; counted once |
| Input path: U11 TPS259851 eFuse (≈ 0.6 mΩ) + RS1 0.5 mΩ shunt (INA226) |  |  |  | 0.3 | 0.2 |  | TI TPS25985 R_ON ≈ 0.59 mΩ (DS); I²R at the input current |
| **Total CB 12 V input** | | | | **210.0 W (17.5 A)** | **177.9 W (14.8 A)** | | |

## Findings
1. **CB 12 V input: ≈ 201 W worst / 169 W typical at PPT 130 W, and ≈ 210 / 178 W at 138 W.**
   - The ICD v3 §20.4 figure was ≈ 138 W worst / 128 W sustained, but that assumed PPT 88 W.
   - The system total therefore rises by about 63 W (PPT 130) or 72 W (PPT 138) over that figure. Against the 445 W ceiling, the LPT or firmware limits must hold this.
2. **Input current:** 17.5 A worst at 138 W, which is inside the U11 TPS259851 ILIM of about 25 A. Recheck the LUG1/LUG2 and plane rating (≥ 20 mm, L5+L6) at about 15 A continuous.
3. **VRM loading:**
   - **PPT 130 W is a 105 W-TDP-class setting** (PPT = 1.35 × TDP gives about 96 W). That conflicts with `docs/v3_lane_cpu_research.md` §3, which says the BIOS must lock PPT ≤ 88 W and X parts are out.
   - VRM loading at 130 W: about 110 A VDDCR across 5 phases, so ≈ 22 A per phase continuous. The SiC654 is a 50 A stage, so this is OK electrically, but stage loss rises to about 3 W per phase (SiC654 Fig. 9).
   - About 17–20 W of VRM heat goes into the core plate. The thermal check M-AM5-1 must be redone.
4. **DIMM type:** the board uses **UDIMM** (UMAX C-90414), with the PMIC on the module fed from the 5 V VIN_BULK rail (U7). No SODIMM option is placed.
5. **VL822 hub (U16):**
   - It is a **separate chip on the CPU board** (`usb_hub.kicad_sch`, sheet 'USB 10G hub (U16 VL822-Q7)'), fed from PROM21 10G #4.
   - Its 4 downstream ports go over J3/HS1 k6–k9 to IOB USB-A A1–A4 (ICD v3 line 566, `prom21.kicad_sch`, `iob_hs.kicad_sch`).
   - The IOB has no USB3 hub of its own; its CH334 hubs U32–U35 are USB2 only.
   - **Its 0.8–1.5 W is therefore NOT in the IOB's 95–110 W**, which is the IOB 12 V input (IOB plan §7 / ICD §13). It is counted here.
   - The USB-A VBUS power for A1–A4 is on the IOB 5V_A rail and stays in the IOB budget.
6. **Main uncertainties:**
   - AMD NDA rail data: VDDIO_MEM, S5 rails, and whether VDD_MISC sits inside PPT.
   - The VL822 datasheet power figure is 'TBD'.
   - Real DIMM power at 2DPC.
   - Measure all of these at bring-up with the CB INA226.
