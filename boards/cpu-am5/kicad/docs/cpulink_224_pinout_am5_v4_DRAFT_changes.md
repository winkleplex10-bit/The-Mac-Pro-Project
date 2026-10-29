# J1 (CPU-LINK, Amphenol ME1022410103011 Mini Cool Edge 224) — v4 DRAFT change note
Date: 2026-10-28 (ET). Author: CPU Board. DRAFT ONLY: not applied to KiCad, not pinned, not pushed. For Base Board & Connectors review, then Aidan's approval.
Basis: Aidan via Base Board & Connectors — "Revise J1 to add 12 V pins from the CPU board"; frozen config (/workspace/docs/am5-cpu-board-frozen-config.md); v3 file cpulink_224_pinout_am5_v3.csv.

## Result: fits. 16 contacts found without losing any live function.
| Class | v3 | v4 DRAFT |
|---|---|---|
| Signal | 132 (incl. 8 SATA0/RSVD_HS, 2 USB2_FACES) | 126 |
| GND | 78 | **80** (+2 CC_PRSNT short fingers, also GND, unchanged) |
| Power | 8 standby (in) | 8 standby (**out**) + **8 P12V (out)** = 16 |
| Spare | 4 RSVD_HS (NC) | 0 |
Total 224.

## Layout
- Pins 1–53: unchanged (FP Gen5 x16, FP_REFCLK, USB2_FACEP, G-S-S-G pattern).
- 54–77: SSD link 0 (CPU NVMe x4) lanes 0–3, then SSD link 1 (CPU GPP x4) lanes 0–3, Gen5. A=TX, B=RX, a GND row after every lane (same shielding as FP).
- 78–79: SSD0_REFCLK (A) / SSD1_REFCLK (B); 80 GND row.
- 81–91: low-speed: USB2_MCU, USB2_SPARE, SLP/reset/power/thermal sideband, I2C0, UART0, FAN (all v3 signals kept, moved).
- 92 GND; 93 3V3_SB ×2; 94–96 5V_SBY ×6 (now CB → base); 97–102 GND (6 rows = 12); **103–106 P12V ×8**; 107–111 GND ×10; A112 CC_PRSNT2#, B112 GND.
- 12 V sits at the far end of bay 4, away from all Gen5 pairs, with 11 rows of low-speed + ≥2 GND rows between it and the nearest high-speed pair (refclk at row 79).

## Pins reassigned (why)
- SATA0 B70/B71/A73/A74: dropped per frozen config (no SATA in baseline).
- RSVD_HS_A1/A2 A76/A77/A79/A80: reserved NC, freed.
- USB2_FACES B76/B77: SSD board A doesn't use USB2 (frozen config); freed.
- FS_* Gen4 slot A/B (v3 rows 54–55, 58–68, 82–87, 101–105) → renamed/repacked as SSD0/SSD1 Gen5 rows 54–77. This also takes the old slot-B lanes out of bay 4 where they were mixed in with sideband (better Gen5 SI).
- FS_REFCLK / FS_REFCLK1 → SSD0_REFCLK / SSD1_REFCLK at row 78–79.
- Sideband, USB2_MCU, USB2_SPARE: same nets, moved to rows 81–91.
- 5V_SBY/3V3_SB: same count (6 + 2), moved to 93–96, direction reversed (CB generates standby from 12 V standby and feeds the base board). CB standby buck must be sized for base-board standby load + own load (6.6 A 5V / 2.2 A 3V3 contact capacity at 1.1 A; ~4.5 A / 1.5 A at 0.75 A derating) [check].
- New P12V ×8 rows 103–106: 8 × 0.75 A = 6.0 A derated (8.8 A at full 1.1 A rating). Feed from CB 12 V after the TPS259851 eFuse — eFuse ILIM (~25 A) and the CB 12 V plane (verified to ~15 A) must now cover 17.9 A CPU board + up to 6 A base board ≈ 24 A → **re-check plane and ILIM; flag for Aidan**.

## Ground target note
Total GND 80 ≥ 78 (requirement met). Literal "+8 GND" (86) was not reached; the 12 V return has 22 GND contacts in rows 97–112 next to it. If 86 is wanted, these could go (lowest impact first):
1. USB2_FACEP B51/B52 (GPU face aux USB2; GPU on hold, USB2 can come from the base hub) → +2
2. FAN_PWMOUT / FAN_TACHIN (fan control already via base MCU over I2C) → +2
3. UART0_TX / UART0_RX (EC↔BP MCU; I2C0 covers it, loses a debug path) → +2
4. BIOS_SEL (optional dual-image select; could be an I2C GPIO) → +1
5. USB2_SPARE (J3 already carries a USB2 to the base hub) → +2

## Open
- Exact base-board 12 V current (Base Board & Connectors) — if >6 A, more P12V pins needed (take from the list above).
- REFCLK indices and SSD lane polarity/order on AM5 are NDA [GAP]; lane reversal may be needed at layout.
- Not applied to KiCad schematic/PCB; nothing pushed.

## 2026-10-28 17:54 EDT: Aidan's decision (relayed by Base Board & Connectors)
- J1 P12V (rows 103-106, 8 pins) is fed from LUG1/LUG2 AHEAD of the CPU board TPS259851 eFuse ("pull the power before that fuse"). The base board carries its own eFuse.
- The CPU board eFuse/plane load stays about 17.9 A (26.3 A at 230 W); the 12 V plane re-check is still open.
- Standby buck upsizing: NOT approved yet, unchanged.
- The v4 map is accepted by Base Board & Connectors; pinning still waits for Aidan.
