---
title: "StarCraft II profiles and portraits"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "Reading a player's profile on Sunken, finding the portrait in it, turning a portrait ID into a cell on one of 17 portrait sheets, looking up character names, and what a client can change."
sources:
  - name: "Superiority, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/superiority"
    note: "the profile read request and response, the PORT value, the portrait catalog, the sheet layout and the rate limits"
  - name: "StarCraft II 5.0.16.97563"
    note: "the Profile and Toon command lists, the name lookup, the ladder commands and the write requests, from the client's own code"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-24/25: profile reads, the block format, the other cosmetic keys and name lookups"
---

**Every StarCraft II player shows a portrait.** A chat client finds it in one of two places: in the player's [presence](/bnet2/sc2-presence/), or by reading their profile. The profile read is a [Sunken](/bnet2/sunken/) record on the Profile slot (14).

Marks on this page: ✅ **confirmed live** (Invigoration, 2026-09-24/25), ⚠️ from **one source** (named) or **inferred**, 📖 **from the client** (the game's own code, not tried live), 🛑 **unknown**. The notation (`u(n)`, `blob`, `opt`) is the one on [the chat page](/bnet2/sunken-chat/#notation).

## Where a portrait comes from

| Source | What it gives | Used for |
|---|---|---|
| Presence field `0x10013` | The portrait directly: sheet u16, cell u16 | A chat member's portrait, when it's there |
| Presence field `0x10014` | A profile address: label u32, ID u64 | Reading the profile when there's no `0x10013` |
| A friend record | A profile address | Reading a friend's profile |

**For chat members,** use `0x10013` when the presence has it, and read the profile otherwise. **For friends,** read the profile, and fall back to `0x10013`. That's the order Superiority uses. ⚠️ Superiority

**Every profile address seen live had the label `0xCAFEBABE`.** ✅ Confirmed live. Don't rely on that; pass whatever label you're given.

## Profile read: the request

Profile slot 14, command 0. ✅ Confirmed live; layout from Superiority.

```
client hash    u(32)     0
request ID     u(32)     a new number; every answer carries it back
label          u(32)     the profile address
record ID      u(64)
flags          u(5)      0: no reserved flag, the "All" selection, no reader
path length    u(8)
path           raw(path length)
align
```

**The portrait is under path `[0x14]`.** ⚠️ Superiority. Other paths aren't documented, which is why wins and ladder rank are still [open questions](/bnet2/open-questions/).

**Byte example**, request 1, address `0xCAFEBABE` / `0x12345678`, path `[0x14]`:

```
c0 06 00 00 00 00 00 00 00 c9 5f d7 57 06 00 00 00 02 46 8a cf 00 01 14
```

`c0 06` is the route. The rest follows the layout above. Built here; the same builder reproduces Superiority's own retail-layout test vector (request 24, path `[4]`) byte for byte.

## Profile read: the answers

The answers come back on the same slot and command, each carrying the request ID. ✅ Confirmed live; layout from Superiority.

```
kind           u(2)
  0 Start:     packet count u(32), record type u(32)
  1 Block:     length u(14) (at most 8192), align, that many bytes
  2 Failure:   error code u(16)
  3 Cache:     nothing ("you already have it")
request ID     u(32)
align
```

- **Start** says how many Blocks will follow. **Start with 0 packets, Failure and Cache** all mean there's no data to read.
- **Blocks** carry the data. Join them in order until you've had the count Start gave.
- **A Block with no Start before it** is the whole answer on its own. ⚠️ Superiority
- In Superiority's retail example, Start announced 1 packet of record type 6145 (`0x1801`). What record types mean is 🛑 unknown.
- A live read of path `[0x14]` came back as a single 1,566-byte Block. ✅ Confirmed live

## The block

**The data is a run of entries, each a 4-character key and a number.** ✅ Confirmed live

```
06 14 f0   k k k k   01   value
```

- `k k k k` is the key, 4 ASCII characters, such as `PORT`.
- The `14` matches the path that was read. ⚠️ Inferred: entries are keyed under their path.
- What `06`, `f0` and `01` mean is 🛑 unknown.
- **Search for the whole 8-byte key**, for example `06 14 f0 50 4f 52 54 01` for `PORT`. It can be anywhere in the data.

### The packed number

The value is a variable-length number. ⚠️ Superiority

```
marker = first byte
if marker = 0:  value = 0
else:
    n     = (marker >> 4) - 11        # 0 to 4 more bytes; anything else is invalid
    value = marker AND 0x0F
    for each of the next n bytes:  value = (value << 8) OR byte
    value = value >> 1
```

The low bit dropped by the last shift is 🛑 unknown. Markers from `0x01` to `0xAF` weren't seen and aren't handled.

**Worked examples:**

| Entry | Marker | Value |
|---|---|---|
| `06 14 f0 50 4f 52 54 01 f1 5f ce 10 68` | `f1`: 4 more bytes | `0x1_5fce1068 >> 1` = **2951153716**, the default portrait |
| `06 14 f0 50 4f 52 54 01 eb ae 83 64` | `eb`: 3 more bytes | `0xb_ae8364 >> 1` = **97993138**, sheet 0 cell 15 |
| `06 14 f0 49 43 4f 4e 01 00` | `00` | **0**, for key `ICON` |

The first two are Superiority's worked examples, and the rule was run here on all three.

### Other keys in the block

A live read of path `[0x14]` held **122 keys**, each with a packed number, in ASCII order. **None of their meanings is confirmed.** ✅ Confirmed live that they're there

| Key | Value seen | Guess |
|---|---|---|
| `PORT` | a portrait ID | The portrait. ⚠️ Superiority |
| `BADG` | a large ID | A badge. 🛑 |
| `EMOT` | 0 | Emoticons. 🛑 |
| `CSKI` | a large ID | A console skin. 🛑 |
| `Anim` | a large ID | An animated portrait. 🛑 |
| `GRBn` | a large ID | A banner. 🛑 |
| `ICON` | 0 | An icon. 🛑 |
| `Lcns` | 0 | 🛑 |
| `SPRY` | a large ID | A spray. 🛑 |
| `SpUD` | a large ID | 🛑 |
| The other 39 keys starting `P`, 36 starting `T` and 37 starting `Z` | large IDs | One per unit or building of each race, such as `PZlt`, `PPrb`, `TMar`, `TScv`, `ZLng`, `ZOvl`: probably each one's chosen skin. ⚠️ Inferred |
| `PCSK`, `TCSK`, `ZCSK`; `PRBn`, `TRBn`, `ZRBn`; `PVOI`, `TVOI`, `ZVOI`; `PCAL`, `TCAL`, `ZCAL` | large IDs | Per-race versions of something: console skin, banner, voice? 🛑 |

## From portrait ID to picture

**A catalog maps each `PORT` ID to a sheet and a cell.** Superiority's catalog has **573 entries**, each `(portrait ID, sheet, cell)`. ⚠️ Superiority. Some entries, for checking a copy:

| Portrait ID | Sheet | Cell |
|---|---|---|
| 905359 (the smallest) | 5 | 8 |
| 97993138 | 0 | 15 |
| 2951153716 (the default) | 0 | 0 |
| 4288809372 (the largest) | 10 | 28 |

An ID that isn't in the catalog has no known picture. Show the default, or nothing.

**Presence field `0x10013` skips the catalog:** it already holds the sheet and the cell, as two big-endian u16s. For example `00 00 00 0f` is sheet 0, cell 15.

### The sheets

| | |
|---|---|
| Sheets | **17**, numbered 0 to 16 |
| Each sheet | 6 × 6 cells, **152 px** square, so 912 × 912 px |
| Cell order | Row by row: row = cell ÷ 6, column = cell mod 6 |
| Cell's position | x = column × 152, y = row × 152 |

So sheet 0, cell 15 is row 2, column 3, at (456, 304). ⚠️ Superiority

**The portraits are Blizzard's art.** Superiority packages them as 17 sheet images. This site doesn't host or link them.

## Being polite: rate limits

Superiority limits profile reads like this, and Invigoration does the same. ⚠️ Superiority

- **Read each profile address at most once a session**, and remember every answer, misses included.
- **At most 16 reads unanswered** at a time.
- **A token bucket**: 40 reads a second, with bursts of up to 20.
- **Only read what you'll show:** chat members with no `0x10013`, and friends.

Invigoration also gives up on a read that's had no answer after 30 seconds, so a lost answer can't hold a slot forever. How strict Battle.net itself is isn't known. 🛑

## Profile commands

The Profile slot's full command list, from the game's `CommandID` enum: 📖

| Cmd | Name | Notes |
|---|---|---|
| 0 | Read | [above](#profile-read-the-request) ✅ |
| 1 | AddressQuery | a player's profile address, from a presence ID, character name, account ID or handle |
| 2 | ResolveToonHandleToName | [names for character handles](#names-for-character-handles) ✅ |
| 3 | ResolveToonNameToHandle | the reverse |
| 4 | SettingsAvailable | server → client: where the account's, game's and character's settings records are |
| 5 | ChangeSettings | client → server: string settings |
| 6 | S2SinglePlayerStatEvents | |
| 7 | S2ChangeLeagueShowcase | which league badges the profile shows |
| 8 | SendStatsUIEvent | |

## Names for character handles

Profile slot 14, command 2, both ways. Club member lists and some other records give characters as handles; this turns up to 32 of them into names. ✅ Confirmed live

**Request:**

```
count   u(6)
        then per character: program u(32), region u(8), realm u(32), ID u(64)
align
```

**Reply** (a scrambled struct, see [clans and groups](/bnet2/sc2-clubs/#scrambled-structs)):

```
filler  15 bits
count   u(6), then per character:
  tag       opt: u(5) byte count, align, bytes     the clan tag
  handle    program u(32), region u(8), realm u(32), ID u(64)
  name      opt: region u(8), program u(32), realm u(32), u(7) byte count − 2, align, bytes
  result    u(16)   0: found
align
```

The name comes back with its code, e.g. `Raynor#123`, and the clan tag without brackets. ✅

## Changing a profile

**There's no general "write my profile" request.** 📖 What a client can change:

| What | Where | Request |
|---|---|---|
| **Portrait** (and other unlockables) | Toon slot, command 11; the answer is command 12 | the unlockable's category (`PORT` for portraits), its ID (the number stored after `PORT`), the 40-byte handle of the unlock-definition file it comes from (one of those listed at sign-in), and a token |
| **Motto** | Toon slot, command 9 | the text: u(12) byte count, align, bytes |
| Account, game and character settings | Profile command 5 | a list of (index, text) pairs |
| League showcase | Profile command 7 | up to 3 team profiles and ladder IDs |
| Character name | Toon commands 14 and 16 | |

Which unlock-definition file to name is the part to confirm before choosing a portrait live. 🛑

## Wins, league and rank

They aren't in the profile paths a chat client reads. They come from the **Ladder** service: 📖

| Cmd | Name | Gives |
|---|---|---|
| 0 | GetAssignment | league (Bronze to Grandmaster), division, tier, and a scaled rating |
| 9 | GetRankings | rank, and game data as key/value pairs: wins, losses, points |
| 10 | GetMembers | a division's members |

**Which Sunken slot the Ladder service is on isn't fixed in the client's code**: it's read from the service object at run time. It's probably one of the slots nothing else uses (2, 6, 7 or 9). One capture of the game opening a profile would settle it. 🛑

