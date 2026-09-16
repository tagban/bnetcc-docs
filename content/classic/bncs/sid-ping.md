---
title: "SID_PING"
layout: "packet"
protocol: "BNCS"
message_id: "0x25"
categories: ["BNCS"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Measures latency. The server sends a value and the client sends the same value back."
s2c:
  when: "Sent as soon as a game client connects, and again from time to time."
  fields:
    - { type: "UINT32", name: "Ping value", notes: "Any value the server chooses. The client returns it unchanged.", confidence: verified }
c2s:
  when: "Sent in reply to the server's `SID_PING`."
  fields:
    - { type: "UINT32", name: "Ping value", notes: "The value from the server's `SID_PING`.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "sends `SID_PING` on connect, tested with real clients"
---

The time between the server sending `SID_PING` and the client's reply is the latency shown beside each user in a channel list.

Some clients and bots wait for this message before they continue logging on, so a server should send it as soon as the connection opens instead of waiting to be asked.
