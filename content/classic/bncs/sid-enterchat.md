---
title: "SID_ENTERCHAT"
layout: "packet"
protocol: "BNCS"
message_id: "0x0A"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Moves a logged-on client into chat and tells it the name it will appear under."
c2s:
  when: "After a successful account logon."
  fields:
    - { type: "STRING", name: "Account name", notes: "The server uses the account from the logon, not this field.", confidence: single }
    - { type: "STRING", name: "Statstring", notes: "*Diablo II* uses this to choose which realm character enters chat.", confidence: single }
s2c:
  fields:
    - { type: "STRING", name: "Unique name", notes: "The name this client appears under. If the same account is already online, the server adds a suffix such as `#2`.", confidence: verified }
    - { type: "STRING", name: "Statstring", notes: "The game-specific profile other users see: icon, record and, for *Diablo II*, the character.", confidence: verified }
    - { type: "STRING", name: "Account name", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
---

The client always shows the **unique name** from the reply, which can differ from the account name it logged on with.
