# MacPro6,2 I/O board — AM5 plan (draft, I/O & Storage, 2026-10-26)

Supersedes the Z790-era routing in /workspace/macpro62-io-board-plan.md. Source map is CPU & Base Board's **draft** (docs/am5-cpu-board-frozen-config.md, not yet signed off by Aidan). J2 (MCIO-74 display) is frozen and not touched here.

## 1. Frozen port list (Aidan, Oct 26) — rev 2 per base-iob-megarray-review.md and interboard-bandwidth-map.md
| Port | Data source | Display | Main IOB parts |
|---|---|---|---|
| USB-C C3, C4: USB4 40G | ASM4242 ← PROM21 DL1 Gen4 x4 | DPD → ASM4242 DP-in 1, shared by both USB4 ports. DP-in 2 is unfed (an option for Aidan) | ASM4242, USB4 retimers, PD controllers |
| USB-C C1, C2: 10G + DP Alt | CPU USB 10G #1, #2 | DPA → C1, DPB → C2 over the MEG-Array | Alt-mode mux/redriver, PD |
| USB-C C5: USB 3.2 10G | CPU USB 10G #3 | – | mux/redriver, PD |
| USB-C C6: USB 3.2 10G | PROM21 USB 10G (the CPU has only 4 ports) | – | mux/redriver, PD |
| USB-A 1–4: 10G | CPU USB 10G #4 → **VL822 hub on the IOB** | – | VIA Labs VL822 (1 up / 4 down, 10G), port power switches |
| 2.5GbE ×2 | PROM21 flex x1 each | – | i226-V ×2 |
| HDMI 2.1 | – | DPC over the MEG-Array → FRL retimer | HDMI 2.1 FRL retimer |

Navi23 has exactly **4 display streams**: DPA → C1, DPB → C2, DPC → HDMI and DPD → USB4. The two USB4 ports share one stream.

**PROM21 downlink 2 is spare** now that Aidan dropped the boot NVMe on the chipset. Boot comes from the SSD board, which has 2× Gen5 x4 over MCIO.

## 2. Base→IOB link: 300-position MEG-Array, 4 mm (84500 plug / 84501 receptacle, 10×30)
- **Part check:** the Amphenol datasheet lists 300 positions as 10×30, with plug 84500 and receptacle 84501 at 4 mm. The same table also shows a 5.5 mm and an 8 mm option [1].
- **Pin map (rev 3, UHBR20):** docs/pinmaps/base-iob-megarray.csv, laid out as a physical grid.
  - Rows A–K, skipping I. **Gap:** I didn't confirm Amphenol's row lettering and A1 orientation from a footprint drawing.
  - **Rows A–C hold display** (DPA, DPB, DPC, DPD: 20 pairs).
  - **Row D is a full GND row.**
  - **Rows E–F hold PCIe** (15 pairs, including 3 REFCLKs).
  - **Row G is a full GND row.**
  - **Rows H–K hold USB 10G and USB2** (17 pairs).
  - Each row runs G-P-N-G, so every pair has GND on both sides. Columns 3 and 28 are GND, which separates the blocks from the single-ended pins in columns 1–2 and 29–30.
- **Pin usage:** 52 pairs (104 pins) + 140 GND + 26 single-ended = **270 used, 30 spare**.
  - About 2.5 GND per pair, above the 1.5–2 target, because of the two isolation rows.
  - The spare spread is: 8 in the DP block, 2 in PCIe, 14 in USB and 6 among the single-ended pins.
- **UHBR20 margin note:** DPA, DPB and DPC run at 20 Gb/s per lane, which is at the edge of the MEG-Array's 28–32 Gb/s rating (and 32 Gb/s is only documented at 4 and 14 mm).
  - Keep the display traces as short as possible on **both** the base board and the IOB.
  - SI & Fab must check Amphenol's 4 mm S-parameters before the layout is frozen.
  - DPD runs at HBR3, 8.1 Gb/s (see §5a).
