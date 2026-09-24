---
title: "Sunken records"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "StarCraft II's native service connection: records packed bit by bit, with no length field."
sources:
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
---

Every fact on this page comes from one source, so it is all ⚠️ single source until checked elsewhere.

Sunken is a plain TCP connection, separate from Front. After sign-in hands over to it, it's encrypted with **RC4, with a separate key state for each direction**. Once decrypted, it's a stream of bit-packed records.

## Reading bits

The decoder keeps one cursor for the whole record and reads **each byte from bit 0 (lowest) to bit 7**, then moves to bit 0 of the next byte. A value can cross a byte boundary. When it does, the bits read first become the **higher-order** part of the value.

```
read(width):
    value = 0
    while width > 0:
        take  = min(width, bits left in current byte)
        chunk = (current byte >> current bit) & ((1 << take) - 1)
        value = (value << take) | chunk
        advance cursor by take; width -= take
```

## The route: what every record starts with

| Bits | Field | Meaning |
|---|---|---|
| 6 | Command | The command within the service. |
| 1 | Service flag | `1`: a service record follows. `0`: a command response. |
| 4 | Service slot | Only when the flag is `1`. Which service, such as slot 5 for Chat. |

So a service record's route is **11 bits**, and its payload starts at bit 3 of the second byte.

**A command response** has no slot and no payload: 6 command bits, the zero flag, then a **9-bit result**. That's exactly 16 bits, always two bytes.

## Where a record ends

**Records have no length field.** The route, together with the direction, selects the payload's schema, and decoding that schema moves the cursor to the end of the payload. Then:

1. Skip **zero bits** up to the next byte boundary. They must be zero.
2. The next byte starts the next record.

| Payload part | Bits it uses |
|---|---|
| Fixed-width value | The width given by its schema |
| Array, string or blob | A count, then that many elements or bytes. Strings and blobs may first align to a byte. |
| Optional value | One presence bit, then the value if present |
| Choice | A selector, then the chosen value |
| Structure | Each member in turn, including any filler bits |

**Counts are stored relative to their minimum.** A count allowed to be 1 to 64 is stored as the count minus 1, in 6 bits. A count with a fixed value uses no bits at all.

Because the schema decides where a record ends, **a client can't skip a record it doesn't understand**. StarCraft II's schemas are compiled into the game, using Blizzard's BSN format. SC2Docs documents about 592 of these types.

## Worked example: leaving a chat channel

The client sends Chat command 2, `LeaveRequest`, for channel 6. It's two bytes: `42 35`.

| Where | Bits | Value | Meaning |
|---|---|---|---|
| Byte 0, bits 0–5 | 6 | 2 | Command 2 |
| Byte 0, bit 6 | 1 | 1 | A service slot follows |
| Byte 0, bit 7, then byte 1, bits 0–2 | 1 + 3 | 0 then 101 = 5 | Slot 5: Chat |
| Byte 1, bits 3–5 | 3 | 110 = 6 | `channelIndex` = 6 |
| Byte 1, bits 6–7 | 2 | 00 | Padding to the byte boundary |

Route (11 bits) + payload (3 bits) + padding (2 bits) = 16 bits = 2 bytes.

For the records a chat client sends and receives, and the layouts of the other records that arrive alongside them, see [StarCraft II chat on Sunken](/bnet2/sunken-chat/).
