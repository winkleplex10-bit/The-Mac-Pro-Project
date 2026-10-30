# SSD board A — 2× Gen5 x4 direct from CPU (draft, 2026-10-26)

- **Drives:** 2× M.2 2280 M-key, PCIe 5.0 x4 each, no switch.
- **Input:** Amphenol MEG-Array 300 (84500/84501, 10x30, 4 mm stack) from the base board, as J12 at the upper-left stock position (stock frame -35.13, 31.33 mm, axis +46.5 degrees; KiCad 114.87, 68.67; pinout in docs/pinmaps/base-ssd-megarray.csv) carrying two independent x4 links: CPU NVMe x4 root port → M.2 #1, CPU GPP x4 → M.2 #2 [AMD AM5 QRG]. 16 pairs + 2 REFCLK pairs + per-link PERST#, CLKREQ#, PEWAKE#, SMBus, PRSNT#. No bifurcation needed.
- **Gap:** AMD doesn't publicly document Gen5 on the GPP x4 for every 7000/9000 SKU; drive #2 may train at Gen4.
- **Retimer:** Gen5 retimer on the base board (CPU & Base Board plan); none on SSD board unless SI & Fab's loss model says so.
- **Power:** ~30 W (2× ~12–14 W Gen5 drives + margin), 3.3 V at ~9 A from 12 V buck. Thermal: Gen5 drives need heatsinks / airflow (Mechanical & Thermal).
- **Gen5 routing notes:** 85 Ω diff, TX AC caps 220 nF 0201 at TX side, intra-pair skew ≤ 5 mil, no stubs (backdrill or blind vias where needed), low-loss material per SI & Fab, REFCLK HCSL routed as 85 Ω pair, SRIS not needed (common clock).

## Update 2026-10-26 (Aidan)
- The boot NVMe on the chipset has been dropped, so **boot now comes from the SSD board**. It keeps 2× Gen5 x4 over the 300-pin MEG-Array. PROM21 downlink 2 is now spare.

## Status 2026-10-28
Proceeding: two native CPU x4 Gen5 ports, no switch. Link uses TI DS320PR810 redriver on the base board, with a PT5081L/PT5161L-class retimer fallback footprint (SI & Fab to confirm the budget).
- Correction (SI & Fab, 2026-10-28): the x8 link (2 x4) needs TWO DS320PR810s, up to 1.75 W each. Layout rule: Gen5 runs on the SSD board from the base connector to each M.2 slot stay at 60 mm or less, including the M.2 connector.

## Connector update 2026-10-29 (Aidan)
The base-board link is a 300-pin MEG-Array (84500/84501, 4 mm stack). MCIO is retired for this board. The pinout is drafted by Base Board & Connectors and the board-end column is filled in by I/O & Storage. It carries 16 Gen5 pairs, 2 REFCLKs, per-drive PERST#/CLKREQ#/PEWAKE#, shared SMBus, and about 2.5 A of 12 V with 2x pin margin, with the rest ground or spare.

## Power input (2026-10-29 11:48, Aidan, via Base Board & Connectors)
The SSD board has its own PSU 12 V input on the stock second-D700 GPU feed connector. 12 V no longer goes over J12; its 12 former 12 V pins become GND or spare, and Base Board & Connectors owns the pinmap change. The input eFuse (soft-start, about 4 A limit for board A) sits right at the PSU connector. Estimated board A draw is about 2.0 A typical and 2.9 A worst case at 12 V. Board B would be about 6-7 A, which the stock feed should handle; the rating needs confirming with Power Supply. The connector pinout and position on the face board need Mechanical & Thermal's check.
