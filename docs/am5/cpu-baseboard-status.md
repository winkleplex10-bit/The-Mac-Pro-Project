# MacPro6,2 CPU board (CB) + base board/backplane (BP): status brief
Read-only review, 2026-10-21 (ET). Nothing in the source projects was changed: DRC/ERC were re-run with kicad-cli 9 on copies in /tmp/rv.

## 1. Board matrix

| Project | Role | Cu layers | Footprints | Copper routed? | Schematic | DRC (re-run) | ERC (re-run) |
|---|---|---|---|---|---|---|---|
| macpro62-am5-v3 | **Current CB** (AM5 Ryzen 7000/9000 + PROM21) | 10 (proposal stackup) | 57 | No (no tracks or zones) | Block level only (10 stub sheets, 0 BOM symbols) | 0 violations, **131 unconnected** (= the netted J1/J3 pads, nothing routed) | 0 |
| macpro62-am5 | CB v1, AM5 8000G/Phoenix draft | 10 | 57 | No | Block | 0 / 0 | 0 |
| macpro62-lga1700 (-v2, -v3) | LGA1700/Z790 CB, **parked** ("we are doing AMD"); v3 is an unedited copy | 10 | 53 | No (no nets) | None | 0 / 0 (all three) | n/a |
| macpro62-cpu-carrier | COM-HPC carrier, **archived fallback** since 10-01 | 8 | 34 | No | Block stubs | **11 violations** (all lib_footprint_issues: stock KiCad libs missing on this box, an environment issue, not a design one) | **192 label_dangling** (hierarchical stubs, as expected) |
| macpro62-backplane-v3 | **Current BP** | **6** (JLC06161H-2116) | 155 | **Yes, fully routed** + JLC outputs (18 Gerber/drill files, 44 BOM lines, 143 parts) | Full | 0 / 0 / 0 parity | 0 |
| macpro62-backplane-v2 | BP A2 | 4 | 152 | Routed (A1 base) | Full | 0 / 0 | 0 |
| macpro62-backplane | BP A1 | 4 (JLC04161H-7628) | 152 | Routed | Full | 0 / 0 | 0 |

Completion state:
- **CB AM5 v3:** floorplan and placement are done. J1 CPU-LINK (224 pads) and J3 MCIO-124 (real footprint) are netted. U1 is an LGA1718 socket placeholder with synthetic lands, U2 is a PROM21 placeholder, and U3 is the SVI3 controller. All three are NDA-blocked. The VRM, DIMMs (real footprint, pins not netted), M.2 J8, TPM, VL822 hub and others are still area or placeholder parts. There is no component-level schematic and no routing. **Not fabricable.**
- **BP v3:** schematic, placement, routing, DRC/ERC and fab outputs are done. Slot B was routed at x4 with 0.000 mm intra-pair skew. The board is waiting on Aidan's approvals before ordering (see §5).

## 2. Key connectors and interconnects between faces
- **I-1 CPU-LINK:** the CB J1 224-finger card edge mates directly with BP J1, an Amphenol Mini Cool Edge 224 (ME1022410103011, vertical SMT). The v3 pinout re-assigns 21 contacts. GND drops from 80 to 78 and RSVD from 13 to 4.
- **I-2 IOB-HS1:** CB J3 (MCIO 124 RA, back side, top edge) connects to IOB J1 through a crossed plug-to-plug MCIO-124 cable. It carries the USB3 lanes, i226 lanes and the iGPU DP links (DDI → C5/C6).
- **I-4 BP → faces:** BP J9 feeds Face P (x16) and BP J10 feeds Face S (x8 = slot A plus slot B). Both are MCIO-124 RA receptacles (Amphenol G97R24332HR, LCSC stock 0). The cables are straight-to-straight, narrow plug, zero jog (fp6/O-10), about 55 mm mating face to mating face. That is a **custom length (U-21 RFQ)** and below the 150 mm catalogue minimum.
- **I-3 DISPLAY-LINK:** Face P J_DISP (MCIO 74) connects to IOB J2.
- **I-5 Face AUX:** BP J3 and J4 are GH15 (BM15B-GHS-TBT) connectors to each module's J_AUX. The cable runs are about 56 and 64 mm.
- **Other cables:** I-6 IOB-LINK (BP J6 ↔ IOB J6, GH15) and the PSU harness (IOB J5 → BP J2, Micro-Fit 2×4). The CB takes 12 V through LUG1/LUG2.
- **Rigid-flex MCIO jumper:** documented only as backup B1. No flex boards exist for CB/BP.