- **Display now crosses the base board:** GPU → J2 retargeted to the base board (owned by GPU Board and Base Board; the old J2 files are not edited here) → base → MEG-Array → IOB DP-Alt muxes and the HDMI retimer.
- **Rating:** up to 32 Gb/s (4 mm and 14 mm documented) [1], and 28 Gb/s at 4/6 mm per GS-20-033 [2]. 0.45 A per contact, so no power goes through this connector [review A2].

## 3. Sources (draft, not signed off)
- **CPU:** USB 10G ×4 (C1, C2, C5, VL822), USB2 ×1.
- **PROM21:** Gen4 x4 to the ASM4242, flex x1 ×2 to the i226 chips, USB 10G ×1 (C6), USB2 ×6.
- **GPU:** DPA, DPB, DPC, DPD.
- **PROM21 DL2:** spare.

## 4. USB2 tally
| Need | USB2 source | Over MEG |
|---|---|---|
| C3 USB4 | PROM21 USB2 direct → ASM4242/port USB2 | 1 |
| C4 USB4 | PROM21 USB2 direct | 1 |
| C1, C2 (DP-Alt) | PROM21 USB2 ×2 | 2 |
| C5 | CPU USB2 | 1 |
| C6 | PROM21 USB2 | 1 |
| USB-A 1–4 | VL822 built-in USB2 hub; upstream from PROM21 USB2 | 1 |
| **Total** | CPU 1/1 + PROM21 6/6 | **7** |

- **Balance:** 10 ports are served with 7 pairs. The CPU uses 1 of its 1 USB2 and PROM21 uses 6 of its 6, so **0 spare**.
- **Gap:** PROM21's 6 USB2 count comes from the press, not an AMD datasheet.
- **Gap:** whether the ASM4242 integrates or passes USB2 for its USB4 ports isn't public (NDA). If it supplies its own, 2 PROM21 USB2 are freed.
- **Fallback if PROM21 has fewer USB2:** a USB2 hub on the base board, e.g. USB2514B. That's also a gap; I haven't opened its datasheet.
- **Not covered:** nothing is left for internal USB (Bluetooth, fan MCU). That would need a hub port.

## 5. Display and USB4 signal conditioning (Aidan: full UHBR20 display)
**Placement rule:** every retimer or redriver sits right next to its port connector, and the MEG-Array → retimer run is as short as possible. The order on the IOB is MEG-Array → (short) → retimer → connector.

| Path | Pick | Type / rates | Power | Package | Datasheet / availability |
|---|---|---|---|---|---|
| C1, C2 DP Alt + USB 10G | **Parade PS8838** (preferred) | Retimer **and** Type-C switch. USB 3.2 Gen2x1 + DP 2.1 up to **UHBR20**. LTTPR. Pin assignments C/D/E | "low power"; number not public (**gap**) | 4.7 × 8.0 mm QFN-62 | [P1]. Full datasheet looks NDA (**gap**). No LCSC listing found |
| C1, C2 alternative (public datasheet) | **Diodes PI2DPX2020A** | Linear redriver with 4:4 crossbar and AUX/SBU switch. USB 3.2 Gen2x1 + 2-lane DP, or 4-lane DP 2.1 UHBR20 | 160 mA at 1.8 V, about 0.29 W | WLGA-32, 2.85 × 4.5 mm | [D1]. LCSC C6147447, 0 in stock, about $9.28 at qty 1 [D2] |
| HDMI 2.1 FRL | **TI TDP2004** (it exists, verified) | 4-channel linear redriver. AC-coupled HDMI 2.1 source up to **12 Gb/s** (FRL). Also DP 2.1 to 20 Gb/s. Transparent to FRL link training | 160 mW per channel, about 0.64 W | WQFN-40, 4 × 6 mm | [T1]. TI is Active. A third-party Shenzhen listing shows TDP2004IRNQR in stock; LCSC stock isn't confirmed (**gap**) |
| DPD → ASM4242 DP-in 1 | **None planned** | HBR3 only (see 5a). The path is short and on-board | – | – | Add a TDP2004 footprint only if SI & Fab's loss check fails |
| C3, C4 USB4 | **Intel JHL8040R** (one per port) | Thunderbolt 4 / USB4 retimer, single port, DP 1.4 | 0.75 W TDP | 6 × 6 mm | [I1]. Intel lists "Expected Discontinuance Q3'26", which is now. The electrical datasheet is by application only [I2]. Mouser listed stock at $4.34 [I3] (**gap**) |

