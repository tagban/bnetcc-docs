---
title: "SID_NULL"
layout: "packet"
protocol: "BNCS"
message_id: "0x00"
categories: ["BNCS"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Keep-alive. An empty message both sides may send so an idle connection stays open."
c2s:
  when: "Every few minutes while the connection is otherwise quiet."
s2c:
  when: "From time to time. The client doesn't need to reply."
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

`SID_NULL` is exactly the 4-byte header, `FF 00 04 00`. Sending it regularly lets either side notice a connection that has silently died, such as after a network drop.
