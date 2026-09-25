---
title: "StarCraft: Remastered messages"
categories: ["Battle.net 2.0"]
products: [S1]
summary: "Every classic-protocol service and method StarCraft: Remastered uses after sign-in, with IDs and message layouts: characters, chat, whispers, friends and stats."
sources:
  - name: "The StarCraft: Remastered client's own library (libClientSdk)"
    note: "method IDs and message layouts, read from its registration and serialization code"
  - name: "sc1-research, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/sc1-research"
    note: "the classic connection, and the first method names"
  - name: "Superiority, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/superiority"
    note: "WhisperEchoReceived, and account whispers' field types"
  - name: "novares"
    note: "early captures of the classic connection"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-24: CreateToon, Battle.net whispers, and a friend request sent and accepted"
---

StarCraft: Remastered's classic connection carries protobuf RPC (see [StarCraft: Remastered chat](/bnet2/scr-chat/#classic-connection-framing) for the framing and scrambling). Each call names a **service** and a **method** by 32-bit ID.

**Where these come from.** The IDs and message layouts on this page were read from the game's own client library, `libClientSdk.dylib` (macOS, build of 2026-08-04). Its registration code stores each method's ID with `mov dword [rbp-0x154], imm32` (bytes `C7 85 AC FE FF FF` and the ID), next to the code that builds the method's name. For a name of up to 15 characters, which fits inside the string object, the ID comes just **before** the name. For a longer one, which needs its own buffer, it comes just **after**: that's how AcceptInvitation, DeclineInvitation and WhisperEchoReceived were found. Every message class's serializer writes its field tags as constants. Every layout below that we could check against a live session matched. Status markers:

- ✅ **Confirmed live**: used against Battle.net by Invigoration on 2026-09-24.
- 📖 **From the client**: read from the library's code. The field numbers and types are exact; a field's *meaning* is inferred from how the client fills it, and is said so where it matters.

The IDs aren't FNV-1a, FNV-1, CRC-32, CRC-32C, Jenkins one-at-a-time or Murmur3 of the service or method names (checked), so they have to be taken from the client.

## Services

| Service | Package | ID |
|---|---|---|
| Authentication | `classic.protocol.v1.authentication` | `0x17CDFF07` |
| GameAccount | `classic.protocol.v1.game_account` (service `GameAccount`) | `0x354252A4` |
| GameVersion | | `0x3D930F0E` |
| Legacy | | `0xD0C0F33D` |
| LegacyChat | `classic.protocol.v1.legacy_chat` | `0xF4E11A78` |
| LegacyFriends | `classic.protocol.v1.legacy_friends` | `0x5AEF361A` |
| AuroraChat | `classic.protocol.v1.aurora_chat` | `0x924CCFDA` |
| AuroraFriends | `classic.protocol.v1.aurora_friends` | `0xAA4E1E00` |
| ToonProfile | `classic.protocol.v1.toon_profile` | `0x8B952A18` |
| Gateway | | `0x2FD59FA3` |
| Setting | | `0x6781876B` |

## Methods

