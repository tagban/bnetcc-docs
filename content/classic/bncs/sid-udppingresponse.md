---
title: "SID_UDPPINGRESPONSE"
layout: "packet"
protocol: "BNCS"
message_id: "0x14"
categories: ["BNCS", "Logon"]
products: [STAR, SEXP, SSHR, JSTR, DRTL, DSHR, W2BN]
summary: "Tells the server the UDP test worked, by echoing the code the server sent over UDP."
c2s:
  when: "After the client receives `PKT_SERVERPING` over UDP, and before `SID_ENTERCHAT`."
  fields:
    - { type: "UINT32", name: "UDP code", notes: "The value from `PKT_SERVERPING`. Official servers used `bnet`.", confidence: verified }
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "older logon tested with a real Warcraft II client"
---

**If the client never sends this,** the server marks the user with the **No UDP** flag (`0x10`), which other players see as a plug icon, and the client can't create or join games.

**Timing matters on official servers.** Sending this before the version check starts, or after entering chat, got clients disconnected.

**Diablo is unresolved.** BNETDocs lists *Diablo* among the games that send this message. It also records that official Battle.net always showed *Diablo* users with the No UDP flag regardless. This hasn't been confirmed with a real *Diablo* client.
