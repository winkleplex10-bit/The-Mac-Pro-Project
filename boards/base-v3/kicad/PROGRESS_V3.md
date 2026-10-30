# BP v3 (hybrid storage lanes) work log
Copy of kicad/macpro62-backplane rev A1 (originals untouched; checksums /workspace/scratch/v2_baseline/originals.sha256).
Plan: /workspace/docs/storage-lanes-options.md §3 (hybrid). GPU keeps x16 (J9 unchanged), slot A unchanged,
slot B = PCH RP21 Gen4 x2 over ex-RSVD CPU-LINK pairs -> J10 lanes 4-5 + REFCLK1; PERST1#/CLKREQ1#/WAKE1# on the BP.
Rules: 4 layers, existing HS/SATA/USB2 untouched (0 skew, 2/2 vias), no rip-up / single-net passes only, don't push.

## 19:49 ET: v3 copy made from v1 A1 (work/ not copied)
- J10 BP-end contacts (rows swap vs the module end in the plan doc): host TX lane 4/5 -> B20/21, B23/24; host RX -> A20/21, A23/24;
  REFCLK1 -> A29/A30; PERST1# -> B29; CLKREQ1# -> A26; WAKE1# -> A27; PRSNT1# -> B30 (bp_pins.mcio_bp_end + S2X J1 module end).

