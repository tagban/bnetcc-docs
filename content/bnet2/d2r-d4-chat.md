---
title: "Diablo II: Resurrected and Diablo IV chat"
categories: ["Battle.net 2.0"]
products: [OSI, Fen]
summary: "Channel chat, whispers, channel lists and keepalives over Front RPC, once a D2R or D4 client is signed in."
sources:
  - name: "novares"
    note: "the main source for this page"
  - name: "d4-bnet-mitm (a Diablo IV Battle.net proxy)"
    url: "https://github.com/cjbrigato/d4-bnet-mitm"
    note: "independent source for the Front framing and RPC header"
---

Unless a line says otherwise, everything on this page comes from novares and is ⚠️ single source. The byte example was rebuilt here from the rules on this page and matched the source's bytes exactly. It is still one source: novares.

D2R and D4 chat runs on the same **[Front](/bnet2/front/)** WebSocket the game signed in on. There's no separate chat server. Every chat action is an ordinary Front RPC: one binary WebSocket message, a 2-byte big-endian header length, the protobuf header, then the protobuf body. ✅ Verified

This page starts **after** sign-in and the first channel join. It doesn't cover signing in.

## Protobuf shorthand

Bodies below are written as field lists, built in the order shown:

| Notation | Wire bytes |
|---|---|
| `V(f, n)` | Tag `f × 8`, then `n` as a varint |
| `F32(f, n)` | Tag `f × 8 + 5`, then 4 bytes, little-endian |
| `F64(f, n)` | Tag `f × 8 + 1`, then 8 bytes, little-endian |
| `S(f, text)` | Tag `f × 8 + 2`, varint length, UTF-8 text |
| `M(f, message)` | Tag `f × 8 + 2`, varint length, a nested message |
| `+` | Concatenate |

## The header on a chat call

