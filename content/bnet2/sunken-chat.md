---
title: "StarCraft II chat on Sunken"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "Keeping the RC4 stream going, and the Sunken records for chat, whispers, joining channels and keepalives."
sources:
  - name: "novares"
    note: "the main source for this page"
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
    note: "independent source for the bit order, the route and the RC4 switch"
  - name: "Superiority, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/superiority"
    note: "the whisper record's other target types"
---

Unless a line says otherwise, everything on this page comes from novares and is ⚠️ single source. Lines marked ✅ agree with [SC2Docs](https://superiority-sc2docs.pages.dev/) as well. The byte examples were rebuilt here from the rules on this page and matched the source's bytes exactly.

This page picks up where [StarCraft II: signing in](/bnet2/sequences/starcraft-ii-logon/) ends: the Sunken connection is resumed, encryption is on and the client is in a channel. How records are packed into bits is on [Sunken records](/bnet2/sunken/).

## Keeping RC4 going

Each direction has **its own RC4 state**: a 256-byte table and two counters, `i` and `j`. ✅ Verified. Once encryption is on, never rekey; just keep running each state.

```
for each byte:
    i = (i + 1) AND 255
    j = (j + table[i]) AND 255
    swap table[i] and table[j]
    out = in XOR table[(table[i] + table[j]) AND 255]
```

- **Decrypt each received byte exactly once**, and add it to a buffer of plaintext.
- **Parse only whole records** from that buffer, and keep any partial record for the next read.
- **Encrypt what you send with the outgoing state**, which is independent of the incoming one.

## Writing bits

Records have no length field; the schema says where each one ends. ✅ Verified. Bits fill each byte from bit 0 upwards. A value that crosses a byte boundary is split, and **its high-order part goes first**. ✅ Verified

```
writeBits(width, value):
    remaining = width
    while remaining > 0:
        offset = position MOD 8
        take   = min(remaining, 8 - offset)
        chunk  = (value >> (remaining - take)) AND ((1 << take) - 1)
        output[position DIV 8] |= chunk << offset
        remaining -= take
        value     &= (1 << remaining) - 1
        position  += take
```

Each record starts with its **route**: command (6 bits), a service flag of 1 (1 bit), then the service slot (4 bits). ✅ Verified. The payload follows straight after, and the record is zero-padded to a whole byte.

`blob(n, text, minimum)` is written as the UTF-8 length **minus `minimum`** in `n` bits. Skip to the next byte boundary, then write the bytes. Use 64-bit arithmetic for 64-bit fields.

## Service slots

| Slot | Service | Slot | Service |
|---|---|---|---|
| 1 | Connection | 10 | S2 master (seasons) |
| 3 | Friends | 11 | Cache |
| 4 | Presence | 12 | Party |
| 5 | Chat ✅ | 13 | S2 maps |
| 8 | Achievements | 14 | Profile |
| | | 15 | Toon (character) |

## Records the client sends

**A message or whisper holds at most 255 characters and 1,020 UTF-8 bytes** (the `blob(10, text, 0)` below). A longer one can't be encoded; cut it or split it before sending. ✅ Confirmed live

**StarCraft II chat has no slash commands.** Whatever a client handles itself is up to it: a whisper is its own record, and there's no emote record, so Invigoration sends `/me text` as `*text*`. Anything else starting with `/` is simply posted as chat. ✅ Confirmed live

| Record | Slot / command | Payload, in order |
|---|---|---|
| Channel message | 5 / 11 | `blob(10, text, 0)`, channel index (3 bits) |
| Whisper to a character | 5 / 19 | target type `1` (3), region (8), program `0x5332` `S2` (32), the character's realm (32), `blob(7, name, 2)`, `blob(10, text, 0)` |
| Whisper to a presence | 5 / 19 | target type `0` (3), presence ID (32), `blob(10, text, 0)` ⚠️ Superiority |
| Whisper to an account | 5 / 19 | target type `3` (3), account ID (32), `blob(10, text, 0)` ⚠️ Superiority |
| Whisper to a character handle | 5 / 19 | target type `5` (3), program (32), region (8), realm (32), character ID (64), `blob(10, text, 0)` ⚠️ Superiority |
| Public channel list | 5 / 21 | nothing |
| Join a public channel | 5 / 0 | type `2` (2), locale `0x656E5553` `enUS` (32), channel ID (16), a new join token (32) |
| Join a club's chat | 5 / 0 | type `3` (2), `0` (16), club ID (32), a new join token (32). See [clans and groups](/bnet2/sc2-clubs/#clan-chat) ✅ |
| Ping | 1 / 10 | present `1` (1), timestamp high 32 bits, timestamp low 32 bits |
| Pong | 1 / 12 | the ping's present bit and timestamp, copied |

**Public channel IDs:** General **1033**, Trade **1034**, Help **1035**.

**A channel index is 3 bits** (0 to 6), ✅ Verified. After joining, use the index the server gives you in its join result, not one you picked.

**Ping every 30 seconds**, with a timestamp in microseconds. The server echoes it back, so use one steady clock. Answer the server's pings straight away.

### Byte examples (before encryption)

| Record | Bytes |
|---|---|
| `hello` to channel index 0 | `4b 05 05 68 65 6c 6c 6f 00` |
| Join General (1033), join token 1 | `40 75 2b 72 aa 13 20 09 00 00 00 01` |
| Whisper `hello` to `Test`, region 1, realm 1 | `53 0d 01 00 01 4c 32 00 00 00 01 02 54 65 73 74 01 01 68 65 6c 6c 6f` |

Take the first. `4b` holds command 11 (bits 0–5), the service flag (bit 6) and the top bit of slot 5 (bit 7, a 0). The low 3 bits of `05` finish the slot. The 10-bit text length, 5, comes next, high part first: five 0 bits fill the rest of that byte, and the low five bits (`00101`) start the next `05`. Then the record aligns to a byte, and `hello` follows. The final `00` holds the 3-bit channel index 0 and its padding.

## Records the server sends

Every record that arrives **must** be decoded, even ones a chat client doesn't care about, because only its schema says where the next record starts. **If a record isn't in your decoder, stop.** You can't skip it by guessing.

### Notation

| Notation | Meaning |
|---|---|
| `u(n)` | An unsigned `n`-bit number |
| `s(n)` | A signed `n`-bit number |
| `bool` | One bit |
| `align` | Skip to the next byte boundary |
| `blob(n, min)` | An `n`-bit length plus `min` (0 if not given), align, then that many bytes |
| `name` | `blob(7, 2)`, as UTF-8 |
| `raw(n)` | Align, then `n` bytes |
| `skip(n)` | Skip `n` bits |
| `opt{ … }` | A presence bit, then the contents only if it's 1 |
| `addr` | `skip(96)`, a record address |
| `toonHandle` | `skip(136)` |
| `cacheHandle` | `raw(40)` |
| `fixed(N)` | Skip ahead to byte `N` of the record (stop if already past it) |
| **stop** | The record is malformed. Stop reading the stream. |

### Chat records

**Chat 11: a message**

```
sender handle   u(32)
text            blob(10) as UTF-8
channel index   u(3)
align
```

**Chat 1: people joining and leaving**

```
end of initial list   bool
channel index         u(3)
count                 u(6) + 1
repeat count times:
    kind u(2)
      0  left:     handle u(32), u(16)
      1  joined:   handle u(32), presence ID u(32), MemberStatus
      2  changed:  handle u(32), MemberStatusSingle
      3  stop
align

MemberStatus:        u(3) entries of MemberStatusSingle; keep the last character found
MemberStatusSingle:  arm u(3)
      0  other u(8): 0 → u(8); 1 → u(16) count, then that many u(32); else stop
      1  u(2), opt{ u(2) }, bool
      4, 6  bool
      5  the character: region u(8), program u(32), realm u(32), name
      7  nothing
      2, 3  stop
```

Use the character's name from arm 5 as the member's display name, keyed by their handle.

**Chat 27: the result of joining**

```
if bool (it failed):
    reason u(16), opt{ u(4) }, opt{ u(32) }       → done
u(32)
channel index   u(3)          (above 6: stop)
skip(64), u(4)
channel name    opt{ skip(45); identity u(2):
                     0 → blob(7, 2) as UTF-8
                     1, 2 → skip(48), no name
                     3 → stop }
opt{ skip(24); p = u(3) (at most 4); skip(p × 32 + 32);
               r = u(3) (at most 4); skip(r × 32 + 32) }
opt{ u(32) }
opt{ u(32) }
```

**Chat 22: public channel list.** `u(37)`, then `u(6)` entries of `u(8) u(16) u(24)`, then `u(16)`, align.

**Chat 24: channel categories.** `u(6)` entries of `u(8) u(16) u(16)`, then `bool`, align.

**Chat 26: channel member counts.** `bool`, `skip(27)`, `opt{ s(32) }`, then `u(6)` entries of `skip(23) u(32) u(16) bool`, align.

**Incoming whispers aren't documented yet.** 🛑 Unknown

### Connection records

| Command | Layout |
|---|---|
| 1 | Disconnect: error code `u(16)`, align |
| 3 | `u(32)`, align |
| 10 | Ping: `opt{ raw(8) }` timestamp, align |
| 11 | `if u(1) = 1: u(32), u(32)`, align |
| 12 | Pong: `opt{ raw(8) }` timestamp, align |
| 13 | Message frame (below) |
| 14 | Game site info: `skip(48)`, align, then `u(7)` entries of `blob(6)` and `opt{ align, skip(48) }`, align |

**Message frame (Connection 13):**

```
size          u(14)            (above 14336: stop)
data          raw(size)
frame type    u(8)
count         u(6)             (above 32: stop)
repeat count times: kind u(8)
    0  size u(32), encoding u(32)
    1  name u(32), hash u(32), command u(6), opt{ label u(32), epoch u(32) }
    2  type u(7), arm u(3), n u(11) (above 1024: stop), then skip n × width
          width by arm: 0–2 → 32, 3 → 72, 4 → 64, 6 → 136, 5 or 7 → stop
    3  id u(32), reply bool
    5  label u(32), type u(32), epoch u(32)
    6  result u(16), message blob(14) as UTF-8
    7  command u(1) + 1
    8  seconds u(32)
    9  sequence ID u(16), more bool
    4 or anything else: stop
align
```

### Character (Toon) records

**Toon 0: character list.** `u(6)` entries of `name`, `s(32)`, `skip(3)`, flags `u(32)`, `addr`, realm `u(32)`; align. The first entry with a name is the character to use.

**Toon 6: character selected.** `addr`, `toonHandle`, realm `u(32)`, `s(32)`, `name`, align.

**Toon 10: welcome.**

```
u(32)
u(4) entries of: cacheHandle, u(32)
bool, u(32), skip(31), u(32), blob(6), skip(128)
u(3) entries of: u(32), u(32), skip(1), u(8), then u(5) × u(32)
u(8) entries of: skip(4), cacheHandle
skip(3), u(16), blob(13), blob(13), s(32)
align
```

**Toon 13: billing update.** `u(32)`, `skip(19)`, `opt{ s(32) }`, `skip(28)`, `opt{ u(32) }`, `u(8)`, align.

**Toon 14:** align.

### Presence records

| Command | Layout |
|---|---|
| 0 | `skip(19)`, `bool`, `u(32)`, `u(32)`, `blob(11)`, `skip(11)`; then three lists, each `u(4)` entries, of `u(32)`, `u(32)` and `u(16)`; `opt{ bool, u(32) }`, `u(8)`, align |
| 1 | `u(7)` entries of: `skip(3)`, `if u(1) = 0: u(16)`, `bool`, `u(8)`, `u(32)`; align |
| 2 | `bool`, align |
| 3 | `u(6)` entries of `u(32) u(64)`; align |
| 4 | `u(4) + 1` entries of `toonHandle`; align |
| 10 | result `u(16)`, align |

### Friends records

```
AccountName:      blob(8), blob(8)
CustomMessage:    s(32), blob(9)
Character:        region u(8), program u(32), realm u(32), name
```

| Command | Layout |
|---|---|
| 6 | `u(7)` entries of `Character`, `addr`, `u(32)`; `bool`, align |
| 30 | `opt{ bool }`, then `u(7)` friendship updates (below), align |
| 31 | `opt{ bool }`, then `u(7)` entries of: `skip(9)`, `u(32)`, `opt{ blob(7) }`, `skip(20)`, `opt{ AccountName }`, `u(32)`; align |
| 33 | `u(7)` entries (above 64: stop) of `u(1)`, `Character`; `opt{ bool }`, align |

A **friendship update** is `op u(2)`:

- **0 or 2:** a friend, `arm u(2)`:
  - **0, a character:** `toonHandle`, `blob(7, 2)`, `addr`, `opt{ blob(9) }`
  - **1, an account:** `u(32)`, `opt{ AccountName }`, `opt{ blob(7) }`, `addr`, `opt{ CustomMessage }`, `opt{ blob(9) }`, `s(32)`, `skip(64)`, `u(32)`
  - **2, presence:** `u(32)`, `opt{ CustomMessage }`, `s(32)`
  - **3:** stop
- **1:** removed. `u(1)`: 0 → `u(32)`, 1 → `toonHandle`
- **3:** stop

### Other records

| Slot / command | Layout |
|---|---|
| Cache 9 | `u(6)` entries of: `skip(23)`, align, handle `raw(40)`, published `s(32)`. Then token `u(32)`, total `u(16)`, offset `u(16)`, align |
| Party 0 | `fixed(18)`, align |
| Profile 4 | `u(2)`, `blob(6)`, `addr`, align |
| S2 maps 49, 50, 57 and the other club records | Slot 13 is the **club** service. Command 50 is a list, not a fixed 38 bytes. Every layout is on [clans and groups](/bnet2/sc2-clubs/) ✅ |
| S2 master 27 | Current season (below) |

**Current season (S2 master 27):**

```
if bool: skip(16), done
skip(1)
m = u(7)    (above 100: stop);  skip m × 425
l = u(9)    (above 448: stop);  skip l × 189
skip(42), opt{ skip(32) }
skip(16), opt{ skip(16) }
skip(89)
opt{ skip(16) }, opt{ skip(32) }, opt{ skip(16) }
skip(64)
c = u(9)    (above 448: stop);  c entries of: skip(149), opt{ skip(32) }
```