## 20:2x ET: v3 = AM5 Ryzen 7000/9000, slot B on the 2nd CPU x4 at FULL x4 (CPU-LINK v3 pinout, no 2nd cable)
- docs/cpulink_224_pinout_draft.csv rewritten as CPU-LINK v3 (v1 copy in work/cpulink_v1.csv). Slot B pins (all GND-flanked):
  TX (A row): lane4 A82/83 (was GND pair inside A81-A84), lane5 A86/87 (PWRBTN#->B99, RSTBTN#->A104), lane6 A101/102 (BIOS_SEL->B89, GPIO0 dropped), lane7 A54/55 (RSVD_REFCLK2)
  RX (B row): lane4 B82/83 (RSVD_HS_B2), lane5 B86/87 (SMB_CLK/DAT, DNP-isolated), lane6 B104/105 (RSVD_LS3/4), lane7 B54/55 (RSVD_HS_B1)
  REFCLK1: B101/102 (GPIO3/RSVD_LS2; B100/B103 GND). Spares left: RSVD_HS_A1 (A76/77), RSVD_HS_A2 (A79/80). GND 80 -> 78.
  Why not A76-A80 for TX: their escapes are boxed in by USB2_MCU (L3 squiggle 134.6-137.6) / USB2_SPARE (L3+L4) / SATA0_RX L3 diag -> kept RSVD.
- bp_pins: J10 set B mapped (BP end: REFCLK1 A29/30, PERST1# B29, CLKREQ1# A26, WAKE1# A27, PRSNT1# B30 NC).
- bp_model: J10 = mcio_nets("FS", 8, setb=True); WAKE0# (J1 A99) + J10 A9/A27 = CB_WAKE_N; appended R64 (1k PLTRST->FS_PERST1_N), Q12 (2N7002 FS_HOLD clamp), R65 (10k FS_CLKREQ1_N->3V3_AUX_S). A1 refdes unchanged.
- HS regex (bp_fix/bp_clean2/bp_ls) now includes REFCLK1.
- tools/v3_apply.py: sets the 42 changed pad nets on the routed A1 board (no rebuild), rips CB_PWRBTN_N (moved pin), removes the A82/A83 GND via + A81 stub, gives A81 its own GND via (133.24,114.97). -> work/v3_s0.kicad_pcb
- tools/bp_pair2.py: JSON-configured coupled-pair router (bp_pair generalised; +HS spacing, L3<->L4 reference rule, 45-deg only).
- Routing topology: RX4-6 + REFCLK1 on L1 north of J1 -> west through the J1/J10 gap -> around J10's SW end -> J10 outer side -> A pads (0 vias).
  TX4-6: J1 escape via -> L3 under J1 -> west/NW on L3 -> L1 (outer of the RX group) -> dive to L4 at the landing -> between-row via -> B pads.
  Lane 7 TX/RX: key-gap channel into the pocket on J10's inner side.

## 20:35 ET: slot B routed at x2 (lanes 4-5 + REFCLK1); x4 not routable on this 4L BP -> lanes 6-7 NC on the BP
- J1 P/N per contact pair chosen for the route (CSV updated): RX5 P=B87/N=B86, RX6 P=B105/N=B104, REFCLK1 P=B102/N=B101; TX4-6/RX4 P on the east pad.
- bp_pair2: direction-aware A* states within 3 mm of the end (45-deg arrival was being missed).
- Order/boards: s1 RX4 (L1, 0 vias) -> s2 REFCLK1 (L3 under J1 -> L1 -> L4/L3, kept off L1 near J10) -> s3 RX5 (L3 -> L1, 2 vias, outer L1 landing on A23/24)
  -> s4 TX5 (west route, L4 landing via between-row vias) -> s5 TX4 (west/south route, 6 vias, ~106 mm). All hard conflicts 0; USB2/SATA untouched.
- After lanes 4-5, lane 6 (RX6/TX6) has no path left (dry runs: no goal) -> FS_BP_LANES = 6 in bp_model: J1 A101/102,B104/105,A54/55,B54/55
  and J10 lanes 6-7 pads are NC on the BP (CPU-LINK v3 still defines all 4 lanes, so a 6-layer BP can do x4 with no cable change). -> work/v3_s6.kicad_pcb
- LS nets to re-route (work/v3_ripped.txt) incl. 3V3_SB/5V_SBY/3V3_AUX_S/VREG_AVDD pieces; R64/Q12/R65 still to place.

## 20:43 ET: Aidan -> BP v3 goes 6 layers, slot B full x4. 4L x2 attempt archived (work/v3_s1..s7, bp_fix run on v3_s7 left to finish; result not used)
## 20:55 ET: 6L conversion
- Stackup JLC06161H-2116: F.Cu L1 sig | In1 L2 GND | In2 L3 sig | In3 L4 NEW sig "L4_SIG_SLOTB" | In4 L5 GND (new solid plane) | B.Cu L6 (ex-L4). Two GND planes In1 + In4.
  Existing copper keeps its KiCad layer -> every v1 pair keeps geometry, length, skew and vias.
- Impedance (tools/zsolve): outer 0.26/0.125 = 85.5 ohm; existing In2 0.21/0.127 = 88.7-89.7 ohm (kept, in tolerance); new inner pairs 0.24/0.127 = 84.5-85.7 ohm. docs/impedance_v3_6L.json.
- B.Cu now references the In4 plane, so the 4L L3<->L4 reference rule is gone; the new rule is In2 <-> In3 (broadside: no overlap with foreign copper).
- tools: v3_6l.py (layer table, stackup, In3/In4 GND zones, rule areas extended), bp_fix/bp_pair2 BP6=1 mode (4 routing layers), v3_specs BP6 widths + lane 7 specs.
- bp_model FS_BP_LANES back to 8. RX7 polarity P=B55/N=B54 (CSV updated). Base = work/v6_s1.kicad_pcb (6L, RX4 from 4L s1 kept: L1, 0 vias).

## 21:04 ET: 6L slot B dry runs + first commit chains (BP6=1, NOREROUTE=1, single-pair passes, HS/SATA/USB2 never ripped)
- Dry runs on v6_s1: every pair finds a path with 2-3 vias, 35-46 mm (4L was up to 6 vias / 106 mm). Lane 7 needed reg x1 141 -> 157 (J1 lanes 7 sit east at x 152).
- TX7: the A-row south via sites (y 115.4) collide with USB2_FACEP_N (B.Cu, x 152.9, protected) -> new start j1_gap_via: L1 stub NW into the J1 row gap,
  pair vias at (152.20/151.60, 112.95), then B.Cu north. Polarity unchanged (P=A54/N=A55).
- v3_specs: ENDL env (per-pair J10 landing layer; clk/tx6 land on In3), pre-stub widths follow BP6 W[L3] = 0.24.
- Order matters: tx6's L3 run north blocks the REFCLK1 start; rx7's L3 diag crosses TX7's between-row via sites at J10 -> tx7 before rx7, clk before tx6.
  Chains: c (clk rx5 tx5 tx6 rx7: tx4/rx6 failed), a (rx6 tx6 rx5 tx5 tx4 rx7: clk failed). Trying orders f/g/h now.
- bp_finish: 6L zone set (L1..L6 GND pours, In1 + In4 full-connection planes), stitch grid needs all six fills.

## 21:37 ET: router fixes + chain m (Aidan killed the obsolete 4L bp_fix pid 872688; 4L result not used)
- DRC on chain-k board showed P/N self-shorts: tight 45-45 zig-zag U-loops at J1 starts (clk, rx7) and sharp end turns (tx4, tx7).
  bp_pair2: MINRUN = 6 grid steps (0.3 mm) of straight run before any turn; end/start relief no longer overrides the In2<->In3 broadside rule.
- clk and rx7 now leave J1 heading NORTH from the via pair (j1_north_via_n) -> polarity REFCLK1 P=B101/N=B102, RX7 P=B54/N=B55 (base work/v6_s1b).
- Chain m (spec6d): clk 34.0/34.9 mm 4 vias, rx6 42.5/44.8 mm 0 vias, rx5 39.8/41.9 mm 3 vias, tx6 52.9/53.9 mm 4 vias, tx7 43.2/44.2 mm 2 vias,
  rx7 40.1/38.5 mm 2 vias -> work/v6_m6. tx5 aborted (broadside over REFCLK1 on In3), tx4 no path -> retrying (chains p/q/r).
- LS clean-up pass on the old chain-k board left 6 LS nets unrouted (FS_CLKREQ1_N, CC_PRSNT2_N, CB_I2C0_SDA, FS_PWR_EN, FP_SMB_SDA, DVDD); R65 re-anchored
  next to R41 (3V3_AUX_S) -> will redo the LS pass on the final pair board.
## 21:42 ET: base board re-made
- My clean-up glob deleted work/v6_s1 / v6_s1b; re-made as work/v6_base.kicad_pcb = v3_6l.py(v3_s1) + REFCLK1 swap (verified against v6_m1: identical pads/tracks except the clk routing). Copy: v6_base.KEEP.
- spec6e = spec6d + every other pair's fixed J1/J10 via sites reserved (blocks, all routing layers) so an early pair cannot sit on a later pair's landing vias.

## 21:57 ET: all slot-B pairs routed on 6L (work/v6_D8.kicad_pcb)
- bp_pair2 NOSTITCH=1 during the chain (the router's own GND return vias were landing in the J1 row gap and blocking RX6's escape); return vias added after (tools/v3_stitch.py).
- Order clk -> rx6 -> tx4 -> tx5 -> rx5 -> tx6 (VIAC 25) -> tx7 -> rx7 (chain B, tx6 redone as D6). Every pair hard-conflict 0, HS/SATA/USB2 untouched.
  clk 31.6/32.3 mm 4 vias | rx6 42.5/44.8 mm 0 | tx4 48.6/49.5 mm 3 | tx5 56.5/57.5 mm 3 | rx5 66.0/67.9 mm 3 | tx6 64.0/65.0 mm 4 | tx7 43.2/44.2 mm 2 | rx7 40.1/38.5 mm 2 (rx4 from A1: L1, 0 vias). Skew tuned next.

## 22:12 ET: slot-B pairs final geometry (work/v6_E6 -> E8)
- DRC-style own check found P/N pinches from pre-fix routes: ripped + re-routed REFCLK1, RX4, RX5, TX7 (single-pair passes). bp_pair2 now treats the pair's own fixed
  vias as obstacles for the pair body. TX7 start v2 (j1_gap_via2): P via (152.05,112.40), N via (151.45,113.00), USB2_FACEP_N via kept >= 0.3 mm away.
  REFCLK1 inner corner at the J10 landing hand-fixed (In3, (129.84,89.72)); P/N spacing check 0 issues; In2/In3 broadside overlap 0.
- bp_tune (TUNE_RE slot-B): every pair 0.000 mm intra-pair skew (lengths/vias in the final report).
- tools/v3_stitch.py: 23 GND return vias at slot-B pair vias (19 sites had no room: J1/J10 via fields, covered by the existing 3 mm GND stitch grid).
- R64 (97.30,105.85), Q12 (102.50,106.35) r90, R65 (99.50,106.00) next to R41 (3V3_AUX_S). LS single-net pass (RIP=0) running -> v6_F1.

## 22:48 ET: LS routing done (v6_K0)
- LS nets ripped by the slot-B chain were restored from v6_base / pre-6L copies where they clear (work/graft.py), then single-net passes (RIP=0, HS/SATA/USB2/slot-B never touched).
- Walled U1/J1 pins got escape vias (work/autovia.py): U1.1, U1.7, U1.55, U1.56, U1.57, U1.80, J1.A96, J1.A105. Blocking LS nets ripped and rerouted one net at a time.
- Broadside rule kept for LS too: temporary In2/In3 keepouts over slot-B pair copper (work/bsko.py) while rerouting 5V_SBY, CB_THERMTRIP_N, FS_PERST_N, CB_FAN_PWM, CB_UART0_RX; keepouts removed (v6_K0).
- Own connectivity check (work/conn.py, GND/3V3_SB = planes): 0 split nets. Slot-B: 9 pairs 0 skew, P/N issues 0, broadside overlap 0. v1 48 pairs identical to work/skew_v1_baseline.txt. HS/SATA/USB2 copper identical to E8.
- Next: bp_post (6L zones, stitch, clean) -> v6_L.

## 23:15 ET: bp_post on v6_K0 -> v6_L
- bp_finish fixed for KiCad 9 SWIG (removed items kept alive in KEEP; two-stage BPF_STAGE=A/B in bp_post.sh; backup work/bp_finish_pre_dupfix.py.bak). 6L zones filled.
- v6_L DRC: 22 unconnected, mostly 3V3_SB (U1 pins etc.: 3V3_SB copper had been ripped by the slot-B chain and was left to the plane stitch, which is not enough), plus CB_UART0_TX and FS_PWR_GOOD breaks. Next: graft/route 3V3_SB on K0, re-run bp_post.

## 00:05 ET: 3V3_SB + LS breaks (v6_M -> v6_P)
- 3V3_SB grafted from v6_base (K1), duplicates removed (work/dedupe.py, 93 dupes from earlier grafts), bp_post -> v6_M (19 unconnected).
- drcfix + fragment removal (work/rmitems.py) + single-net routes with broadside keepouts -> v6_N3; bp_post -> v6_P: 20 unconnected (U1 3V3_SB pins, R52/R53/R47, J1 B107/B108, UART0_RX, PWR_ALERT, EN_5V), 6 clearance (FS_CLKREQ1_N vs H1, FS_PRSNT_N vs GND via).
- Cause: the In2 3V3_SB plane already covers U1, but the base per-pin escapes (17 vias, under-QFN like v1) were taken by LS re-routes (13 LS nets, 0 HS). Next: rip those 13 LS nets, restore base 3V3_SB escapes, re-route the 13 one net at a time.

## 00:58 ET: patching stopped (did not converge) -> clean LS re-route with Freerouting
- Rip-and-patch rounds on the U1 area (v6_Q*..S5) kept trading one blocked QFN pin for another (last state: 2 nets open). Per Aidan (00:54), switching to: lock HS/SATA/USB2/slot-B + GND + base 3V3_SB escapes, delete all other LS copper, one bounded Freerouting run on 6L with broadside keepouts, then single-net clean-up.
- New tools/bp_ls6.py (6L copy of bp_ls.py).
- 00:55 (box clock) prep: v6_K0 -> LS copper deleted (5270 items), HS/SATA/USB2/slot-B + GND locked, base 3V3_SB escapes re-grafted (233 items, locked), L3_3V3_SB plane kept -> work/ls6_fan.kicad_pcb + ls6_fan.dsn (7209 keep-outs incl. In2<->In3 broadside, L2/L5 = power layers).
- Freerouting fr-2.1.0, job_timeout 00:25:00, nohup, pid 989478 -> work/ls6_fan.ses.
- FR run 1 (blank LS, 25 min): best 37 unrouted connections, 35 nets split (U1 fan-out) -> not used.
- FR run 2: base LS copper re-grafted onto the clean board (work/graft.py now uses real pad shapes, CL 0.095; 3828 LS items, unlocked so FR may move them) -> 60 nets with a gap -> work/ls6b_fan.dsn, FR 25 min, pid 1000963.
- 01:46 FR run 3 started: ls6_fan + v1 U1-area copper (r9, 827 items locked; 3 v3 GND stitch vias near U1-north removed; 5 nets keep partial v1 copper where TX6_P/TX5_N cross) + base LS graft unlocked (58 split nets) -> work/ls6c_fan.dsn, 25 min timeout.
- FR run 2 finished 01:57 (25 min timeout, pass 25, 52 unrouted) -> work/ls6b_routed.kicad_pcb: 46 nets split (KiCad-side). Not used.
- 02:13 FR run 3 done (pass ~25, 36 unrouted) -> work/ls6c_routed.kicad_pcb: 34 nets split; remaining breaks are J1 west B-row/A-row CB_* pins boxed in by slot-B L1/L3/L4 pairs + some J4/J10/south nets. FR run 4 (resume of run 3) started with L2/L5 allowed for LS inside x98-152 y100-136, wire keep-outs 0.6 mm around HS copper on adjacent layers (tools/bp_ls6.py L25=...), 25 min.
- 02:39 FR run 4 done (28 unrouted at timeout) -> work/ls6d_routed.kicad_pcb: 18 nets split (KiCad-side): 3V3_AUX_S 5V_SBY CB_I2C0_SCL CB_PWRBTN_N CB_PWR_ALERT_N CB_THERMTRIP_N CB_WAKE_N FP_THERM_TRIP_N FS_MOD_LED_N FS_PERST_N FS_PRSNT_N FS_PWR_GOOD QSPI_SD1 SYS_INT_N TRIP_N USB_DM_M VREG_AVDD VREG_LX. Next: move the blocking slot-B pair segments at J1 west (user 02:34).
- 02:50-03:40 single-net clean-up on FR run 4 (work/seq.sh, bp_fix, broadside keep-outs) -> work/ls6e_seq.kicad_pcb: 3 nets split (5V_SBY B110/B111 vs A-row group, CB_WAKE_N J1.A99 -> J10 (new v3 net), FS_PRSNT_N). Slot-B stats unchanged (skew 0.000, vias 4/0/3/0/2/3/3/4/2).
- Slot-B move analysis: RX6 north-corridor variant (work/rx6move.py) rejected: going north from the B104/B105 pins flips P/N sides vs the existing north run (needs a crossover). New tool work/reach.py (0.1 mm grid min-cost path on L1/L3/L4/L6, broadside rule, slot-B copper crossable at a cost) shows CB_WAKE_N has a path WITHOUT moving any slot-B pair (only LS in the way): A99 -> L1 -> via (116.6,112.2) -> L6 under the rows -> via (113.8,109.1) -> L3 north. Routed that way (/tmp/wk1), the 5 LS nets in the way are re-routed one by one (work/reachseq.sh).
- 03:07 LS complete per conn.py (0 split excl. GND/3V3_SB pours): work/ls6h.kicad_pcb. CB_WAKE_N routed via the reach.py path (L1 -> L6 under the J1 rows -> L3 north, 2 vias), then bp_fix single-net for CB_FAN_PWM/FAN_TACH/THERMTRIP (THERMTRIP via reach.py, L1, 0 vias)/5V_SBY/FS_PRSNT_N (+1 bridging segment). No slot-B pair had to move after all: the J1-west blockers were LS copper, not pair copper. Slot-B stats unchanged.
- 03:08 USB2_MCU_P: 2 duplicate copies of a 0.07 mm L3 segment (135.9,114.9) had been dropped by dedupe in the ls6c graft; restored so HS copper is item-for-item identical to v6_E8 (3111 items) and the v1 48-pair skew table matches work/skew_v1_baseline.txt exactly. Broadside temp keep-outs removed -> work/ls6h_nobs.kicad_pcb; bp_post -> work/v6_T.kicad_pcb started.
- 03:25 bp_post done (work/v6_T); DRC fix-ups with single-net/manual passes -> v6_U..v6_AB (dangling/fragment removal, duplicate-via removal, reach.py/bp_fix single-net reconnects). Slot-B unchanged.

## 03:42 ET: DRC clean-up done -> work/v6_AL (DRC 0 / parity 0 / unconnected 0)
- v6_AB -> v6_AL, single-net/manual fixes only:
  - CB_I2C0_SDA L4 jog moved off the 5V_SBY via (108.9,111.2) (clearance).
  - Dead tails removed (CB_RSMRST_N L6, CB_I2C0_SDA L1/L6/L4 + orphan via, CB_THERMTRIP_N overlap junction replaced by one clean L1 segment, rip remnants).
  - 3V3_SB: R52.2 L4 link (reach.py); R19/R23 L3 island joined by a short reach.py link; R53.2 island (boxed in by 5V_SBY on L3) joined after one single-net rip of FS_PWR_GOOD, which was re-routed (reach.py, 0 vias).
  - GND islands: 2 GND vias in the U1 exposed pad (109.5/111.5, 127.5; the EP had none after the v1 U1-area copy); J7.33 tied to J7.39 by an L1 GND track (x 123.9) so the J7.27/33 pour piece is no longer floating. SW1 pad 2 (101.5,113.88) set to solid zone connection (starved thermal).
  - Broadside: LS on L4 under v1 L3 HS (USB2_FACES/MCU/SPARE, FS_REFCLK) existed since FR (ls6h: 6 nets). Temporary keep-outs (work/bsko.py, SBRE env) and single-net re-routes of CB_UART0_TX, CB_FAN_PWM, FP_THERM_ALERT_N, FS_PWR_GOOD and 5V_SBY -> overlap 0 in both directions (work/bside.py). One GND stitch via at (116.49,115.83) removed (clearance to the new 5V_SBY).
- Checks on v6_AL: conn.py 0 split; GND and 3V3_SB one component each incl. pours (work/zisl.py); slot-B 9 pairs skew 0.000, vias 4/0/3/0/2/3/3/4/2, P/N issues 0; HS/SATA/USB2 copper identical to v6_E8; v1 48-pair skew table identical to work/skew_v1_baseline.txt.

## 03:43 ET: v6_AL -> backplane.kicad_pcb (project folder)
- Previous project files kept in work/pre_final/. pro/dru unchanged (identical to work/pro_backup).
- tools/build_bp_sch.py re-run (26 symbols, 155 parts). ERC: 0 errors / 0 warnings (erc_report.txt).
- Project DRC with schematic parity first showed 9 net_conflict warnings: NC pads whose auto "unconnected-(...)" net names still carried the old pin names (J1 A104 GPIO1->RSTBTN#, J1 B89 SMB_ALERT#->BIOS_SEL, J9 A26/A27/A29/A30/B29/B30 RSVD->CLKREQ1/WAKE1/REFCLK1+/-/PERST1/PRSNT1, J10 B30 RSVD->PRSNT1). Those 9 single-pad nets were renamed (no copper on them).
- Final: DRC 0 violations, 0 unconnected, 0 parity issues (drc_report.txt), zones refilled. Copy: work/v6_final.kicad_pcb.
- 03:43 J10 value text was stale ("x2 ... lanes 6-7 NC" from the earlier x2 build; lanes 6-7 ARE routed). tools/bp_model.py line 153 + board J10 value -> "Face S x4 + slot B x4 (v3: lanes 4-7 + REFCLK1)" (backup work/pre_final/bp_model.py.bak); sch rebuilt; ERC 0; DRC 0 / unconnected 0 / parity 0.

## 03:43 ET: jlc_out (6 layers)
- python3 tools/jlc_out.py backplane.kicad_pcb jlc -> 18 gerber/drill files (L1..L6 + mask/paste/silk/edge, PTH/NPTH), gbrjob LayerNumber 6, BOM 44 lines, CPL 143 placed (0 bottom). Previous jlc/ kept in work/pre_final/jlc_prev.
- BOM vs previous: +Q12 (2N7002), +R64 (1k), +R65 (10k), J10 text fixed.

## 03:44 ET: cost note
- /workspace/macpro62-cost-estimate.md §11: close-out note added (delta unchanged: +$25-35 excl. CPU, -$52..+$102 incl. CPU). cost_update.py not run. Backup /workspace/scratch/macpro62-cost-estimate.pre_v3final.md.

## 03:44 ET: previews
- tools/render.sh -> docs/preview_v3_L1.png (F.Cu+silk), docs/preview_v3_L3.png (In2), docs/preview_v3_L4.png (In3), docs/preview_v3_L6.png (B.Cu).

## 03:44 ET: README v3 section added (backup work/pre_final/README.md.bak)

## 03:45 ET: ICD v3 check
- /workspace/macpro62-interface-control-v3.md: rev-3 audit row 'RSVD ×13' (no ×14 left); v3 row 'GND ×78, RSVD ×4'. Board J1 matches: 78 numbered GND pins (+4 BL lock pads), 4 RSVD (RSVD_HS_A1/A2 P/N); BIOS_SEL B89 and RSTBTN# A104 NC on the BP (moved).

## 03:45 ET: sync zip
- mkzips.py backplane-v3 am5-v3 backplane-v2 lga1700-v2 + DOCS (ICD v3, parked ICD rev4) -> /workspace/macpro62-sync-icd.zip: kept 402 (all old entries byte-identical, 0 missing), added 445, total 847, testzip OK, no work/ entries. Pre-run copy: /workspace/scratch/macpro62-sync-icd.pre_v3final.zip.
- v1/AM5 originals: sha256sum -c v2_baseline/{originals,am5_original}: 273 OK; the only mismatch is the sync zip itself (expected, entries added).
- Not pushed.

## 2026-10-19 12:15 ET: DRU unit fix (local only, not pushed)
- KiCad 9.0.2 rejected the whole .kicad_dru because the values had no units, so the custom pour rules never ran in DRC or zone fills. Values now in mm. The pour rule now applies to tracks only (`A.Type == 'Track'`); as written it cut the J1 GND vias off every plane.
- Refilled the board. Pour to 85R pairs is now >= 0.50 mm and pour to 90R pairs >= 0.40 mm (measured). It was 0.20 mm before (zone clearance only).
- Fixes: J7 pad 45 GND: 0.2 mm stub plus a GND via at (123.95,131.75).
- DRC 0 / 0 unconnected. jlc/ regenerated: copper and drill changed, BOM/CPL unchanged. Backup: /workspace/backups/<board>-predru-20261019-1157.tgz

## 2026-10-29 I/O Meg-Array (J13)
- J13 added: 84501 receptacle (same footprint as J11/J12) at (148.9, 146.8), rot 0.65 deg. Stock field (-1.73,-48.74) shifted +0.63 mm x / ~1.9 mm inward so the worst body corner sits 0.75 mm inside the disc edge and the body clears KO6_S2 by ~0.3 mm. A1 at (130.42, 141.29); row A faces board centre.
- J7 (M.2 SATA boot DNP placeholder) removed from the PCB (boot NVMe dropped); schematic still has it -> annotate/remove there.
- 568 track segments/vias under J13 ripped (power-sequencing/standby/interlock nets). Reroute pending.
- OPEN: J2 (PSU Micro-Fit), J6 (IOB-LINK JST) and ~15 small parts (Q5/Q7/Q8/Q9/D1/D2/U8/JP1/D8/R13/R14/R16/R48/R56/C20) still overlap J13. No free board area outside the Gen5 channel; needs a decision (J2 likely obsolete with CPU-board-only power; J6 functions could fold into J13 spares).
- J13 pads have no nets yet (schematic symbol not added). Pin map: /workspace/docs/pinmaps/base-iob-megarray.csv base-end column.

## 2026-10-29 09:30 J2/J6 deleted (Aidan approved), J6 folded into J13
- PCB+schematic: J2, J6 removed; J7 removed from schematic. J13 symbol added (sch at 1234.44,647.70), 300 pads netted from base-iob-megarray.csv.
- J13 new pins: J7/J8 USB2_SPARE_P/N, J10 HALL_A_N, J11 HALL_B_N, J13/J14/J16/J17 3V3_SB (each beside GND), J19/J20 I2C_SYS_SCL/SDA, J22 SYS_INT_N; C29 -> PWRBTN_IN_N, H29 -> IOB_PRSNT_N (existing IOB rows).
- Small parts moved off J13 (no courtyard overlaps left).
- Orphaned by J2/J7 removal (flagged, not deleted): 12V_MAIN_IN has no source (J1 P12V v4 pins not yet in base J1), 11V_SB_IN (D2,D9), PSU_PS_ON_N (Q9), PSU_PWR_OK (R54), 3V3_M2 (Q3,C17,C18), M2_DEVSLP (R10), SATA0_* labels on J1.
- WARNING: tools/build_sch.py still generates J2/J6/J7; do not rerun it without updating.

## 2026-10-29 ~09:45 [DRAFT: J1 v4 not yet pinned by Aidan] J1 v4, J14 MCIO (CB J3), dead-net cleanup
- DRAFT: J1 re-pinned to the full v4 draft (108 pins; table docs/J1_v4_applied_20261029.csv). The 12 V rows could not be added alone: A104/B104/A105/B105 carried RSTBTN#, FS_RX6 and PWR_ALERT# in v3. P12V (8 pins A/B103-106) -> EFUSE_IN -> U25 TPS259824L -> 12V_MAIN_IN.
- 127 J1 fanout segments now on the wrong net were ripped; 85 dead-net segments deleted. SSD-lane fanout from J1 must be rerouted.
- Deleted D2, D9, Q9, R54, Q3, C17, C18, R10, J9, J10 (sch+pcb). SATA0 labels went with the J1 remap.
- J14 MCIO-124 RA (base end of CB J3) added to sch, netted from mp62-cb-j3 rev2 (bb_contact column = mirrored side). Mapping: /workspace/docs/pinmaps/base-cbj3-j14-mcio-map.csv. NOT PLACED: staged off-board at (240,100); no front-side space.
- U27 TCA6408A @0x20 on I2C_SYS (P0 IOB_PLT_RST_N w/ R127 pull-down, P1/P2 USB OC#, P3/P4 LEDs) + R128/R129/C84, placed on B.Cu near (150,141.7).
- MCU: GPIO38 I2C_BB_SCL, GPIO10 I2C_BB_SDA (PIO target), GPIO20 CB_SMB_ALERT_N.

## 2026-10-29 11:50 [DRAFT J1] J1 v4 rev2, SSD 12 V removed, eFuse resized
- J1 mirrored to am5-v4 DRAFT rev2: P12V on A/B102-107 (12 pins, A102/B102/A107/B107 added) -> EFUSE_IN; B81/B82/B83/B90 -> GND (USB2_SPARE, BIOS_SEL, duplicate PWRBTN# dropped). PWRBTN to CB now only via J14 (J3 PWR_BTN#).
- USB2_SPARE_P/N (J13 J7/J8) to be fed from the planned base USB2 hub, not J1.
- J12 J1-J12 now GND (SSD board has own PSU input). J25 SSD_3V3_SB_OPT kept. 12V_MAIN_IN feeds only U24 + local loads.
- U25 ILIM R122 249R -> 300R (~5.0 A typ per SLVSEI3D p.9) for ~3.5 A load.
- 10 stale segments ripped. ERC: 0 errors, 330 dangling-label warnings (erc_report_20261029_1150.txt).

## 2026-10-29 ~13:30-14:10 EDT  J14 placed (Aidan approved top side, 13:26)
- Backup: /workspace/backups/backplane-v3-pre-J14place.tgz. Script: tools/j14_place.py (build_sch.py NOT run).
- J14 -> MP62_Placeholders:MP62_MCIO_124P_Vertical_SMT_TE2360189_PLACEHOLDER (SFF-TA-1016 vertical, 0.60 pitch, courtyard 44.75 x 13.81). F.Cu, (150.00, 130.00), rot 180 (A1 at +x as before). Amphenol DS-0002 URL returns 404, so footprint is from TE 2360189 drawing; row pitch / peg positions UNVERIFIED vs G97V24332HR. Sch Footprint field text-edited to match.
- Pin nets: all 68 rows of /workspace/docs/pinmaps/base-cbj3-j14-mcio-map.csv match; 0 mismatches. SH pegs -> GND.
- Keep-out cleared: x 127-173, y 123.1-137 (J14 courtyard x 127.58-172.42, y 123.10-136.91). Cable lane toward J1 is above board (plug exits at ~14 mm); only low parts allowed there (0402/0805/SOT-23 placed there).
- Moved 54 parts:
  - R100: (175.0, 136.0) -> (175.85, 135.05) [1.3 mm]
  - R56: (170.5, 135.95) -> (172.6, 144.45) [8.8 mm]
  - R57: (169.15, 135.6) -> (174.0, 144.65) [10.3 mm]
  - Q5: (129.72, 134.95) -> (125.05, 130.8) [6.3 mm]
  - Q11: (133.88, 126.11) -> (129.55, 120.6) [7.0 mm]
  - Q8: (165.22, 124.95) -> (161.05, 120.65) [6.0 mm]
  - R12: (164.1, 135.65) -> (173.2, 146.6) [14.2 mm]
  - R34: (137.15, 122.61) -> (135.9, 117.75) [5.0 mm]
  - C4: (162.16, 121.88) -> (169.6, 120.9) [7.5 mm]
  - Q4: (138.38, 137.1) -> (122.9, 144.15) [17.0 mm]
  - C3: (161.38, 125.66) -> (165.15, 118.3) [8.3 mm]
  - D8: (161.0, 136.25) -> (176.45, 144.45) [17.5 mm]
  - R42: (139.15, 122.61) -> (137.9, 117.75) [5.0 mm]
  - R17: (161.65, 133.1) -> (157.95, 121.7) [12.0 mm]
  - R15: (139.15, 133.1) -> (144.95, 121.75) [12.8 mm]
  - J8: (139.28, 128.07) -> (136.3, 105.0) [23.3 mm]
  - C7: (158.38, 122.66) -> (157.75, 107.4) [15.3 mm]
  - R9: (141.65, 135.6) -> (126.15, 135.6) [15.5 mm]
  - C6: (157.66, 126.38) -> (154.05, 106.7) [20.0 mm]
  - R49: (164.1, 132.65) -> (153.2, 122.0) [15.2 mm]
  - R51: (143.15, 128.1) -> (149.5, 121.4) [9.2 mm]
  - R46: (143.15, 125.11) -> (146.9, 117.75) [8.3 mm]
  - R16: (143.5, 133.45) -> (142.1, 117.75) [15.8 mm]
  - R11: (143.65, 136.1) -> (149.65, 118.9) [18.2 mm]
  - D5: (156.1, 133.88) -> (174.0, 149.5) [23.8 mm]
  - D1: (129.77, 129.03) -> (124.95, 124.65) [6.5 mm]
  - C29: (155.13, 126.58) -> (153.25, 117.8) [9.0 mm]
  - C37: (145.13, 122.58) -> (143.9, 117.75) [5.0 mm]
  - R55: (145.15, 128.6) -> (140.6, 117.75) [11.8 mm]
  - R60: (145.15, 125.61) -> (151.3, 117.75) [10.0 mm]
  - Q7: (164.22, 129.45) -> (180.2, 145.65) [22.7 mm]
  - R13: (153.45, 136.5) -> (155.45, 118.1) [18.5 mm]
  - R59: (155.15, 129.6) -> (158.25, 117.75) [12.3 mm]
  - C28: (153.13, 129.59) -> (171.6, 121.3) [20.2 mm]
  - C26: (153.13, 126.58) -> (151.25, 107.45) [19.2 mm]
  - C27: (153.13, 123.58) -> (148.9, 107.35) [16.8 mm]
  - D10: (161.41, 129.66) -> (177.8, 126.15) [16.8 mm]
  - Q6: (147.1, 134.88) -> (125.45, 118.75) [27.0 mm]
  - C1: (147.13, 128.09) -> (156.55, 121.5) [11.5 mm]
  - R63: (147.15, 125.11) -> (145.5, 107.45) [17.7 mm]
  - R8: (146.6, 131.15) -> (139.1, 122.1) [11.8 mm]
  - R21: (152.1, 132.65) -> (160.4, 117.8) [17.0 mm]
  - C36: (132.63, 130.09) -> (124.6, 134.2) [9.0 mm]
  - C39: (157.13, 130.09) -> (145.45, 117.75) [17.0 mm]
  - R33: (134.65, 130.1) -> (124.25, 136.55) [12.2 mm]
  - R58: (159.15, 130.1) -> (169.4, 117.8) [16.0 mm]
  - C24: (151.13, 123.58) -> (146.9, 107.35) [16.8 mm]
  - C25: (151.13, 129.59) -> (167.9, 117.8) [20.5 mm]
  - C23: (151.13, 126.58) -> (143.9, 107.4) [20.5 mm]
  - R14: (151.0, 135.95) -> (152.1, 157.7) [21.8 mm]
  - C19: (149.13, 126.58) -> (134.05, 117.75) [17.5 mm]
  - C21: (149.13, 123.58) -> (141.75, 107.45) [17.7 mm]
  - C22: (149.13, 129.59) -> (140.0, 107.4) [24.0 mm]
  - R48: (150.0, 133.45) -> (150.5, 157.7) [24.3 mm]
- Ripped (NOT rerouted), 47 nets: 3V3_SB (84 seg/27 via), 5V_SBY (33 seg/3 via), AUXP_EN_N (10 seg/5 via), AUXS_EN_N (24 seg/6 via), BP_OTEMP_N (13 seg/0 via), CB_CARRIER_HOT_N (19 seg/1 via), CB_I2C0_SDA (16 seg/2 via), CB_PWRBTN_N (20 seg/0 via), CB_PWR_ALERT_N (10 seg/1 via), CB_SUS_S3_N (31 seg/5 via), CC_PRSNT1_N (12 seg/1 via), CC_PRSNT2_N (5 seg/1 via), FP_PWR_GOOD (4 seg/1 via), FP_THERM_ALERT_N (13 seg/3 via), FS_HOLD (19 seg/1 via), FS_MCIO_PRSNT_N (10 seg/0 via), FS_PERST_N (15 seg/2 via), FS_PRSNT_N (13 seg/1 via), FS_THERM_TRIP_N (7 seg/0 via), GND (109 seg/23 via), HALL_B_N (6 seg/0 via), I2C_SYS_SCL (1 seg/0 via), I2C_SYS_SDA (4 seg/1 via), ILK_A (12 seg/0 via), LED11_K (8 seg/0 via), LED_ST_K (8 seg/0 via), M2_EN_N (10 seg/0 via), MCU_LED_N (24 seg/5 via), MCU_RUN (14 seg/3 via), MCU_SWCLK (15 seg/1 via), MCU_SWDIO (12 seg/1 via), PSON_DRV (2 seg/0 via), PSU_PWR_OK_M (10 seg/1 via), PS_ON_REQ_N (3 seg/1 via), PWRBTN_IN_N (12 seg/1 via), SYS_INT_N (17 seg/0 via), TRIP_N (11 seg/1 via), USB2_MCU_N (13 seg/0 via), USB_DM_M (6 seg/1 via), USB_DP_M (18 seg/1 via), VIN (11 seg/0 via), VIN_F (5 seg/0 via), VIN_OR (2 seg/1 via), VREG_AVDD (17 seg/3 via), XIN (4 seg/1 via), XOUT (8 seg/1 via), XOUT_C (22 seg/3 via)
- No Gen5 nets, J1/J11/J12/J13/U20-U22 untouched.
- ERC: 0 errors / 331 warnings (work/erc_j14.txt). Own courtyard check: 0 overlaps involving J14 or moved parts. Full DRC running in background -> work/drc_j14.txt (30 min timeout). Flag: crystal load caps C36/C37 still far from Y1 (pre-existing).

## 2026-10-29 ~17:50-18:15 EDT Fab-push phase 1 (Aidan pt89u "make it fab ready")
- Backup: /workspace/backups/backplane-v3-pre-fabpush.tgz (whole project, pre-change).
- **J1 = APPROVED / FINAL** (Aidan 2026-10-29): /workspace/kicad/macpro62-am5-v4/docs/cpulink_224_pinout_am5_v4_PINNED.csv (md5 2379c873..., byte-identical to v4 DRAFT rev2). Base J1 pads checked pin-by-pin: 0 power/GND class mismatches (12x P12V A/B102-107 = EFUSE_IN, B81/B82/B83/B90 = GND, A93/B93 = 3V3_SB); all other differences are naming only (CB_ prefix, PET/PER=TX/RX, SSD1 lanes = FS_TX/RX4-7). Note: A91 RSTBTN_N is unconnected on the base (pad named GND in symbol) - cosmetic, flag.
- **OpenCore boot drive dropped (Aidan):** M2_EN_N net + its 2 global labels deleted; Q4 (2N7002, only drove M2_EN_N) and R9 (DNP pull-up, only on M2_EN_N) deleted from sch+pcb with their attached labels. AUXP_EN_N / AUXS_EN_N KEPT: they gate Q1/Q2 -> 3V3_AUX_P/S feeding J3/J4 aux headers, not the boot drive.
- **No NDA parts (Aidan 17:53):** U23 PT5161L_ALT_DNP placeholder (0 pins, no support parts) deleted from sch (instance + lib symbol + note text) and pcb.
- Dead-part check (NOT deleted, all still on live nets in sch): Q7 (PS_ON_REQ_N/ILK_A/ILK_B), Q8 (THERM_LATCH/ILK_B/PSON_DRV), R12 (PSON_DRV-GND), R15 (PS_ON_REQ_N pull-up), R55 (PSU_PWR_OK_M only pad -> truly dangling). PSON_DRV has no load since J2 was deleted, so the Q7/Q8/R12 interlock chain output is dead; deleting it removes the PS_ON interlock function -> needs Aidan.
- ERC after edits: 0 errors.
- Placement legalizer work/legalize.py (log work/legalize.log): courtyard/keep-out/board-edge/Gen5-copper aware spiral search around each part's net centroid (C36/C37 at Y1 pins). Fixed R14,R48 (edge ring), R57,D5,D8,R12 (KO6_S3), C83/U26, C82, C79, R121, J8 (out of J14 lane -> 113.2,138.8 near U1), C36/C37 (now ~1.7 mm from Y1 pins), and pulled most long-moved J14 parts back to <=8 mm of their nets. Q7: no legal spot within 15 mm (left; dead-chain part, see above).
- J11@KO6_S6 / J12@KO6_S1: courtyard-only intrusion (courtyard edge 2.87 / 2.47 mm from hole centre vs 3.0 mm KO radius; nearest pads 6.4 / 6.0 mm away vs 1.65 mm hole pad radius). Keep-outs are drawn bigger than needed; not real copper conflicts. Connectors not moved.
- Netclasses: new PWR_HI (EFUSE_IN, 12V_MAIN_IN) 1.5 mm / 0.2 clr / 0.8-0.4 via; PWR 0.6 mm; PWR_FINE (3V3_SB) 0.4 mm.
- All non-PCIE_85R copper ripped (old routing collided with moved parts); PCIE_85R copper locked; Freerouting 2.1.0 (box-local JRE 21) routing all non-PCIE nets via work/bp.dsn -> bp.ses.
- **BLOCKER found:** Gen5 is not connected through the redrivers in the schematic netlist. J1 FP_*/FS_* nets have pads only on J1; U20/U21/U22 *_A nets only on the redriver; J11 has no PCIE nets (GPU face pinout open). The 92 J1 Gen5 fanout nets carry stub copper to nowhere (old direct-route remnants, up to 89 mm). The net splice (J1 FS_*/FP_* -> *_A) is a schematic change; not done.

## 2026-10-29 ~19:45 EDT Resume after interruption (executor)
- State found: Gen5 net splice ALREADY applied (sch + pcb, 18:35; ERC 0 err in work/erc_splice.txt). J1 FP_* <-> U20 A side, J1 FS_* <-> U21/U22 A side, U21/U22 *_B <-> J12. U20 B side (FP_*_B) U20-only, waiting for GPU-face pinout. Dead J1 Gen5 copper already deleted (0 PCIE track length). Freerouting job on work/g5.dsn (non-Gen5 classes) running since 19:12, pass 1 = 491 unrouted.
- Backup: /workspace/backups/backplane-v3-pre-gen5splice.tgz (19:45, excl. work/v6_*).
- Step 0 (Aidan 19:44 approved): Q7,Q8,R12,R15,R55 + 12 attached global labels removed from sch. PCB NOT yet updated (pcbnew removal script segfaulted once, retry blocked by Auto-review classifier error); pcb unchanged, backup work/pcb_pre_pson.kicad_pcb. Sch nets gone: PSON_DRV, PSU_PWR_OK_M, ILK_B. ERC: 0 errors (work/erc_pson.txt).
