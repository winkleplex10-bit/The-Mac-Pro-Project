# Mains-side design & certification options — 600 W 12V-only PSU, Mac Pro 6,1 bay
Date: 2026-10-25. Constraints: 120 V, stock inlet 100–250 V / 6 A, 2-pin +/- header to PSU, system-fan cooled, ~5 mm gap to CPU board. Nobody contacted, nothing bought.

## 1(c) Pre-certified 600 W 12 V modules (mains side already certified; only DC side custom)  — RECOMMENDED
| Module | Size (mm) | Rating / cooling | Eff. | Certs | Link |
|---|---|---|---|---|---|
| MEAN WELL LOP-600-12 | 127 x 76.2 x 35 (~339 cm³) | 12 V/50 A; 600 W with 23 CFM forced air, 360–400 W convection; 150% peak 3 s (900 W) | typ 93%, up to 95% | IEC/UL 62368-1 (CB, TUV, UL), EN55032/CISPR32 EMC, Class I or II | https://www.meanwell.co.uk/power-supplies/medical-grade-power-supplies/lop-600-series ; https://www.meanwell.com/newsInfo.aspx?c=1&i=1303 |
| Vox Power EIRE600-12 | 127 x 76.2 x 28 (~271 cm³) | 600 W forced air or conduction; 450 W convection @115 VAC; 5 V/2 A bias + 12 V fan out, AC_OK, inhibit | up to 96% | ITE + medical, Class I/II, Class B conducted/radiated | https://www.vox-power.com/industrial-power-supplies/eire600-industrial/ |
| (reference, not a fit) Vox NEVO+600S | modular, fan-cooled | 600 W; 6 A input at 120 V | 86–89% | — | https://resources.ampheo.com/static/datasheets/vox-power/nevo-600s-5834-dk000.pdf |

