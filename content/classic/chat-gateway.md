---
title: "Chat gateway (telnet)"
categories: ["Classic Battle.net", "Historical"]
products: [CHAT]
summary: "A plain-text way into Battle.net chat, used by early bots and by people with a telnet program. Retired by Blizzard in 2005."
bnetdocs_documents: [17, 31, 10]
sources:
  - name: "Command Center: bnetcc-proto line framing"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetcc-proto/src/line.rs"
    note: "message format and line handling"
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
    note: "protocol selector bytes"
---

**This protocol is historical.** Blizzard deprecated the chat gateway in 2005 and later turned it off: official servers now disconnect any client that sends its protocol byte. Community servers may still offer it.

The chat gateway let anything that could open a TCP connection and send lines of text join Battle.net chat, with no game, CD key or version check. It could only chat. See [Chat gateway: logon](/classic/sequences/chat-gateway-logon/) for the handshake step by step.

## Starting a session

1. Connect to TCP port 6112 and send the byte `0x03`. Some servers also accept a lowercase `c` (`0x63`).
2. Send the byte `0x04` followed by CR LF to begin logging on.
3. The server asks for the account name, then the password. Both are sent as **plain text**, each ending with CR LF.

The password travels unencrypted. The server lowercases it before checking, which matches what the game clients do before hashing.

## Rules for gateway users

- Users appear with the **`CHAT`** product and always carry the **No UDP** flag (`0x10`).
- They can't create or join games.
- On official Battle.net they could only enter a few public channels: *Blizzard Tech Support*, *Open Tech Support*, *Public Chat* and *The Void*.
- Other users' statstrings aren't sent, so there are no icons, records or characters.
- Sending a binary game message over the gateway got the connection closed and the address briefly banned.

## Message format

Every line the server sends has the form:

```
<id> <NAME> <data>
```

- **`id`** is four decimal digits.
- **`NAME`** is a word that repeats the meaning of the id. It can be ignored when parsing.
- **`data`** may contain spaces. When a message has no data, there's no space after the name.
- **User flags** appear as four hexadecimal digits, such as `0010`.
- **Product codes** appear forwards (`STAR`), not reversed as in binary messages.
- **Quoted messages** are not escaped. The quotes are simply decoration and can be removed.

### How the ids are numbered

The ids mirror the binary protocol:

- **1000 plus a chat event ID**, written in decimal, is a chat event. `EID_INFO` is `0x12`, which is 18, so an information message is `1018`.
- **2000 plus a BNCS message ID**, written in decimal, is a converted game message. `SID_ENTERCHAT` is `0x0A`, which is 10, so the unique-name message is `2010`.

## Messages

| Id | Name | Data | Binary equivalent |
|---|---|---|---|
| `1001` | USER | `<name> <flags> [<product>]`, one per user already in the channel | `EID_SHOWUSER` |
| `1002` | JOIN | `<name> <flags> [<product>]`, a user joined | `EID_JOIN` |
| `1003` | LEAVE | `<name> <flags>`, a user left | `EID_LEAVE` |
| `1004` | WHISPER | `<name> <flags> "<text>"`, a whisper to you | `EID_WHISPER` |
| `1005` | TALK | `<name> <flags> "<text>"`, another user spoke. Your own messages are **not** echoed back. | `EID_TALK` |
| `1006` | BROADCAST | `"<text>"`, a server announcement, with no user name | `EID_BROADCAST` |
| `1007` | CHANNEL | `"<channel>"`, you entered a channel. Channel flags aren't included. | `EID_CHANNEL` |
| `1009` | USER | `<name> <flags> [<product>]`, a user's flags changed | `EID_USERFLAGS` |
| `1010` | WHISPER | `<name> <flags> "<text>"`, your whisper was sent. When whispering friends, the name is `your friends`, which contains a space. | `EID_WHISPERSENT` |
| `1018` | INFO | `"<text>"`, information from the server | `EID_INFO` |
| `1019` | ERROR | `"<text>"`, an error from the server | `EID_ERROR` |
| `1023` | EMOTE | `<name> <flags> "<text>"`, an emote, including your own | `EID_EMOTE` |
| `2000` | NULL | none. Sent about every 30 seconds while idle. | `SID_NULL` |
| `2010` | NAME | `<name>`, your unique name in chat, such as `JoeUser#2` | `SID_ENTERCHAT` |

The square brackets around the product are part of the message.

## Sending

After logging on, every line the client sends is handled exactly like the text of `SID_CHATCOMMAND`: plain text talks in the channel, and lines starting with `/` are commands. Text sent without a line ending is joined to the next line.

## Staying connected

The server sends `2000 NULL` about every 30 seconds of inactivity, but official Battle.net never disconnected gateway users for being idle. Many gateway bots still sent a harmless command such as `/time` now and then to keep the connection active.

## How servers handle the gateway

A server that offers the gateway reads line by line, not byte by byte, and must cap line length so an endless line can't exhaust its memory. It should also accept a bare LF line ending, which bots written on Unix systems often send. Command Center's gateway currently greets the client and handles lines, and is being extended toward full chat.
