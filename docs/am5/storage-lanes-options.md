# MacPro6,2 storage lanes: chipset-storage v3 plan (option B)

Written 2026-10-08 19:50 ET. Research and planning only. **No board files were edited and nothing was pushed.** The BP and LGA1700 v2 copies are being edited by another task right now; this doc only proposes changes.

Scope (Aidan, 2026-10-08): the RAID-chip option (A) is **dropped**. This doc covers only option B: storage PCIe from the chipset, with the **GPU keeping x16**. That means the PCH on LGA1700, and PROM21 or the CPU storage lanes on AM5. It defines a **v3** alongside the originals and the x8/x8 v2.

Tags: [Sourced] = datasheet, project file or public page; [Inference] = derived; [Estimate] = rough number; [Unverified] = needs a check.

---

## 0. TL;DR

1. **There are plenty of free PCH lanes. The limit is the CPU-LINK pins.**
   - Z790 has four untouched Gen4 x4 root-port groups: RP13–16, RP21–24, RP25–28, and RP5–8 (reserved for the AQC107 but not routed).
   - With the GPU on FP lanes 0–15, the only high-speed CPU-LINK contacts left for storage are:
     - the 4 FS pairs (x4);
     - the 4 RSVD HS pairs (a further **x2**);
     - the RSVD REFCLK2 pair.
2. **Slot A x4** can move to PCH **RP25** (Flex lanes 34–37, CLKSRC 8) **with no CPU-LINK pin change**. The FS pins are simply re-sourced on the CB.
   **Slot B is limited to x2**, on PCH **RP21** (Flex lanes 30–31, CLKSRC 14). It uses **10 of the 13 RSVD pins**: 4 HS pairs and REFCLK2. That leaves 3 low-speed RSVD pins.
   **A second full x4 cannot reach Face S** without giving up GND shield fingers (there is room for only one more pair) or adding a second cable.
3. **Recommendation: v3 "hybrid".**
   - Keep **slot A on the CPU x4 (PEG60)**, as now.
   - Put only **slot B on the chipset at x2** (Intel PCH RP21; AM5 PROM21 Gen4 port).
   - Keep the M.2 boot drive J8 on PCH RP9.
   Why:
   - The CPU x4 can never go to the GPU, so moving slot A to the PCH only frees a port that has nowhere better to go.
   - The DMI load is the same either way (one PCH x4 drive plus one PCH x2 drive).
   - The hybrid needs the fewest CB changes.
   - It maps 1:1 onto the AM5 CB, so **one BP v3 serves both CPU boards**.
   - The literal "all face storage on the PCH" variant (v3-allPCH, §3.6) is fully specified below. It is only equivalent if J8 moves to the freed CPU x4 at the same time.
4. **Is the hardware cost delta ≈ $0?**
   - The S2X module is unchanged (slot B just trains at x2).
   - The BP adds one gate plus a couple of resistors and five routed pairs (about $0.1–2 per order). An optional clock buffer would add about $5–12 per order [Estimate].
   - The CB is not routed yet, so re-sourcing lanes costs layout time only.
