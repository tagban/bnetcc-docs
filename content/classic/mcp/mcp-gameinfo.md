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
    - { type: "UINT32", name: "Status", notes: "Game flags, or `0xFFFFFFFF` when the game is gone (the client still draws the panel from the fields that follow).", confidence: verified }
    - { type: "UINT32", name: "Uptime", notes: "Seconds, shown as \"Elapsed Time\".", confidence: verified }
    - { type: "UINT8", name: "Creator's level", notes: "The level the level difference is measured from.", confidence: verified }
    - { type: "UINT8", name: "Level difference", notes: "`0` shows \"Level N\"; `1`–`99` shows a range around the creator's level (kept within 1–99); `100` or more shows no level line.", confidence: verified }
    - { type: "UINT8", name: "Maximum players", notes: "`1`–`7` shows \"Up to N Players\"; anything else shows no line.", confidence: verified }
    - { type: "UINT8", name: "Characters in the game", confidence: verified }
    - { type: "UINT8 × 16", name: "Class of each character", confidence: verified }
    - { type: "UINT8 × 16", name: "Level of each character", confidence: verified }
    - { type: "STRING", name: "Description", notes: "Copied without a length check: keep it to 31 characters.", confidence: verified }
    - { type: "STRING × count", name: "Character names", notes: "One per character in the game, each copied without a length check: keep them to 15.", confidence: verified }
sources:
  - name: "Diablo II 1.14d Game.exe"
    note: "the reply handler at 0x0044ACA0 and the panel drawn by 0x00442EB0, read while building Command Center's game details (October 2026)"
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
