# Remaining work (WIP)

Status of the Fledgling board as of the saved files. Sources: the 2026-11-14 DRC report in this folder, the layout log, and a script-based check of `hardware/Fledgling.kicad_pcb` (`tools/`). KiCad's own DRC is the authority. The script check is approximate and is only meant to point at where to look.

## Layout

- [ ] **Plane connections (main open task).** 23 unconnected items (D7 and C17 fixed 2026-11-17 with 0.45/0.2 mm vias), all power. Every pour connects through-hole pads only, so each SMD power pad needs its own via. The +3V3 pins of U3 (1/53/54, 11, 20, 38, 44/45/49), the B.Cu decoupling parts (C15, C16, C17, R8, R32, D7) and J12.2 have none. Neither does GND at U3.47/C11.2, nor VBUS at J1 A9/B4 and U7.5. The area is too dense for an automatic fix: it needs a hand re-route of the U3 power fan-out. See design-decisions.md section 6.
- [x] **Dangling vias and tracks** cleaned up 2026-11-17: 15 pass-through vias and 5 dead stubs removed. Left: 5 VBUS vias, to be tied in with the VBUS plane work, and a cosmetic GPIO22 overshoot at J13 pin 6.
- [x] **J1 pad B8 short** (GND via over SBU2, with hole-clearance and mask-bridge errors): fixed 2026-11-17 by moving the via 0.18 mm.
- [ ] **Thermal relief error.** KiCad 10 reports it on J1's GND shield pin (B.Cu, 1 spoke to an isolated island). The older report named J13.
- [x] **Dead-end +5V copper near J2** removed 2026-11-17.
- [ ] **Silkscreen.** Not started: 38 reference designators, the logo and function labels. The report shows 17 overlaps, 10 pads clipped by solder mask and 6 clipped by the board edge (all at the MH1 corner).
- [ ] **Library mismatches.** 5 footprints differ from their library copies and 3 are missing from the Fledgling library. These predate the layout work.
- [ ] **3D check** of XT30 and USB-C mating directions.
- [x] **DRC re-run** on 2026-11-17 (`DRC-2026-11-17.rpt`): 29 errors (25 of them unconnected items), 68 warnings. Re-run again after the layout items above.
- [ ] **Gerber and drill export**, then a fab quote.

## Design decisions

Settled on 2026-11-16 and written up in [`design-decisions.md`](design-decisions.md). The schematic and board changes were made on 2026-11-17.

- [x] Pyro fuse: keep 5 A (bench-measure igniter current before ordering)
- [x] Feed-forward capacitors: C35 560 pF and C36 330 pF set in the schematic and BOM (DNP). Still to verify on the bench
- [x] E220 supply: J2 pin 6 moved from +5V to +3V3 in the schematic and board, BOM note updated. Still to check E220 output power at 3.3 V on the bench
- [x] Telemetry packet format: deferred, no PCB impact
- [ ] Review of buck converter loops, USB and QSPI routing, which DRC does not judge

## Verification not done

- No board has been fabricated, powered or flown.
- Pyro-channel behavior (off at power-up, reset and MCU fault) is a design intent that has not been tested on hardware.
