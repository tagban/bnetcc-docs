---
title: "SID_CHATCOMMAND"
layout: "packet"
protocol: "BNCS"
message_id: "0x0E"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Sends a chat message or a slash command such as `/whisper` or `/join`."
c2s:
  fields:
    - { type: "STRING", name: "Text", notes: "Up to 223 characters. Text starting with `/` is a command.", confidence: verified }
sources:
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
    note: "length limit"
---

There is no reply with this message's ID. The server answers with `SID_CHATEVENT`: `EID_TALK` to everyone in the channel for a message, or `EID_INFO` or `EID_ERROR` in reply to a command.

Official clients limit a message to 224 bytes including its terminating zero. Real Battle.net disconnected clients that sent a carriage return or line feed inside the text.