| Service | Method | ID | Direction | Status |
|---|---|---|---|---|
| Authentication | AuthSession | `0x95F59163` | Client → Server | ✅ |
| GameAccount | GetToons | `0xBC18EDE5` | Client → Server | ✅ |
| GameAccount | **CreateToon** | `0x6697AC0A` | Client → Server | ✅ |
| GameAccount | DeleteToon | `0x194E5421` | Client → Server | 📖 |
| GameAccount | LinkLegacyAccount | `0x7CACB4BE` | Client → Server | 📖 |
| GameAccount | ToonUpdated | `0xF75CAEE5` | Server → Client | ✅ |
| GameAccount | TaiwanLegalDisclaimer | `0xCD95EB4C` | | 📖 |
| GameVersion | SetGameVersion | `0xD48DE460` | Client → Server | ✅ |
| Legacy | Connect | `0x607716CD` | Client → Server | ✅ |
| LegacyChat | SetOnline | `0xD5EBA117` | Client → Server | ✅ |
| LegacyChat | Connect | `0x78D3F5A8` | Client → Server | ✅ |
| LegacyChat | JoinChannel | `0x00C47F9F` | Client → Server | ✅ |
| LegacyChat | SendMessage | `0x5851FB2D` | Client → Server | ✅ |
| LegacyChat | SendCommand | `0x1FEE1493` | Client → Server | ✅ |
| LegacyChat | ChannelsUpdated | `0xC04DAC29` | Server → Client | ✅ |
| LegacyFriends | AddFriend | `0xB56227C5` | Client → Server | 📖 |
| LegacyFriends | DelFriend | `0x40C3DD7D` | Client → Server | 📖 |
| LegacyFriends | Connected | `0xDADDB5B7` | Server → Client | ✅ arrives |
| LegacyFriends | Disconnected | `0xA0E4A7AB` | Server → Client | 📖 |
| LegacyFriends | FriendUpdated | `0xB8A4E3FB` | Server → Client | 📖 |
| AuroraChat | SendWhisper | `0x6251CCD8` | Client → Server | ✅ |
| AuroraChat | WhisperReceived | `0x7255E575` | Server → Client | 📖 |
| AuroraChat | WhisperEchoReceived | `0x82B844A8` | Server → Client | 📖 |
| AuroraChat | StartTypingUser | `0x162162E4` | Client → Server | 📖 |
| AuroraChat | StopTypingUser | `0xEAB58590` | Client → Server | 📖 |
| AuroraFriends | SendInvitation | `0xF7C61139` | Client → Server | ✅ |
| AuroraFriends | AcceptInvitation | `0xF7E2F4AB` | Client → Server | 📖 |
| AuroraFriends | DeclineInvitation | `0xE10265CB` | Client → Server | 📖 |
| AuroraFriends | RemoveFriend | `0xCA10E52C` | Client → Server | 📖 |
| AuroraFriends | FriendUpdated | `0xEC7E2FD1` | Server → Client | ✅ |
| AuroraFriends | InvitationUpdated | `0x4A8E2E5E` | Server → Client | ✅ arrives |
| ToonProfile | GetAvatar | `0x464D320D` | Client → Server | 📖 |
| ToonProfile | AvatarUpdated | `0x6F3EE514` | Server → Client | 📖 |
| ToonProfile | GetStats | `0x81F5E3C9` | Client → Server | ✅ |

LegacyChat's other callbacks (channel messages, whispers, emotes, notices) are listed on [StarCraft: Remastered chat](/bnet2/scr-chat/#legacychat-receiving). AuroraChat methods `0xF90D37BF` and `0x8ECE5580` arrive at sign-in with body `{1: 0}`; their names weren't found.

## GameAccount: characters

A **character** (toon) belongs to one gateway. Gateways are announced at sign-in: 10 U.S. West, 11 U.S. East, 20 Europe, 30 Korea, 45 Asia.

### ToonInfo

| # | Field | Type |
|---|---|---|
| 1 | Character ID | uint64 |
| 2 | Name | string |
| 3 | Gateway | uint64 |

**GetToons** takes an empty request and answers with repeated field 1: `ToonInfo`. ✅

### CreateToon

Creates a character on a gateway. The client sends it from its character screen: **after** AuthSession and GetToons, **before** Legacy.Connect. The new character can then be played at once. ✅ Confirmed live

| Request # | Field | Type |
|---|---|---|
| 1 | Name | string |
| 2 | Gateway | uint64 |

| Response # | Field | Type |
|---|---|---|
| 1 | The new character | `ToonInfo` |

Worked example (✅): creating `Raynor` on U.S. West.

```
request  body: 0A 06 52 61 79 6E 6F 72  10 0A
               field 1 "Raynor"          field 2 = 10
response body: 0A 0C  08 05  12 06 52 61 79 6E 6F 72  18 0A
               field 1 { id 5, name "Raynor", gateway 10 }
```

A name can exist once per gateway, so the same name on another gateway is a separate character. What Battle.net answers for a taken or disallowed name hasn't been seen yet. 🛑

