---
title: "Front messages"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "The protobuf methods and messages StarCraft II uses on Front while signing in."
sources:
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
---

Every fact on this page comes from one source, so it is all ⚠️ single source until checked against another client or project.

## Methods

| Direction | Service / method | Message | Purpose |
|---|---|---|---|
| Client → Server | ConnectionService / 1 | `ConnectRequest` | Opens the RPC session, asking for "bindless" RPC. |
| Client → Server | AuthenticationServer / 1 | `LogonRequest` | Starts signing in. |
| Server → Client | ChallengeNotify / 3 | `ChallengeExternalRequest` | Sends the client to Blizzard's web sign-in. No response. |
| Client → Server | AuthenticationServer / 7 | `VerifyWebCredentialsRequest` | Submits the short-lived credential from the web sign-in. |
| Server → Client | AuthenticationClient / 5 | `LogonResult` | The result: account, game accounts, region and a 64-byte session key. |
| Server → Client | AuthenticationClient / 14 | `GameAccountSelectedRequest` | Reports which game account was selected. |
| Client → Server | AuthenticationServer / 8 | `GenerateWebCredentialsRequest` | Asks for a reusable credential for next time. |
| Client → Server | GameUtilities / 1 | `ClientRequest` | Asks for the StarCraft II handoff to Sunken. |

AuthenticationClient methods 10 through 14 can arrive as callbacks at any time during sign-in: 10 reports a logon update and 14 the game-account selection. Methods 11 to 13 expect no response.

## ConnectRequest

| # | Field | Type |
|---|---|---|
| 1 | `client_id` | ProcessId, optional |
| 2 | `bind_request` | BindRequest, optional |
| 3 | `use_bindless_rpc` | bool, optional, default `true` |

## LogonRequest

| # | Field | Type | StarCraft II sends |
|---|---|---|---|
| 1 | `program` | string | `S2` |
| 2 | `platform` | string | The platform, such as `Mc64` for 64-bit macOS |
| 3 | `locale` | string | For example `enUS` |
| 4 | `email` | string | |
| 5 | `version` | string | The Battle.net SDK identity built into the game. The exact value for each build is on SC2Docs. |
| 6 | `application_version` | int32 | `0` |
| 7 | `public_computer` | bool | |
| 10 | `allow_logon_queue_notifications` | bool, default `false` | |
| 12 | `cached_web_credentials` | bytes | A reusable credential from an earlier sign-in, if there is one |
| 14 | `user_agent` | string | |
| 15 | `device_id` | string | |

## LogonResult

| # | Field | Type |
|---|---|---|
| 1 | `error_code` | uint32, required |
| 2 | `account_id` | EntityId |
| 3 | `game_account_id` | repeated EntityId |
| 4 | `email` | string |
| 5 | `available_region` | repeated uint32 |
| 6 | `connected_region` | uint32 |
| 7 | `battle_tag` | string |
| 8 | `geoip_country` | string |
| 9 | `session_key` | bytes (64 bytes) |
| 10 | `restricted_mode` | bool |
| 11 | `client_id` | string |

## Web credentials

| Message | # | Field | Type |
|---|---|---|---|
| `ChallengeExternalRequest` | 1 | `request_token` | string |
| | 2 | `payload_type` | string |
| | 3 | `payload` | bytes |
| `VerifyWebCredentialsRequest` | 1 | `web_credentials` | bytes |
| `GenerateWebCredentialsRequest` | 1 | `program` | fixed32 |
| `GenerateWebCredentialsResponse` | 1 | `web_credentials` | bytes |
| `GameAccountSelectedRequest` | 1 | `result` | uint32, required |
| | 2 | `game_account_id` | EntityId |

**Two different credentials.** The short-lived credential from the web sign-in is used once, with method 7. The reusable credential from method 8 is sent in `LogonRequest` next time. A client should replace it after every successful use, and fall back to the web sign-in when it's rejected.

## The Sunken handoff: ClientRequest

| # | Field | Type | StarCraft II sends |
|---|---|---|---|
| 1 | `attribute` | repeated Attribute | The attributes below |
| 2 | `host` | ProcessId | Omitted |
| 3 | `account_id` | EntityId | Omitted |
| 4 | `game_account_id` | EntityId | The **first** StarCraft II game account from `LogonResult` |
| 5 | `program` | fixed32 | Omitted |
| 6 | `client_info` | ClientInfo | Omitted |

| Attribute | Type | Value |
|---|---|---|
| `LogonTokenRequest` | string | `0.0.1` |
| `environment` | string | The region, such as `US` |
| `session_key` | blob | The 64-byte session key from `LogonResult` |
| `locale` | string | For example `enUS` |

The response, `ClientResponse`, is another list of attributes. These carry everything Sunken needs:

| Attribute | Contents |
|---|---|
| `address` | The Sunken server's address. The port is 1119 when not given. A bracketed IPv6 address may include a port after the bracket. |
| `session_key` | Exactly 64 bytes, used for the Resume proof and to derive the encryption keys. |
| `account_region` | The region number, 0 to 255. |
| `game_account_name`, `account_mail` | The account's identity. |
| `logon_response` | A bit-packed `LogonResponse3` with status, timeouts, account data and settings. |

## Attributes and variants

An `Attribute` is a name (field 1) and a `Variant` value (field 2). The Variant field number tells you its type:

| # | Type | # | Type |
|---|---|---|---|
| 2 | bool | 7 | embedded message |
| 3 | signed integer (int64) | 8 | four-character code |
| 4 | double | 9 | unsigned integer (uint64) |
| 5 | string | 10 | entity ID |
| 6 | bytes | | |
