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
    - { type: "UINT32", name: "Flags", notes: "`0x800` when the playing character is hardcore, otherwise `0`.", confidence: verified }
    - { type: "STRING", name: "Search text", notes: "1.14d always sends it empty. When set, only games whose names contain it are returned.", confidence: verified }
s2c:
  when: "Once for every game, then once more to end the list."
  fields:
    - { type: "UINT16", name: "Request ID", notes: "Echoes the request.", confidence: verified }
    - { type: "UINT32", name: "Token", notes: "The game's number on the server. The client keeps one entry per token (its low 16 bits).", confidence: verified }
    - { type: "UINT8", name: "Players", confidence: verified }
    - { type: "UINT32", name: "Status", notes: "Game flags (the client stores nothing else from it). `0xFFFFFFFE` ends the list; `0xFFFFFFFF` makes the client drop the list panel, so never send it in a list.", confidence: verified }
    - { type: "STRING", name: "Game name", notes: "Absent on the final message.", confidence: verified }
    - { type: "STRING", name: "Description", notes: "**The message must end right after it.** With anything more, the client shows the list without this game.", confidence: verified }
sources:
  - name: "Diablo II 1.14d Game.exe"
    note: "the reply handler at 0x0044B2D0 and the lobby loop at 0x00441500, read while building Command Center's game list (October 2026)"
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

**Ending the list.** BNETDocs describes the list as ending with a message whose game name is empty. Command Center ends it with status `0xFFFFFFFE`, stopping right after that field, and a real 1.14d client accepts that.

**What a realm lists.** ✅ The client re-asks every 15 seconds and holds up to 1000 entries. ⚠️ Command Center lists only games the asking character could join — the same expansion, hardcore and ladder kind, a difficulty it has reached, within the game's level difference, and not full — and lists password-protected games, since the client has a password box for them. That the official realm filtered the same way is reconstructed, not captured.