**DeleteToon** takes `{1: character ID (uint64)}`. 📖

### ToonUpdated (server → client)

| # | Field | Type |
|---|---|---|
| 1 | The character | `ToonInfo` |
| 2 | Removed | bool |

Sent once per character at sign-in, and again when one changes. ✅

## AuroraChat: Battle.net whispers

These are **Battle.net whispers**, addressed to an account rather than a character, so they reach a friend in any game, in the Battle.net app, or on mobile.

| SendWhisper request # | Field | Type |
|---|---|---|
| 1 | Recipient's account ID | **fixed32** (tag `0x0D`) |
| 2 | Text | string |

✅ Confirmed live: a whisper sent this way to a friend was delivered, and Battle.net answered the call with a short reply whose contents aren't known. The client's own parser refuses a varint in field 1, so it has to be fixed32.

Worked example: `hi` to account `0x01020304`.

```
0D 04 03 02 01   field 1, fixed32 0x01020304 (little-endian)
12 02 68 69      field 2, "hi"
```

**WhisperReceived** (server → client) has the same shape, with the sender's account ID in field 1. 📖

**WhisperEchoReceived** (server → client, `0x82B844A8`) has the same shape too, with the **recipient's** account ID: Battle.net's copy of a whisper this account sent. 📖 From the client and Superiority. In a live session, no echo arrived for the whispers that session sent itself, so show your own whispers when you send them, and treat an echo as one sent from somewhere else (the game, the Battle.net app) unless it matches one you just sent. ⚠️

