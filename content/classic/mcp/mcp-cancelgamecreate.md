---
title: "MCP_CANCELGAMECREATE"
layout: "packet"
protocol: "MCP"
message_id: "0x13"
categories: ["MCP", "Games"]
products: [D2DV, D2XP]
summary: "Tells the realm the player gave up on creating a game, such as while waiting in the creation queue."
c2s:
  when: "No payload, and no reply."
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
