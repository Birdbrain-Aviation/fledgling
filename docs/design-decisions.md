# Design decisions (2026-11-16)

Open items from the operations sheet, now settled or deliberately deferred. None of the schematic or PCB changes below have been made yet; they need KiCad and a DRC run.

## 1. Pyro fuse (F1): keep 5 A, sized from Firewire data

MJG Firewire initiators (the igniter this board is sized for), per the supplier listings:

| Property | Value |
|---|---|
| Bridgewire resistance | 1 ohm +/- 0.2 ohm |
| Maximum no-fire current | 0.30 A |
| Maximum test current | 0.04 A |
| Recommended nominal firing current | 1 A |

The BOM notes an all-fire current of 0.6 A. The listings I found are inconsistent on that figure, so treat it as unconfirmed.

A 2S pack across a 1 ohm bridgewire drives roughly 6.4-7.3 A (the BOM's own estimate) for a few milliseconds until the wire burns open. The fuse has to pass that pulse, so it cannot be sized to the 1 A firing current. A 5 A fast 1206 fuse (Littelfuse 0466005) stays, and it should still open on a sustained short. I did not re-check the fuse's I2t rating against its datasheet.

Continuity checking runs about 60 uA, far below the 0.04 A test limit.

**Still to do:** measure real igniter current on the bench (Estes and nichrome too, if those will be used) before ordering.

## 2. AP63301 feed-forward capacitors: C35 and C36

Both footprints already exist on the board, marked Do Not Populate: C35 (3.3 V buck, across R23) is labelled 56 pF and C36 (5 V buck, across R25 + R26) is labelled 47 pF. Neither is in the BOM.

Those values don't suit this board. They come from Diodes' reference designs, which use a top feedback resistor of about 157-182 kohm. Here the top resistors are much lower: 31.6 kohm for 3.3 V and 52.1 kohm (47 k + 5.1 k) for 5 V. The feed-forward capacitor value goes inversely with the top resistor, so the capacitors need to be larger.

Scaling the Diodes AP63301 evaluation-board values (100 pF with 182 kohm at 3.3 V, and 100 pF with 157 kohm at 5 V, using the same 2 x 22 uF output capacitors as this board):

| Rail | Top resistor | Computed | Choose |
|---|---|---|---|
| 3.3 V (C35) | 31.6 kohm | about 575 pF | 560 pF C0G |
| 5 V (C36) | 52.1 kohm | about 300 pF | 330 pF C0G |

This is a scaled estimate, not a value printed in the datasheet. The crossover frequency in the datasheet equation isn't stated. The same 0603 pad should take these values, but confirm the footprint size in KiCad. Plan to fit them and check load-step response on the bench, and leave them DNP if the output is stable without them.

**Done 2026-11-17:** C35 is now 560 pF DNP (LCSC C55393) and C36 330 pF DNP (LCSC C1664) in the schematic and BOM. Both values are scaled estimates to tune on the bench.

## 3. E220 supply: move to 3.3 V

The E220-900T22D is listed with a 2.3-5.5 V supply range, so 3.3 V is within spec. One third-party manual summary recommends 5 V for best performance, and I couldn't confirm what that means for output power. Plan to check the actual range with a bench range test before flight.

Transmit current is about 110 mA at 5 V, so it will be somewhat higher at 3.3 V. That is well within the 3 A AP63301 on the 3.3 V rail, but it adds transmit bursts to the rail the barometer and IMU use, so watch sensor noise during transmit.

**Still to do:**
- Bench-check E220 output power and range at 3.3 V.

**Done 2026-11-17:** J2 pin 6 now connects to +3V3 in the schematic and on the board (a short stub and via to the +3V3 plane on In2.Cu), and the BOM note is updated. The board's +5V trunk used to run straight through that pad on F.Cu and on to the other 5 V loads, so it was re-routed: it now leaves the existing +5V via at the left of D10, runs on B.Cu under J2 (0.5 mm wide) and returns to F.Cu through a new via to the right of J2. This also pushed some neighbouring B.Cu traces aside. DRC counts did not change from before the edit (see `DRC-2026-11-17.rpt`), but the detour has not been reviewed beyond DRC.

## 4. Telemetry packet format: deferred

No effect on the PCB. Decide when firmware work starts.

## BOM status

The Google Sheet "Fledgling BOM" and `bom/Fledgling_BOM.csv` now carry the decisions above: C35 (560 pF) and C36 (330 pF, shares the C41 part) as DNP feed-forward capacitors, J2 pin 6 noted as 3.3 V, and F1 recorded as 5 A pending a bench measurement. The schematic and PCB were updated on 2026-11-17 (see above).

## 4. Layout fixes, 2026-11-17 (made by Claude with design control delegated by me)

- **J1 pad B8 short.** A GND stitching via at (108.67, 118.97) mm sat on top of USB-C pad B8 (SBU2, unconnected). This caused the short, hole-clearance and front solder-mask bridge errors. Deleting it was tried first, but it was the only via feeding a small B.Cu GND island, so the island went unconnected. The via was moved 0.18 mm right instead, to (108.85, 118.97) mm, which clears the pad and still stitches the island. All three errors cleared.
- **Leftover +5V copper near J2.** After the +5V trunk was re-routed under J2 on B.Cu, about 5 mm of the old F.Cu +5V route (the diagonal past the RADIO label and the short run above C48) was left dangling. It was removed in four segments. C48 pad 1 still connects to +5V through the trunk.
- DRC after these changes (`DRC-2026-11-17-block1.rpt`): 26 errors (25 of them unconnected items, plus the J13 thermal relief), 67 warnings.

## 5. Dangling vias and tracks, 2026-11-17

- **15 pass-through vias removed.** These sat in the middle of a track on one layer with nothing on the other layer, so they did no electrical work: GPIO12, GPIO18, LOADCELL_A-, LOADCELL_EXC (2), U5_BST, QSPI_SCLK, QSPI_SD2, QSPI_SD3, SWCLK, SWD, Net-(D3-A1) (2), Net-(Q1-G) and VSYS. Removing them takes away drill hits and small antenna stubs on the QSPI and SWD lines.
- **Dead stubs removed** at GPIO6 (via plus about 3 mm off J2 pin 1), Net-(Q3-G) (via plus 1.2 mm off Q3), PYRO_BUS (1.1 mm off J8), GPIO2 (0.7 mm off R31) and Net-(D8-DO) (1.5 mm overshoot past a T-junction on B.Cu). Each net was checked before and after: connectivity is unchanged, and unconnected stays at 25.
- **Kept on purpose:** the 5 VBUS vias near J1/D2/U7 belong with the VBUS plane connection (next block), and the long GPIO22 track flagged as dangling is the real route to J13 pin 6. It overshoots the pad slightly, which is cosmetic. Deleting it disconnected J13 pin 6, so it was restored.
- DRC after this block (`DRC-2026-11-17-block2.rpt`): 26 errors (25 unconnected and the J1 shield thermal relief), 47 warnings.

## 6. Plane connections around U3: tried, not fixed (2026-11-17)

Board unchanged in this block. What was found:

- All the copper pours (GND on F.Cu, B.Cu, In1.Cu; +3V3 and VBUS on In2.Cu) are set to **connect through-hole pads only**. So an SMD pad never joins a pour on its own layer. It needs its own via to the inner plane. 12 groups of +3V3 SMD pads have no such via: U3 pins 1/53/54, 11, 20, 38 and 44/45/49, the B.Cu decoupling parts C15, C16, C17, R8, R32 and D7, and J12 pin 2. GND has U3 pin 47 and C11.2. VBUS has J1 A9/B4 and U7 pin 5.
- **Tried: a local +3V3 pour on B.Cu under U3.** It fragmented into islands, created new GND islands, and added 6 thermal-relief errors without reducing the unconnected count. Reverted.
- **Tried: letting the F.Cu and B.Cu GND pours connect SMD pads.** That gave 37 errors and the same 25 unconnected. Reverted.
- **Tried: an automated via placer** (0.55/0.25 mm vias, 0.127 mm clearance, stubs up to 3 mm). It found no legal spot for any of these pads. The U3 area has 0.127 mm signal traces on every layer within about 2 mm of each pad.

**What it needs:** a hand re-route of the U3 power fan-out. Put the +3V3 vias in the gaps between pad rows, or push some GPIO and QSPI traces out of the way. Then add a via next to each B.Cu decoupling cap. A tighter via (0.45/0.2 mm) would make room if the fab supports it. JLCPCB's 4-layer process does. This is the main open layout task.

**Partial fix (same block, second pass):** with smaller 0.45/0.2 mm vias, a legal spot was found next to D7 pad 1 (via at 131.75, 119.3) and next to C17 pad 1 (via at 126.80, 125.83, with a 1.7 mm B.Cu stub). Both now reach the +3V3 plane. To allow this, the board minimums were lowered: via diameter 0.55 to 0.45 mm, drill 0.25 to 0.2 mm, annular ring 0.13 to 0.125 mm. These are within JLCPCB's standard 4-layer capability (0.3 mm via / 0.15 mm drill). Unconnected went from 25 to 23 and errors from 26 to 24 (`DRC-2026-11-17-block3.rpt`). The other 10 +3V3 groups, the 2 GND pads and 3 VBUS pads still need the hand re-route described above.

## 7. VBUS plane and USB shield, 2026-11-17

- **VBUS In2.Cu zone.** It was the same priority (0) as the board-wide +3V3 plane on In2, so the fill between them was ambiguous. It also stopped short of the five VBUS vias around J1, which is why they showed as dangling. The zone now has priority 1 and is enlarged to 104-113 x 116.5-126.5 mm. No +3V3 via or In2 track sits in that area. The five VBUS vias are now on the plane, which removed 5 warnings. J1 A9/B4 and U7 pin 5 are still unconnected: their F.Cu stubs don't reach any of those vias. They need the same short hand-routed hop as the U3 pads.
- **J1 shield pads.** The four GND shield pads of the USB-C connector are set to a solid zone connection instead of thermal relief. This fixes the "1 spoke to an isolated island" error and gives the shield a stronger ground. Soldering those pads needs a little more heat.
- DRC after this block (`DRC-2026-11-17-block4.rpt`): 23 errors (all unconnected items), 42 warnings.
