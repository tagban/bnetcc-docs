---
title: "SID_JOINCHANNEL"
layout: "packet"
protocol: "BNCS"
message_id: "0x0C"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Joins a chat channel."
c2s:
  fields:
    - { type: "UINT32", name: "Flags", notes: "How to join. See the table below.", confidence: verified }
    - { type: "STRING", name: "Channel", notes: "Up to 31 characters.", confidence: verified }
  values:
    - name: "Flags"
      items:
        - { value: "0x00", meaning: "Join only if the channel already exists.", confidence: single }
        - { value: "0x01", meaning: "First join after logging on. The server may choose the product's home channel and sends its message of the day.", confidence: single }
        - { value: "0x02", meaning: "Forced join. No message of the day.", confidence: single }
        - { value: "0x05", meaning: "*Diablo II*'s first join.", confidence: single }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
---

There is no reply with this message's ID. The server answers with `SID_CHATEVENT` messages: `EID_CHANNEL` naming the channel joined, then one `EID_SHOWUSER` for every user already there, including the joining client. If the join is refused, it sends `EID_CHANNELFULL` or `EID_CHANNELRESTRICTED` instead.
