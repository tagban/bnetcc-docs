---
title: "SID_GETCHANNELLIST"
layout: "packet"
protocol: "BNCS"
message_id: "0x0B"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Asks for the list of public channels shown in the client's channel picker."
c2s:
  fields:
    - { type: "DWORD", name: "Product code", notes: "Sent backwards: `STAR` is `RATS`.", confidence: single }
s2c:
  fields:
    - { type: "STRINGLIST", name: "Channel names", notes: "Ends with an empty string.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
---