| # | Field | Value |
|---|---|---|
| 1 | `service_id` | `0` on a request, `254` on a reply ✅ Verified |
| 2 | `method_id` | The method number. Left out of a normal reply |
| 3 | `token` | A new number for each request; replies carry it back |
| 5 | `size` | The body's length |
| 6 | `status` | Missing or `0` means success |
| 9 | `is_response` | `1` on a reply |
| 11 | `service_hash` | FNV-1a of the service name ([how](/bnet2/front/#which-service-a-call-is-for)) |

Treat a message as a **reply** if `service_id` is 254 *or* `is_response` is 1. Anything else is a call from the server: route it by service hash and method.

**Keep a separate token counter for each connection.** Increase it before each new request and match replies by token.

## Services

| Service | FNV-1a hash | Used for |
|---|---|---|
| `bnet.protocol.channel.v2.ChannelService` | `0x798D39D1` | Sending chat, listing, finding and joining channels |
| `bnet.protocol.channel.v2.ChannelListener` | `0x1AE52686` | Incoming chat and roster changes |
| `bnet.protocol.channel.v2.membership.ChannelMembershipListener` | `0x018007BE` | Channel descriptions |
| `bnet.protocol.whisper.v2.client.WhisperService` | `0xFEE1AA14` | Sending whispers |
| `bnet.protocol.whisper.v2.client.WhisperListener` | `0x62615E21` | Incoming whispers |
| `bnet.protocol.account.v1.AccountService` | `0x8B2A82A2` | Looking up a BattleTag |
| `bnet.protocol.connection.ConnectionService` | `0x65446991` | Keepalives |

The hashes were computed here from the names, and the ChannelService one appears in the source's byte example.

## Identifiers

**D2R and D4 encode the same handle differently.** D2R uses fixed-width fields; D4 uses varints.

```
D2R Handle = F32(1, low 32 bits of game account ID) + F32(2, title ID) + V(3, region)
D4  Handle = V(1, game account ID)                  + V(2, title ID)   + V(3, region)

ChannelId  = M(2, V(1, host label) + V(2, host epoch)) + F32(3, channel ID) + V(4, region)
```

- **The title ID is the program code as a big-endian ASCII number:** `OSI` = `0x4F5349` for D2R, `Fen` = `0x46656E` for D4.
- **A channel needs all four parts** of its ChannelId. The number alone doesn't find it.
- Game account IDs are 64-bit. Don't pass them through a floating-point number.

## Send a message: ChannelService method 23

```
D2R body = M(1, Handle) + M(2, ChannelId) + M(3, S(4, text))
D4  body = M(2, ChannelId) + M(3, S(4, text)) + M(4, Handle)
```

Text is UTF-8, **up to 255 bytes**. A successful reply is the only acknowledgement.

### Byte example (D2R)

Game account 456, title `OSI`, region 1; channel 99 on host 1, epoch 2, region 1; token 1; text `hello`.

```
00 0d                              header length: 13
08 00                              service_id 0
10 17                              method_id 23
18 01                              token 1
28 26                              size 38
5d d1 39 8d 79                     service_hash 0x798D39D1
0a 0c 0d c8 01 00 00               M(1, Handle): F32(1, 456)
      15 49 53 4f 00                             F32(2, 'OSI')
      18 01                                      V(3, 1)
12 0d 12 04 08 01 10 02            M(2, ChannelId): M(2, host 1, epoch 2)
      1d 63 00 00 00                             F32(3, 99)
      20 01                                      V(4, 1)
1a 07 22 05 68 65 6c 6c 6f         M(3, S(4, "hello"))
```

The D4 version has the same header with `size` 36. Its body puts the Handle last, with varint IDs: `… 22 0a 08 c8 03 10 ee ca 99 02 18 01`.

## Receive chat and roster changes: ChannelListener

Each call names its channel in nested field 3. **Ignore calls for channels you haven't joined.**

| Method | Nested field 4 holds |
|---|---|
| 10 | A message: sender handle in field 1, text in field 3 (field 4 in older replies) |
| 3 | A member who joined or changed |
| 4 | The handle of a member who left |

A member has a UTF-8 name in field 2 and an account ID in field 6. D2R usually puts the member's handle in nested field 1; D4 usually uses nested field 7, falling back to 1. Match members on game account ID, title ID *and* region, then use your roster to turn a message's sender handle into a name.

## Whispers

1. **Find the account.** AccountService method 13: `M(1, S(4, battleTag)) + V(2, 1)`. The account ID is in the reply's nested field 12, field 1. Older replies put the number directly in field 12.
2. **Send.** WhisperService method 4: `V(1, account ID) + M(2, S(1, text))`.
3. **Receive.** WhisperListener method 1. Nested field 2 is the whisper: text in field 5 (field 3 in older replies), sender's account ID in field 2. The outer field 3 is the sender's BattleTag.

## Channel list and joining a channel

**List public channel types:** ChannelService method 5.

```
UniqueType = F32(2, program) + S(3, channel type)
D2R body   = M(1, Handle) + M(2, M(1, UniqueType))
D4  body   = M(2, M(1, UniqueType)) + M(4, Handle)
```

| Game | `program` | Channel type |
|---|---|---|
| D2R | `OSI` | `public_default` |
| D4 | `Fen` | `public_test` |

The reply repeats field 1, one per channel. Each has a UniqueType (nested 1), a name (2) and an identity (3).

**Find a channel:** method 6, with an identity from the list.

```
Options  = M(1, UniqueType) + S(2, identity) + F32(3, 0x656E5553)     ('enUS')
D2R body = M(1, Handle) + M(2, Options)
D4  body = M(2, Options) + M(3, Handle)
```

**Two things answer, in either order:** the reply to method 6, and ChannelMembershipListener method 1 with the channel's description in nested field 3. Wait for both. A description has ChannelId (nested 1), UniqueType (nested 2), name (3), members (repeated 6) and identity (nested 110, field 1).

**Join it:** method 10 subscribes.

```
D2R body = M(1, Handle) + M(2, ChannelId)
D4  body = M(2, ChannelId) + M(3, Handle)
```

The reply's nested field 1 is the channel and its roster. **Only switch channels once this succeeds.**

| Method | Same body as method 10 | Does |
|---|---|---|
| 11 | ✔ | Stops updates from a channel |
| 31 | ✔ | Leaves a channel |

## Keepalives: ConnectionService

| Direction | Method | What to do |
|---|---|---|
| Client → Server | 5 | Every **30 seconds**: empty body, new token. Don't wait for a reply. |
| Server → Client | 3 | Echo. Reply with its token, `service_id` 254, `is_response` 1. Copy its fixed64 field 1 into your fixed64 field 1, and its bytes field 3 into your bytes field 2. |
| Server → Client | 4 | The server is asking you to disconnect. |

WebSocket Ping and Pong frames are separate and still need answering.
