---
title: "MCP_CHARLIST"
layout: "packet"
protocol: "MCP"
message_id: "0x17"
categories: ["MCP", "Characters", "Historical"]
products: [D2DV, D2XP]
status: "Older form of `MCP_CHARLIST2`, without expiry dates."
summary: "Lists the account's characters, without expiry dates."
c2s:
  fields:
    - { type: "UINT32", name: "Characters to list", confidence: verified }
s2c:
  fields:
    - { type: "UINT16", name: "Characters requested", confidence: verified }
    - { type: "UINT32", name: "Characters on the account", confidence: verified }
    - { type: "UINT16", name: "Characters returned", confidence: verified }
    - repeat: "For each character returned"
      fields:
        - { type: "STRING", name: "Name", confidence: verified }
        - { type: "STRING", name: "Portrait", confidence: verified }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
