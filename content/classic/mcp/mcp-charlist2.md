---
title: "MCP_CHARLIST2"
layout: "packet"
protocol: "MCP"
message_id: "0x19"
categories: ["MCP", "Characters"]
products: [D2DV, D2XP]
summary: "Lists the account's characters for the character-select screen, with when each one expires."
c2s:
  fields:
    - { type: "UINT32", name: "Characters to list", notes: "The official client asks for 8.", confidence: verified }
s2c:
  fields:
    - { type: "UINT16", name: "Characters requested", confidence: verified }
    - { type: "UINT32", name: "Characters on the account", confidence: verified }
    - { type: "UINT16", name: "Characters returned", confidence: verified }
    - repeat: "For each character returned"
      fields:
        - { type: "UINT32", name: "Expires", notes: "Seconds since January 1, 1970. `0xFFFFFFFF` never expires.", confidence: verified }
        - { type: "STRING", name: "Name", confidence: verified }
        - { type: "STRING", name: "Portrait", notes: "The character's statstring, without the product code and name that chat statstrings start with.", confidence: verified }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

A classic *Diablo II* client can't play *Lord of Destruction* characters, so a realm should leave them out of the list for that client. *Lord of Destruction* sees both kinds.

When the player returns to character select from chat, the client asks again on the realm connection it already has open.
