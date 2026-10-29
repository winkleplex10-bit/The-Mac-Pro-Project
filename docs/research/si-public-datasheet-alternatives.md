# SI & Fab: Gen5 retimer/redriver and connector-model alternatives with public datasheets
Date: 2026-10-26. Research only. No vendor was contacted and nothing was ordered.
Status: estimates where noted. Stock levels were not checked live unless stated.

## Repeaters (PCIe 5.0, 32 GT/s)
| Part | Type | Lanes | EQ @16 GHz | Public full datasheet? | Power | Package | Availability |
|---|---|---|---|---|---|---|---|
| TI DS320PR810 | Linear redriver | 8 ch (one direction each; x4 = 1 chip) | CTLE up to 22 dB | YES: https://www.ti.com/lit/ds/symlink/ds320pr810.pdf (38 pp: pinout, 3.3 V single rail, 160 mW/ch, package/land pattern, SMBus/EEPROM/pin-strap) | ~1.3 W/chip | 64-WQFN 5.5x10 mm, 0.5 mm pitch | TI.com, DigiKey, Mouser (stock not checked) |
| TI DS320PR1601 | Linear redriver | x16 (32 ch) | CTLE 21 dB | YES: https://www.ti.com/lit/ds/symlink/ds320pr1601.pdf (TX AC caps integrated, Intel retimer common footprint) | 164 mW/ch, ~5.2 W | 354-nfBGA 22.89x8.9 mm | TI.com showed out of stock (sample limit) |
| TI DS320PR410 / 4-ch family | Linear redriver | 4 ch | ~20-22 dB | Yes, TI public (not opened this pass) | ~0.6 W | WQFN | TI/distributors |
| TI Gen5 *retimer* | none found | | | TI sells no PCIe 5.0 retimer | | | |
| Diodes PI3EQX32908E / PI3EQX32904 | Linear redriver | 8 / 4 ch | programmable linear EQ (dB not confirmed) | Product page plus brief public (https://www.diodes.com/part/view/PI3EQX32908E). Full datasheet download not verified. | n/a | W-QFN3590-62 | Diodes/DigiKey (not checked) |
| Microchip XpressConnect PM8658 (x8) / PM8659 (x16) | Retimer | x8 / x16, bifurcates to x1/x2/x4 | ~36 dB per side (spec-class) | NO: product brief only (features, ordering, 8.5x13.4 / 8.9x22.8 mm). Full datasheet, power and ballmap gated through myMicrochip/NDA. | not public | BGA, Intel standard footprint | Microchip direct, sales |
| Astera Aries PT5081L / PT5161L | Retimer | x8 / x16 | ~36 dB per side | NO: NDA | ~5-9 W (press) | BGA, Intel footprint | NDA/sales |
| Parade, Kandou (Matterhorn), Montage (M88RT51632), Broadcom (Vantage 5), Renesas, NXP | Retimers | x8/x16 | | None publish full Gen5 retimer datasheets. All are NDA or sales-only. NXP and Renesas have no catalog Gen5 PCIe retimer. | | | |
| Intel | (spec owner) | | | Public: "PCIe 5.0 Retimer Supplemental Features and Standard BGA Footprint" white paper, linked from https://www.intel.com/content/www/us/en/io/pci-express/pci-express-architecture-devnet-resources.html (the 4.0 version is at cdrdv2-public.intel.com/828369). It gives the standard x16/x8 ballmap and signal list. | | | |

Key point: every Gen5 retimer (Astera, Microchip, Montage, Broadcom, Parade, Kandou) is NDA-gated. However, all of them use Intel's PUBLIC standard BGA footprint, and TI's DS320PR1601 is footprint-compatible. So the base board can be laid out on the public Intel ballmap with the public TI redriver datasheet, then populated with either the TI redriver or a retimer later. The retimer's own power rails and strap details would still need the NDA datasheet.

## Can public linear redrivers close 29-46 dB?
- A linear redriver does not reset the budget. Its CTLE (~21-22 dB) cancels ISI loss, but it also amplifies crosstalk and noise, and the whole channel is link-trained end to end. It is transparent to training: AMD's TX presets and the RX DFE adapt through it.
- **One redriver near mid-path, about 29-38 dB end to end:** plausible. TI markets DS320PR parts for exactly this, extending server Gen5 channels well past 36 dB. Keep the pre-redriver segment around 20-25 dB or less so the CTLE isn't overdriven, and keep crosstalk low (ground every pair at the connectors).
- **About 40-46 dB end to end:** marginal. It would need IBIS-AMI simulation and real lane-margining on hardware. Gen4 fallback stays mandatory.
- **Two cascaded redrivers per path:** not recommended. Noise and crosstalk add, the gain stages compound, and TI guidance generally favours a single stage. It doesn't fix the problem at the top of the range.
- Verdict: public redrivers are a credible quality option for the SSD x8 and likely the GPU x16 if measured loss lands at or below ~38 dB. Above that, a retimer (NDA) is the honest answer. A low-loss laminate cuts both the loss and the risk.

## Connector S-parameter models
- Samtec SEARAY: public product pages and the "High-Speed Characterization" reports (plots). Touchstone and 3D SI models are by request via e3dmodels@samtec.com, free but not an anonymous download. BOR models are NDA. SEARAY's own protocol table lists PCIe 5.0 as "No" at its PAM4 rating basis. Check the AcceleRate HD/HP alternatives.
- Amphenol MEG-Array: datasheet rates 32 Gb/s at 4 and 14 mm. No public Touchstone found, so the request stays with Communications.
- MCIO (SFF-TA-1016): the SFF spec is public. Vendor (Amphenol/Molex) S-params are by request.
- No anonymous public 32G array-connector S-parameters were found. Requests via e3dmodels are a "contact vendor" action, so they go to Communications.

## Gaps
- Live LCSC/DigiKey/Mouser stock not verified. JLC/LCSC availability of BGA DS320PR1601 is unknown.
- Diodes full datasheet download and dB boost not confirmed.
- Whether TI IBIS-AMI models are freely downloadable has not been confirmed.
- Direct PDF of Intel's Gen5 footprint white paper not fetched.
