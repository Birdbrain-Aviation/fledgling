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

**Still to do:** change C35 and C36 values in the schematic, and add both to the BOM.

## 3. E220 supply: move to 3.3 V

The E220-900T22D is listed with a 2.3-5.5 V supply range, so 3.3 V is within spec. One third-party manual summary recommends 5 V for best performance, and I couldn't confirm what that means for output power. Plan to check the actual range with a bench range test before flight.

Transmit current is about 110 mA at 5 V, so it will be somewhat higher at 3.3 V. That is well within the 3 A AP63301 on the 3.3 V rail, but it adds transmit bursts to the rail the barometer and IMU use, so watch sensor noise during transmit.

**Still to do:**
- J2 pin 6 currently connects to +5V. Rewire it to +3V3 in the schematic and reroute it on the board. The 5 V trace to it currently runs about 45 mm along the bottom edge.
- Update the BOM note ("VCC 5 V") for J2.

## 4. Telemetry packet format: deferred

No effect on the PCB. Decide when firmware work starts.

## BOM status

The Google Sheet "Fledgling BOM" and `bom/Fledgling_BOM.csv` now carry the decisions above: C35 (560 pF) and C36 (330 pF, shares the C41 part) as DNP feed-forward capacitors, J2 pin 6 noted as 3.3 V, and F1 recorded as 5 A pending a bench measurement. The schematic and PCB have not been changed yet.
