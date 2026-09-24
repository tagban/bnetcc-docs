---
title: "StarCraft: Remastered: signing in"
layout: "sequence"
categories: ["Sequences", "Battle.net 2.0"]
products: [S1]
summary: "From the Aurora WebSocket to a chat channel: sign-in, the classic server's address and ticket, the key-folded seed, AuthSession and the startup calls."
steps:
  - { section: "Aurora: connect" }
  - { from: client, raw: "wss://us.actual.battle.net:1119/", transport: "jsonrpc.aurora.v1.30.battle.net", note: "One JSON `[header, body]` array per WebSocket message.", confidence: verified }
  - { from: client, raw: "ConnectionService / 1", note: "Connect, with `use_bindless_rpc: true`.", confidence: verified }
  - { from: server, raw: "ConnectionService / 3", note: "Echo, at any time from here on. Answer every one, on this socket, for as long as it's open.", confidence: verified }
  - { section: "Aurora: sign in" }
  - { from: client, raw: "AuthenticationServer / 1", note: "Logon, program `S1`, with the saved web credential.", confidence: verified }
  - { from: server, raw: "ChallengeNotify / 3", optional: true, note: "Only when the saved credential is missing or refused: Blizzard's web sign-in.", confidence: verified }
  - { from: client, raw: "AuthenticationServer / 7", optional: true, note: "VerifyWebCredentials, with the value from the web sign-in.", confidence: verified }
  - { from: server, raw: "AuthenticationClient / 5", note: "LogonResult: session key, account ID, game account ID, BattleTag.", confidence: verified }
  - { from: client, raw: "AuthenticationServer / 8", note: "GenerateWebCredentials: a new saved credential for next time.", confidence: verified }
  - { section: "Aurora: find the classic server" }
  - { from: client, raw: "GameUtilities / 1", note: "ProcessClientRequest carrying a `ConnectToServerRequest`.", confidence: verified }
  - { from: server, raw: "GameUtilities / 1 response", note: "A `ConnectToServerResponse`: the classic WebSocket URL and a 56-byte ticket.", confidence: verified }
  - { section: "Classic: connect and authenticate" }
  - { from: client, raw: "Classic WebSocket", transport: "wss, path /S1/v2/rpc/client", note: "The scrambling seed is folded from this handshake's `Sec-WebSocket-Key`. From here Battle.net allows about **6 seconds** to finish startup.", confidence: verified }
  - { from: client, raw: "Authentication / AuthSession", note: "The ticket, the Aurora session key and IDs, and the client's identity.", confidence: verified }
  - { from: server, raw: "Gateway / GatewayUpdate", note: "One call per gateway: 10, 11, 20, 30, 45.", confidence: verified }
  - { from: server, raw: "AuthSession response", note: "Carries a 64-byte server proof.", confidence: verified }
  - { section: "Classic: start the game session" }
  - { from: client, raw: "GameAccount / GetToons", note: "The account's characters, each with its gateway.", confidence: verified }
  - { from: client, raw: "GameVersion / SetGameVersion", note: "`1.23.10.13515`.", confidence: verified }
  - { from: client, raw: "Legacy / Connect", note: "`{1: character ID}`. Picks the character, and with it the gateway.", confidence: verified }
  - { from: client, raw: "LegacyChat / SetOnline", note: "Empty body.", confidence: verified }
  - { from: client, raw: "LegacyChat / Connect", note: "`V(1, 0)`. Battle.net then sends the public channel list.", confidence: verified }
  - { from: client, raw: "LegacyChat / join a listed channel", note: "By ID, as the first join. See [StarCraft: Remastered chat](/bnet2/scr-chat/#channel-joins).", confidence: verified }
sources:
  - name: "sc1-research, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/sc1-research"
    note: "the sign-in sequence, the seed fold, the AuthSession body, the classic header fields and the retail client's identity"
  - name: "novares"
    note: "the GetToons reply layout and the Legacy.Connect argument, from a capture of the retail client"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-24: every step above, the 6-second limit and the stall after a recent session"
