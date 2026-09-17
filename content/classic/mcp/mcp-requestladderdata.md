---
title: "MCP_REQUESTLADDERDATA"
layout: "packet"
protocol: "MCP"
message_id: "0x11"
categories: ["MCP", "Ladder"]
products: [D2DV, D2XP]
summary: "Asks for 16 entries of a ladder, starting at a given rank."
c2s:
  fields:
    - { type: "UINT8", name: "Ladder type", notes: "See the table below.", confidence: verified }
    - { type: "UINT16", name: "Starting position", notes: "Zero-based. The official client always asks in steps of 16.", confidence: verified }
  values:
    - name: "Ladder types"
      items:
        - { value: "0x00", meaning: "Classic hardcore, all classes. `0x01`–`0x05` are one class each, in class order.", confidence: verified }
        - { value: "0x09", meaning: "Classic softcore, all classes. `0x0A`–`0x0E` are one class each.", confidence: verified }
        - { value: "0x13", meaning: "*Lord of Destruction* hardcore, all classes. `0x14`–`0x1A` are one class each.", confidence: verified }
        - { value: "0x1B", meaning: "*Lord of Destruction* softcore, all classes. `0x1C`–`0x22` are one class each.", confidence: verified }
s2c:
  fields:
    - { type: "UINT8", name: "Ladder type", confidence: verified }
    - { type: "UINT16", name: "Total size", notes: "Of the whole reply, across all its messages.", confidence: verified }
    - { type: "UINT16", name: "This message's size", confidence: verified }
    - { type: "UINT16", name: "Offset", notes: "Where this message's data starts within the whole reply. Large replies arrive in pieces.", confidence: verified }
    - { type: "UINT32", name: "Rank of first entry", confidence: verified }
    - { type: "UINT32", name: "Number of entries", confidence: verified }
    - { type: "UINT32", name: "Unused", notes: "`16`.", confidence: verified }
    - repeat: "For each entry"
      fields:
        - { type: "UINT64", name: "Experience", confidence: verified }
        - { type: "UINT8", name: "Flags", notes: "Class in the low bits; `0x08` your own character, `0x10` dead, `0x20` hardcore, `0x40` *Lord of Destruction*.", confidence: verified }
        - { type: "UINT8", name: "Acts completed", confidence: verified }
        - { type: "UINT16", name: "Level", confidence: verified }
        - { type: "UINT8 × 16", name: "Name", notes: "Padded with zeros.", confidence: verified }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

Official ladders list down to rank 500.