## 3. PCIe lane allocation (CB AM5 v3 → faces, ICD v3 §20.3)
| CPU source | Width | Path | Sink |
|---|---|---|---|
| GFX | x16 Gen4/5 | CPU-LINK → BP J9 | Face P lanes 0-15 (all live) |
| GPP#1 | x4 | CPU-LINK → BP J10 set A | Face S slot A (FS 0-3), REFCLK0 |
| GPP#2 | x4 | CPU-LINK v3 re-pinned → BP J10 set B | Face S slot B (FS 4-7), REFCLK1 = CPU GPP_CLK; on BP v3 it trains at **x4** |
| Chipset link | x4 | on the CB | PROM21 |
| PROM21 free Gen4 x4 | x4 | on the CB | J8 M.2 boot |
| PROM21 USB 10G + VL822 hub, iGPU DP0/DP1 | – | J3 → IOB | IOB C1–C6, A1–A4 |

On the BP, Gen5 redrivers were removed at A1. The Gen4 loss estimate is 9.5–16.8 dB against a 28 dB budget. The BP lane lengths are 39–65 mm for Face P and 32–70 mm for slot B.

## 4. Inconsistencies found
1. **The requested "ICD rev4" is not newer.** `macpro62-interface-control-rev4.md` is a PARKED, unedited copy of rev 3 (the superseded v2 x8/x8 plan). The ICD of record is **`macpro62-interface-control-v3.md`**, §20.
2. **CPU target disagrees across the AM5 docs.**
   - The am5-v3 README header, the AM5 board plan §0 and arch spec v0.2 item 35 still say Ryzen 8600G/8700G (Phoenix) at cTDP 45 W, with "GFX x8 → Face P".
   - PROGRESS_V3 and ICD v3 say Ryzen 7000/9000 (Raphael/Granite Ridge), GFX x16 live, 65 W.
   - The same documents also say Dasharo/openSIL **boots only 8000G** on AM5. That leaves the v3 target without a known firmware path.
3. **Arch spec v0.2 is stale.** It is dated 10-01 and still calls LGA1700 "primary" (item 35). It has no entry for the AM5 v3 switch or the parked LGA1700. The SM-1 note ("Face S = PEG60 x4, ASM2824 switch") is also out of date.
4. **ICD v3 §12, the lane/clock map, is still the LGA1700/Z790 table** (PCH HSIO, SRC11/12, U-12/U-13 PCH CLKOUT/SATA). Only §20.3 has the AM5 map. §12 and U-12/U-13 have not been rewritten for PROM21. O-7 (PECI on Raptor Lake) is also obsolete under AMD.
5. **J8 M.2 boot source moved** from CPU GPP to the PROM21 free x4. The AM5 plan still shows "GPP x4 → M.2 boot".
6. **The CPU-LINK v3 pinout drops SMB_CLK/DAT/ALERT# and GPIO0-3** (ICD §20.1). Check that the IOB/BP firmware pin map (RP2350 `gpio_map.json`) and the ICD §11 I²C map are reconciled. On the CB side the CSV is documentation only, because the CB schematic has no nets.
7. **CB layer count:** 10L is a "proposal (placeholder dielectrics)". The BP v3 is a real JLC 6L stackup. The carrier is 8L. No CB stackup is fixed.
8. **The power total is over the ceiling.** System worst case with a 65 W 9600/7600 and a 150 W Face P is about 447 W against the 445 W ceiling. It relies on LPT/Eco capping.
9. **Carrier DRC 11:** these are missing stock libraries on the box. The README's "0 violations" was true when it was generated.

## 5. Open decisions for Aidan
1. **CPU SKU and firmware.** Option A is Ryzen 8000G (boots today on Dasharo, GFX x8 to Face P). Option B is 7000/9000 (x16 + slot B x4, but no open-firmware boot path yet).
2. **BP v3 order approvals:**
   - ICD 3.1 FS-lane reversal
   - INA226 replacing INA228
   - J7 M.2 DNP (where BIOS/OpenCore boots)
   - R27 → R33
   - RP2350B GPIO re-map
   - U1/Y1/U2 moves
   - Storage-face deviations D-2X-1, D-2X-2 and D-S1
3. **AM5 NDA path.** The LGA1718 land map, PROM21 ballout and SVI3 tools are required before any real CB schematic or layout. Who pursues AMD access, or is a different approach preferred?
4. **Formally retire LGA1700 (v1–v3) and the COM-HPC carrier,** or keep them as fallbacks.
5. **Custom ~55 mm MCIO-124 cable RFQ (U-21).** The receptacle G97R24332HR also shows LCSC stock 0.
6. **Power ceiling.** Accept the 447 W worst case with LPT/45 W Eco capping, or limit Face P to 130 W.
7. **Docs cleanup.** Approve updating arch spec v0.3 and the ICD §12/§16 to AM5, and marking the rev4 file as parked in its file name.
