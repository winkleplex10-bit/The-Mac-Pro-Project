# SI & Fab answers to Base Board & Connectors (map rev 2) — 2026-10-26
Research only. No MSI data. Nothing ordered. [Est] = my estimate, [Src] = cited.

## 1. MEG-Array 300-pos @ 4 mm S-parameters
- No public Touchstone files or IL/RL/NEXT tables found for MEG-Array at 4 mm. Datasheet gives only data-rate ratings (4 mm rated 32 Gb/s per prior research) [Src: https://www.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf]. GS-20-033 product spec is mechanical/qualification, no S-params in public copy.
- Figures at 4.05/6/8 GHz: **GAP**. Planning placeholder [Est]: IL ≤0.5 dB @ 8 GHz incl. footprint, NEXT better than −35 dB with GSSG. Must not be used for sign-off.
- How to get: request SI models (Touchstone .s4p/.s16p for chosen stack height & footprint) via Amphenol CS "Contact Us / Request SI models" on the product page or a distributor FAE (Mouser/Arrow); typically NDA.

## 2. MCIO 124 on J2 (and J9/J10)
- Public: rated 32 GT/s PCIe 5.0, 85 Ω [Src: https://www.amphenol-cs.com/product-series/mini-cool-edge-0-60mm.html ; https://www.amphenol-ast.com/v3/en/product_view.aspx?id=370]. No public Touchstone found; IL at 8/16 GHz for connector: **GAP** (request from Amphenol/Molex).
- SFF-TA-1016 cable-assembly IL limits per length: spec is at https://www.snia.org/sff (SFF-TA-1016); I did not extract per-length numbers → **GAP**. Planning [Est]: 30 AWG twinax ≈ 1.0–1.3 dB per 100 mm @ 16 GHz plus ~1–1.5 dB per mated pair; 0.5 m cable ≈ 7–9 dB @ 16 GHz.

## 3. Gen5 end-to-end budget (16 GHz, PCIe 5.0 CEM-style ~36 dB bump-to-bump) [Est]
| Segment | dB @16 GHz |
|---|---|
| AMD package (CPU) | ~3–5 (PCIe base spec reference package allowance; AMD value under NDA: GAP) |
| CPU board 1080A L8, 100–150 mm @ 0.10 dB/mm | 10–15 |
| Vias/breakout (2–3 transitions) | 1–2 |
| J1 224-pos card edge (mated) | 1–2 |
| Backplane (rev-2 estimate) | 18–35 incl. above? — standalone backplane traces 50–150 mm FR4 ≈ 5–15 |
| J9/J10 MCIO + 0.3–0.5 m cable | 5–9 |
| Receiver board trace + package (GPU / SSD) | 4–8 |
| **Total** | **~29–46 dB** vs 36 dB |
Verdict: **Retimers required** on J9 (x16) and J10 (2× x4) for margin; only the best case closes and FR4 at Df 0.02 is ~0.1 dB/mm. Placement: on the base board near J1 side/midpoint so each half is ≤~25 dB. Gen5 redrivers (TI DS320PR810/1610, linear) are not recommended — they don't reset jitter/budget. Retimer candidates: Astera Aries PT5161L (x16) / PT5081L (x8); Parade PS8935? (unverified Gen5 part — GAP); Montage M88RT51632 (x16); TI DS560? none. Lanes: J9 one x16 retimer; J10 one x8 retimer bifurcated 2× x4 (Aries supports bifurcation). Power ~5–10 W x16. Cite vendor pages before final selection (GAP).

## 4. Base-board Gen5 switch instead of SSD retimer
- Electrically yes: a switch terminates the link both sides, so it splits loss like a retimer [Src: PEX89024 https://www.broadcom.com/products/pcie-switches-retimers/expressfabric/gen5/pex89024 ; Switchtec PFX Gen5 https://ww1.microchip.com/downloads/en/DeviceDoc/00003776.pdf].
- Cost: switch $$ (hundreds USD, distribution-limited) vs retimer (~$30–80 [Est]); power ~14 W vs ~5 W; latency ~100–150 ns vs <10 ns; supports 2× x4 (or 4× x4) downstream natively. Availability: Broadcom/Microchip Gen5 switches are mostly via direct/NDA — GAP.
- Place it near the midpoint of the path (base board) to split loss. Verdict: only worth it if more than x8 of NVMe or lane-sharing is wanted; otherwise an x8 retimer is cheaper, cooler, lower-latency. Aidan's call.

## 5. JLC10161H-1080A loss
Formula: α_c ≈ 36·√f / (w_mil·Z) × K_rough (K=1.5) dB/in; α_d = 2.3·f·Df·√Dk dB/in. FR4 TG170 Dk 4.1 (stripline), 3.4 eff (microstrip), Df 0.02 [JLC Dk values https://jlcpcb.com/impedance ; Df ~0.02 typical FR4, JLC Df not published there — GAP]. Diff stripline uses odd-mode Z=42.5 Ω.
| Line | f GHz | cond | diel | total dB/in | dB/mm |
|---|---|---|---|---|---|
| L3/L8 85 Ω diff w0.1242 | 4.05 | 0.52 | 0.38 | 0.90 | 0.035 |
| | 6 | 0.64 | 0.56 | 1.20 | 0.047 |
| | 8 | 0.74 | 0.75 | 1.48 | 0.058 |
| | 16 | 1.04 | 1.49 | 2.53 | 0.100 |
| L1 50 Ω SE w0.1115 | 4.05 | 0.50 | 0.34 | 0.84 | 0.033 |
| | 6 | 0.60 | 0.51 | 1.11 | 0.044 |
| | 8 | 0.70 | 0.68 | 1.37 | 0.054 |
| | 16 | 0.98 | 1.36 | 2.34 | 0.092 |
Low-loss (Df 0.008, Dk 3.7) would give 85 Ω diff ≈ 1.61 dB/in @16 GHz (−36%). JLC standard multilayer offer is FR4; a low-loss/Rogers hybrid availability for 10-layer at JLC is not confirmed — GAP (check jlcpcb.com quote page "material").

## 6. MCIO variant pin counts (SFF-TA-1016)
- OCP M-XIO r1 v1.0 (SFF-TA-1016 pinouts): **38-pin = x4 (4i), 74-pin = x8 (8i), 148-pin = x16 (16i)**; it states 124-pin "is not recommended since it does not have enough pins to enable 2x8 mode with all required sideband signals" [Src: https://www.opencompute.org/documents/m-xio-r1-v1p0-rc4-pdf/].
- Commercial 124-pos parts are sold as **x16** (e.g. 124P host to 2× 74P x8 breakout, Gen5 32 GT/s) [Src: https://www.genuinemodules.com/image/catalog/pdf/1/CAB-MCIOi16-2xMCIOi8.pdf ; https://www.eproductsolutions.com/mcio-124p-to-two-mcio-74p-500mm].
- So both the "124 = x8" (M&T) and "74 = x4, 124 = 8i" assumptions are **incorrect**: 74 = x8, 124 = x16 with reduced sideband (one REFCLK/PERST set), 148 = x16 with full dual sideband.
- J9 (GPU Gen5 x16, single link): 124-pin is OK (single sideband set). Use 148 if per-x8 sideband is ever needed.
- J10 (SSD 2× x4): a 74-pin x8 part suffices if its two REFCLK/PERST sets are available (74-pin has sideband for ~one port + FLEXIO; check SFF-TA-1016 pin list) — otherwise 2× 38-pin x4 or 124/148. Current 124 on J10 (~82 pins used) works but is oversized.
- Molex NearStack/Amphenol datasheet direct links and the SFF-TA-1016 PDF itself not opened this pass — GAP.

## Gaps
MEG/MCIO Touchstone; SFF-TA-1016 cable IL table; AMD package loss; JLC Df & low-loss material; retimer/switch pricing & availability; Parade Gen5 part number.
