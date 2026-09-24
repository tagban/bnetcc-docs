---
title: "StarCraft: Remastered chat"
categories: ["Battle.net 2.0"]
products: [S1]
summary: "SC:R's two WebSockets, the scrambled classic connection, and the LegacyChat service that carries its chat."
sources:
  - name: "novares"
    note: "the main source for this page"
  - name: "sc1-research, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/sc1-research"
    note: "the classic connection's scrambling scheme"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-24: characters, gateways, joins, member lists, operators, sending, slash commands and friends"
---

Unless a line says otherwise, everything on this page comes from novares and is ⚠️ single source. The byte example was rebuilt here from the rules on this page, including the scrambling, and matched the source's bytes exactly.

Sections marked ✅ **confirmed live** were checked by Invigoration against Battle.net on 2026-09-24. The sections from [Characters and gateways](#characters-and-gateways) onwards were added then, and mark each fact.

**StarCraft: Remastered doesn't chat like StarCraft II.** SC2 chats over bit-packed [Sunken](/bnet2/sunken/) records. SC:R chats over protobuf RPC on a WebSocket of its own, through a service called **LegacyChat**, and sees the channels classic StarCraft players know.

This page starts **after** sign-in and the first channel join. It doesn't cover signing in.

Signing in, the classic server's address and the seed are on [StarCraft: Remastered: signing in](/bnet2/sequences/starcraft-remastered-logon/).

## Two connections

| Connection | Format | Used for |
|---|---|---|
| **Aurora** | WebSocket, JSON text | The Battle.net session. After sign-in, only keepalives matter here. |
| **Classic** | WebSocket, binary, **scrambled** | Chat: LegacyChat, plus its own keepalives |

**Both must stay open, and both need their keepalives answered.**

## Choosing a server

SC:R has three separate layers of "server". Keep them apart in code and settings:

| Layer | Chosen by | Notes |
|---|---|---|
| **Battle.net region** | The account | Where the Aurora connection signs in. |
| **Gateway** | The player, per session | Within the US: **10 = U.S. West, 11 = U.S. East**. Characters (toons) belong to one gateway. ⚠️ Single source. Other regions' gateway numbers are 🛑 unknown. |
| **Classic chat address** | Battle.net, during sign-in | **Never fixed.** Battle.net hands out the classic WebSocket address for the chosen gateway, so always use the one it returns. How that exchange works isn't documented here yet. 🛑 Unknown |

The classic connection isn't the 1998-era [BNCS](/classic/connecting/) protocol on TCP 6112, even though its chat looks the same to players.

**Update, 2026-09-24.** Gateways are announced at sign-in: 10, 11, 20 (Europe), 30 (Korea) and 45 (Asia). See [Characters and gateways](#characters-and-gateways). The classic address comes from a `ConnectToServer` request that names **no gateway**; the gateway follows from the character chosen in Legacy.Connect. See [signing in](/bnet2/sequences/starcraft-remastered-logon/#aurora-connecttoserver). ✅ Confirmed live

## Aurora keepalive

Aurora messages are JSON arrays of `[header, body]`. When Battle.net sends ConnectionService (hash `0x65446991`) method **3**, reply with:

- `service_id: 254`
- the same `token`
- `is_response: true`
- `status: 0`
- the body you received

Method **4** means Battle.net wants to disconnect.

## Classic connection: scrambling

**Every classic WebSocket message is scrambled** with a 32-bit seed agreed during sign-in (🛑 how the seed is chosen isn't documented here). Unscramble each incoming message before reading it. Scramble each outgoing message, including replies, after building it.

All arithmetic is unsigned 32-bit, and `ROL(x, n)` rotates left by `n` bits. **Start again from the seed for every message.**

```
out = copy of the message
key = seed

for lane = 0 to min(4, length) - 1:          # first 4 bytes
    key = ROL(key, 1)
    out[lane] ^= (key >> (lane * 8)) & 0xFF

offset = 4
while offset < length:
    prev   = little-endian uint32 of the SCRAMBLED bytes at offset - 4
             (the input when unscrambling, the output when scrambling)
    rotate = NOT((offset AND 31) XOR prev) AND 31
    key    = ROL(prev, (32 - rotate) AND 31)
    for lane = 0 to 3, stopping at the end:
        key = ROL(key, 1)
        out[offset] ^= (key >> (lane * 8)) & 0xFF
        offset += 1
```

Each 4-byte block's key comes from the scrambled block before it, so a scrambler must read back its own output as it goes.

**How the seed is chosen:** it's folded from the client's own `Sec-WebSocket-Key`. See [the seed](/bnet2/sequences/starcraft-remastered-logon/#classic-the-websocket-and-its-seed). ✅ Confirmed live

## Classic connection: framing

Once unscrambled, a message holds **one or more** RPC frames back to back:

```
offset  size            field
0       2               header length (UINT16, big-endian)
2       header length   RPC header (protobuf)
...     header's size   RPC body (protobuf)
```

**Unlike [Front](/bnet2/front/), every header field is a varint**, including the service hash:

| # | Field | Value |
|---|---|---|
| 1 | Service | The service hash |
| 2 | Method | The method ID (these are 32-bit hashes too) |
| 3 | Token | A new number for each request |
| 4 | Routing | `2525111537` (`0x968224F1`) on requests the client sends |
| 5 | Size | The body's length |
| 6 | Status | `0` on requests. Non-zero in a reply means an error. |
| 9 | Response | `0` request, `1` response |

Read the body using `size`, then carry on with the next frame in the same message.

**Correction, 2026-09-24.** Field 6 is an **object ID**, not a status. It's `0` on the client's requests, and a reply to a server call must echo the call's object ID. Field 12 is a request trace, sent on the AuthSession call only. Replies carry no status to check. See [the corrected fields](/bnet2/sequences/starcraft-remastered-logon/#classic-header-fields-corrected). ✅ Confirmed live; from sc1-research

## LegacyChat: sending

LegacyChat's service hash is **`0xF4E11A78`**. Use a new token for every request. `V`, `S` and `M` are the [protobuf shorthand](/bnet2/d2r-d4-chat/#protobuf-shorthand).

| Operation | Method | Body |
|---|---|---|
| Send a message | `0x5851FB2D` | `V(1, channel ID) + S(2, text)` |
| Whisper | `0x1FEE1493` | `V(1, channel ID) + S(2, "whisper") + S(3, recipient) + S(3, text)` |
| Join a channel by name | `0x1FEE1493` | `V(1, channel ID) + S(2, "channel") + S(3, channel name)` |
| List channels | `0x78D3F5A8` | `V(1, 0)` |
| Join a listed channel | `0x00C47F9F` | `V(1, target channel ID)` |
| Leave a channel | `0x84F6DDA8` | `V(1, channel ID)` |

- **`0x1FEE1493` runs a named command.** Field 2 names it and each field 3 is one argument. The whole whisper text goes in **one** field 3, and so does the whole channel name.
- **Don't send slash commands as messages.** `/w` and `/join` typed into the message method aren't commands; use the methods above.
- **Only believe a channel change when the server confirms it** (see below), not when you send the join.
- **`0x78D3F5A8` is also LegacyChat.Connect**, the last startup call. ✅ Confirmed live
- **Joining a listed channel by ID only works outside a channel.** See [Channel joins](#channel-joins). ✅ Confirmed live

### Byte example: `hello` to channel 9

Token 1, before scrambling:

```
00 1a                              header length: 26
08 f8 b4 84 a7 0f                  service 0xF4E11A78 (LegacyChat)
10 ad f6 c7 c2 05                  method  0x5851FB2D (send a message)
18 01                              token 1
20 f1 c9 88 b4 09                  routing 0x968224F1
28 09                              size 9
30 00                              status 0
48 00                              request
08 09                              V(1, 9)
12 05 68 65 6c 6c 6f               S(2, "hello")
```

Scrambled with seed `0x12345678`, the same 37 bytes go on the wire as `f0 43 aa db 24 51 7c ee … a1 35 23 64 16 4e`.

## LegacyChat: receiving

**Reply to every classic call from the server.** Use the same service, method, token and routing, set the response flag to 1, and send an empty body. For ConnectionService method 3, echo its body back instead. Scramble the reply like any other message.

| Method | Carries |
|---|---|
| `0xC04DAC29` | Channel list changes: repeated field 1, each with a change type (field 1) and a channel (nested field 2). Type 1 removes the channel; any other type adds or updates it. |
| `0xC583300A` | The channel you're in, in nested field 2. |
| `0xFA88D3E1` | Whisper |
| `0x850B6EE3` | Channel message |
| `0xAA6957AA` | Broadcast |
| `0x1580B7A1` | Information |
| `0xD52809ED` | Error |
| `0x632D6CFD` | Emote |

**A channel** has its ID in field 1, internal name in field 2, display name in field 5 and members in repeated field 3. **A member** has a name (field 1), flags (field 2) and repeated attributes (field 3), each attribute being a name (field 1) and value (field 2).

**The six message kinds aren't fully mapped yet.** 🛑 A working approach reads them by shape: walk the length-delimited fields in order, up to four levels deep. Treat a non-empty, valid UTF-8 string with no control characters as text, and try anything else as a nested message. If there's more than one text, the first is the sender and the last is the message. That's a fallback, not a schema; please add the real field layouts here when they're captured.

## Characters and gateways

**GetToons** (GameAccount `0x354252A4`, method `0xBC18EDE5`, empty body) is the first startup call. Its reply lists every character on the account, on every gateway. ✅ Confirmed live; the layout was first read from a retail capture (novares).

```
repeated field 1, one per character:
    1   character ID   varint
    2   name           string
    3   gateway        varint
```

Two characters called `Raynor`, ID 1 on U.S. West and ID 2 on U.S. East:

```
0a 0c  08 01  12 06 52 61 79 6e 6f 72  18 0a      M(1, V(1, 1) + S(2, "Raynor") + V(3, 10))
0a 0c  08 02  12 06 52 61 79 6e 6f 72  18 0b      M(1, V(1, 2) + S(2, "Raynor") + V(3, 11))
```

- **A character belongs to one gateway.** The same name can exist on several, as separate characters with separate IDs.
- **Pick the character by gateway, then by name,** and pass its ID to Legacy.Connect. That's what puts the session on a gateway. ✅ Confirmed live
- **If the account has no character on the chosen gateway**, create one first with [GameAccount.CreateToon](/bnet2/scr-messages/#createtoon) (`{1: name, 2: gateway}`), after GetToons and before Legacy.Connect. It answers with the new character, which can be played at once. ✅ Confirmed live

**Gateways are announced during AuthSession**, one **GatewayUpdate** call each (service `0x2FD59FA3`, method `0xF5570066`). ✅ Confirmed live

```
1   gateway   message
      1   ID          varint
      2   name        string, as the game shows it
      3   short code  string            ⚠️ inferred
      5   ?           varint, 1 seen     ⚠️ inferred: online
      7   ?           string            ⚠️ inferred: a news URL
2   ?         varint, 0 seen
```

| ID | Gateway |
|---|---|
| 10 | U.S. West |
| 11 | U.S. East |
| 20 | Europe |
| 30 | Korea |
| 45 | Asia |

The IDs were announced live to a U.S. account. Whether that account can use 20, 30 or 45 isn't known. 🛑

Byte example, U.S. West: `0a 0f 08 0a 12 09 55 2e 53 2e 20 57 65 73 74 28 01 10 00`.

**One SC:R session per account** seems to be the rule. See [the stall after a recent session](/bnet2/sequences/starcraft-remastered-logon/#the-stall-after-a-recent-session). ⚠️ Inferred

## Channel joins

SC:R is in **one channel at a time**. Joining another takes you out of the current one. ✅ Confirmed live

| Where you are | How to join | Confirmed by | |
|---|---|---|---|
| **In no channel** (right after startup) | Join a listed channel by ID, `0x00C47F9F` | A channel-list update (`0xC04DAC29`) that includes it | ✅ Confirmed live |
| **In a channel** | The command method `0x1FEE1493` with `"channel"` and the name | The current-channel call (`0xC583300A`) | ✅ Confirmed live |

- **From inside a channel, a join by ID is silently ignored.** Use the channel command. It works for any channel, listed or not, and creates one that doesn't exist. ✅ Confirmed live
- **From outside any channel, the channel command is ignored.** To start in a private channel, join a listed one by ID first, then use the command. Invigoration enters `Open Tech Support` first. ✅ Confirmed live
- **A listed channel can come back with a different ID** than the one listed, as a new instance. Match the confirmation on the ID, or on the name when it carries members. Rejoin by name after a reconnect, not by ID. ⚠️ Single source (Invigoration)
- **Being taken out of a channel** arrives as LegacyChat `0xB07FD98A`, with the channel's ID in field 1. ⚠️ Single source (Invigoration)

**Public channels** listed on U.S. West, with their IDs there: Blizzard Chat (1), Blizzard Tech Support (2), Brood War (3), Brood War Games (4), Brood War Ranked (5), Custom Maps (6), Open Tech Support (7), Protoss Strategy (8), Public Chat (9), Terran Strategy (10), Zerg Strategy (11). ✅ Confirmed live. Other gateways' lists weren't checked.

## Member lists

**Every channel-list update carries the channel's whole member list**, not a change. To find who joined and left, compare it with the list before. The first list after entering a channel is who was already there. ✅ Confirmed live

- **The current-channel call usually has no members.** The list follows in a channel-list update, usually about a second later, but sometimes 20 seconds or more. Asking for the channel list again (`0x78D3F5A8` with `V(1, 0)`) may bring it sooner. ✅ Confirmed live
- **Channels in the list often carry only the internal name** (field 2). Use it as the display name when field 5 is empty. ✅ Confirmed live

### Member fields

| # | Field | Notes |
|---|---|---|
| 1 | name | The character name |
| 2 | flags | **2 = channel operator**, seen on a channel's owner. Only 0 and 2 have been seen. ✅ Confirmed live |
| 3 | attribute | Repeated. Each is a name (field 1) and a value (field 2), both strings. |

| Attribute | Value | |
|---|---|---|
| `program_id` | The classic product code, in normal reading order: `SEXP`, `W2BN` and `DRTL` were seen | ✅ Confirmed live |
| `battle_tag` | The member's BattleTag | ✅ Confirmed live |

- **Diablo II members carry no `program_id` at all.** No code means Diablo II. Whether they're on Lord of Destruction isn't said. ✅ Confirmed live
- **SC:R players showed `SEXP`.** Whether one who owns only the original shows `STAR` isn't known. 🛑
- **There's no statstring**, so no ladder rating, wins or icon beyond the product. ✅ Confirmed live
- Diablo (`DRTL`) members were seen in Open Tech Support. Warcraft III members weren't seen at all.

## Your own lines

**Battle.net doesn't echo your own channel messages or whispers back to you.** Show them yourself when you send them. ✅ Confirmed live

## Slash commands

**Send typed commands with the command method**, `0x1FEE1493`, not the message method. Field 2 is the command word, lower-case and without the slash. Field 3 is the first argument. A second field 3 holds **the rest of the line, as one argument.** The answer comes back as an Information or Error message.

`/kick Raynor spamming the channel` in channel 9:

```
V(1, 9) + S(2, "kick") + S(3, "Raynor") + S(3, "spamming the channel")
```

`/channel` this way is ✅ confirmed live. The same split for other commands (`/whois`, `/kick`, `/ban`, `/designate`) is how Invigoration sends them; ⚠️ single source (Invigoration). It matches the `whisper` and `channel` bodies above.

## Friends

The Battle.net friends list arrives on the classic socket as **AuroraFriends FriendUpdated**: service `0xAA4E1E00`, method `0xEC7E2FD1`. Battle.net sends one call per friend right after sign-in, then another whenever a friend changes. Reply to each as usual. ✅ Confirmed live

```
1   friend    message
      1   account ID   varint
      2   BattleTag    string
      3   real name    string   only for Real ID friends who share it
      4   program      string   the game or app they're in: "S1", "S2", "Fen", "BSAp"…; empty when offline
      5   online       varint   1 when online
      6   ?            varint   ⚠️ inferred: away
      7   ?            varint   ⚠️ inferred: busy
      8, 9  ?          string   🛑 thought to say what they're doing
2   change    varint   0 in every one seen; ⚠️ 1 is taken to mean removed
```

- **Field 3 is the friend's real name.** Treat it as private: don't show it unless the user asks for real names.
- **`BSAp` is the Battle.net mobile app.** `Fen` is Diablo IV. ✅ Confirmed live
- **The account ID is the same one StarCraft II's presence carries** (field `0x10005`), so the two lists can be matched. ✅ Confirmed live
- **Friend invitations** on this socket aren't decoded. 🛑

Friend `Raynor#1234`, account 12345678, online in SC:R:

```
0a 18                              M(1, …), 24 bytes
      08 ce c2 f1 05               V(1, 12345678)
      12 0b 52 61 79 6e 6f 72 23 31 32 33 34     S(2, "Raynor#1234")
      22 02 53 31                  S(4, "S1")
      28 01                        V(5, 1)
10 00                              V(2, 0)
```