---

**This is the whole sign-in for *StarCraft: Remastered* (SC:R), done without the game.** It was confirmed live (Invigoration, 2026-09-24) on U.S. West, from sign-in to sending chat. Chat itself is on [StarCraft: Remastered chat](/bnet2/scr-chat/).

SC:R uses two WebSockets. **Aurora** is the Battle.net session, in JSON. **Classic** is the game's own RPC, in scrambled protobuf. Both stay open for the whole session, and both need their keepalives answered.

Marks on this page: ✅ **confirmed live** (Invigoration, 2026-09-24), ⚠️ from **one source** or **inferred**, 🛑 **unknown**. The step table's marks mean the same.

## Aurora: the connection

| Item | Value | |
|---|---|---|
| URL | `wss://us.actual.battle.net:1119/` | ✅ Confirmed live |
| Subprotocol | `jsonrpc.aurora.v1.30.battle.net` | ✅ Confirmed live |
| Message | A JSON array `[header, body]` | ✅ Confirmed live |
| Frame type | The client sends text frames. **Battle.net sends its JSON in binary frames**, so read both kinds. | ✅ Confirmed live |

Aurora is the same RPC as StarCraft II's [Front](/bnet2/front/), with the same services, methods and message names, written as JSON instead of protobuf bytes. Field names are the protobuf field names in snake_case. See [Front messages](/bnet2/front-messages/) for what each one means.

**A request header** has `service_hash`, `method_id`, `service_id: 0` and a new `token`. **A response** has `is_response: true`, the same `token` and a `status`. A non-zero status means the request was refused. ✅ Confirmed live

**Numbers may arrive as JSON numbers or as strings**, so accept both. ✅ Confirmed live

| Service | Hash |
|---|---|
| `bnet.protocol.connection.ConnectionService` | `0x65446991` |
| `bnet.protocol.authentication.AuthenticationServer` | `0x0DECFC01` |
| `bnet.protocol.authentication.AuthenticationClient` | `0x71240E35` |
| `bnet.protocol.challenge.ChallengeNotify` | `0xBBDA171F` |
| `bnet.protocol.game_utilities.GameUtilities` | `0x3FC1274D` |

