---
title: "SID_GETICONDATA"
layout: "packet"
protocol: "BNCS"
message_id: "0x2D"
categories: ["BNCS", "Files"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, WAR3, W3XP]
summary: "Asks which icons file draws user icons in chat, so the client can download it."
c2s:
  when: "After the version check and before entering chat. Official Battle.net disconnected clients that sent it at other times."
s2c:
  fields:
    - { type: "FILETIME", name: "File time", confidence: verified }
    - { type: "STRING", name: "File name", notes: "Such as `icons.bni`. The client downloads it over BNFTP when its own copy is older.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "a real Warcraft II client shows blank icons without this reply"
---
