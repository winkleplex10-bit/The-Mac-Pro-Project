# SI & Fab: one array connector + flex instead of MCIO-124 + MCIO-74 (research only, 2026-10-25 ET)
No project files edited. Nothing ordered or quoted. Estimates are marked [Est]; anything uncited is a gap.

## 0. Topology facts from project docs (these change the question)
- GPU host link: Navi 23 = **PCIe 4.0 x8** (docs/gpu-board-prior-art.md L41/L55). The BP is budgeted Gen4 with Gen5 redrivers removed and the firmware forces Gen4 (archive/kicad/macpro62-backplane/docs/loss_budget_A1.md). **Gen4 governs.** An AM5 Gen5 root trains down to the lowest common rate.
- Display: J_DISP carries **5 links, not 3**: DL0/DL1 DP 4-lane to USB-C (TUSB1046A on the IOB), DL2 DP++ to HDMI through **TDP158** on the IOB, and DL3/DL4 DP 2-lane alt-mode (gpu-board-prior-art.md L42).
- **The two joints go to different boards.** PCIe goes face J_PCIE to BP J9 (about 55 mm, cable-plan §1). Display goes face J_DISP to IOB J2. One connector on the face means a **Y-split flex** (one branch to the BP, one to the IOB), or the display has to go through the BP. Mechanical & Thermal needs to confirm this.

