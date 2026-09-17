---
title: "MCP_CREATEGAME"
layout: "packet"
protocol: "MCP"
message_id: "0x03"
categories: ["MCP", "Games"]
products: [D2DV, D2XP]
summary: "Creates a closed-realm game. It does **not** join it: the client sends `MCP_JOINGAME` next."
c2s:
  fields:
    - { type: "UINT16", name: "Request ID", notes: "Starts at 2 and goes up by 2 with each game created.", confidence: verified }
    - { type: "UINT32", name: "Difficulty", notes: "`0x0000` Normal, `0x1000` Nightmare, `0x2000` Hell.", confidence: verified }
    - { type: "UINT8", name: "Unused", notes: "`1`.", confidence: verified }
    - { type: "UINT8", name: "Level difference allowed", notes: "`0xFF` for no limit.", confidence: single }
    - { type: "UINT8", name: "Maximum players", confidence: single }
    - { type: "STRING", name: "Game name", notes: "Up to 15 characters.", confidence: verified }
    - { type: "STRING", name: "Password", confidence: verified }
    - { type: "STRING", name: "Description", confidence: verified }
s2c:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: verified }
    - { type: "UINT16", name: "Game token", confidence: verified }
    - { type: "UINT16", name: "Unused", notes: "`0`.", confidence: verified }
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Created.", confidence: verified }
        - { value: "0x1E", meaning: "Game name not valid.", confidence: verified }
        - { value: "0x1F", meaning: "A game with that name already exists.", confidence: verified }
        - { value: "0x20", meaning: "Game servers are down. The client shows \"Server Down\".", confidence: verified }
        - { value: "0x6E", meaning: "A dead hardcore character can't create games.", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
