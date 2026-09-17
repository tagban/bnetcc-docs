---
title: "MCP_GAMELIST"
layout: "packet"
protocol: "MCP"
message_id: "0x05"
categories: ["MCP", "Games"]
products: [D2DV, D2XP]
summary: "Lists the realm's open games, **one reply message per game**."
c2s:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: verified }
    - { type: "UINT32", name: "Unused", notes: "`0`.", confidence: verified }
    - { type: "STRING", name: "Search text", notes: "Normally empty. When set, only games whose names contain it are returned.", confidence: single }
s2c:
  when: "Once for every game, then once more to end the list."
  fields:
    - { type: "UINT16", name: "Request ID", notes: "Echoes the request.", confidence: verified }
    - { type: "UINT32", name: "Index", notes: "The game's number on the server.", confidence: verified }
    - { type: "UINT8", name: "Players", confidence: verified }
    - { type: "UINT32", name: "Status", notes: "Game flags. On the final message that ends the list, `0xFFFFFFFE`.", confidence: verified }
    - { type: "STRING", name: "Game name", notes: "Empty on the final message.", confidence: single }
    - { type: "STRING", name: "Description", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

**Ending the list.** BNETDocs describes the list as ending with a message whose game name is empty. Command Center ends it with status `0xFFFFFFFE`, stopping right after that field, and a real 1.14d client accepts that.
