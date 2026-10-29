# MacPro6,2

An open PCB redesign of the Mac Pro (Late 2013, "trashcan"). It keeps the enclosure, the triangular thermal core, the fan and the stock 450 W PSU, and replaces every board with new ones.

- `docs/`: the architecture spec (v0.2), the face module spec, the lineup research, the stock hardware reference and the service references
- `boards/`: current boards (cpu-am5, base-v3, io, ssd, gpu-placeholder)
- `power/`, `firmware/`: current PSU/power and firmware docs
- `archive/`: superseded and parked work
- `mechanical/`: board outlines (DXF), scan traces and 3D-print test parts

Status: early design. The CPU board is AM5 v4 (Ryzen 7000/9000, 1.6 mm 1080A; LGA1700 archived) with an Apple-style contact frame. The faces are an open module spec (GPU on Face P, storage on Face S).

## Current status
See [docs/STATUS-2026-10-28.md](docs/STATUS-2026-10-28.md) (2026-10-28 decisions: GPU on hold, Gen5 TI redrivers, SSD board A only) and [docs/STATUS-2026-10-26.md](docs/STATUS-2026-10-26.md) (AM5 baseline, firmware, power, thermal, connector research).
