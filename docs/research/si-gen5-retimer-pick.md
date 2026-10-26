# SI & Fab — Gen5 x16 GPU retimer pick (research only, 2026-10-26)

Nothing ordered or edited. Public sources only. **EST** = estimate, not published.

## Sources
- Astera PT5161L product brief: https://www.asteralabs.com/wp-content/uploads/2021/03/Astera_Labs_PT5161L_Product_Brief.pdf
- PT5161L public short datasheet (package/orderables only): https://resources.ampheo.com/static/datasheets/astera-labs/pt5161lrs.pdf
- LCSC listing PT5161LRS (C6365355): https://www.lcsc.com/product-detail/C6365355.html
- Montage M88RT51632 page: https://web.montage-tech.com/PCIe_Retimer/M88RT51632
- Montage product brief (PB0005, 2026-03): https://www.montage-tech.com/uploads/files/202605/PB0005_M88RT51632_ProductBrief_20260326.pdf
- Montage flyer: https://www.montage-tech.com/sites/default/files/2023-06/PCIe%205.0%20Retimer%20Flyer_English.pdf

## Comparison
| Item | Astera PT5161L | Montage M88RT51632 |
|---|---|---|
| Full datasheet | NDA (portal); public brief + package/orderable sheet | NDA; public brief + flyer |
| Lanes / bifurcation | 16; x16, 2x8, 4x4, 8x2 | 16; x16, 2x8, 4x4 (card vendor listing) |
| Reach | 36 dB @ 32 GT/s | 36 dB @ 32 GT/s |
| Power | Not public. EST ~6–9 W active x16 (gap) | Not public. Card w/ chip: 10.6–16.4 W board (not chip). EST similar 6–9 W |
| Package | 354-pin FC-CSP, 8.9 x 22.8 mm, 1.71 mm typ thick | 354-ball FCCSP, 8.9 x 22.8 mm |
| Ball pitch | Not public (gap) | Not public (gap) |
| Rails | Not in public docs (gap; EST 0.9 V + 1.8 V class) | 1.8 V and 0.9 V |
| Refclk | 100 MHz HCSL in; HCSL out; Common, SRNS, SRIS | 100 MHz; Common, SRNS, SRIS; 100 MHz out |
| Config | SMBus or EEPROM; C/Python SDK | SMBus or EEPROM (I2C) |
| AC caps | Integrated | M88RT51632TR integrated; base SKU external |
| Lane reversal / polarity | Lane reversal supported, auto polarity | Polarity inversion stated; lane reversal not stated (gap) |
| Pinout | Intel Retimer Supplemental Spec | Same footprint size/ball count; pin compatibility not confirmed (gap) |
| Availability | LCSC lists PT5161LRS; stock/price not shown publicly at check (gap) | No distributor found; sold via Montage/agents |

## Gen4 x8 Navi23 behind x16 retimer
- PCIe Base Spec 5.0 §4.3 (Retimers): a retimer must support all data rates below its max and participate in link training transparently; link width and rate are negotiated between the upstream and downstream ports, and the retimer follows (forwards TS1/TS2). Unused lanes that fail receiver detect are left out of the link, so x16→x8 is handled by normal LTSSM width negotiation. (Spec text paraphrased; spec itself is member-only.)
- Astera: "Compliant to all PCIe 5.0 rates and Retimer functional requirements"; supports lane reversal.
- Montage: "Compliant with PCIe 5.0 Base Specification, backward compliant with PCIe 4.0 and below."
- So both should train to x8 at 16 GT/s. Wire Navi23 to lanes 0–7 (or 15–8 with reversal on Astera). Gen4 EQ is done on each side of the retimer. Not tested by us; neither vendor publishes a narrower-endpoint interop note.

## Recommendation: Astera PT5161L (PT5161LRS)
- Distributor listing at LCSC/JLC ecosystem; Montage has no public distribution.
- Integrated AC caps, explicit lane reversal, documented SDK and diagnostics, largest field base (server/GPU risers).
- Montage M88RT51632 is a credible second source of the same package size; keep it as an alternate if pin compatibility checks out.

## Gaps
1. Power (typ/max) and rail currents for both: NDA datasheets.
2. Ball pitch and land pattern: NDA (needed for JLC BGA/fanout rules).
3. PT5161L rail voltages not public.
4. Real stock and price: not visible publicly.
5. Montage lane reversal and pin compatibility with Astera unconfirmed.
