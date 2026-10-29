# Stock 6,1 base board connector positions (from Aidan's flatbed scan, 2026-10-28)
Scale ~26.7 px/cm from printed ruler; board dia ~122 mm. Accuracy ~±2 mm / ±3°. Board centre = origin, +Y toward the two upper connectors.
- CPU card-edge (silver): horizontal, centreline ~12 mm below centre.
- I/O Meg-Array: centre ~(0, -46) mm, long axis horizontal (parallel to CPU edge).
- GPU face Meg-Array (upper-left): centre ~(-35, +34) mm, r~48 mm, at ~135° from I/O; long axis rotated ~45° (long side faces centre).
- SSD face Meg-Array (upper-right): centre ~(+35, +34) mm, mirror of GPU.
- GPU/SSD centre to I/O centre: ~87 mm straight line.
Decision (Base Board & Connectors): each face gets its own Meg-Array 300 on Apple's footprint/position, own pinout. Left/right assignment provisional.