## 1. PCIe 4.0 x8 budget at 8 GHz (limit 28 dB; PCIe 4.0 CEM, as used in loss_budget_A1.md)
| Segment | dB @ 8 GHz | Source |
|---|---|---|
| Root pkg + CPU board + CPU-LINK edge + BP (as routed) | 6.1–10.5 | loss_budget_A1.md |
| MEG-Array × 2 (BP end and face end) | 0.5–1.5 [Est] | rated 28–32 Gb/s NRZ (Amphenol datasheet; FCI GS-20-033), so 8 GHz sits well inside the rated band. **No public S-params** |
| Flex, adhesiveless PI, 55–150 mm (2.2–5.9 in) at 0.2–0.4 dB/in | 0.4–2.4 [Est] | PI Df 0.003 @10 GHz (DuPont/Qnity Pyralux AP/TFH); IPC paper "Impedance and loss vs frequency for flex materials" (electronics.org E5&S30_01). Narrow 85 Ω flex traces push toward the upper end |
| Face board | 0.5–1.8 | face spec §4 via loss_budget_A1 |
| Endpoint pkg | 2–3 | loss_budget_A1 |
| **Total** | **≈ 9.5–19 dB** | **Passes with 9–18 dB margin. No retimer needed.** |
Gen5 for reference only (36 dB @ 16 GHz): the BP doc already estimates 18–35 dB without the array connector. Add 2 × MEG-Array at 16 GHz (the rating covers 32 Gb/s only at the 4 and 14 mm stacks; GS-20-033 says 28 Gb/s at 4/6 mm, which is **below Gen5's 32 GT/s**) plus about 0.8–4.7 dB of flex, and **Gen5 would need a retimer** on the BP (or the BP-G5 redrivers) plus vendor S-params. Navi 23 doesn't need this.
Return loss and crosstalk: four separable interfaces become four (two array joints instead of two MCIO joints), so the count is unchanged. The BGA pads at 1.27 mm need anti-pads and a ground ring to stay near 85 Ω. Keep TX and RX in separate row blocks (NEXT).

## 2. DP HBR3 (8.1 Gb/s, Nyquist 4.05 GHz)
[Est] budget per lane: GPU pkg + face trace about 1.5–3 dB, MEG-Array × 2 about 0.3–0.8 dB, flex 55–200 mm about 0.3–1.6 dB, IOB trace to TUSB1046A/TDP158 about 0.5–1.5 dB. **Total ≈ 2.6–6.9 dB** before the IOB redriver. TUSB1046A and TDP158 are both linear or retiming conditioners that already sit on the IOB, so the far end is already equalised.
- **Gap:** I found no public VESA DP 1.4 HBR3 source-to-connector channel loss limit (the VESA spec is member-only). Against typical vendor app-note figures (around 10 dB+ for a TX-to-redriver segment) this passes, but I couldn't cite that limit.
- DPC/HDMI: DL2 is DP++ into TDP158 (HDMI 2.0 TMDS, 6 Gb/s per lane max, level-shifting and AC-coupled input). The flex only carries the GPU-side DP-level signal, so the HDMI TMDS levels never cross the array connector. HDMI 2.1 FRL isn't relevant because Navi 23's TDP158 path is HDMI 2.0 class. The TDP158 output stage was not re-checked.
- **No new redriver needed** beyond the existing IOB TUSB1046A/TDP158, if the flex is 200 mm or shorter.

## 3. Pin/ground allocation
Signals (from the project topology):
- PCIe: 8 TX + 8 RX pairs = 32, REFCLK pair = 2, PERST#/CLKREQ#/WAKE#/SMBCLK/SMBDAT/PRSNT# = 6.
- Display: lanes 4+4+4+2+2 = 16 pairs = 32, AUX × 5 pairs = 10, HPD × 5 = 5, HDMI DDC/CEC/CFG ≈ 3.
- **HS pairs 33 (66 pins), low speed ≈ 24.** There's no power through the connector (MEG-Array is about 0.45 A/contact; faces have power lugs).

| Pattern (1.27 mm grid; per Amphenol's MEG-Array practice, pairs on adjacent row positions, grounds at pair boundaries) | HS + GND | + LS | + TX/RX/display isolation rows | Total | 200-pos (10×20) | 300-pos (10×30) |
|---|---|---|---|---|---|---|
| G-S-S-G with shared grounds (1 G per pair, 1.5 pins per signal) | 66 + 33 | 24 | 2 rows × 10 = 20 | **143** | fits (57 spare) | fits (157 spare) |
| G-S-S-G-G (2 G per pair, ~checkerboard ground density) | 66 + 66 | 24 | 20 | **176** | fits (24 spare, tight) | fits (124 spare) |
**Recommendation:** 300-pos with the 2-G pattern for SI margin, or 200-pos shared-G if the footprint is limited. The **Amphenol pin-assignment app note / S-param model is a gap**. It needs a request, since the vendor's recommended S:G ratio wasn't public.
**Height caveat (from the Amphenol number selector):** the **200-pos comes at 6 mm** (84516 plug + 55724 receptacle). The **300-pos has no 6 mm option**: it's 5.5 mm (84500 + 84502) or 8 mm (84500 + 84553). So 300-pos at 5.5 mm is the match for the "5.5 OK" target.
SEARAY 0.8 mm (backup): rated 28 Gb/s NRZ, PCIe 4.0 "capable" (samtec.com/products/seaf8). A 200/240-pos part at 7 mm fits the same counts. Samtec's channel models are free, which is the better SI documentation route.

## 4. JLC manufacturability
- **Assembly:** JLC Standard PCBA does BGA down to 0.3 mm pitch, so 1.27 mm is easy. **X-ray is applied automatically** to BGA/QFN/LGA and charged in the quote. A report is downloadable (jlcpcb.com/capabilities/pcb-assembly-capabilities; jlcpcb.com/help/article/x-ray-inspection-report-interpretation-guide).
- JLC says its system "cannot guarantee 100% identification", so a **connector** BGA (MEG-Array) and **SEARAY solder-charge** parts may not trigger X-ray. Request X-ray on them in the order remarks.
- Reflow 240 ± 5 °C (Standard). Check it against the LF MEG-Array profile in GS-20-033 [gap].
- **Sourcing:** I couldn't confirm MEG-Array or SEARAY in LCSC/JLC stock. The broker Sierra IC lists 84516-202LF about 1,997 and -102LF about 164 (broker data, unverified). Expect global-sourcing or consigned parts.
- **PCB:** a dog-bone fanout works at 1.27 mm with no via-in-pad needed. JLC's POFV is free on 6–20 layers if you want shorter stubs. Stencil: follow GS-20-033's paste and pad spec [gap: not extracted].
- **Flex:** BGA on polyimide needs an FR4/steel stiffener under each connector. JLC FPC impedance control, stiffeners, and BGA-on-FPC assembly were **not verified**. Neither was a Y-split rigid-flex.

## 5. Gaps
1. No MEG-Array S-params at 5.5/6/8 mm. The 32 Gb/s rating is only stated at 4 and 14 mm.
2. VESA HBR3 channel limit is not public.
3. Flex loss for our actual stackup and width: I need JLC's flex impedance and loss data or a coupon.
4. Real flex length and Y-split routing (Mechanical & Thermal), plus whether display can route through the BP instead.
5. Amphenol pin-assignment guidance and mating cycles.
6. LCSC stock and price. JLC BGA-on-FPC and X-ray on connector-type BGA/solder-charge parts (needs an order-remark confirmation).
7. MCIO-74 contact list re-read against the 5-link display set (DL3/DL4 included).

> **Stale note (2026-10-25):** DL3/DL4 above are stale. Aidan's locked display plan has 3 live links (DPA, DPB to DP-alt C1/C2; DPC to HDMI via TDP158; DPD unrouted spare), so 12 display lane pairs, not 16. Also superseded by Aidan's 2026-10-25 baseline (PCIe 5.0 x16 to GPU): the Gen4-only conclusion no longer covers the slot/backplane.