The hashes are FNV-1a of the names ([how](/bnet2/front/#which-service-a-call-is-for)), and each was checked here.

### Answering Echo

When Battle.net calls ConnectionService method **3**, reply with `service_id: 254`, the same `token`, `is_response: true`, `status: 0`, and the body it sent. ✅ Confirmed live. **Keep answering during the web sign-in too.** Left unanswered, Battle.net drops the connection after a couple of minutes. ⚠️ Single source

## Aurora: signing in

**LogonRequest** (AuthenticationServer method 1), as JSON. ✅ Confirmed live

| Key | Value |
|---|---|
| `program` | `"S1"` |
| `platform` | `"Mac"` (the platform Invigoration signs in as) |
| `locale` | `"enUS"` |
| `application_version` | `65559` |
| `version` | `"65559"` |
| `cached_web_credentials` | The saved web credential, base64 |
| `web_client_verification` | `true` |
| `allow_logon_queue_notifications` | `true` |

**With no saved credential**, Invigoration sends a zero placeholder in the same format (`US-` then 32 zeros, then `-0000`, base64-encoded), and Battle.net answers with a web challenge. ⚠️ Single source (Invigoration's approach)

**A web challenge** is ChallengeNotify method **3** with `payload_type: "web_auth_url"` and `payload`, the sign-in URL in base64. Check it's `https` on a `battle.net` host before opening it. Send the value the page returns with AuthenticationServer method **7**, `{ "web_credentials": base64 }`. ChallengeNotify method **4** with `passed: false` means the sign-in failed. ✅ Confirmed live

**LogonResult** arrives as AuthenticationClient method **5**. ✅ Confirmed live

| Key | Meaning |
|---|---|
| `error_code` | 0 on success |
| `session_key` | base64. Goes into AuthSession. |
| `account_id` | `{ high, low }` |
| `game_account_id` | An array of `{ high, low }`. The first is the SC:R game account. |
| `connected_region` | 1 for the Americas |
| `battle_tag` | For example `Tagban#1555` |

**Get a new saved credential straight away** with AuthenticationServer method **8**, `{ "program": 21297 }` (`"S1"` as a big-endian number, `0x5331`). The reply's `web_credentials` is the credential to present next time. ✅ Confirmed live. Save it at once, not at the end: it stays valid even if a later step fails.

## Aurora: ConnectToServer

The classic server's address comes from **GameUtilities method 1** (ProcessClientRequest). The body is a list of attributes, each `{ "name": …, "value": { "string_value": … } }`. ✅ Confirmed live

| Attribute | Value |
|---|---|
| `client_request` | `classic.protocol.v1.aurora.ConnectToServerRequest` |
| `protobuf` | The request below, as base64 |
| `server_instance` | `Release` |

**ConnectToServerRequest:**

| # | Field | Value |
|---|---|---|
| 2 | program | `0x5331` (`S1`) |
| 3 | game version | `1.23.10.13515` |
| 4 | platform | `0x4D633634` (`Mc64`) |

**The reply's attributes** hold `client_response` = `classic.protocol.v1.aurora.ConnectToServerResponse`, and `protobuf`, base64 (the value may be a `blob_value` or a `string_value`). ✅ Confirmed live

| # | Field | Value |
|---|---|---|
| 1 | URL | The classic WebSocket, a `wss://` URL on a `battle.net` host |
| 2 | ticket | **56 bytes**, used once in AuthSession |

- **Never hard-code the classic host.** Use the URL Battle.net returns, after checking it's `wss` on `battle.net`.
- **Connect to path `/S1/v2/rpc/client`** on that host, keeping any query Battle.net added. ⚠️ Single source (sc1-research). Warcraft III: Reforged uses `/W3/…`.
- **The request names no gateway.** The gateway is chosen later, by the character passed to Legacy.Connect. ✅ Confirmed live: one sign-in listed characters on both U.S. West and U.S. East, and played on U.S. West. Playing on U.S. East this way hasn't been tried live yet. ⚠️

## Classic: the WebSocket and its seed

The classic connection is TLS on port 443, then an ordinary RFC 6455 upgrade. Invigoration sends no `Sec-WebSocket-Protocol`. ✅ Confirmed live

**The scrambling seed is folded from the client's own `Sec-WebSocket-Key`.** Nothing about it is sent. So the client must know the exact key it put in the handshake. Many WebSocket libraries hide it, and Invigoration writes its own handshake for this reason. ✅ Confirmed live; the fold is from sc1-research, which matched it against the retail client.

All arithmetic is unsigned 32-bit.

```
nonce = base64-decode(Sec-WebSocket-Key)        # always 16 bytes
seed  = (program << 7) XOR 0x10831105           # program = 0x5331 ("S1")

for i = 0 to 15:
    b       = nonce[i], sign-extended to 32 bits   # 0x80..0xFF become 0xFFFFFF80..0xFFFFFFFF
    shifted = (b << ((i MOD 4) × 8)) AND 0xFFFFFFFF
    if i < 4: seed = seed OR  shifted
    else:     seed = seed XOR shifted
```

For SC:R the starting value is `0x10AA8985`. Warcraft III: Reforged would use program `0x5733` (`W3`). ⚠️ Single source (sc1-research)

**Test vector** (sc1-research's captured connection):

| | |
|---|---|
| `Sec-WebSocket-Key` | `RNam504UhTYmXuZv34oqHA==` |
| Nonce | `44 d6 a6 e7 4e 14 85 36 26 5e e6 6f df 8a 2a 1c` |
| Seed | `0xBAB6E072` |
| First 4 bytes of AuthSession, plain | `00 44 08 87` |
| The same 4 bytes, scrambled | `e5 c5 bf 2c` |

The rule was run here and gave both values.

The scrambling itself, and the RPC framing inside it, are on [StarCraft: Remastered chat](/bnet2/scr-chat/#classic-connection-scrambling).

### Classic header fields, corrected

sc1-research's field list, confirmed live, differs from the older one on the chat page in two places:

| # | Field | Value |
|---|---|---|
| 6 | Object ID | **Not a status.** `0` on the client's requests. A reply to a server call must **echo** the call's object ID. |
| 12 | Request trace | Bytes, `RT-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX` with random hex digits. Sent on the AuthSession call only. |

Replies carry no status to check. A refused request shows up as a chat error message, or as a step that never gets its answer. ✅ Confirmed live

## Classic: AuthSession

Service `0x17CDFF07`, method `0x95F59163`. It's the first call on the classic socket. ✅ Confirmed live. Field layout from sc1-research.

| # | Field | Type | Value |
|---|---|---|---|
| 1 | ticket | bytes | The 56-byte ticket from ConnectToServer |
| 2 | session info | message | Below |
| 3 | program | varint | `0x5331` (`S1`) |
| 4 | game version | string | `1.23.10.13515` |
| 5 | client identity | string | A 20-byte install identity, as base64 text. sc1-research records the retail client's value. |
| 6 | capabilities | varint | `0x00030100` |
| 7 | platform | varint | `0x4D633634` (`Mc64`) |
| 8 | ? | varint | `1`. 🛑 Meaning unknown |

**Session info** (field 2):

| # | Field | Type | Value |
|---|---|---|---|
| 1 | session key | bytes | From LogonResult |
| 2 | application version | varint | `65559` |
| 3 | locale | varint | `0x656E5553` (`enUS`) |
| 4 | platform | varint | `0x4D633634` (`Mc64`) |
| 6 | account IDs | message | `{1: account high, 2: account low, 3: game account high, 4: game account low}`, from LogonResult |
| 7 | session type | varint | `0x44444354` (`DDCT`) |

**The reply** carries the server's proof in field 3. It was 64 bytes in every live session. Invigoration only checks that it's 48 or 64 bytes long; what it proves isn't known. 🛑

These are the identity constants of retail build 1.23.10.13515. Battle.net checks them. ⚠️ Single source (sc1-research)

## Classic: the startup calls

After AuthSession, the client makes these calls **in this order, each after the one before is answered.** Service and method are 32-bit hashes, sent as varints. ✅ Confirmed live

| Step | Service | Method | Body | Reply |
|---|---|---|---|---|
| GetToons | GameAccount `0x354252A4` | `0xBC18EDE5` | empty | The characters (below) |
| SetGameVersion | GameVersion `0x3D930F0E` | `0xD48DE460` | `S(1, "1.23.10.13515")` | empty |
| Legacy.Connect | Legacy `0xD0C0F33D` | `0x607716CD` | `V(1, character ID)` | empty |
| SetOnline | LegacyChat `0xF4E11A78` | `0xD5EBA117` | empty | empty |
| LegacyChat.Connect | LegacyChat `0xF4E11A78` | `0x78D3F5A8` | `V(1, 0)` | The channel list |

`V` and `S` are the [protobuf shorthand](/bnet2/d2r-d4-chat/#protobuf-shorthand).

- **LegacyChat.Connect is the same method as "List channels"** on the chat page. Sent again later, it asks for the channel list again.
- **Legacy.Connect's field 1 is the character ID from GetToons**, not a gateway number. sc1-research sends `1`. A retail capture sent `3` for the character whose ID was 3 (novares). Invigoration sends the chosen character's ID, and that's the character it plays as. ✅ Confirmed live
- **Then join a channel.** The first join, outside any channel, is by ID. See [Channel joins](/bnet2/scr-chat/#channel-joins).
- **On the way out**, Invigoration calls LegacyChat `0x6DEB8B04` (Disconnect) with an empty body before closing. Whether that lets Battle.net end the session sooner is 🛑 unknown.

GetToons' reply and the gateway list are on [StarCraft: Remastered chat](/bnet2/scr-chat/#characters-and-gateways).

### Byte example: Legacy.Connect

Character 1, token 4, before scrambling:

```
00 1a                              header length: 26
08 bd e6 83 86 0d                  service 0xD0C0F33D (Legacy)
10 cd ad dc 83 06                  method  0x607716CD (Connect)
18 04                              token 4
20 f1 c9 88 b4 09                  routing 0x968224F1
28 02                              size 2
30 00                              object ID 0
48 00                              request
08 01                              V(1, 1): character 1
```

Scrambled with the test vector's seed `0xBAB6E072`, it goes on the wire as `e5 9b bf 16 ce 3d 75 a2 … be 51 e2 da`. Built here from the rules on this page.

### Other calls during startup

Battle.net makes several calls of its own while startup runs. Every one needs the usual reply ([how](/bnet2/scr-chat/#legacychat-receiving)), even when its meaning is unknown. ✅ Confirmed live

| Service / method | When | Meaning |
|---|---|---|
| `0x2FD59FA3` / `0xF5570066` | During AuthSession, five times | GatewayUpdate, one per gateway |
| `0xAA4E1E00` / `0xEC7E2FD1` | After AuthSession, once per friend, then on changes | FriendUpdated ([layout](/bnet2/scr-chat/#friends)) |
| `0x6781876B` / `0x799CF7BD` | Sometimes many times, before the gateways | 🛑 Unknown |
| `0x2B740BA5` / `0x836B9689` | During AuthSession | 🛑 Unknown |
| `0x924CCFDA` / `0xF90D37BF` and `0x8ECE5580` | During AuthSession | 🛑 Unknown |
| `0x17CDFF07` / `0xF2C64BA6` and `0xA9CB45FC` | After AuthSession | 🛑 Unknown |
| `0x354252A4` / `0xF75CAEE5` | After AuthSession | 🛑 Unknown |
| `0x5AEF361A` / `0xDADDB5B7` | After the first join | 🛑 Unknown |

## The 6-second limit

**Battle.net closes the classic socket about 6 seconds after it opens if startup isn't finished.** In one live session the socket opened at 02.200 and closed at 08.051, with GetToons sent at 03.056 and never answered. ✅ Confirmed live

A normal startup, from the socket opening to LegacyChat.Connect's reply, took about 1.5 seconds. So:

- **Send each startup call as soon as the one before is answered.** Don't route replies through anything slow.
- **Don't wait for a person** between AuthSession and LegacyChat.Connect. Choose the character before connecting, or sign in once only to list characters, close, and connect again.

## The stall after a recent session

**Straight after another SC:R session on the same account ends, a new one can stall.** AuthSession succeeds, then GetToons is never answered, and the 6-second limit closes the socket. ✅ Confirmed live

- It happened when connecting right after a sign-in that only listed characters and then closed.
- A retry 5 seconds later stalled the same way. One about 50 seconds later went through.
- It also happened once with no SC:R session on the account in the previous hour, and a retry 10 seconds later went through. So a recent session isn't the only cause. ✅ Confirmed live
- Invigoration retries every 10 seconds, up to six times. A connect that stalls once is typically in chat about 20 seconds after starting.

**Leave properly.** Before closing, Invigoration sends Aurora's ConnectionService **RequestDisconnect** (method 7, body `{"error_code": 0}`, no reply), as a Battle.net client does when it logs out, and LegacyChat's Disconnect on the classic socket. Whether that shortens the stall for the next session isn't confirmed. ⚠️
- The likely cause is that Battle.net still treats the account's last SC:R session as live. ⚠️ Inferred. It suggests **one SC:R session per account at a time**, so two gateways at once on one account probably won't work. That hasn't been tested. 🛑

**An SC:R session and a StarCraft II session on one account at once do work.** ✅ Confirmed live
