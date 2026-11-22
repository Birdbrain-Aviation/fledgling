# Fabrication outputs: NOT FOR FAB

`Fledgling-gerbers-NOT-FOR-FAB-2026-11-21.zip` holds the Gerbers (F.Cu, In1.Cu, In2.Cu, B.Cu, mask, paste, silkscreen, Edge.Cuts, job file) and the Excellon drill files (PTH and NPTH). They were exported from KiCad 10 on 2026-11-21 from the board in `hardware/` at that date.

**Do not order from these.** KiCad DRC still reports 22 unconnected power connections (see `docs/remaining-work.md`). Most are the RP2350's +3V3 pins and decoupling caps with no via to the In2.Cu +3V3 plane, so a board built from these files would not power up correctly. They are here to show the layer set and to let the board be previewed in a Gerber viewer such as JLCPCB's.

Settings: 4.6 mm coordinate format, X2 attributes with netlist, Gerber job file, drill origin absolute, millimetres.
