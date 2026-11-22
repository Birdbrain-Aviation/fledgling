# Fabrication outputs

`Fledgling-gerbers-2026-11-22.zip` holds the Gerbers (F.Cu, In1.Cu, In2.Cu, B.Cu, mask, paste, silkscreen, Edge.Cuts, job file) and the Excellon drill files (PTH and NPTH), exported from KiCad 10.0.6 on 2026-11-22 from the board in `hardware/` at commit time. That board has 0 DRC errors and 0 unconnected items (`docs/DRC-2026-11-22-final.rpt`).

**Still not checked by a fab.** Nothing has been ordered, no CAM check has been run, and the routing has not been reviewed electrically (see `docs/remaining-work.md`). Do a JLCPCB (or other fab) CAM check and read the layer previews before ordering.

Settings: 4.6 mm coordinate format, X2 attributes with netlist, Gerber job file, drill origin absolute, millimetres. Files were renamed from the working copy's name to `Fledgling-*`.
