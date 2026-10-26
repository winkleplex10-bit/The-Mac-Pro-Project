# MacPro6,2 rail requirements (collected 2026-10-26)

## GPU Board (estimates, not measured; GPU work is on Aidan's hold)
- Input is 12V only; all other rails are made on-board. Standby draw from 12V is well under 1A.
- Continuous: about 160W, roughly 13.5A at 12V. Design for 17A (about 15A at a 180W cap).
- Spikes: about 25-30A on 12V for under 1ms (1.5-2x average); a little above average for about 10ms. Typical figures for an RDNA2 card, not measured.
- Feed: a dedicated 12V connector next to the VRM input caps. The slot or MCIO carries only signals plus a little aux power.
- Connector: a 2x3 or 2x4 Micro-Fit-class header rated 20A or more, or a short bus-bar or blade pair. Keep the 12V loop short and low-inductance; the board has its own bulk input caps.
- NOTE: these figures are for the Navi23 (RX 6600 XT-class) board. Aidan's stated target is an xx70-class GPU (220-250W), so flag the mismatch to Aidan and Master Bot in the consolidated proposal.

## Firmware & Software (proposal)
- Signals: PS_ON# (active low, driven by the EC or Super I/O); PWR_OK with ATX timing (100-500ms after 12V is in regulation, dropped at least 1ms before it falls out); a separate open-drain standby-good; AC-OK early warning of at least 1ms; PMBus at 100kHz; an open-drain SMBALERT#/OCW# line OR'd into PROCHOT_L and a GPU throttle input.
- Standby: 12V_SB in the ATX12VO style, at least 1.5-2A.
- Power limiting in three layers: static firmware budgets (PPT/TDC/EDC, GPU TBP, USB PD about 100W) plus 10-15% margin; a ~100ms EC loop on PMBus power; and a hardware OCW that throttles fast. The PSU must allow 20-30% short peaks above 600W.
- Gap: whether AGESA allows runtime power-limit changes.

## Mechanical & Thermal (provisional)
- CPU: 105W steady with bursts to about 125W (estimated from Aidan's stress test), which is about 120-140W at 12V into the CPU board.
- GPU about 160W. SSD plus I/O about 40-60W, by their estimate. Their working total is about 450-520W.
- Fan: assume 12V PWM at 1-2A. They want a switched 12V fan rail, a tach readback, and a PSU overtemperature flag; fan control stays on the board. The PSU needs about 6 CFM.
- Carrier: stays inside the stock outline, case and 6 holes. Only about 5mm to the CPU board, so nothing tall faces it. The 28mm module leaves about 5mm for the carrier.
- 12V route: around the outer edge, as a bus bar or 8-10 AWG crimped pair under 100mm long, rated 70C or more, landing on lugs or press-fit tabs on the base board. Keep it away from the PCIe 5.0 and display paths.

## I/O & Storage (estimates)
- I/O board: 12V only. Six USB-C ports at 15W (90W) plus four USB-A at 4.5W (18W) is about 120W from 12V; chips add 12-15W. Total about 135W continuous (11.3A), 13A peak, budget 15A. It wants its own harness straight from the PSU: Micro-Fit 2x4 or 2x5 with 4 pins of 12V, 4 of GND and 1-2 of 12V_SB.
- SSD board: 12V. About 30W with 2 drives, or about 65W with 4 drives plus a switch (5.5A, 6.5A peak). It's fed through the base board's face-module power pins.
- Standby: about 2W (0.17A at 12V).

## Consolidated worst case at 12V (Power Supply)
- CPU 120-160W (105W cap, or 142W Eco) + GPU 160-180W + I/O 135W + SSD 65W + fan up to 24W = about 505-565W on the Navi23 board.
- With an xx70 GPU at 220-250W, the total is about 625-640W, over the 600W limit.
- USB PD and the I/O figures assume all ports loaded at once; the firmware PD budget (about 100W) adds diversity.
- Standby: 1.5-2A at 12V_SB per F&S, against an I/O standby need of about 0.17A plus EC/SPI.

## Updates 2026-10-26 ~5:38 PM ET
- GPU Board: the RX 6600/Navi23 is dropped; the likely replacement is an RTX 5070 with a power limit (not final). Plan the 12V GPU feed for up to about 250W (about 21A) plus spike margin, on a separate 12V input. The earlier 160W figures are void.
- Base Board & Connectors (map rev 2, /workspace/docs/interboard-bandwidth-map.md): 12V stays on bus bars and lugs; no power on MCIO (0.5A per pin) or the Meg-Array (0.45A per pin). The base board now carries an Astera PT5161L Gen5 x16 retimer, about 9W; there's no switch on the base board. A possible PEX89024 Gen5 switch (about 14W) on the SSD board, and a VL822 hub on the I/O board (power TBD).
- New uncapped worst case: CPU board 215 + GPU 250 + I/O 135 + SSD 65(+14 switch) + retimer 9 + fan 24 = about 700-715W at 12V. That exceeds a 600W supply on the 6A inlet, so the 850W path needs the 10A+ inlet and a cooling upgrade.
