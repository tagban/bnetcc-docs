---
title: "Front RPC"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "The regional Battle.net connection: protobuf RPC carried in WebSocket messages over TLS."
sources:
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
  - name: "d4-bnet-mitm (a Diablo IV Battle.net proxy)"
    url: "https://github.com/cjbrigato/d4-bnet-mitm"
    note: "independent source used to cross-check the Front framing and RPC header"
---

## Connecting

| Step | Detail | Confidence |
|---|---|---|
| 1 | Open TCP port **1119** to the regional Front server. | ✅ Verified |
| 2 | Start **TLS**. | ✅ Verified |
| 3 | Upgrade to a **WebSocket** (RFC 6455) with the subprotocol **`v1.rpc.battle.net`**. The server must select the same subprotocol, or the client rejects it. | ✅ Verified |

After that, **one binary WebSocket message holds exactly one RPC message.** Messages are limited to 16 MiB.

## Framing

```
offset  size            field
0       2               header length (UINT16, big-endian)
2       header length   RPC header (protobuf bgs.protocol.Header)
...     rest of message RPC body (protobuf, may be empty)
```

- **The 2-byte prefix counts only the header**, not the body. Unlike Classic Battle.net, it is **big-endian**. ✅ Verified
- **The body is whatever remains** of the WebSocket message. ✅ Verified
- **`size` is optional.** If the header includes it, it must equal the body's length. StarCraft II requests may leave it out. ⚠️ Single source

## The RPC header

| # | Field | Type | Meaning | Confidence |
|---|---|---|---|---|
| 1 | `service_id` | uint32, required | `0` on requests. `0xFE` (254) on responses. | ✅ Verified |
| 2 | `method_id` | uint32 | The method within the service. | ✅ Verified |
| 3 | `token` | uint32, required | Matches a response or callback to its request. | ✅ Verified |
| 4 | `object_id` | uint64 | An optional service object being addressed. | ✅ Verified |
| 5 | `size` | uint32 | The body's length in bytes. | ✅ Verified |
| 6 | `status` | uint32 | The call's result code. | ✅ Verified |
| 7 | `error` | repeated message | Structured error details. | ✅ Verified |
| 8 | `timeout` | uint64 | An optional request timeout. | ✅ Verified |
| 9 | `is_response` | bool | Marks a response explicitly. | ✅ Verified |
| 10 | `forward_targets` | repeated message | Optional forwarding targets. | ✅ Verified |
| 11 | `service_hash` | fixed32 | Identifies the service: see below. Little-endian on the wire, like every protobuf fixed32. | ⚠️ Single source |
| 13 | `client_id` | string | An optional client identifier. | ⚠️ Single source |
| 14 | `fanout_target` | repeated message | Optional fan-out targets. | ⚠️ Single source |
| 15 | `client_id_fanout_target` | repeated string | Optional client-ID fan-out targets. | ⚠️ Single source |
| 16 | `client_record` | bytes | An optional opaque client record. | ⚠️ Single source |

## Which service a call is for

A request names its service with `service_hash`: the **32-bit FNV-1a hash of the full protobuf service name**, and `service_id` stays `0`. ⚠️ Single source

```
hash = 0x811C9DC5
for each byte of the service name (UTF-8):
    hash = hash XOR byte
    hash = (hash * 0x01000193) mod 2^32
```

Services used while signing in include:

- `bnet.protocol.connection.ConnectionService`
- `bnet.protocol.authentication.AuthenticationServer` and `AuthenticationClient`
- `bnet.protocol.challenge.ChallengeNotify`
- `bnet.protocol.game_utilities.GameUtilities`
- `bnet.protocol.account.AccountService`
- `bnet.protocol.session.SessionService` and `SessionListener`

**The very first call is special.** `ConnectionService` method 1 (Connect) uses `service_id` `0`, `method_id` `1` and `token` `0`, together with the ConnectionService hash. ⚠️ Single source

## Requests, responses and callbacks

Both sides make calls:

- **Client calls:** the client sends a request with a token. The server answers with `service_id` `0xFE`, the **same token** and a status.
- **Server callbacks:** the server calls a *listener* service on the client, such as `AuthenticationClient`, with its own token. If the method declares a response, the client replies with `service_id` `0xFE`, the callback's token and status `0`, **even when the response body is empty**. Methods declared `NO_RESPONSE` get no reply at all.

**Callbacks can arrive while a request is still waiting for its answer,** so a client must read and dispatch every complete message as it arrives instead of assuming the next message is its reply. Outside the sign-in exchange, StarCraft II only answers `ConnectionService` Echo automatically. ⚠️ Single source