Notes / gaps:
- Both fit inside the 250–340 cm³ envelope from psu_850w_research.md, but the stock 661-7542 is a **curved** board along the chassis edge (tekdep teardown, https://tekdep.com/mac-pro-2013-a1481-teardown); a flat 127x76 brick may not fit the bay. Bay measurements decide this.
- LOP-600 needs 23 CFM for 600 W; Mechanical & Thermal's estimate for the PSU section is ~9 CFM. At ~9 CFM expect ~400–450 W continuous unless derating curves show otherwise → a 520 W operating point is borderline. EIRE600 (450 W convection, conduction option) is the better thermal fit; check its derating curve vs 40 °C inlet.
- Input current: 600 W / 0.93 ≈ 645 W ≈ 5.4 A at 120 V, 6 A at ~108 V → inside 6 A inlet only at nominal; firmware cap near 520–560 W sustained recommended.
- Not yet checked (search budget): Delta, Murata, Bel, Advanced Energy/Artesyn (Excelsys), Cincon, XP Power, TDK-Lambda 600 W 3x5" parts. Same 3x5" class exists from several of these; verify per datasheet before choosing.
- Mounting a certified component PSU still requires end-product checks (spacing to chassis, bonding, enclosure, inlet/fuse), but these are much smaller than certifying a custom primary.

## 1(a) Contract custom AC-DC design firms
Not researched to a verified shortlist this pass. Candidate types: module makers' custom/modified-standard groups (Vox Power, MEAN WELL modification service, SL Power, XP Power, Bel, Advanced Energy) — these usually want volume (NRE typically tens of $k; unpublished). Freelance/consultancy power engineers are the realistic route for a one-off. GAP: no firm confirmed to take individual clients.

## 1(b) Labs / NRTLs (UL Solutions, Intertek ETL, TÜV, CSA, SGS) — published ranges are third-party estimates; NRTLs don't publish prices
- UL 62368-1 initial listing: ~$8k–20k, 8–16 weeks for simple products (https://krono-labs.com/guides/ul-nrtl-safety-listing); other estimates $3k–15k+ testing plus factory inspection and ongoing fees (https://factoryfollow.com/en/ul-certification-guide.html). Listing assumes ongoing production + factory follow-up — poor fit for one unit.
- FCC Part 15B (SDoC, unintentional radiator): ~$1.5k–3k mid-tier lab, $3k–5k tier-1 (https://ideambox.com/downloads/product-safety-and-certification/); some quote $500–1.2k (https://www.wowohcool.com/blog/certifications-us-eu-guide/).
- For a single, owner-built unit, the relevant route is an NRTL **field evaluation** (one-off label) rather than listing — not priced here; GAP.
- Legal note: for a personal-use, non-marketed device, NRTL listing is not federally required; FCC Part 15 still applies to operation (no harmful interference).

## 2. Earth path in the Mac Pro 6,1
Known: stock PSU 661-7542, 12.1 V / 37.2 A, sandwiched between I/O panel and logic board, removed with I/O board as a unit (iFixit teardown step 17/22, https://www.ifixit.com/Teardown/Mac+Pro+Late+2013+Teardown/20778; guide https://www.ifixit.com/Guide/Mac+Pro+Late+2013+Power+Supply+Replacement/21212). Uses a 3-prong IEC C13/C14-style cord (Class I).
GAPS (no public source found): how the inlet earth pin bonds to chassis (lug/screw vs. through PSU), whether the PSU's earth is via its mounting screws, bonding wire size. A search-summary claim that "chassis is grounded via PSU mounting hardware" was unsourced and is NOT relied on. Aidan's description (2-pin +/- header) implies earth does not go through the header → must be confirmed by inspection/continuity (unplugged) from inlet earth pin to chassis and PSU mounting points.

IEC/UL 62368-1 Class I requirements (summary; verify against the standard text, clause 5.6):
- Accessible conductive parts that could become hazardous on a single fault must be bonded to protective earth; protective bonding conductors sized for the protective-device current (table in 5.6.3/5.6.4).
- Earthing terminal: dedicated, not relying on solder alone, not used to fix other parts, earth connection makes first/breaks last.
- Bonding resistance test (5.6.6): high test current (based on the circuit's overcurrent-protection rating, e.g. ~2x rating for a set time); limit ≈0.1 Ω (or voltage-drop limit) per spec table — exact values to verify.
- With an open-frame module: its earth/PE pad must be screwed to chassis with a dedicated bonded fastener per the module's install manual.

## Recommendation
Use a pre-certified 3x5" 600 W 12 V module (EIRE600-12 first, LOP-600-12 second) as the mains side, after bay measurements confirm fit, and build only a custom DC-side board (standby, sequencing, sensing, bus bars). Add a dedicated, tested PE bond from inlet earth pin to chassis and module PE. Cap sustained load ~520–560 W. Avoid a fully custom primary unless the module can't physically fit; that route needs a qualified power engineer plus NRTL field evaluation and ~$10k+.

## Stock PSU measurements from Aidan's scans (2026-10-26, ruler-scaled, about +/-1-2mm)
- PCB: about 159 x 103 mm. Case: about 33mm tall, 104mm wide at the base and 80mm at the top; length still to be confirmed.
- Six mounting holes in three pairs, about 96mm apart side to side, at about 19, 84 and 149mm from the top edge (65mm pitch).
- Four output lugs on the top edge. Rails: 12.1V main and 11.0V standby.
- Fit: the Vox EIRE600-12 (127x76x28) fits, on a carrier board with the 11V standby, lugs and signal header. The LOP-600 (35mm tall) is too tall.
- Scans: /workspace/psu/scans/
- Label (photo in scans/stock_psu_label.jpg): AcBel Polytech FSD004. Input 100-240Vac, 50-60Hz, 6A. Outputs 12.1V at 37.2A and 11.0V at about 0.54A (that part of the label is partly obscured). Bulk capacitors: at least three Rubycon CXW 450V 180uF (105C). The new standby supply should be sized at about 1A.
- Lugs (from the back scan, about +/-1mm): 4 lugs in two corner pairs, each soldered with a 2x2 pad pattern about 8mm wide and 5.5mm tall. Lug centers are about 7, 20, 82 and 95mm from the left edge (12.7mm pitch within each pair), with the pads about 6.5mm below the top edge. Lug pin assignments (12.1V / 11V / GND) are still to be confirmed by continuity check, and positions by calipers. Zoomed view: scans/lug_zoom.png