**USB4 retimer alternative:** Parade PS8830 (USB4 Gen3x2, DP to UHBR20, 6 × 6 mm BGA-105, single 3.3 V) [P2]. Its datasheet also looks NDA (**gap**). Because the JHL8040R is EOL, the PS8830 is the more future-proof choice, but compatibility with the ASM4242 isn't public for either part (**gap**).

**HDMI side:** HDMI FRL tops out at 12 Gb/s per lane, so UHBR20 doesn't apply. The GPU drives TMDS/FRL natively on DPC over DP++. The TDP2004 needs an external HPD level shifter and a DDC buffer or level shifter [T1].

### 5a. ASM4242 DP-in: HBR3 only
ASMedia's product page says the DP sink ports are "Compliance DP V1.4a … up to HBR3 … 8.1Gbps per lane" [A1]. **The ASM4242 doesn't accept UHBR.**
- Run DPD at **HBR3** (the GPU negotiates down through link training).
- The two USB4 ports share that one stream, up to 32.4 Gb/s.
- No retimer is needed on the short MEG-Array → ASM4242 path.

## 7. Power
### USB port budget
| Load | Calc | W |
|---|---|---|
| USB-C ×6 | 5 V / 3 A = 15 W each | 90 |
| USB-A ×4 | 4.5 W each | 18 |
| Chips: ASM4242, VL822, i226 ×2, retimers, muxes, PD, hub | estimate | 12–15 |
| **Total** | at about 90 % conversion | **≈135 W ≈ 11.3 A @ 12 V** |

- **Input:** 12 V **direct from the PSU on a Molex Micro-Fit 3.0**, budgeted at **15 A**.
- **Not through the MEG-Array:** at 0.45 A per contact it can't carry power.
- **Standby:** about 2 W, covering i226 wake-on-LAN, USB wake and PD dead-battery logic. **Gap:** the PSU's 12 V standby current needs confirming with Power Supply.
- **Gap:** the chip figures are estimates. VL822 and ASM4242 power aren't public.

## 8. Open decisions (for Aidan)
0. Feed ASM4242 DP-in 2 (currently unfed), e.g. with a DP switch, or accept that the two USB4 ports share DPD. J3 over budget: move derived sideband to the base board (review P4).
1. ASM4242 DP-in 2: leave it unfed or add a switch (DPD is fixed to DP-in 1).
2. C1/C2: PS8838 retimer (NDA) vs PI2DPX2020A redriver (public). USB4 retimer: JHL8040R (EOL) vs PS8830.
3. Sign-off on CPU & Base Board source map.
4. MEG-Array stack height (4 vs 6 mm) after mechanical check.

