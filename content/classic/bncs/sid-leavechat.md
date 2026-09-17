---
title: "SID_LEAVECHAT"
layout: "packet"
protocol: "BNCS"
message_id: "0x10"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Leaves chat without disconnecting, such as when entering a game or, in *Diablo II*, returning to character select."
c2s:
  when: "No payload, and no reply. To chat again the client sends `SID_JOINCHANNEL`."
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
---
