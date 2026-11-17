# Remaining work (WIP)

Status of the Fledgling board as of the saved files. Sources: the 2026-11-14 DRC report in this folder, the layout log, and a script-based check of `hardware/Fledgling.kicad_pcb` (`tools/`). KiCad's own DRC is the authority. The script check is approximate and is only meant to point at where to look.

## Layout

- [ ] **Plane connections.** The DRC report lists 26 unconnected items, nearly all plane or power nets: U3's +3V3 pins (11, 38) and the decoupling capacitors around it (C15, C16, C17, R8, R32, D7), U3 GND pad 47, J12 pin 2, and VBUS at J1 pad A9 and U7 pin 5. Fix with vias to the planes or a local +3V3 pour under U3.
- [ ] **Dangling vias (22).** Several are on signal nets (QSPI_SCLK, QSPI_SD2, QSPI_SD3, SWCLK, SWD, GPIO6, GPIO12, GPIO18, load-cell lines). Each needs checking: either a leftover stub to delete or a route that was never finished.
- [ ] **Dangling tracks (4).** On Net-(D8-DO) near J7, PYRO_BUS near J8, GPIO22 near C16 (11 mm long), and GPIO2 near J13.
- [x] **J1 pad B8 short** (GND via over SBU2, with hole-clearance and mask-bridge errors): fixed 2026-11-17 by moving the via 0.18 mm.
- [ ] **J13 thermal relief.** GND pin has 1 spoke where 2 are required. J13 is Do Not Populate.
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
