---
title: "MCP_JOINGAME"
layout: "packet"
protocol: "MCP"
message_id: "0x04"
categories: ["MCP", "Games"]
products: [D2DV, D2XP]
summary: "Joins a closed-realm game. On success the client leaves the realm and connects to the game server."
c2s:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: verified }
    - { type: "STRING", name: "Game name", confidence: verified }
    - { type: "STRING", name: "Password", confidence: verified }
s2c:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: verified }
    - { type: "UINT16", name: "Game token", notes: "The game's number on the game server.", confidence: verified }
    - { type: "UINT16", name: "Unused", notes: "`0`.", confidence: verified }
    - { type: "UINT32", name: "Game server address", notes: "An IPv4 address in **network byte order**.", confidence: verified }
    - { type: "UINT32", name: "Game hash", confidence: verified }
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Joined. The client closes the realm connection and connects to the game server on TCP port 4000.", confidence: verified }
        - { value: "0x29", meaning: "Wrong password.", confidence: verified }
        - { value: "0x2A", meaning: "No such game.", confidence: verified }
        - { value: "0x2B", meaning: "Game is full.", confidence: verified }
        - { value: "0x2C", meaning: "The character doesn't meet the game's level requirement.", confidence: verified }
        - { value: "0x6E", meaning: "A dead hardcore character can't join games.", confidence: single }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

**Every field is sent, even on failure.** The client reads all six fields before it looks at the result, so a failure reply must still include the token, address and hash, as zeros.

The game server (D2GS) listens on port **4000**, and the client can't be told to use another port. The client presents the game token and hash when it logs on to the game server.
