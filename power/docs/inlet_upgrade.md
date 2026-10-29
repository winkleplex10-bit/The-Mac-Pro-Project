# Mac Pro (Late 2013 / MacPro6,1 chassis) AC inlet upgrade: research notes
Status: research only. Nothing bought, nobody contacted. Mains wiring must be done or checked by a qualified person.

## 1. Stock inlet (Apple 923-0505)
- It's a separate field-replaceable part (printed P/N 604-4796) that holds the inlet in Apple's shaped housing. iFixit "Mac Pro Late 2013 AC Socket Replacement" (https://www.ifixit.com/Guide/Mac+Pro+Late+2013+AC+Socket+Replacement/21214): you remove the PSU and I/O board, the inlet cable routes through a plastic clip to the PSU, and **4x T4 Torx screws** hold the socket to the housing.
- The parts listings give no dimensions (https://www.macrecycling.com/SKU-100897-AC_Power_Inlet_923~0505.html, https://tekdep.com/product/a1481-original-ac-inlet-923-0505-for-2013-mac-pro). Material is listed as plastic and metal.
- Cord: the Mac Pro takes a standard IEC C13 cord, so the receptacle face is a C14 (3-pin, earthed). I believe this from the stock cord, but I didn't find a datasheet that says so. **Confirm by test-fitting a standard C13 PC cord.**
- Inference (not confirmed): the receptacle is a standard-geometry C14 insert in a custom bezel and housing, with a flying lead to the PSU's 2-pin L/N header. Earth is bonded separately.

## 2. Where the 6A rating comes from
There's no Apple document on this. The C14 face itself is a 10A IEC / 15A UL connector type (IEC 60320; see the Schurter 0711 data below). So the "100–250V, 6A" label is most likely the **system input rating set by the PSU** (450W at the bottom of the range: about 4.5–5A plus margin). The flying-lead gauge and the insert's own certification could also limit it.
To check: read the wire gauge and temperature printed on the inlet leads, and any UL/VDE mark molded on the insert. If the insert is a certified 10A/15A C14 with 18 AWG or heavier 105°C leads, the stock inlet may already be able to carry about 8A. That still needs a qualified person's sign-off, plus a heat-rise check at full load.

## 3. Small certified C14 inlets rated 10A IEC / 15A UL
| Part | Mount | Key size | Ratings / approvals | Source |
|---|---|---|---|---|
| Schurter 4300.0704 (series 0711) | Snap-in from front, solder terminals | Panel 0.8–2.0mm; snap X=20.3/20.5mm (the standard C14 snap-in cutout is about 27.0×19.5mm per the general Schurter drawing, **verify against the PDF**) | 10A IEC / 15A UL/CSA, UL E96454, CSA 73165, 70°C pins, 62368-1 | https://www.schurter.com/en/datasheet/0711 |
| Schurter series 1061 (C14) | Snap-in, solder/QC/screw terminals | see datasheet | 10A/15A | https://www.schurter.com/en/datasheet/1061 |
| Qualtek 703W-00/54 | Right-angle **PCB mount** plus flange screws | Panel cutout 31.1×23.3mm, flange 40mm hole spacing, PCB pins 9mm apart | UL/CSA 15A, VDE/CCC 10A | https://www.qualtekusa.com/product/703w-00-54/ ; drawing https://www.suntronic.org/datasheet/9e/703W-00-54.pdf |
| Qualtek 703W-00/03, /04 | Screw flange (40mm centers), 0.187/0.250 QC tabs | standard screw-flange C14 | UL/CSA 15A, VDE/CCC 10A | https://www.qualtekusa.com/product/703w-00-03/ |
Not researched this pass: Bulgin, Kycon, CUI, Feller, Interpower and Volex. They have equivalent snap-in and screw C14s at the same standard sizes. The C14 face itself is fixed by IEC 60320, so no certified C14 gets much smaller than about 27×19.5mm at the face and about 20mm deep behind the panel.

## 4. Cord side
- A standard C13 cord is rated 10A (IEC) / 15A (UL, with 14–16 AWG SJT). Typical PC cords are 18 AWG, which is only 10A in the US. At about 8A that's fine, but for the 850W build specify a **UL 15A cord (14 or 16 AWG SJT)**.
- Apple's cord gauge: not found. Read it off the cord jacket (e.g. "18AWG/3C SVT").

## 5. Safety needs for the swap (IEC/UL 62368-1)
- A dedicated protective earth lead from the inlet's PE tab to the chassis. Use its own screw/stud with a star washer and don't share it with anything else. Earth gets made first and broken last. Then verify earth continuity (≤0.1Ω) and hipot.
- Internal L/N/PE wire: 16 AWG (good for 10–13A) or 18 AWG (about 10A, marginal for 15A), rated 105°C, 300V or more, UL1015/1007-class or double-insulated. Leave creepage/clearance at 3mm or more from SELV/metal, and heat-shrink the solder joints.
- Mechanical: the inlet must be screwed or captive-snapped so cord insertion and removal forces (around 50–80N) can't push it out. Use a metal or V-0 bracket, never just glue. Add strain relief or clip the leads so pulling on the cord can't load the solder joints. Keep the plastic clip routing.
- Add a fuse or protection matched to the new PSU input (normally inside the PSU).

## 6. Recommendation
1. First check whether the **stock 923-0505 already holds a standard certified C14**. If it does, and its leads are 18 AWG or heavier at 105°C, the frame doesn't need any rework. Only the leads might need to go up to 16 AWG.
2. If it doesn't, the best fits are a **front snap-in Schurter 0711 (4300.0704)** on a thin 1–1.6mm metal adapter plate cut with the standard C14 cutout and screwed to Apple's 4 T4 bosses, or a **Qualtek 703W-00/03** screw-flange inlet if the 40mm flange fits. The 703W-00/54 PCB type only makes sense if the inlet goes onto the new carrier PCB.

## 7. Measurements for Aidan (unplugged, PSU drained)
- The outside of the frame opening (W×H) and the depth available behind it to the nearest obstruction
- The C14 face itself (W×H, blade spacing), to check whether it's standard
- The 4 T4 screw positions (center-to-center) and the boss thickness
- Panel/frame wall thickness at the inlet (snap-ins need 0.8–2.0mm)
- Any markings on the insert (UL/VDE/maker) and on the leads (AWG, °C, UL style)
- Lead length, and how earth is bonded (the tab and where it goes)
- The text on the stock power cord jacket
- Photos of all of the above with a ruler
