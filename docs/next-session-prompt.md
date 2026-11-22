# Prompt: re-place and re-route Fledgling

You have full design control over my KiCad board "Fledgling". Your goal is to re-place parts so the board can be routed completely, then route it to **0 DRC errors and 0 unconnected items**. Ask me only before something that can't be undone. Otherwise decide, and log every decision.

## Where things are
- KiCad 10.0.6 project on my PC: `C:\Users\homeoffice\Desktop\Fledgling\` (`Fledgling.kicad_pcb`, schematic sheets `Fledgling/IO/Power/Sensors.kicad_sch`).
- GitHub repo: `Birdbrain-Aviation/fledgling`. Board files are in `hardware/`, notes in `docs/`. Read `docs/design-decisions.md` and `docs/remaining-work.md` first.
- **All traces and vias have been cleared** (2026-11-22). Parts, zones and the board outline are in place, and 223 connections are unrouted. The previous fully routed attempt is in `hardware/archive/Fledgling_routed_2026-11-21.kicad_pcb` (on my PC it's `Fledgling_routed_backup_2026-11-22.kicad_pcb`). It failed: 22 power pads around the RP2350 had no room for a via.

## Board facts
- 90 x 40 mm, 4 layers. F.Cu: signals plus a GND pour. In1.Cu: GND plane. In2.Cu: +3V3 plane, with a VBUS island (priority 1, about 104-113 x 116.5-126.5 mm, by the USB-C). B.Cu: signals plus a GND pour.
- **All pours connect to through-hole pads only.** Every SMD power or GND pad needs its own via (or a track to one) to reach its plane. This is the main thing that broke the last layout.
- Rules: 0.127 mm minimum clearance and track width. Power net class: 0.5 mm tracks. Pyro net class: 0.3 mm clearance. Copper-to-edge 0.3 mm. Hole-to-hole 0.3 mm (0.25 mm is acceptable to JLCPCB).
- **Vias: 0.45 mm diameter / 0.2 mm drill.** This is JLCPCB's free tier. A diameter of 0.4 mm or less costs extra, and drills under 0.2 mm aren't standard on multilayer. Board minimums are already set to allow 0.45/0.2.
- Fab target: JLCPCB 4-layer.

## Don't move or change
- Edge connectors and their orientation: USB-C J1 (left edge), XT30 J5/J9 (right edge, pin 1 = GND, pin 2 = +), terminal blocks J6/J7/J8/J10 (top edge), JST connectors along the bottom edge (J2 radio, J12 OLED, J14 load cell, J11 servo), J13 header, J3 SWD.
- Mounting holes MH1-MH4, Edge.Cuts, the silkscreen label/logo footprints (LBL1, LBL2, LOGO1). Re-check label clearance after moving parts.
- Schematic and nets, unless a change is truly needed. Ask first if it is.
- Decisions already made: E220 (J2 pin 6) on +3V3, C35 560 pF and C36 330 pF (both DNP), pyro fuse 5 A.

## What went wrong last time (the area to fix)
The RP2350 (U3, QFN-60, near (122, 124) mm) was boxed in. QSPI lines to the flash (U1), the +1V1 regulator network (L1, VREG_LX, VREG_AVDD) and GPIO fan-out covered both outer layers. That left no legal 0.45/0.2 via spot for U3's +3V3 pins (1/53/54, 11, 20, 38, 44/45/49), the B.Cu decoupling parts (C15, C16, C17, R8, R32, D7), U3.47/C11.2 GND, or the USB VBUS pads (J1 A9/B4, U7 pin 5). Rip-up scripts and Freerouting both failed at that placement.

## Approach
1. **Placement first.** Read Raspberry Pi's "Hardware design with RP2350" guide and copy its minimal-design layout ideas.
   - Move U1 (flash) and its QSPI path so it doesn't wall off U3.
   - Move the +1V1 regulator parts (L1 and its caps) to one side with a tight loop.
   - Put one decoupling cap per power pin on B.Cu under or next to its pin, each with its own via.
   - Leave a free ring around U3 for vias.
   - Spread anything else that is crowded, such as the pyro FETs and the buck converters, if it helps.
2. **Plan the power vias before routing any signals.** Place a +3V3 via next to every U3 +3V3 pin and decoupling cap, a GND via for every SMD GND pad, and VBUS vias at J1/U7 inside the VBUS island. Check that each via lands on its plane.
3. **Route in this order:** USB D+/D- as a pair (90 ohm differential, short, no vias if possible), crystal XIN/XOUT, then the regulator/power loops, then QSPI (short, matched-ish), then the remaining GPIO and signals. The Pyro net class keeps 0.3 mm clearance.
4. **Stitch the GND pours** so there are no isolated islands, with GND vias in any pocket of pour.
5. **Finish.**
   - Fix silkscreen overlaps.
   - Final DRC must show 0 errors and 0 unconnected. Library-mismatch warnings are fine.
   - Export Gerbers and drill files to `fab/`.
   - Re-render `docs/images`, then update the README, `remaining-work.md` and `design-decisions.md`.

## How to work with the tools (lessons from last time)
- Computer use: request **"PCB Editor 10.0 (standalone)"** and **"KiCad 10.0"**.
  - `computer_open_application` on the PCB Editor often spawns a **blank second PCB Editor** about 10 s later, in front of the real one. Wait, check the title bar says "Fledgling — PCB Editor", and close the blank one (its window title is just "PCB Editor") before clicking.
  - File dialogs only accept typing in the File name box. Pick files by clicking them in the list.
- Fast loop: edit `Fledgling.kicad_pcb` with a script, write it to the PC, then in KiCad use **File > Revert** to reload. Run **Inspect > Design Rules Checker** with "Refill all zones" ticked. Use **Save...** in DRC to write a report you can stage and read.
- `device_commit_files` once wrote a **stale cached copy** when the same output filename was reused. Always use a new, unique staged filename. After writing, stage the file back and compare its md5.
- Freerouting is an option *after* re-placement:
  - Use v1.9.0 under `xvfb-run`. v2.1 ignores its pass limit and timeout.
  - Export Specctra DSN from KiCad. Notch the In2 +3V3 plane polygon around the VBUS island, and limit the via list to `Via[0-3]_450:200_um`.
  - After importing the session, check via sizes. Last time the imported vias had a 0.075 mm annular ring.
  - Running it needs my approval in that session.
- Only keep a change if KiCad's DRC confirms it is better. Commit and push to GitHub after each verified stage. Commit messages end with the session attribution lines.

## Deliverable
A fully routed Fledgling board with 0 DRC errors and 0 unconnected, saved on my PC and pushed to GitHub. Include fab-ready Gerbers and a short summary of every part move and why.
