---
title: "Connecting to a Classic server"
categories: ["Classic Battle.net"]
sources:
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
    note: "framing, selector byte and ports, cross-checked against Atlas and gowarcraft3"
---

## Ports

| Port | Transport | Used for |
|---|---|---|
| 6112 | TCP | The Battle.net connection itself (BNCS), for every Classic game and the chat gateway |
| 6112 | UDP | Connectivity tests between server and client, and peer-to-peer game traffic for *Diablo*, *StarCraft* and *Warcraft II* |
| 6112 | TCP | *Warcraft III* game hosting (the player can change this port) |
| Given by the server | TCP | The *Diablo II* realm (MCP). The address and port arrive in `SID_LOGONREALMEX`. |
| 4000 | TCP | *Diablo II* game servers. The client cannot be told to use another port. |

## The first byte: choosing a protocol

Right after the TCP connection opens, the client sends **one byte** that tells the server which protocol follows. The server does not answer this byte.

| Byte | Protocol that follows | Confidence |
|---|---|---|
| `0x01` | BNCS, the game protocol. *Diablo II* also sends this on its realm connection. | ✅ Verified |
| `0x02` | BNFTP, file transfer (version-check files, `icons.bni`, terms of service, advertisement banners) | ✅ Verified |
| `0x03` | The chat gateway (telnet), now historical | ✅ Verified |

A server that receives any other first byte should close the connection without replying.

## How messages are framed

Different protocols in the Classic family frame their messages differently. Mixing them up is the most common mistake when writing a client or server.

| Protocol | Header | Length counts |
|---|---|---|
| BNCS | `FF`, message ID (1 byte), length (2 bytes) | the whole message, including its 4-byte header |
| MCP (*Diablo II* realm) | length (2 bytes), message ID (1 byte). There is no `FF`, and the length comes first. | the whole message, including its header |
| W3GS (*Warcraft III* games) | `F7`, message ID (1 byte), length (2 bytes) | the whole message, including its header |
| Chat gateway | Text lines ending in CR LF | — |

An empty BNCS message, such as a keep-alive, is exactly four bytes: `FF 00 04 00`.

## Data types

**Every number is little-endian.**

| Type | Size | Meaning |
|---|---|---|
| `UINT8`, `UINT16`, `UINT32`, `UINT64` | 1, 2, 4, 8 bytes | Unsigned integers |
| `STRING` | varies | Text ending in a zero byte |
| `STRINGLIST` | varies | Several `STRING`s, ending with an empty one |
| `FILETIME` | 8 bytes | A Windows file time: 100-nanosecond intervals since January 1, 1601 |
| `DWORD` (four-character code) | 4 bytes | A code such as `STAR` or `IX86`, stored as a `UINT32`, so its letters appear **reversed** on the wire: `STAR` is sent as `52 41 54 53` (`RATS`) |
| `VOID` | varies | Raw bytes with no further structure |

## Text encoding and limits

- *StarCraft* products (`STAR`, `SEXP`, `SSHR`, `JSTR`) send chat text as UTF-8. The other Classic games use ISO 8859-1.
- Chat messages are limited to 224 bytes, including the terminating zero.
- Channel names are limited to 31 characters, and account names to 15.
