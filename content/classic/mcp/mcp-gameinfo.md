---
title: "MCP_GAMEINFO"
layout: "packet"
protocol: "MCP"
message_id: "0x06"
categories: ["MCP", "Games"]
products: [D2DV, D2XP]
summary: "Details of one game, requested when the player selects it in the game list."
c2s:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: single }
    - { type: "STRING", name: "Game name", confidence: single }
s2c:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: single }
    - { type: "UINT32", name: "Status", notes: "Game flags. `0` means no information; `0xFFFFFFFE` means the request wasn't valid.", confidence: single }
    - { type: "UINT32", name: "Uptime", notes: "Seconds.", confidence: single }
    - { type: "UINT8", name: "Level restriction", confidence: single }
    - { type: "UINT8", name: "Level difference allowed", confidence: single }
    - { type: "UINT8", name: "Maximum players", confidence: single }
    - { type: "UINT8", name: "Characters in the game", confidence: single }
    - { type: "UINT8 × 16", name: "Class of each character", confidence: single }
    - { type: "UINT8 × 16", name: "Level of each character", confidence: single }
    - { type: "STRING", name: "Description", confidence: single }
    - { type: "STRING × 16", name: "Character names", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
