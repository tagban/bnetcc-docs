---
title: "SID_FRIENDSLIST"
layout: "packet"
protocol: "BNCS"
message_id: "0x65"
categories: ["BNCS", "Friends"]
products: [STAR, SEXP, D2DV, D2XP, WAR3, W3XP]
summary: "Asks for the player's friends list, with where each friend is."
c2s:
  when: "No payload. *Warcraft III* asks right after logging on."
s2c:
  fields:
    - { type: "UINT8", name: "Number of friends", confidence: verified }
    - repeat: "For each friend"
      fields:
        - { type: "STRING", name: "Account name", confidence: single }
        - { type: "UINT8", name: "Status", notes: "Flags: `0x01` mutual, `0x02` do not disturb, `0x04` away.", confidence: single }
        - { type: "UINT8", name: "Location", notes: "`0x00` offline, `0x01` not in chat, `0x02` in chat, `0x03` public game, `0x04` private game, `0x05` private game with a mutual friend.", confidence: single }
        - { type: "DWORD", name: "Product code", notes: "The friend's game, sent backwards (`W3XP` is `PX3W`). `0` when offline.", confidence: single }
        - { type: "STRING", name: "Location name", notes: "The channel or game, when relevant.", confidence: single }
sources:
  - name: "Command Center: WARCRAFT3.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3.md"
---

A reply with zero friends, a single `00` byte, lets the client's friends panel finish loading. *Diablo II* doesn't receive friend updates automatically, so it asks again from time to time.
