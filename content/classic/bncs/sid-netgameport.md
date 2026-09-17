---
title: "SID_NETGAMEPORT"
layout: "packet"
protocol: "BNCS"
message_id: "0x45"
categories: ["BNCS", "Games"]
products: [WAR3, W3XP]
summary: "Tells the server which TCP port this *Warcraft III* client hosts games on."
c2s:
  when: "After logging on. There is no reply."
  fields:
    - { type: "UINT16", name: "Port", notes: "6112 unless the player changed it in the game's settings.", confidence: verified }
sources:
  - name: "Command Center: WARCRAFT3.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3.md"
---

*Warcraft III* games are hosted by a player over TCP. Other players connect straight to the host's address and this port, so the host needs it forwarded.
