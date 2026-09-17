---
title: "MCP_MOTD"
layout: "packet"
protocol: "MCP"
message_id: "0x12"
categories: ["MCP"]
products: [D2DV, D2XP]
summary: "Asks for the realm's message of the day, shown in the chat lobby."
c2s:
  when: "After a character is selected or created."
s2c:
  fields:
    - { type: "UINT8", name: "Unused", notes: "Ignored by the client.", confidence: verified }
    - { type: "STRING", name: "Message of the day", confidence: verified }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
