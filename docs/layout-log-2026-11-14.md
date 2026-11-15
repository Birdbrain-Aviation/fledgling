> **About this log.** This is the design log from the 2026-11-14 layout session, written by Claude (the AI assistant I used for layout automation and routing scripts). "My tooling" and "my own claims" below refer to Claude's scripts, not mine. It is kept here unedited as a record of what was done and what is still open. Some counts differ from the saved DRC report in this repo, because the report was run before the last edits.

# Fledgling: the 90x40 four-layer board, built

Session of 2026-11-14 on the user's PC. Continues `claude/fledgling-kicad-steps-2026-11-13.md` (the plan) and `claude/fledgling-design-rules-2026-11-13.md` (why the rules changed).

Board: `C:\Users\homeoffice\Desktop\Fledgling\Fledgling.kicad_pcb`.
Pre-edit backup: `Fledgling_pre90x40.kicad_pcb.bak` / `.kicad_pro.bak` in the same folder.
Custom rules: `Fledgling.kicad_dru`.

**Final state: 1 DRC error, 67 warnings, 37 unconnected.** First run was 315+ errors.
Pads 464, vias 388, track segments 1,804, nets 105.

## What is in the board

- **90 x 40 mm** outline, Edge.Cuts (100,100)-(190,140).
- **137 footprints positioned**, 70 moved for the resize (46 by a +20 mm x-shift, 24 individually), then 4 more moved to clear collisions. LOGO1 at (145.35, 123.0), not the stale +20 shift.
- **4-layer stackup**: F.Cu / prepreg 0.1 / In1.Cu / core 1.24 / In2.Cu / prepreg 0.1 / B.Cu, 1.6 mm. Layer ids In1.Cu = 4, In2.Cu = 6.
- **Design rules**: Default 0.127 mm track and clearance, via 0.55/0.25; Power clearance 0.127; hole-to-hole 0.3; min via 0.55; min through-hole 0.25; min annular 0.13. Pyro class untouched at 1.0 mm / 0.3 mm.
- **Six zones**: GND on In1.Cu, +3V3 on In2.Cu, VBUS island on In2.Cu at (107.0,117.5)-(112.0,126.0), GND pours on F.Cu and B.Cu, and a `PyroTap` rule area. Zone clearance 0.2 mm, **thru-hole-only thermal reliefs** (SMD pads connect solid; through-hole pads keep spokes for hand soldering).
- **Custom rule** in `Fledgling.kicad_dru`: 0.15 mm clearance for Pyro-class copper inside `PyroTap` (x 118.4-120.3, y 107.6-112.1), so the sense tap can reach R10 while the firing path keeps 0.3 mm everywhere else. 0.15 mm is still above IPC-2221's 0.1 mm for 0-15 V external uncoated.

## Collisions fixed

Moved, with all affected nets rerouted:
- **J7** (111.00, 104.50) -> **(112.75, 104.50)**. Its body came within ~1.5 mm of MH1's centre, where an M3 screw head needs 2.75 mm. (The keepout violation itself was only 0.027 mm of pad edge — the courtyard/mechanical clash was the real problem.)
- **J8** (121.00, 104.50) -> **(121.50, 104.50)** — forced, because J7 could not clear MH1 without hitting J8.
- **J13** (131.5, 133.0) -> **(131.5, 132.0)**, clear of J12.
- **C38** (145.6, 115.4) -> **(146.3, 115.4)**, clear of C37.

**All courtyard, keepout and NPTH-inside-courtyard errors are now zero.**

The moves also displaced five original tracks that merely passed near the moved pads rather than terminating on them (/RUN, Net-(D8-DO), /GPIO9, /GPIO22, PYRO_BUS); these were found by re-checking and rerouted.

## Both pyro sense taps are connected

`/Pyro/PYRO1_N` to R16 and `/Pyro/PYRO_BUS` to R10 now route. Two findings:
- A "split the tap onto its own net" fix is **not possible** — R10 pin 1 is electrically the same node as PYRO_BUS, so it would need a net-tie or 0-ohm part in the schematic.
- PYRO1_N was never actually stuck: it is Default class (0.127 mm), and only my tooling was applying Pyro clearance to it. Only PYRO_BUS needed the rule area.

## The gap the plan missed

The routing treated GND, +3V3 and VBUS as planes, so none were routed. But **an SMD pad on an outer layer does not reach an inner plane by itself — it needs a via.** 138 pads had no via to their plane; that was the entire "253 unrouted" figure. Fixed with generated connection vias plus GND pours on the outer layers. 138 -> 37.

## Bugs found in my own tooling

- **Unconnected pads were invisible to the clearance checker.** In `router2.py`, a pad whose net starts with `unconnected-` gets net id 0 and is then dropped from `R.pads`, which is what `aclr()` iterates — so those pads read as free space. This put a GND via through U6 pad 11. A re-check against all 458 pads (the router saw 433) found exactly 3 bad items, all from my own passes, none from the original routing.
- **Non-plated through-holes were invisible too** — same filter. J1's two USB-C mounting holes were not modelled by my checks and were not in the DSN given to Freerouting, which is why 12 tracks and a via sat 0.00-0.19 mm from them. `aclr()` now models NPTH at 0.25 mm hole clearance.
- **Footprint-embedded zones do not move with the footprint** when you edit its `(at ...)` in the file: KiCad stores their polygons in board coordinates. Each mounting hole carries a keepout, so moving MH2/MH4 by file edit left their keepouts at the old x=166.5 — 199 "items not allowed" errors against live tracks.
- **GUI zone drawing through computer use is unreliable.** Corner clicks after the properties dialog produced a degenerate 2-point polygon, and starting a second zone on the first one's corner destroyed the first. All zones were ultimately written into the file using the syntax KiCad itself emits.
- **Stitching vias ignored the Pyro 0.3 mm clearance** — one landed 0.225 mm from J8's PYRO_BUS pad.
- **`min_through_hole_diameter` was left at 0.3** while the new vias drill 0.25, which alone produced 199 errors.

## Correction to an earlier claim

`PYRO1_N` and `PYRO2_N` are **Default** class, not Pyro — the only Pyro pattern is `*PYRO_BUS*`. The note in the 13 November doc saying my tooling had those nets at the wrong clearance was itself wrong; 0.15 was correct then and they are 0.127 now.

## What is left

**1 error:** a thermal relief on J13's GND pin resolves only 1 spoke against a minimum of 2, on the B.Cu pour. J13 is Do Not Populate, so nothing is soldered there.

**37 unconnected:** plane-net pads that could not get a via — 19 GND, 15 +3V3, 3 VBUS, mostly U3's own +3V3 pins and the inner decoupling ring. These need interactive routing or a local +3V3 pour under U3.

**67 warnings:** ~33 silkscreen (the step was never started — 38 reference designators in `reffix90.json`, the logo and 13 function labels are all still to place), ~21 dangling vias, 4 dangling tracks, 8 library-footprint mismatches that predate this work, 1 copper sliver.

**Not started:** silkscreen, 3D check of the XT30 and USB-C mating directions, Gerber export.