## Sources
[1] https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf
[2] https://www.amphenol-cs.com/media/wysiwyg/files/documentation/gs-20-033.pdf
[3] AMD AM5 quick reference: https://www.amd.com/content/dam/amd/en/documents/partner-hub/ryzen/amd-socket-am5-quick-reference-guide.pdf
[4] VL822: https://www.via-labs.com/product_show.php?id=99
[1b] Amphenol MEG-Array part table (10x30, 84500/84501): https://www.farnell.com/datasheets/3946610.pdf
[P1] https://www.paradetech.com/products/ps8838-20gbps-usb-c-retiming-switch-for-host-application-with-usb-3-2-gen-2x1-and-dp-2-1-uhbr20/
[P2] https://www.paradetech.com/products/ps8830/
[D1] https://www.diodes.com/part/view/PI2DPX2020A ; https://www.diodes.com/databrief/download/PI2DPX2020A-brief.pdf
[D2] https://www.lcsc.com/product-image/C6147447.html
[T1] https://www.ti.com/product/TDP2004 ; https://www.ti.com/lit/ds/symlink/tdp2004.pdf
[A1] https://www.asmedia.com.tw/product/e20zx49yU0SZBUH5/363Zx80yu6sY3XH2.html
[I1] https://www.intel.com/content/www/us/en/products/sku/186251/intel-jhl8040r-thunderbolt-4-retimer/specifications.html
[I2] https://community.intel.com/t5/Thunderbolt-Share/Datasheet-of-the-JHL8040R-for-a-non-professional/m-p/1702277
[I3] https://www.mouser.com/c/semiconductors/interface-ics/i-o-controller-interface-ic

## Decisions 2026-10-28 (Aidan, via Master Bot)
- C1/C2: keep Parade PS8838 retimer.
- C3/C4 USB4: ASM4242 host stays; PS8830 retimers held as fallback footprints pending simulation.
- MEG-Array grid unchanged.

## Base link position (2026-10-29, from Base Board & Connectors)
The I/O board uses a MEG-Array 300 (84500 plug / 84501 receptacle, 4 mm stack). The stock field centre is (-1.73, -48.74) mm with the axis at 0.65 degrees. The origin is the gold-hole midpoint, with +y toward the core. The base-end column is still pending.

## 12 V feed (2026-10-29)
Aidan's decision, passed on by Base Board & Connectors: the board stays at the 4 mm stack. The 12 V supply (15 A budget) comes up from the base board through current-rated standoffs, at least 2x 12 V and 2x GND. They sit to the right of J13, at about base KiCad x 178-192, y 135-142. The direct PSU Micro-Fit is dropped. To do: reserve the matching screw and pad positions on the I/O board, with 12 V and GND pours tied to them, and put the input eFuse and bulk capacitors right at the standoffs. Exact positions are pending from Base Board & Connectors.
Provisional standoffs, in base KiCad top-side coordinates (mirror them for the I/O board): P1 12V (182.0, 141.5), P2 GND (189.5, 139.5), P3 GND (182.0, 133.0), P4 12V (190.0, 131.0). They use M3 screws from the I/O top through plated holes, with a 7.5-8 mm round pad, no solder mask, and a via ring. The part is Wurth 746600330R plus a 1 mm shim, or the WA-SMSI 4 mm spacer. The eFuse sits on the base board; the I/O board keeps its bulk caps. The I/O outline still has no KiCad file, so whether it covers x 178-192, y 128-145 is unverified.

## Supersedes the 12 V standoff sections above (2026-10-29 11:30, Aidan, via Base Board & Connectors)
"PSU feeds the I/O board directly like stock." The I/O board is the upright rear panel, as in stock (iFixit: flex 923-0501). WITHDRAWN: the P1-P4 standoffs and the base-side eFuse. The PSU DC-out goes straight to the I/O board input, and the I/O board carries its own eFuse and bulk caps. The data path is J13 (base) -> a custom flex with a Meg-Array 300 at each end -> the I/O board. Open: whether the flex can carry UHBR20, USB4 and PCIe Gen4, and its stiffeners and length (SI & Fab and Mechanical & Thermal).

## Port layout (Aidan, 2026-10-29)
Follows stock Mac Pro 6,1 rear panel. The six Thunderbolt 2 positions become USB-C:
- Bottom pair: USB4 (ASM4242 + PS8830 retimers)
- Middle pair: DisplayPort Alt mode (PS8838)
- Top pair: USB 3.2
USB-A x4, 2x 2.5GbE, HDMI 2.1b in stock positions. All I/O on flex from J13. Outline waits on Aidan's full 3D scan of the backplate (being redesigned).
