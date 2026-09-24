---
title: "StarCraft II presence"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "The Sunken presence records, the fields they carry, how a friend or chat member is tied to a presence, and how to tell online, away, busy and in game."
sources:
  - name: "Superiority, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/superiority"
    note: "the presence decoders, the avatar, profile, character, account and status fields, and the status rules"
  - name: "novares"
    note: "independent source for the bit layouts of Presence 0 and 1"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-24: the field table, the game account, BattleTag and game-account name fields, and friends coming online"
---

**Presence is how StarCraft II learns who is online, and what they're doing.** It arrives on [Sunken](/bnet2/sunken/) in the Presence slot (4), alongside chat. The bit layouts of every presence record are on [StarCraft II chat on Sunken](/bnet2/sunken-chat/#presence-records). This page explains the two that carry values.

Marks on this page: ✅ **confirmed live** (Invigoration, 2026-09-24) or from two sources, ⚠️ from **one source** (named) or **inferred**, 🛑 **unknown**. The notation (`u(n)`, `blob`, `opt`) is the one on [the chat page](/bnet2/sunken-chat/#notation).

## How it works

Presence never names anyone. Battle.net first announces a table of **fields** (Presence 1). After that, each **update** (Presence 0) carries a presence ID and new values for some of those fields, by handle. **Who a presence belongs to is worked out from the values it holds**: an account ID, a character handle or a profile address. ✅ Two sources (Superiority, novares), and confirmed live

## Presence 1: the field table

Battle.net sends it during sign-in, before any update. ✅ Confirmed live. Later announcements add to the table or replace entries.

```
count            u(7)
repeat count times:
    client only  bool
    writable     bool
    ephemeral    bool
    no size      bool
    size         u(16)        only when "no size" is 0: the value's fixed byte count
    server only  bool
    type ID      u(8)
    handle       u(32)
align
```

**A field with no fixed size** takes its size from the update that carries it. The meaning of the four flag bits is taken from the names in Superiority's decoder; nothing on this page depends on them.

**Byte example**, two fields: `0x10005` (4 bytes, type 5) and `0x1001E` (no fixed size, type 25):

```
41 04 02 00 04 05 00 02 00 05 14 09 00 10 01 0e
```

`41 04` is the route (Presence slot 4, command 1). The count, 2, starts in the top bits of `04`. Built here from the layout above.

## The fields that matter

One live session announced **69 fields**. Their handles fall in blocks: `0x10001`–`0x10022`, `0x30001`–`0x30006`, `0x50001`–`0x50014`, `0x60001`, `0x70001`–`0x70006` and `0x90001`–`0x90003`. Sizes and type IDs below are from that announcement. ✅ Confirmed live. Values are big-endian.

| Handle | Size | Type | Value | Meaning | |
|---|---|---|---|---|---|
| `0x10003` | 4 | 6 | | A session mark (see [status](#status)) | ⚠️ Superiority |
| `0x10005` | 4 | 5 | u32 | Account ID | ✅ Confirmed live |
| `0x10009` | 4 | 6 | | A session mark | ⚠️ Superiority |
| `0x1000E` | varies | 17 | region u8, program u32, u32, length u8, UTF-8 | The game account's name. For SC2, the character and its code, such as `Raynor#123`. The length byte is the name's length **minus 2**. The u32 is probably the realm. ⚠️ Inferred | ✅ Confirmed live |
| `0x10010` | 1 | 11 | 0 or 1 | Away (older field) | ⚠️ Superiority |
| `0x10011` | 1 | 11 | 0 or 1 | Busy (older field) | ⚠️ Superiority |
| `0x10013` | 4 | 15 | table u16, offset u16 | Portrait (see [profiles and portraits](/bnet2/sc2-profiles/)) | ⚠️ Superiority |
| `0x10014` | 12 | 19 | label u32, ID u64 | The character's profile address | ⚠️ Superiority |
| `0x10015` | 7 | 21 | account ID in the first 4 bytes | Account info | ⚠️ Superiority |
| `0x10018` | 9 | 23 | region u8, program u32, ID u32 | **The game account, and which game it's in** | ✅ Confirmed live |
| `0x10019` | 17 | 22 | region u8, program u32, realm u32, ID u64 | Character handle | ⚠️ Superiority |
| `0x1001B` | 4 | 5 | u32 | Account ID (the "social" one; server only) | ⚠️ Superiority |
| `0x1001E` | varies | 25 | length u8, UTF-8 | **BattleTag**, on chat members and friends | ✅ Confirmed live |
| `0x10020` | 1 | 11 | 0 or 1 | Away | ⚠️ Superiority |
| `0x10022` | 1 | 11 | 0 or 1 | Busy | ⚠️ Superiority |
| `0x50002` | 1 | 11 | 0 or 1 | In a game | ⚠️ Superiority |
| `0x50004` | varies | 13 | | Probably the clan tag | ⚠️ Inferred |

**The program in `0x10018` is a FourCC, big-endian and padded with zeros at the front.** So a player in SC:R reads `00 00 53 31` (`S1`), Diablo IV reads `00 46 65 6E` (`Fen`) and the Battle.net mobile app reads `42 53 41 70` (`BSAp`). ✅ Confirmed live. **This is how a StarCraft II client can show which game a friend is in.**

Example values, for account 12345678 playing StarCraft II as `Raynor#1234`:

| Handle | Bytes |
|---|---|
| `0x10005` | `00 bc 61 4e` |
| `0x10018` | `01 00 00 53 32 00 bc 61 4e` |
| `0x1001E` | `0b 52 61 79 6e 6f 72 23 31 32 33 34` |

**No field carries league, MMR, wins or achievements.** 🛑 See [Open questions](/bnet2/open-questions/).

## Presence 0: an update

```
?                    skip(19)
offline              bool         0 = online, 1 = offline (it's inverted)
local presence ID    u(32)
master presence ID   u(32)
field data           blob(11)     the new values, back to back
?                    skip(11)
cleared handles      u(4) count, then that many u(32)
handles              u(4) count, then that many u(32)
variable sizes       u(4) count, then that many u(16)
?                    opt{ bool, u(32) }
?                    u(8)
align
```

✅ Two sources (Superiority, novares). The inverted online bit is from Superiority. ⚠️

**Splitting the field data.** Walk `handles` in order. Each value's length is its field's fixed size, or, for a field with no fixed size, the **next** entry of `variable sizes`. The lengths must use up the data and the sizes list exactly; if they don't, drop the whole update. ⚠️ Superiority

**A handle that was never announced** means the rest can't be split, since its size is unknown. Keep the values before it and drop the rest. ⚠️ Superiority

**Cleared handles** remove those values from the presence.

**Byte example**, presence 0x1234 (master 0x5678), online, setting `0x10005` to 12345678 and `0x1001E` to `Raynor#1234`:

```
40 04                                   route: Presence slot 4, command 0
00 00 00 00 24 34 00 00 ac 78 04 00     skip(19), online, IDs, data length 16
00 bc 61 4e                             0x10005: 12345678
0b 52 61 79 6e 6f 72 23 31 32 33 34     0x1001E: "Raynor#1234"
00 00 02 00 20 00 05 00 20 03 0e 00 0c 00
                                        skip(11), 0 cleared, 2 handles,
                                        1 variable size (12), the rest
```

Built here from the layout above, using the field table from the Presence 1 example.

## Presence IDs

**Each presence has a local ID and a master ID.** Updates may name either, so treat both as the same presence. When a later update links two IDs that were separate, merge what they hold. ⚠️ Superiority

**The local ID is the one other records use**: a chat member's join (Chat 1, kind 1) carries it, and a whisper can be addressed to it. ⚠️ Superiority

## Tying a presence to a friend or member

A presence belongs to whoever its values name. Use the first that works:

1. **Account ID**, from `0x1001B`, else `0x10005`, else any field announced with type 21. This matches account friends. ✅ Confirmed live
2. **Character handle** `0x10019`. This matches character friends.
3. **Profile address** `0x10014`. A fallback, matched against the profile address a friend record carries.

**Two presences with the same account ID** are the same person seen twice. Fold them into the one updated most recently. ⚠️ Superiority

**The account ID is the one SC:R uses too.** SC:R's FriendUpdated account IDs match `0x10005`. ✅ Confirmed live

## Status

Check in this order. ⚠️ Superiority's rules, and confirmed live that friends show as online and change as they come and go.

1. **The update's offline bit is set:** offline.
2. **The presence once held a session mark** (`0x10003` or `0x10009`) **and now holds neither:** offline. A signed-off presence isn't always sent with the offline bit.
3. **`0x50002` is 1:** in a game.
4. **Away and busy:** of `0x10011`, `0x10010`, `0x10022` and `0x10020`, take the one written **most recently**. On a tie, the later one in that list wins. If its value is 1, the friend is busy (`0x10011`, `0x10022`) or away (`0x10010`, `0x10020`).
5. **Otherwise online.**

**A friend with no presence at all** is shown as offline.

**SC:R has no presence records like these.** Its friends list carries its own online, away and busy fields; see [StarCraft: Remastered chat](/bnet2/scr-chat/#friends).
