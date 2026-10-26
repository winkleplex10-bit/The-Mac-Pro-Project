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
- The boot NVMe on the chipset has been dropped, so **boot now comes from the SSD board**. It keeps 2× Gen5 x4 over MCIO. PROM21 downlink 2 is now spare.
- **Version B:** the 4-drive switch sits **on the SSD face against the thermal core**, not on the base board. Its power (~14–17 W) and cooling therefore belong to the SSD face (Mechanical & Thermal).
