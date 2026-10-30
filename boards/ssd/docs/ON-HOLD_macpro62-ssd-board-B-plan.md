# SSD board B — 4× NVMe behind a Gen5 switch (draft, 2026-10-26)

## Input constraint
The CPU's 8 spare lanes are **two separate x4 root ports**, not one x8 (AMD AM5 QRG; CPU & Base Board). A switch cannot take them as one x8 upstream.

## Switch candidates (public data)
| Part | Lanes / ports | Power typ. | Package | Upstream options | Price / availability |
|---|---|---|---|---|---|
| Broadcom PEX89024 | 24 / 24 | 14 W | 29×29 mm | any port host or downstream; x1–x16; multi-host via NT/shared I/O [1][2] | Broadcom page: "Distributor Inventory: No"; price not public (gap) |
| Broadcom PEX89032 | 32 / 32 | 17.2 W | 29×29 mm | same [2] | not public (gap) |
| Microchip Switchtec PFX PM50028 | 28 lanes / 16 ports / 8 partitions | not public in sources read (gap) | gap | any port upstream or downstream, x1–x16, 8 virtual switch partitions [3][4] | not public (gap) |
| Microchip PM50036 | 36 / 10 partitions | gap | gap | same [4] | gap |
Lane budget: 4 drives × x4 = 16 downstream + 4 or 8 upstream = 20–24 lanes → PEX89024 or PM50028 are the smallest fits. Both are BGA server parts; datasheets and SDK appear NDA (gap).

## Option 1 — one x4 upstream (CPU NVMe x4)
Switch x4 Gen5 up → 4× x4 down. Shared bandwidth ~15.8 GB/s total. Second root port (GPP x4) either unused or feeds a 5th device. Simplest firmware: one host, transparent switch.

## Option 2 — two upstream ports / multi-host partition
Both CPU x4 ports into the switch as two partitions (PM50028 virtual switch partitions; PEX89024 multi-host), e.g. 2 drives per partition. Full ~31.5 GB/s. More complex config (partition setup in switch flash), still two separate PCIe hierarchies to the OS — not one x8.

**Aidan to choose 1 vs 2.**

## Power
~65 W: 4 drives ≈ 48–56 W + switch 14–17 W (Broadcom typ.) — estimate.

## Sources
[1] https://www.broadcom.com/products/pcie-switches-retimers/expressfabric/gen5/pex89024
[2] https://docs.broadcom.com/doc/BC00-0445EN
[3] https://www.microchip.com/en-us/product/pm50028
[4] https://ww1.microchip.com/downloads/en/DeviceDoc/00003776.pdf

## Update 2026-10-26 (Aidan)
- The boot NVMe on the chipset has been dropped, so **boot now comes from the SSD board**. It keeps 2× Gen5 x4 over the 300-pin MEG-Array. PROM21 downlink 2 is now spare.
- **Version B:** the 4-drive switch sits **on the SSD face against the thermal core**, not on the base board. Its power (~14–17 W) and cooling therefore belong to the SSD face (Mechanical & Thermal).

## Status 2026-10-28
ON HOLD per Aidan. Board A proceeds.

## Connector update 2026-10-29 (Aidan)
The base-board link is a 300-pin MEG-Array (84500/84501, 4 mm stack). MCIO is retired for this board. The pinout is drafted by Base Board & Connectors and the board-end column is filled in by I/O & Storage. It carries 16 Gen5 pairs, 2 REFCLKs, per-drive PERST#/CLKREQ#/PEWAKE#, shared SMBus, and about 2.5 A of 12 V with 2x pin margin, with the rest ground or spare.
Position: J12 at the upper-left stock position (stock frame -35.13, 31.33 mm, axis +46.5 degrees). The pinout is in docs/pinmaps/base-ssd-megarray.csv.

## Power input (2026-10-29 11:48, Aidan, via Base Board & Connectors)
The SSD board has its own PSU 12 V input on the stock second-D700 GPU feed connector. 12 V no longer goes over J12; its 12 former 12 V pins become GND or spare, and Base Board & Connectors owns the pinmap change. The input eFuse (soft-start, about 4 A limit for board A) sits right at the PSU connector. Estimated board A draw is about 2.0 A typical and 2.9 A worst case at 12 V. Board B would be about 6-7 A, which the stock feed should handle; the rating needs confirming with Power Supply. The connector pinout and position on the face board need Mechanical & Thermal's check.
