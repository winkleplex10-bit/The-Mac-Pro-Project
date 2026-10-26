# AM5 CPU board: J1-area stiffener, backplate tie-in, washers (DRAFT)

Status: draft from Mechanical & Thermal, 2026-10-23. I read the board (`kicad/macpro62-am5-v3/macpro62_am5.kicad_pcb`) but did not change it. Coordinates are KiCad board mm, with y increasing toward J1. **GAP** means not measured or not published. No dimensions here are invented.

## 1. Inputs (as given or read from the board)
| Item | Value | Source |
|---|---|---|
| Board thickness | 1.6 mm (Apple stock is 2.04) | Aidan's decision |
| Base connector | Amphenol ME1022410103011, rated for a 1.57 mm card | CPU & Base Board |
| J1 tab outline | x 98.055-177.945, shoulder at y 227.018, tip at y 238.278 (11.26 mm tab) | Edge.Cuts |
| J1 key notches | x 116.5 (to y 230.8) and x 137.435-139.285 (to y 231.7) | Edge.Cuts |
| Gold fingers | Pads end about y 235.3; tips at y 238.3 | J1 pads |
| Connector insertion depth / wipe | **GAP**. Needs the Amphenol card drawing for the mating depth. | — |
| Core holes | H1 (103.25, 194), H2 (172.75, 194): Ø5.0 with 9 mm pads. H3 (103.25, 139), H4 (172.75, 139). | board / CPU & Base Board |
| Frame screws | H5 (110.41, 187.75), H6 (166.41, 187.75), H7/H8 at y 145.75: Ø3.4 NPTH | board |
| Back-side height cap / PSU gap | 4.5 mm cap / about 5 mm gap (Aidan's measurement) | — |

**Discrepancy:** in this file, H3 and H4 still use the `CoreMountHole_D5.0_Pad9` footprint. The approved Ø5.5 mm hole with a 9.5 mm pad is not in it, and the H2 slot is not cut. CPU & Base Board should confirm which file holds the edit.

## 2. Back-side parts near J1 (from courtyards)
| Ref | Side | Courtyard | Notes |
|---|---|---|---|
| **J8** M.2 2280 boot | **Back** | x 97.5-186.0, **y 203.7-226.7** | **Covers the whole J1 root on the back.** It is kept in the 2026-10-21 lane plan (README). The floorplan's "remove J8" item is out of date. Module plus connector height: **GAP**. |
| CB1 / CB2 12 V bulk | Back | x 79.8-96.2 / 180.2-196.8, y 169.8-200.2 | Clear of the H1/H2 pads (pad edges x 98.75 / 177.25) |
| DIMM_A1 / DIMM_B1 | Back | x 72.3-79.3 / 197.1-204.1, to y 215.7 | Outside the tab width |
| Front: CAC1 | Front | x 104.8-175.2, y 216.8-225.2 | Front strip between CAC1 and the shoulder is only 1.8 mm |
| Front: COUT1 / U4 | Front | to y 204.2 / 206.2 | Front band **y 206.2-216.8, x 98-178** has no courtyards (copper and routing not checked) |

Free back-side zones near the J1 root:
- **Z1:** y 189.5-203.2, x 98.8-177.2, between the H1/H2 pads and J8. This is the backplate's lower edge.
- **Z2/Z3:** x 79.3-97.5 and x 186.0-197.1, y 200.2-227.0. These are the corners beside J8, outside the tab width.
- **No free back-side area at the tongue root itself** (y 203.7-227) while J8 stays there.

## 3. Stiffener proposal
Rules for every option:
- Nothing on the tab (y > 227.0). The fingers stay bare 1.6 mm FR4.
- Stiffener keepout edge at y ≤ 226.0, giving 1.0 mm setback from the shoulder for the outline tolerance. The connector-body standoff is a **GAP**, so this setback still needs checking against the Amphenol drawing.
- Material: 304 stainless, 1.2 mm thick. This is the same material and gauge as the AM5 force and stiffener frames (WikiChip, see `am5-socket-mechanicals.md`). Add a 0.18 mm polyimide or Mylar insulator on the board side. FR4 (1.0-1.6 mm, bonded) is the lighter, non-conductive alternative. It is about 10x less stiff than steel, so I'd choose it only where there's no screw path.

| Option | Where | Outline | Fixing | Pros / cons |
|---|---|---|---|---|
| **A: backplate extension (recommended baseline)** | Back, zone Z1 | Custom backplate runs on to y ≤ 203.2 across x 98.8-177.2 | Clamped by the **H5/H6 frame screws**, which already pass through the backplate. Clearance cut-outs around H1/H2 of at least Ø9.5. | No new parts or holes. Stiffens the board between the socket and J1, but stops 24 mm short of the tab root. |
| B: front bar | Front, y 206.2-216.8 (or 206.5-216.5 after margin), x 99-177 | 1.0-1.2 mm stainless or FR4 bar | Bonded, or 2-4 small NPTH plus PEM (new holes: a board change) | Closer to the root. Needs the core and heatsink clearance over that band (**GAP**) and a routing check. |
| C: true root stiffener | Back, y 204-226, x 98-178 | Full-width bar at the tongue root | From the backplate or its own fasteners | Best support for the tongue, but **only if J8 moves** or is removed. That is a lane-plan change, so it's Aidan's decision. |

**Why not share H1/H2:** the core screws are stock shoulder screws, and the shoulder sets the clamp stack: board 1.6 + washer 0.4 = 2.0 mm, versus Apple's 2.04 mm. Any plate added under the head adds its thickness to that stack, so the stock 12.72 mm screws would bottom out on the shoulder and couldn't clamp. Using a 0.4 mm plate under the head instead of the front washer would move H1/H2 to a 7.84 mm contact height while H3/H4 stay at 7.44 mm. That tilts the core. So **H1/H2 are clearance holes in the plate.** The backplate ties in through H5/H6 (and H7/H8), as the 12.78 mm frame screws already do. The frame-screw stack with the backplate thickness included is a **GAP**: the backplate thickness isn't measured, and Intel's reference part is 2.2 mm, Apple's is unknown.

## 4. Stack against the 5 mm PSU gap (back side)
| Case | Height above the board's back face | Margin to 5.0 |
|---|---|---|
| Stiffener 1.2 + insulator 0.18 | 1.38 | 3.6 mm |
| Backplate (if 2.2, the Intel reference figure only) + 0.18 | 2.38 | 2.6 mm |
| Shoulder-screw heads on the back (H1-H8) | **GAP** (head height not measured) | — |
| Existing parts: cap 4.5 / BT1 4.1 | 4.5 / 4.1 | 0.5 / 0.9 mm |
| J8 M.2 module plus connector | **GAP** | — |

The 5 mm gap assumes the washers go on the front (board to boss), so the board's back face stays where Apple's was. No stiffener option sits under a part that's capped at 4.5 mm, so the plate itself has room.

## 5. Washers (0.4 mm, between the board front and the core bosses / frame seats)
| Holes | Pad | Washer ID | Washer OD (proposed) | Thickness |
|---|---|---|---|---|
| H1 / H2 (Ø5.0, H2 is a 5.0 × 6.0 slot) | 9.0 | 5.1 | 8.0 (0.5 mm inside the pad edge; covers the 6 mm slot) | 0.40 ± 0.02, 304 stainless, flat |
| H3 / H4 (Ø5.5) | 9.5 | 5.6 | 9.0 | 0.40 ± 0.02 |
| H5-H8 (Ø3.4 frame) | — | **GAP** | **GAP** | 0.40 |

Needs confirmation (**GAP**):
- Shoulder diameter, which must be smaller than the ID: 5.1 / 5.6.
- Whether the shoulder or the head bears on the washer.
- The core boss face diameter, which must be at least the OD.
- Frame-screw shoulder and head dimensions.

## 6. Open decisions for Aidan
1. Choose an option. **A** needs no board change. **A + B** gives better root support. **C** needs J8 moved or removed.
2. Choose the material: stainless 1.2 mm (recommended) or FR4.
3. Confirm that the stiffener doesn't share H1/H2 (reason in section 3).

## 7. Gaps to close
- Amphenol mating depth and connector-body standoff.
- J8 module plus connector height.
- Core and heatsink clearance over y 206-217 on the front.
- Screw head, shoulder and thread dimensions.
- Core boss face diameter.
- Backplate thickness.
- Inner screw vertical span.
- DRC (kicad-cli is not available on the box).
