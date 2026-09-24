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
  - name: "novares"
    note: "early captures of the classic connection"
---

StarCraft: Remastered's classic connection carries protobuf RPC (see [StarCraft: Remastered chat](/bnet2/scr-chat/#classic-connection-framing) for the framing and scrambling). Each call names a **service** and a **method** by 32-bit ID.

**Where these come from.** The IDs and message layouts on this page were read from the game's own client library, `libClientSdk.dylib` (macOS, build of 2026-08-04). Its registration code stores each method's ID with `mov dword [rbp-0x154], imm32` just before building the method's name, and every message class's serializer writes its field tags as constants. Every layout below that we could check against a live session matched. Status markers:

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
| AuroraChat | SendWhisper | `0x6251CCD8` | Client → Server | 📖 |
| AuroraChat | WhisperReceived | `0x7255E575` | Server → Client | 📖 |
| AuroraChat | StartTypingUser | `0x162162E4` | Client → Server | 📖 |
| AuroraChat | StopTypingUser | `0xEAB58590` | Client → Server | 📖 |
| AuroraFriends | SendInvitation | `0xF7C61139` | Client → Server | 📖 |
| AuroraFriends | RemoveFriend | `0xCA10E52C` | Client → Server | 📖 |
| AuroraFriends | FriendUpdated | `0xEC7E2FD1` | Server → Client | ✅ |
| AuroraFriends | InvitationUpdated | `0x4A8E2E5E` | Server → Client | ✅ arrives |
| ToonProfile | GetAvatar | `0x464D320D` | Client → Server | 📖 |
| ToonProfile | AvatarUpdated | `0x6F3EE514` | Server → Client | 📖 |
| ToonProfile | GetStats | `0x81F5E3C9` | Client → Server | 📖 |

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

**WhisperReceived** (server → client) has the same shape, with the sender's account ID in field 1. 📖

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
| SendInvitation | `{1: BattleTag}` | 📖 The response carries one string, meaning unknown. |
| SendInvitationByToon | `{1: character name, 2: gateway (uint64)}` | 📖 |
| AcceptInvitation | `{1: invitation ID (uint64)}` | 📖 |
| DeclineInvitation | `{1: invitation ID (uint64)}` | 📖 |
| RemoveFriend | `{1: account ID (uint32, varint)}` | 📖 Unlike whispers, a plain varint. |

**InvitationUpdated** (server → client, `0x4A8E2E5E`): `{1: InvitationInfo {1: invitation ID (uint64), 2: BattleTag}, 2: removed (bool)}`. ✅ Arrives when someone sends you a request, and again with `2: true` once it's gone.

## LegacyFriends: the classic `/f` list

This is the classic Battle.net friends list, by character name, separate from Battle.net friends.

| Method | Request | Response |
|---|---|---|
| AddFriend | `{1: name}` | `{1: friend ID (uint64)}` |
| DelFriend | `{1: friend ID (uint64)}` | |

**FriendUpdated** (server → client): `{1: removed (bool), 2: FriendInfo {1: ID (uint64), 2–4: strings, 5: enum, 6: attributes}}`. 📖 Meanings of fields 2–6 not yet known.

## ToonProfile: stats and avatars

### GetStats

| Request # | Field | Type | Meaning |
|---|---|---|---|
| 1 | Program | uint32 | A short code such as `S1` packed into a number; sent only when given |
| 2 | Gateway | uint64 | Probably the gateway; sent only when not 0 |
| 3 | Character name | string | **Required**; an empty name is refused |
| 4 | Stat filter | string | A regular expression over stat names; the client defaults to `.*` |
| 5 | | uint32 | Unknown |

| Response # | Field | Type |
|---|---|---|
| 1 | Stats | repeated `Stat {1: name (string), 2: value (uint64), 3: uint32}` |
| 2 | | uint32 |

The game names stats such as `legacy_wins`, `legacy_losses`, `legacy_disconnects`, `mm_wins`, `games_played`, `play_time` and `score_overall`, with `_sum` forms. 📖 This is likely what the in-game `/stats` command shows. Not yet tried live.

### GetAvatar and AvatarUpdated

**GetAvatar** takes `{1: program (uint32), 2: gateway (uint64), 3: character name}`. **AvatarUpdated** (server → client) has the same three fields plus `4: string`. 📖