Name the other side from the friends list: the account ID in field 1 is the one [FriendUpdated](#friendupdated-server--client) carries.

The account ID is a plain 32-bit number (the same one [FriendUpdated](#friendupdated-server--client) carries in field 1), not an `EntityId` pair.

**StartTypingUser / StopTypingUser** take `{1: account ID (fixed32)}`. A **SendWhisperToAllFriends** message also exists: `{1: text, 2: bool}`. 📖

## AuroraFriends: the Battle.net friends list

### FriendUpdated (server → client)

Sent once per friend at sign-in, and again when one changes. ✅

| # | Field | Type | Meaning |
|---|---|---|---|
| 1 | Friend | `FriendInfo` | |
| 2 | Removed | bool | |

| FriendInfo # | Field | Type | Meaning |
|---|---|---|---|
| 1 | Account ID | uint32 | |
| 2 | BattleTag | string | ✅ |
| 3 | Real name | string | Empty unless they share it ✅ |
| 4 | Program | string | The game or app they're in: `S1`, `S2`, `Fen`, `BSAp` (mobile)… empty when offline ✅ |
| 5 | Online | bool | ✅ |
| 6, 7 | Status flags | bool | Probably away and busy; unconfirmed |
| 8 | | string | |
| 9 | Rich presence | `aurora_user.LocalRichPresence` | 📖 |

### Invitations

| Method | Request | Notes |
|---|---|---|
| SendInvitation `0xF7C61139` | `{1: BattleTag}` | ✅ Confirmed live. The response is `{1: string}`; it was `"us"` for a U.S. account, so probably the region. |
| SendInvitationByToon | `{1: character name, 2: gateway (uint64)}` | 📖 ID not found yet. |
| AcceptInvitation `0xF7E2F4AB` | `{1: invitation ID (uint64)}` | 📖 |
| DeclineInvitation `0xE10265CB` | `{1: invitation ID (uint64)}` | 📖 |
| RemoveFriend | `{1: account ID (uint32, varint)}` | 📖 Unlike whispers, a plain varint. |

**InvitationUpdated** (server → client, `0x4A8E2E5E`): `{1: InvitationInfo {1: invitation ID (uint64), 2: BattleTag}, 2: removed (bool)}`. ✅ Arrives when someone sends you a request, and again with `2: true` once it's gone. Answer it with its invitation ID.

**What the sender sees.** ✅ Confirmed live: after SendInvitation, no InvitationUpdated came to the sending session. When the other person accepted, about 8 seconds later, FriendUpdated arrived for the new friend, so the friends list changed on its own. There's no need to poll: Battle.net pushes every friends-list change.

**RemoveFriend** hasn't been tried live. The FriendUpdated that follows it is expected to carry `2: 1` (removed). ⚠️ Inferred

Worked examples:

```
SendInvitation "A#1234":  0A 06 41 23 31 32 33 34
RemoveFriend account 42:  08 2A
AcceptInvitation 300:     08 AC 02
InvitationUpdated, 300 from "A#1234", removed:
                          0A 0B  08 AC 02  12 06 41 23 31 32 33 34   10 01
```

## LegacyFriends: the classic `/f` list

This is the classic Battle.net friends list, by character name, separate from Battle.net friends.

| Method | Request | Response |
|---|---|---|
| AddFriend | `{1: name}` | `{1: friend ID (uint64)}` |
| DelFriend | `{1: friend ID (uint64)}` | |

**FriendUpdated** (server → client): `{1: removed (bool), 2: FriendInfo {1: ID (uint64), 2–4: strings, 5: enum, 6: attributes}}`. 📖 Meanings of fields 2–6 not yet known.

## ToonProfile: stats and avatars

### GetStats

A character's stats: wins, losses and the rest. This is the call behind the game's own `/stats` command, and it works from any SC:R session for any character. ✅ Confirmed live

| Request # | Field | Type | What the game sends |
|---|---|---|---|
| 1 | Program | uint32 | **Nothing.** The field exists (a FourCC packed big-endian), but the game leaves it out |
| 2 | Gateway | uint64 | The character's gateway, e.g. 10 |
| 3 | Character name | string | **Required** |
| 4 | Stat filter | string | `.*`, a regular expression over stat names |
| 5 | | uint32 | `0xFFFFFFFF` |

**Send exactly those values.** ✅ Confirmed live:
- With a program (`SEXP` or `STAR`), Battle.net answers at once, but always with no stats.
- With no program but field 5 set to 0, it doesn't answer at all.

The values were found by running the game's one GetStats call. `STAR` versus `SEXP` only decides which logo the game shows. 📖

Worked example: `Raynor` on U.S. West.

```
10 0A                    field 2: gateway 10
1A 06 52 61 79 6E 6F 72  field 3: "Raynor"
22 02 2E 2A              field 4: ".*"
28 FF FF FF FF 0F        field 5: 0xFFFFFFFF
```

| Response # | Field | Type |
|---|---|---|
| 1 | Stats | repeated `Stat {1: name (string), 2: value (uint64), 3: uint32}` |
| 2 | | uint32: 20 in every reply seen, meaning unknown |

A live reply for a character with only classic games: ✅

```
legacy_disconnects          0
legacy_wins                 879
legacy_losses               0
legacy_toon_creation_time   131200371947981198   a Windows FILETIME: 4 October 2016
```

A character with nothing recorded gets a reply with no `Stat` entries.

**Stat names the game knows:** 📖
- **Record:** `wins`, `losses`, `draws`, `disconnects`, plus ranked (`mm_wins`…) and classic (`legacy_wins`…) versions of each.
- **Activity:** `games_played`, `play_time`, `APM`.
- **Scores:** `score_overall`, `units_score`, `structures_score`, `resources_score`.
- **Unit, structure and resource counts:** `units_produced`, `units_killed`, `structures_razed`, `resources_spent` and so on.

A name can end in `_sum`, or carry `$SEASONID$` for per-season stats. The game groups them as overall, this season, all seasons and custom games.

### GetAvatar and AvatarUpdated

**GetAvatar** takes `{1: program (uint32), 2: gateway (uint64), 3: character name}`. **AvatarUpdated** (server → client) has the same three fields plus `4: string`. 📖

**ToonProfile has only these three methods.** There's no way to set an avatar, a profile or stats: avatars are assigned by Battle.net, and SC:R has no classic profile fields (`profile\description`, `profile\location`…) at all. 📖
