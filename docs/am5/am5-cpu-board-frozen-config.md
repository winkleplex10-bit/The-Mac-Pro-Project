# AM5 CPU board: frozen configuration (DRAFT for Aidan's sign-off)
**Status (rev 2, 2026-10-26 ~17:35 ET): DRAFT. The rev-2 changes below were relayed via Base Board & Connectors and are pending Aidan's confirmation.**

## Rev 2 changes (relayed, pending Aidan)
- **No chipset boot NVMe.** PROM21 downlink #2 is now unused/spare. J8 boot M.2 on PROM21 is dropped.
- **PROM21 uplink load ≈ 1.24x** (as relayed by Base Board & Connectors; down from ~2x). The breakdown hasn't been re-derived here [check].
- **FLAG: the OpenCore boot drive needs a new home.** Options: one SSD-board NVMe (CPU Gen5 x4), the spare PROM21 downlink #2 routed off-board, or elsewhere. Aidan to decide.
- **J3 rev 2** (CPU board → base board, MCIO 124): `kicad/macpro62-am5-v3/docs/mp62-cb-j3_mcio124_host-end_am5_rev2.csv`.
  - Carries: ASM4242 Gen4 x4 (PROM21 downlink #1); 2 i226 x1 (PROM21 flex ports); USB-C C1-C4 (non-USB4) on CPU native USB 10G; 1 PROM21 USB 10G to the USB-A hub path; 1 PROM21 USB2 to a base-board USB2 hub.
  - Also carries 3 REFCLKs and sideband: SLP_S3#/S5#, 3 PERST#, 3 CLKREQ#, WAKE#, PWR_BTN#, I2C + alert, 2 PRSNT#.
  - Removed: iGPU DP, VBAT, USB_OC#, the per-port A/C USB3 links (USB-A ports now behind the base-board hub), and the 4 extra USB2. LEDs/status now go via the base MCU over I2C.
  - Count: 67 signal + 57 GND = 124 contacts, plus 6 mounting pads (130 pads). 13 freed positions were set to GND. G-S-S-G kept.
- **Superseded by rev 2:** USB-C C1-C4 change from "2 DP-alt + 2 USB 3.2" on CPU native USB to "C1-C4 non-USB4" on CPU native USB, and the boot NVMe on PROM21 downlink #2 is removed. Sections below are rev 1 and are kept for history.

Date: 2026-10-26 (ET). Author: CPU & Base Board. Docs only: no KiCad edits, nothing pushed or bought.
Basis: Aidan 2026-10-26: chipset design (PROM21, no PCIe switch); I/O and expansion boards connect to the base board via Meg-Array (like the Mac Pro 6,1); CPU board keeps card-edge J1; freeze the CPU board AM5 config; base board stays flexible. Baseline 2026-10-25: PCIe 5.0 x16 GPU, PCIe 5.0 x8 SSD board (2-4 NVMe), 6x USB-C (2 USB4, 2 DP-alt, 2 USB 3.2), 4x USB-A, 2x 2.5GbE, HDMI 2.1 from the GPU, CPU iGPU outputs unused, 142 W PPT cap, 1.6 mm JLC10161H-1080A.
Tags: [Sourced] = cited public page; [Estimate]; [GAP] = no public data.

## 1. Verified platform facts
| Fact | Value | Source |
|---|---|---|
| Ryzen 9000 native PCIe lanes total/usable | **28 / 24, PCIe 5.0** | [AMD Ryzen 9 9950X page](https://www.amd.com/en/products/processors/desktops/ryzen/9000-series/amd-ryzen-9-9950x.html) [Sourced] |
| Ryzen 9000 native USB | 4x USB 3.2 Gen2 10 Gbps + 1x USB 2.0 | same page [Sourced] |
| AM5 usable lane split | "1x16 or 2x8 PCIe 5.0" graphics + "1x4 PCIe 5.0 + 4x PCIe GPP"; "up to 24 usable PCIe 5.0 lanes" | [AMD Socket AM5 Quick Reference Guide, Nov 2024](https://www.amd.com/content/dam/amd/en/documents/partner-hub/ryzen/amd-socket-am5-quick-reference-guide.pdf) [Sourced] |
| Ryzen 7000 lanes | Same AM5 platform split per the QRG; per-SKU 7000 page not opened this turn → confirm one 7000 SKU page [GAP-minor] | QRG |
| PROM21 (one chip = B650) | Gen4 x4 uplink; 2x Gen4 x4 downlinks; 4x flexible PCIe 3.0 x1 / SATA; 6x USB 3.2 Gen2 (2 can fuse to one 20G); up to 6x USB 2.0; ~7 W; 19x19 FCBGA | [Angstronomics](https://www.angstronomics.com/p/site-launch-exclusive-all-the-juicy), [WePC](https://www.wepc.com/news/am5-prom21-chipset-technical-information-revealednbspnbsp/) [Sourced, press, not AMD datasheet] |
| USB4 controller candidate ASM4242 | PCIe 4.0 **x4** upstream; 2x USB4 40G ports; 2x DP 1.4a sink inputs (4 lanes, HBR3); xHCI; 11x11 FCBGA; SRIS supported | [ASMedia ASM4242](https://www.asmedia.com.tw/product/e20zx49yU0SZBUH5/363Zx80yu6sY3XH2.html), [PCI-SIG listing](https://pcisig.com/asm4242) [Sourced] |
| ASM4242 power, pinout, availability | not public | [GAP] |

**Consequence (important):** the 24 usable lanes are x16 (graphics) + x4 (NVMe) + x4 (GPP). The "x8 SSD board" is therefore **two x4 Gen5 links** (NVMe x4 + GPP x4), not one x8 link. Whether the GPP x4 runs at Gen5 on all 7000/9000 SKUs and how it may bifurcate (x2/x2 for 3-4 NVMe) is NDA → [GAP]. 3-4 drives on x8 needs either bifurcation (if allowed) or a switch on the SSD board (Aidan: no PCIe switch → flag).

## 2. Lane map (frozen proposal)
| CPU lanes | Use | Gen | Route |
|---|---|---|---|
| x16 graphics | GPU face | 5.0 | J1 → base → GPU board |
| x4 NVMe | SSD board link A (NVMe 1) | 5.0 | J1 → base → SSD board |
| x4 GPP | SSD board link B (NVMe 2, or x2+x2 [GAP]) | 5.0 [GAP per SKU] | J1 → base → SSD board |
| x4 chipset | PROM21 uplink | 4.0 | on the CPU board (Option C) |
| USB 10G x4 native | 2x DP-alt USB-C data + 2x USB-C 3.2 | USB 3.2 Gen2 | J3 → base |
| USB 2.0 native x1 | spare / BP MCU | 2.0 | J1 (today USB2_SPARE) |

PROM21 allocation:
| PROM21 resource | Use |
|---|---|
| Gen4 x4 downlink #1 | **ASM4242 USB4** (x4 Gen4) |
| Gen4 x4 downlink #2 | boot NVMe J8 (OpenCore) |
| Flex x1 #1 / #2 | i226-V #1 / #2 (2.5GbE) |
| Flex x1 #3 / #4 | spare (SATA or PCIe x1, e.g. Wi-Fi) |
| USB 10G #1 | VL822 hub upstream → USB-A A1-A4 (shared 10 Gb/s) |
| USB 10G #2-#6 | spare (or move the 2 USB-C 3.2 here and free CPU native ports) |
| USB 2.0 x6 | face P/S, BP MCU, USB-C USB2 legs [count GAP until I/O board pin plan] |
| SATA | none required by baseline |

Display: CPU iGPU unused. GPU display outputs: 2x DP → ASM4242 DP-in (USB4 ports), 2x DP → DP-alt muxes on the I/O board, 1x HDMI 2.1 → I/O board. That is 5 links; Navi23 has 5 PHYs [Sourced earlier, Linux dcn302], but the baseline GPU is "PCIe 5.0 x16", so its display count is [GAP] until the GPU is chosen. GPU display path to the I/O board is a base-board/Meg-Array matter, not the CPU board.
PROM21 uplink oversubscription: x4 Gen4 = 7.88 GB/s shared by USB4 (x4 Gen4), boot NVMe (x4 Gen4), 2 i226, hub → about 2x oversubscribed at full load [Estimate].

## 3. Connector plan
Options for getting the PROM21/USB domain to the I/O board now that I/O meets the base board via Meg-Array:
| Option | J1 carries | Pin math (224) | Verdict |
|---|---|---|---|
| B: PROM21 on CPU board, everything over J1 | 48 Gen5 pairs + 3 refclk + ~22 I/O pairs + ~3 I/O refclk + ~6 USB2 + ~20 sideband + 8 standby | ~198 signal/power pins → ~26 GND | **Does not fit** at a sane ground ratio (today 78 GND) |
| A: PROM21 on base board | 56 pairs (24 Gen5 + x4 uplink) + 4 refclk = 120 + 20 sideband + 8 standby | 148 → **76 GND** (needs 2 fewer GND than today) | Marginal fit; moves boot NVMe/PROM21 power off the CPU board; PROM21 sideband needs [GAP NDA] |
| **C (recommended): PROM21 on CPU board, J3 MCIO 124 re-targeted to the base board** | J1: 48 Gen5 pairs + 3 refclk = 102 pins + ~20 sideband + 8 standby + USB2 ~8 | ~138 → ~86 GND available | **Fits with margin** |

Option C J1 budget: 96 Gen5 data + 6 refclk (GPU, SSD A, SSD B) + ~20 low-speed (existing set: PRSNT x2, PWRBTN, RSTBTN, PLTRST, SUS_S3/S5, RSMRST, THERMTRIP, CARRIER_HOT, PWR_ALERT, VIN_PWR_OK, WAKE, I2C x2, UART x2, FAN x2, BIOS_SEL) + 8 standby (6x 5V_SBY, 2x 3V3_SB) + 4-8 USB2 = ~134-138 → 86-90 for GND/spare. Today's file has 78 GND for 59 pairs; same ground pattern fits. Exact contact map to be generated after sign-off.
Option C J3 (MCIO 124, 80 signal today): ASM4242 x4 Gen4 (8 pairs) + 2 i226 x1 (4) + VL822 4 ports (8) or hub moved to I/O board (2) + 4 native USB 10G (8) + refclks 3 + USB2 + sideband. Removing iGPU DP (6 lane pairs + 2 AUX + 2 HPD = 18 pins) frees room. Whether ASM4242 sits on the CPU board or I/O board: recommend **I/O/base side** (near the ports and the GPU DP-in), so J3 carries its x4 Gen4. J3 cable now goes CPU board → base board (base-board Meg-Array carries on to I/O).
Gen5 channel: base-board Gen5 estimate 18-35 dB vs the 36 dB budget (loss_budget_A1.md, 4L numbers; 1080A loss [GAP]) → **Gen5 redrivers/retimers needed on the base-board path** (previous candidate DS320PR810). Base board side, flexible. Mini Cool Edge is rated 32-56 GT/s [Amphenol datasheet]; Meg-Array Gen5 rating [GAP].

## 4. Power at 142 W PPT
CPU board 12 V ≈ 214.6 W / **17.9 A** [Estimate: cpu-board-power-budget.md scaled at 87 % VRM efficiency]. Under the U11 TPS259851 ILIM ≈ 25 A; **above the ~15 A the LUG/plane (≥20 mm, L5+L6) was checked for → re-check plane width/copper on the 1080A stack (inner 0.5 oz)**. VDDCR ≈ 120 A over 5 phases (≈24 A/phase, SiC654 50 A). ASM4242 power [GAP] (lands on the base/I/O side in Option C). Standby via J1: 6.6 A 5V_SBY / 2.2 A 3V3_SB at 1.1 A/contact.

## 5. Delta vs current KiCad (macpro62-am5-v3) — to do on the next approved KiCad pass
1. Remove iGPU DP (DDIB 4-lane, DDIC 2-lane, AUX, HPD) from J3 and schematics.
2. J1 re-pin: drop FS x4+x4 Gen4 (slot A/B) → SSD link A x4 + link B x4 Gen5 with 2 refclks; keep FP x16 Gen5; review SATA0 (drop), USB2 set; regenerate cpulink_224_pinout_am5_v4.csv and keep the GND count ≥ 78.
3. PROM21 allocation per §2 (downlink #1 → J3 for ASM4242; #2 → J8; flex x1 → i226 x2; USB 10G #1 → VL822).
4. USB4: ASM4242 not on the CPU board (recommended); J3 carries its x4 Gen4 + refclk.
5. J3 fate: keep MCIO 124 RA, re-target CPU board → base board; new J3 pin table (USB4 x4, i226 x2, USB 10G, USB2, refclks, sideband).
6. CPU native USB 10G x4 → J3 (2 DP-alt C data, 2 USB-C 3.2).
7. Stackup/rules to JLC10161H-1080A widths; power plane re-check for 17.9 A.

## 6. Open items for Aidan
1. Approve Option C (PROM21 + boot NVMe on CPU board, J3 MCIO to base board) vs Option A (PROM21 on base board).
2. SSD board = 2x x4 Gen5 (not one x8); 3-4 NVMe needs bifurcation [GAP] or a switch (excluded). Accept 2 NVMe, or allow a switch on the SSD board?
3. ASM4242 location (recommend I/O/base side) and its power [GAP].
4. Gen5 redrivers/retimers on the base board (cost, layers).
5. PROM21 uplink oversubscription (~2x) accepted?
6. GPU choice → display link count (5 needed for 2 USB4 DP-in + 2 DP-alt + HDMI).
7. 12 V plane re-check at 17.9 A on 1080A.

- RTC: use on-board CR2032 (BT1 area) feeding VBAT_RTC_CB; delete VBAT_RTC_IOB input (VBAT not carried on base/I/O Meg-Array). Pending Aidan sign-off. (2026-10-26)

## Decisions 2026-10-28 (relayed by Master Bot from Aidan)
- Firmware: Ryzen 7000/9000 target kept; AGESA via licensed board maker (ODM). openSIL/8000G path not pursued.
- VRM controller: TI TPS53685 (public datasheet, AMD SVI3) replaces NDA controllers; power-stage compatibility (SiC654 vs TI NexFET) to be checked.
- Gen5 lanes (x16 GPU, x4+x4 SSD board A): TI DS320PR1601 / DS320PR810 redrivers on base board, PT5161L retimer fallback footprint + 10 mm heatsink room (Base Board & Connectors owns placement; SI & Fab confirms budget). Nothing on CPU board.
- GPU path on hold: placeholder Gen5 x16; CPU board J1 unchanged.
- SSD board A only (two native CPU x4 Gen5 ports); board B on hold.
- NDA items remaining for CPU board: PROM21 datasheet (justified), AGESA (via ODM).
