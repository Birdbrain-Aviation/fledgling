# Remaining work (WIP)

Status of the Fledgling board as of the saved files. Sources: the 2026-11-14 DRC report in this folder, the layout log, and a script-based check of `hardware/Fledgling.kicad_pcb` (`tools/`). KiCad's own DRC is the authority. The script check is approximate and is only meant to point at where to look.

## Layout

- [ ] **Plane connections (main open task).** 23 unconnected items. A grid maze router (2026-11-21) found no legal route or via spot for any of them. Each one is blocked by a specific trace on the opposite outer layer, so a via can't pass through:
  - C15.1 and R8.1 (B.Cu): /QSPI_SD1 on F.Cu runs over both
  - C16.1 (B.Cu): VSYS and /GPIO16 on F.Cu
  - R32.1 (B.Cu): /GPIO16 on F.Cu
  - U3.1 (F.Cu): a GND track on B.Cu; U3.11: /GPIO1 on B.Cu
  - U3.38, U3.49: +1V1 and /VREG_LX traces around the pins on both layers
  - U3.47 (GND) and C11.2: /VREG_LX, /VREG_AVDD, +3V3 and +1V1 traces
  - J1 A9 (VBUS): /USB_D+ on B.Cu; U7.5 (VBUS): Net-(J1-CC1) on B.Cu
  - J12.2 (+3V3): only route crosses the +5V trunk on F.Cu
  - 12 small GND pour islands on B.Cu/F.Cu with no room for a stitching via
  Fix: move those blocking traces (QSPI_SD1 and GPIO16 first: they clear four pads), then add vias. Re-routing the RP2350 regulator area (+1V1/VREG_LX) by hand is the bigger job.
- [x] **Dangling vias and tracks** cleaned up 2026-11-17: 15 pass-through vias and 5 dead stubs removed. Left: a cosmetic GPIO22 overshoot at J13 pin 6.
- [x] **J1 pad B8 short** (GND via over SBU2, with hole-clearance and mask-bridge errors): fixed 2026-11-17 by moving the via 0.18 mm.
- [x] **Thermal relief error** on J1's shield pin fixed 2026-11-17 (shield pads set to solid connection).
- [x] **Dead-end +5V copper near J2** removed 2026-11-17.
- [x] **Silkscreen clean-up** (2026-11-21): no silkscreen warnings left. LOAD CELL, RADIO, PYRO BATT and MAIN BATT labels moved clear of pads and other silkscreen.
- [ ] **Library mismatches.** 5 footprints differ from their library copies and 3 are missing from the Fledgling library. These predate the layout work.
- [x] **Connector orientation** checked from footprint geometry (2026-11-21): USB-C J1 opens off the left edge; XT30 J5/J9 have power pins inboard and support pegs at the right edge, so they mate off the edge. Pin 1 = GND, pin 2 = + on both. Neither has a 3D model linked.
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
