---
title: "MCP_CHARDELETE"
layout: "packet"
protocol: "MCP"
message_id: "0x0A"
categories: ["MCP", "Characters"]
products: [D2DV, D2XP]
summary: "Deletes one of the account's characters."
c2s:
  fields:
    - { type: "UINT16", name: "Request ID", confidence: verified }
    - { type: "STRING", name: "Character name", confidence: verified }
s2c:
  fields:
    - { type: "UINT16", name: "Request ID", notes: "Echoes the request. BNETDocs' layout omits this field.", confidence: verified }
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results (version 1.10 and later)"
      items:
        - { value: "0x00", meaning: "Deleted.", confidence: verified }
        - { value: "0x49", meaning: "No such character on this account.", confidence: verified }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

**The meaning flipped in version 1.10.** In *Diablo II* 1.09 and earlier, `0x49` meant deleted and `0x00` meant not found.