5. **DMI caveat (Aidan's claim is correct for Z790):**
   - DMI 4.0 x8 = 16 GT/s × 8 = **15.75 GB/s per direction**. It is shared by every PCH device.
   - In the hybrid, PCH storage peaks at 7.88 (J8) + 3.94 (slot B) = 11.8 GB/s.
   - B760 would be DMI x4 (7.88 GB/s), and its RP21 lanes don't exist.

---

## 1. Facts this plan relies on

### 1.1 Intel 700-series PCH (datasheet 743835, `mp62-spec-refs/lga1700/pch700.txt`) [Sourced]

| Item | Z790 | H770 | B760 |
|---|---|---|---|
| DMI 4.0 width | x8 | x8 | **x4** |
| PCH PCIe Gen4 / Gen3 lanes | 20 / 8 | 16 / 8 | 10 / 4 |
| CPU PEG configs | 1x16 or 2x8 | 1x16 or 2x8 | 1x16 only |
| PCIe RAID 0/1/5 (RST) | yes | yes | no |

- **DMI** runs at 16, 8, 5 and 2.5 GT/s with a maximum width of x8. Lane reversal and polarity inversion are supported (§34). The CPU datasheet lists "8 lanes Gen 4 DMI, 16 GT/s".
- **Gen4 x4 throughput:** the datasheet's own example is 7.88 GB/s. That gives Gen4 x8 = 15.75 GB/s and x2 = 3.94 GB/s per direction.
- **Root-port group configs:** 1x4, 1x4 lane-reversed, 2x2, 2x2 lane-reversed, 4x1, or 1x2+2x1. Lane reversal is only available in 1x4 and 2x2. Polarity inversion is always available (it is mandatory in PCIe).
- **Clocks:** SRCCLKREQ#[17:0] means 18 CLKOUT_SRC/CLKREQ pairs (SRC0–17). Any SRC can be assigned to any root port in firmware (coreboot `clk_src` / `clk_req`).
- **Lane naming:** PCIe lane *n* = `PCIEn` = Flex HSIO lane *n+9*. For example, PCIE13 = Flex lane 22 = SATA0, and PCIE14–19 = SATA1–6.

**Z790 Flex HSIO map and current use** (ICD rev 3 §12 + board plan §1.2):

| Flex lanes | PCIe | Type | Root ports | Current MP62 use | Free for v3? |
|---|---|---|---|---|---|
| 0–9 | – | USB3 10G | – | 10 × USB 10G → IOB | no |
| 10–11 | PCIE1–2 | Gen3 | RP1, RP2 (x1) | spare | yes (Gen3 x1 only) |
| 12 | PCIE3 | Gen3 | RP3 | i226 #1 (SRC12) | no |
| 13 | PCIE4 | Gen3 | RP4 | ASM1182e (SRC11) | no |
| 14–17 | PCIE5–8 | **Gen4** | RP5–8 | "reserved AQC107" (not routed, would need a 2nd cable) | yes (if the AQC107 is dropped or kept off-board) |
| 18–21 | PCIE9–12 | **Gen4** | RP9–12 | CB J8 M.2 boot x4 | no |
| 22–25 | PCIE13–16 | Gen4 / SATA | RP13–16 | lane 22 = SATA0 → BP J7 | partly (lanes 23–25; or move SATA0, see note) |
| 26–29 | PCIE17–20 | Gen3 / SATA | RP17–20 | spare | yes (Gen3 or SATA4–7) |
| 30–33 | PCIE21–24 | **Gen4** | RP21–24 | spare | **yes, slot B (v3)** |
| 34–37 | PCIE25–28 | **Gen4** | RP25–28 | spare | **yes, slot A (v3-allPCH)** |
| 38–45 | – | DMI | – | DMI x8 | – |

Note on SATA0: it sits on PCIE13 (Flex 22), which blocks RP13's x4 group. If the RP13–16 Gen4 group is ever wanted, SATA0 can move to SATA4 = PCIE17 (Flex 26, the Gen3/SATA group). This is optional and not needed for v3.

On **B760**, Flex 18–23 and 30–33 are NA, so RP21 doesn't exist. Slot B would have to use RP5–8 (Flex 14–17) instead. The project's chipset is Z790, so v3 assumes Z790 (H770 also works).

### 1.2 Public reference: MSI MS-7D25 (Z690) coreboot devicetree [Sourced]
https://raw.githubusercontent.com/coreboot/coreboot/main/src/mainboard/msi/ms7d25/devicetree.cb

| MSI port | Use | clk_src / clk_req |
|---|---|---|
| CPU PEG x16 | PCIe x16 slot | 0 |
| CPU PEG60 x4 | M2_1 | 9 |
| PCH RP9 | M2_3 | 13 |
| **PCH RP21** | **M2_4 (x4)** | **14 / 14** |
| **PCH RP25** | **M2_2 (x4)** | **8 / 8** |
| PCH RP3 | built-in LAN, `PCIE_RP_CLK_REQ_UNUSED` | 12 |

v3 copies the RP21 and RP25 clock assignments, so the MSI port is a working reference for straps and firmware.

### 1.3 CPU-LINK (Mini Cool Edge 224): what is actually free [Sourced: `kicad/macpro62-lga1700/docs/cpulink_224_pinout_draft.csv`, same as the BP copy]

- **There are 13 RSVD pins, not 14.** A105 became PWR_ALERT#; ICD rev 3 §2 still says 14.

| RSVD pin | Contacts | Type | Shielding |
|---|---|---|---|
| RSVD_REFCLK2_P/N | A54/A55 | HS (A row = CB out) | GND-shielded |
| RSVD_HS_B1_P/N | B54/B55 | HS (B row = CB in / RX) | GND-shielded |
| RSVD_HS_A1_P/N | A76/A77 | HS (CB TX) | GND-shielded |
| RSVD_HS_A2_P/N | A79/A80 | HS (CB TX) | GND-shielded |
| RSVD_HS_B2_P/N | B82/B83 | HS (CB RX) | GND-shielded |
| RSVD_LS2 / LS3 / LS4 | B102 / B104 / B105 | low speed | – |

- Every other HS contact is already used: FP x16 at A/B 2–56 plus FP_REFCLK at A51/52, FS x4 at A/B 58–68 plus FS_REFCLK at A70/71, SATA0, and USB2.
- The only GND run of 4 or more is **A81–A84**. It could carry **one extra TX pair**, but the B row has no matching run for RX.
- **So with the GPU at x16 the ceiling is FS x4 + RSVD x2.** A second full x4 needs either a CPU-LINK revision or a second CB→Face S cable.

### 1.4 S2X storage face J1 mapping [Sourced: `kicad/macpro62-storage-face-2x/tools/model.py`, face pinout CSV, `docs/ICD_CHANGES.md`]

- J1 (MCIO 124) lanes 0–3 go to slot A M.2 lanes 0–3, and J1 lanes 4–7 go to **slot B M.2 lanes 0–3** (`lane % 4`).
  - The MCIO→M.2 order is mirrored and fixed by L1 routing, so there is no lane reversal.
  - Data pairs use polarity inversion (deviation D-2X-2).
- **For a x2 link on slot B, only J1 lanes 4 and 5 are needed:**

| Slot B M.2 lane | J1 lane | Host TX (PET) contacts | Module TX (PER) contacts |
|---|---|---|---|
| 0 | 4 | A20/A21 | B20/B21 |
| 1 | 5 | A23/A24 | B23/B24 |
| unused at x2 | 6, 7 | A32/A33, A35/A36 | B32/B33, B35/B36 |

  An x2 root port reaching M.2 lanes 0–1 trains x2 without lane reversal.

- **Slot B sideband (set B) on J1:**

| Signal | J1 contact | Module behaviour |
|---|---|---|
| REFCLK1± | B29/B30 | 85 Ω, no buffer on the module |
| PERST1# | A29 | 3.3 V, re-buffered by 2N7002s on the module |
| CLKREQ1# | B26 | – |
| WAKE1# | B27 | – |
| MCIO_PRSNT1# | A30 | tied to GND on the module |

- There are no PCIe AC caps on the module for host TX. Host TX caps sit on the CB, and SSD TX caps on the SSD.
- **Conclusion: the S2X module needs no change for v3.**

---

## 2. Bandwidth options with the GPU at x16

| Variant | GPU (Face P) | Face S slot A | Face S slot B | CB J8 | On DMI (peak storage) |
|---|---|---|---|---|---|
| Original (ICD rev 3) | x16 CPU PEG | x4 CPU PEG60 | – (set B not driven) | x4 PCH RP9 | 7.88 GB/s |
| v2 (x8/x8, in progress) | **x8** CPU PEG port 1 | x4 CPU PEG60 | x4 CPU PEG port 2 (FP lanes 8–11 re-routed on the BP) | x4 PCH RP9 | 7.88 GB/s |
| **v3 hybrid (recommended)** | **x16** | x4 CPU PEG60 | **x2 PCH RP21** | x4 PCH RP9 | 11.8 GB/s |
| v3-allPCH (literal ask) | x16 | x4 PCH RP25 | x2 PCH RP21 | x4 **CPU PEG60** (moved) | 11.8 GB/s |
| v3-allPCH, J8 not moved | x16 | x4 PCH RP25 | x2 PCH RP21 | x4 PCH RP9 | 19.7 GB/s (> DMI); PEG60 wasted |

- Navi 23 (the current GPU target) is natively **PCIe 4.0 x8**, so v2 costs it nothing. v3 only matters for an x16 GPU (e.g. RX 9060 XT class, which is x16; Navi 33 is x8 like Navi 23) or if Aidan wants to keep the x16 contract [Inference, see `docs/gpu-board-prior-art.md`].
- **The trade-off is simple:**
  - v2 gives slot B a full Gen4 x4 (7.88 GB/s) off the CPU and halves the GPU link.
  - v3 keeps x16 and gives slot B Gen4 x2 (3.94 GB/s, about a fast Gen3 x4 drive) through the DMI.

---

## 3. v3 plan (hybrid recommended; all-PCH alternative in §3.6)

### 3.1 Root ports and lanes (LGA1700 CB, Z790)

| Function | Source | PCH lanes (CB) | Port config | CLKSRC | Firmware (coreboot style) |
|---|---|---|---|---|---|
| Face P GPU x16 | CPU PEG 1x16 | – | 1x16 | SRC0 (as MSI) | unchanged |
| Face S slot A x4 | **CPU PEG60** (unchanged) | – | 1x4 | **SRC9** (as MSI M2_1) | unchanged |
| **Face S slot B x2** | **PCH RP21** | PCIE21 (Flex 30) → lane 0, PCIE22 (Flex 31) → lane 1 | 1x4 trained x2, or **2x2** (RP21 x2 + RP23 x2 spare) | **SRC14** | `pcie_rp21 on`, `.clk_src = 14`, `.flags = PCIE_RP_LTR \| PCIE_RP_AER \| PCIE_RP_CLK_REQ_UNUSED` (no CLKREQ wire, §3.4) |
| CB J8 M.2 boot | PCH RP9 (unchanged) | Flex 18–21 | 1x4 | SRC13 (as MSI) | unchanged |
| IOB i226 / ASM1182e | RP3 / RP4 | Flex 12 / 13 | x1 | SRC12 / SRC11 | unchanged |

- **Choosing 2x2 over 1x4:** 2x2 leaves RP23 (PCIE23–24) as a spare Gen4 x2 on the CB. It also avoids relying on the x4 root port down-training. Both work; prefer 2x2 [Inference].
- **Not needed for v3:** RP5–8 (AQC107 reserve), RP13–16, RP17–20, RP25–28, RP1–2.
- **U-12 closes on LGA1700** (the PCH SRC assignment): FP = SRC0, FS = SRC9, slot B = SRC14, J8 = SRC13, IOB = SRC11/12. That is 6 of 18 SRCs.

### 3.2 CPU-LINK pins and re-pin

**Slot A: no change** (hybrid).

**Slot B: rename 5 RSVD pairs (10 contacts):**

| Contact | Old name | v3 name | CB source | BP destination (J10, Face S) |
|---|---|---|---|---|
| A76/A77 | RSVD_HS_A1_P/N | **FS_PET4_P/N** | PCH PCIE21_TX via 220 nF AC caps on the CB | J10 lane 4 PET (A20/A21) |
| B82/B83 | RSVD_HS_B2_P/N | **FS_PER4_P/N** | PCH PCIE21_RX | J10 lane 4 PER (B20/B21) |
| A79/A80 | RSVD_HS_A2_P/N | **FS_PET5_P/N** | PCH PCIE22_TX via 220 nF AC caps on the CB | J10 lane 5 PET (A23/A24) |
| B54/B55 | RSVD_HS_B1_P/N | **FS_PER5_P/N** | PCH PCIE22_RX | J10 lane 5 PER (B23/B24) |
| A54/A55 | RSVD_REFCLK2_P/N | **FS_REFCLK1_P/N** | PCH CLKOUT_SRC14 | J10 REFCLK1 (B29/B30) |

- **Pair assignment:**
  - Lane 4 = A1 + B2: both are in the bay-3 group next to FS, so they make the shortest pair.
  - Lane 5 = A2 + B1: B1 is in bay 2 at the FP end, so it is a longer BP route.
  - Lanes are deskewed by the PHY, so lane-to-lane length matching is loose. Intra-pair skew should stay ≤ 0.127 mm as for the other lanes.
  - Swapping lane 4/5 TX/RX groupings is fine as long as each lane's TX and RX go to the same J10 lane. P/N swaps are allowed (polarity inversion).
- **Left after v3:** RSVD_LS2/LS3/LS4 (B102/B104/B105). Suggestion: keep LS2 as an optional CB-driven **SLOTB_PERST#** (a PCH GPIO), so firmware can reset slot B alone. That would be 11 of 13 used. It is not required.
- **No new sideband pins are needed:** PERST1#, CLKREQ1# and WAKE1# are generated or terminated on the BP, per the S2X ICD.
- **Fallback if REFCLK2 must stay free:** a BP 1:2 HCSL buffer (9DBL0242 / 9DBV0241) fanned out from FS_REFCLK. That uses **8 contacts**. All PCH SRC outputs and the CPU PEG reference come from the same PCH clock generator, so a buffered copy stays common-clock [Inference].
- **The AM5 CB drives the same 5 pairs** (§5), so the BP stays CB-agnostic.

### 3.3 Backplane routing changes (proposal only; BP rev A1 is routed 4L, JLC04161H-7628)

1. **Route 4 new 85 Ω pairs** J1 → J10:
   - TX on L3 stripline, like the other host-TX pairs; RX on L1 microstrip, like the other host-RX pairs.
   - Map: A76/77 → J10 A20/21, B82/83 → J10 B20/21, A79/80 → J10 A23/24, B54/55 → J10 B23/24.
   - Same rules as the existing 40 pairs: 2 vias per net, intra-pair skew 0.000–0.127 mm, GND pour ≥ 0.5 mm.
2. **Route REFCLK1:** J1 A54/A55 → J10 B29/B30, 85 Ω pair. The CB does the HCSL termination at the source, as for FS_REFCLK.
3. **PERST1#:** add a 74LVC1G08 (or reuse the PERST0# AND structure) to form `PLTRST# ∧ FACE_S_RDY` → J10 A29, with the same 3.3 V pull and series R as PERST0#.
4. **CLKREQ1#** (J10 B26): terminate on the BP (10 k pull-up to 3V3, not routed to the CB). The CB then runs SRC14 free-running (`PCIE_RP_CLK_REQ_UNUSED`).
5. **WAKE1#** (J10 B27): wire-OR into WAKE0# (both open-drain), for $0.
6. **MCIO_PRSNT1#** (J10 A30, GND on the module): optionally take it to a spare MCU GPIO with a 10 k pull-up for slot B detection and logging.
7. **Leave J10 lanes 6–7 NC.** FP lanes 0–15 → J9 stay unchanged; v3 does **not** use the v2 FP 8–11 → J10 re-route.
8. **Loss budget:**
   - Slot B's BP segment is ~40–80 mm [Estimate; B1 from bay 2 is the long one], which is ≤ 0.6–2 dB.
   - The PCH-to-tab CB trace is longer than the CPU PEG60 trace: about 100–150 mm, roughly +1–3 dB [Estimate].
   - The total stays within the 28 dB Gen4 budget, with about 8–15 dB margin. No redriver is needed.
   - Simulate once vendor S-parameters exist.
9. **Practical note:** the v2 BP copy (in progress) already adds REFCLK1, PERST1#, CLKREQ1# and WAKE1# handling. v3 can be made from v2 by reverting the FP 8–11 re-route and adding the 5 RSVD pairs. Items 3–6 carry over unchanged.

### 3.4 Clocks and sideband for both slots

| | Slot A | Slot B |
|---|---|---|
| Lanes | Gen4 x4, FS_PET/PER0–3 → J1 lanes 0–3 | Gen4 x2, FS_PET/PER4–5 (ex-RSVD) → J1 lanes 4–5 |
| Root port | CPU PEG60 (hybrid) / PCH RP25 (allPCH) | PCH RP21 |
| REFCLK | FS_REFCLK (A70/71) = PCH SRC9 (hybrid) / SRC8 (allPCH) → J1 REFCLK0 | FS_REFCLK1 (A54/55, ex-RSVD_REFCLK2) = PCH SRC14 → J1 REFCLK1 (B29/B30); or BP buffer off FS_REFCLK |
| CLKREQ# | BP-terminated (as now); CB SRC free-running | BP-terminated (J1 B26); CB `PCIE_RP_CLK_REQ_UNUSED` |
| PERST# | BP: PLTRST# ∧ FACE_S_RDY → J1 A11 (as now) | BP: PLTRST# ∧ FACE_S_RDY → J1 A29 (optional: CB GPIO via RSVD_LS2) |
| WAKE# | WAKE0# (CPU-LINK A99) | WAKE1# wire-ORed into WAKE0# on the BP |
| PRSNT# | MCIO_PRSNT0# (A12) | MCIO_PRSNT1# (A30) → BP MCU GPIO (optional) |
| Module | unchanged | unchanged (trains x2) |

### 3.5 CB changes (LGA1700; the CB is a placed floorplan, not routed, so these are net assignments only)

- Add PCH PCIE21/22 TX (with 4 × 220 nF 0201 AC caps) and RX to the ex-RSVD contacts.
- Add CLKOUT_SRC14 to A54/A55.
- Leave SRCCLKREQ14# unconnected, or set it as a GPIO.
- Optionally drive RSVD_LS2 from a PCH GPIO as SLOTB_PERST#.
- **Softstraps:** set the RP21–24 group to 2x2 (or 1x4) and set the RP21 clock in the CSME/FIT image. Copy the MSI MS-7D25 settings.
- **Firmware:** the devicetree entry in §3.1, plus an SMBIOS slot description "Face S slot B (x2)".

### 3.6 v3-allPCH (literal "all storage from the chipset")

Same as above, plus the following:

- **Slot A:** re-source FS_PET/PER0–3 on the CB from CPU PEG60 to **PCH RP25** (PCIE25–28 = Flex 34–37, 1x4; use 1x4 lane-reversed if CB routing prefers).
  - FS_REFCLK becomes **SRC8** (as MSI M2_2). Firmware: `pcie_rp25 on`, `.clk_src = 8`.
  - **No CPU-LINK pin or BP change** for slot A, because the names are unchanged.
- **Move CB J8 to CPU PEG60** (SRC9, like MSI M2_1); RP9 becomes spare. Without this move, PEG60 sits idle and the PCH storage (x4 + x4 + x2 = 19.7 GB/s) exceeds the DMI.
- RP25 also exists on B760, which is a small plus if a B760 fallback were ever used.
- **Compared with the hybrid:** the bandwidth is the same, but there are two more CB re-sources and an extra ICD row change. It also no longer matches AM5, where slot A is CPU GPP anyway (the BP is the same either way).
- **Verdict:** only worth it if Aidan specifically wants the boot drive on CPU lanes.

### 3.7 ICD / document updates (to do in the owning task, not here)

- **ICD §2:**
  - 13 → 3 RSVD remain.
  - Rename the five pairs as in §3.2.
  - Close U-12 with the SRC list.
  - Fix the stale "RSVD ×14" (it is 13).
- **ICD §12:** add RP21 (Flex 30–31) → Face S slot B x2, SRC14. Optionally move SATA0 to SATA4/PCIE17.
- **S2X `docs/ICD_CHANGES.md`:** add a "v3 lane source" paragraph: PCH RP21 x2 via ex-RSVD pins; REFCLK1 = CB-sourced on A54/A55.
- **BP README:** add a v3 variant note.

---

## 4. DMI bandwidth caveat (LGA1700)

- **Link:** DMI 4.0 x8 = 16 GT/s × 8 lanes × 128/130 ÷ 8 = **15.75 GB/s per direction**, full duplex [Sourced: datasheet formula]. Real payload throughput is lower after TLP/DLLP overhead, roughly 85–90% [Estimate].
- **Everything behind the PCH shares it:**

| Device | Peak bandwidth |
|---|---|
| 10 × USB 10G | ≈ 1.2 GB/s each |
| 2 × i226 | 0.3 GB/s each |
| AirPort | ~0.2 GB/s |
| SATA0 | 0.6 GB/s |
| CB J8 | Gen4 x4, 7.88 GB/s |
| Slot B (v3) | Gen4 x2, 3.94 GB/s |

- **Hybrid v3 worst case:** J8 + slot B flat out = 11.8 GB/s, which leaves about 2–4 GB/s for USB and network. In practice that is fine.
- **Two Gen4 drives flat out:** a top Gen4 x4 drive does about 7 GB/s, so two of them ≈ 14 GB/s ≈ 90% of DMI.
- **Copy direction matters:** reads flow PCH → CPU and writes flow CPU → PCH. A drive-to-drive copy therefore loads opposite directions and contends less than "2 × 7 GB/s" suggests.
- **Slot A stays off the DMI in the hybrid**, so heavy Face-S-to-J8 copies only put slot B on the DMI.
- **B760:** DMI x4 = 7.88 GB/s. Even one Gen4 x4 drive could saturate it, so stay on Z790/H770.
- **AM5:** PROM21's uplink is only **PCIe 4.0 x4 = 7.88 GB/s**, half of Z790's DMI (§5).

---

## 5. AM5 check (PROM21 / CPU storage lanes)

Sources:
- `macpro62-am5-board-plan.md` §1/§3/§6, `kicad/macpro62-am5/README.md`, `docs/pinout_delta_summary.txt`, `macpro62-cost-estimate.md` §10.
- PROM21 specs: https://www.wepc.com/news/am5-prom21-chipset-technical-information-revealednbspnbsp/ and https://www.techpowerup.com/295394/amd-zen-4-socket-am5-explained-pcie-lanes-chipsets-connectivity?cp=4

- **PROM21 (single, B650/B850 class)** [Sourced]:
  - PCIe 4.0 x4 **uplink**.
  - **Two Gen4 x4 downstream controllers** (8 lanes).
  - 4 × Gen3 x1/SATA flex ports.
  - 6 × USB 10G.
  - Up to 6 USB2.
- **Current AM5 allocation** [Sourced: plan §3/§6]:
  - **CPU:** GFX → Face P; GPP x4 → Face S slot A; GPP x4 → J8 M.2 boot; x4 → PROM21.
  - **PROM21:** one Gen4 x4 is "reserved AQC107" (not routed). x1 → i226 #1, x1 → ASM1182e (the plan doesn't say which lanes; the Gen3 flex ports are the natural fit [Inference]). SATA0 is on a flex lane.
  - **So one PROM21 Gen4 x4 controller is free.**
- **GPU x16 is impossible on the target CPU:**
  - **Ryzen 8600G/8700G (Phoenix)** has 20 lanes (16 usable), with **GFX x8 max** [Sourced: AMD 8600G page, plan §1]. "GPU keeps x16" therefore cannot be met on the 8000G, whatever the storage plan.
  - Ryzen 7000/9000 (28 lanes, 24 usable) do give x16. Dasharo doesn't boot them yet.
  - On the 8000G, **v2's slot B (FP lanes 8–11) would be dead**, because those lanes aren't driven by the 8000G [Inference from plan §6: "lanes 8–15 not driven by 8000G"]. **v3 works on both.**
- **AM5 v3 (same BP, same CPU-LINK pins as Intel v3):**
  - **Slot A:** CPU GPP x4. No change; this is the AM5 baseline.
  - **Slot B:** **PROM21 free Gen4 x4 controller**, lanes 0–1 → ex-RSVD pairs (FS_PET/PER4–5), trained x2 (3.94 GB/s).
  - **REFCLK1** on A54/A55 has three options:
    - PROM21's downstream clock output, if it has one [Unverified, NDA ballout];
    - a spare CPU/FCH GPP_CLK;
    - a CB-side buffer.
    The fallback BP buffer works too, as long as it is in the same clock domain [Inference].
  - **PERST1# / CLKREQ1# / WAKE1#:** the BP handles them, identical to Intel.
- **Bandwidth:**
  - The PROM21 uplink is Gen4 x4, **7.88 GB/s**. Slot B at x2 (3.94) uses half of it, alongside 6 × USB 10G + VL822 hub, 2 × i226 and SATA.
  - Putting slot A on PROM21 as well would oversubscribe the uplink (7.88 + 3.94 > 7.88). **Do not do all-chipset on AM5.**
  - The hybrid (slot A on the CPU) is the only sensible AM5 mapping. That is why hybrid is the recommended v3 for both platforms.
- **Firmware:** the AM5 CB needs a new coreboot mainboard anyway. Add the PROM21 downstream port and the PCIe lane descriptor. [Unverified: whether openSIL `phoenix_poc` exposes PROM21 downstream-port configuration, or whether PROM21's own SPI image fixes it.]

---

## 6. macOS / OpenCore: booting and using PCH-attached NVMe

- macOS has had native NVMe support since High Sierra. It doesn't care whether the drive hangs off the CPU or a PCH/PROM21 root port; it enumerates standard PCIe bridges. Retail Z690/Z790 boards put most M.2 slots on the PCH, and those boot macOS normally [Inference, common hackintosh practice].
- **Drive choice matters more than topology.** Dortania lists unsupported or problem drives: PM981/PM991, Micron 2200S, SK hynix PC711. It recommends NVMeFix.kext.
  https://dortania.github.io/Anti-Hackintosh-Buyers-Guide/Storage.html
- **Firmware settings:**
  - SATA mode **AHCI**.
  - **No Intel RST/VMD RAID.** Don't enable VMD in the coreboot devicetree.
  - macOS can't use RST RAID, so for striping use AppleRAID (Disk Utility) or software RAID.
  - Dortania's Intel BIOS settings list "SATA Mode: AHCI": https://dortania.github.io/OpenCore-Install-Guide/config.plist/comet-lake.html
- **x2 link width:** NVMe SSDs negotiate down to x2 in practice (as in x2 M.2 slots), and macOS just reports the link width [Inference; PCIe only requires x1 support, so confirm on the chosen SSD].
- **OpenCore** can live on SATA0 (J7) or any NVMe; the macOS volume can live on any of the drives.

---

## 7. Cost delta (vs the original and v2) [Estimate; prices from `macpro62-cost-estimate.md` lines and the JLC fee table]

| Item | v3 hybrid delta | Note |
|---|---|---|
| S2X storage face | **$0** | unchanged (4L JLC Economic, single-sided); slot B trains x2 |
| BP fab | **$0** | same 4L JLC04161H-7628 board, 5 more routed pairs |
| BP parts | **+$0.1–0.5/board** | 74LVC1G08 for PERST1#, 2–3 resistors; WAKE wire-OR free; REFCLK pass-through |
| BP PCBA fee | **+$0–1.5/order** | +1 extended line at $1.53 if the gate isn't a basic part; ~10 extra joints at $0.0017 |
| BP optional HCSL buffer | +$2–5/board + $1.53/order | only if REFCLK2 isn't used (9DBL0242 class; price/stock [Unverified]) |
| CB (LGA1700) | **≈ $0 BOM** | +4 × 0201 AC caps; floorplan is unrouted, so only net assignment and layout time |
| CB (AM5) | ≈ $0 BOM | same; possible clock buffer if PROM21 has no downstream REFCLK [Unverified] |
| Firmware / softstraps | engineering only | coreboot devicetree + FIT softstrap |
| **Total per order (q1, 2 boards)** | **≈ +$0.5–3** (direct REFCLK) / **≈ +$6–13** (with buffer) | |

- **v3 vs v2:** hardware cost is about the same; both add the set-B sideband on the BP.
  - v3 costs a CPU-LINK re-pin (an ICD revision, with CB and BP both touched) and halves slot B's width.
  - v2 costs half the GPU link.
- **Original → v3 hybrid:** adds a working slot B for about $1–3 per order.

---

## 8. Recommendation

1. **Build v3 as the hybrid:**
   - **slot A = CPU x4** (LGA1700 PEG60 / AM5 GPP), unchanged;
   - **slot B = chipset Gen4 x2** (Z790 RP21 on PCIE21–22 with SRC14; AM5 PROM21 spare Gen4 controller);
   - routed over the five GND-shielded RSVD pairs (10 of 13 RSVD pins);
   - BP-generated PERST1#, BP-terminated CLKREQ1#, WAKE1# wire-ORed;
   - S2X unchanged.

   One BP v3 then serves both CBs, and the GPU keeps x16.
2. **Use v3-allPCH (slot A on RP25/SRC8, J8 moved to CPU PEG60) only if** Aidan wants the boot drive on CPU lanes. It has the same bandwidth and more CB churn.
3. **Keep v2 as the better choice if slot B must be a full x4 and the GPU is Navi 23 (x8).** In that case v2 loses nothing.
4. **Don't plan a full second PCH x4 to Face S.** CPU-LINK has no room (only one extra TX pair is possible from GND fingers). That would need a CPU-LINK rev or a second cable.
5. **Next checks (read-only now; edits in the owning tasks):**
   - confirm the J10 host-end contact names in the BP schematic;
   - check the B1 (bay 2) route length on the routed A1 BP;
   - confirm that PROM21 provides downstream REFCLK, from a retail AM5 board schematic or boardview;
   - check the chosen SSD trains at x2.

## 9. Corrections to the earlier summary given to Aidan

- **"The chipset route is likely best":** only partly right.
  - The chipset can feed slot B, but **only at x2** while the GPU keeps x16. The **CPU-LINK pin count**, not the number of PCH lanes, is the binding limit.
  - Moving slot A to the chipset gains nothing, because the CPU x4 can't go to the GPU.
  - Best = hybrid.
- **"DMI x8 ≈ Gen4 x8, shared":** correct for Z790/H770 (15.75 GB/s per direction). It is per direction, and B760 would be x4. AM5's PROM21 uplink is only Gen4 x4.
- **"NVMe RAID chips are NDA-only or expensive":** moot now that option A is dropped (not re-researched).
- **"14 reserved pins":** it is **13** (A105 became PWR_ALERT#). v3 uses 10 and leaves 3 low-speed pins.
