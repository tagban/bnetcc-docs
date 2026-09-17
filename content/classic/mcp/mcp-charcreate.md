---
title: "MCP_CHARCREATE"
layout: "packet"
protocol: "MCP"
message_id: "0x02"
categories: ["MCP", "Characters"]
products: [D2DV, D2XP]
summary: "Creates a character. The new character becomes the one the client plays straight away."
c2s:
  fields:
    - { type: "UINT32", name: "Class", notes: "See the table below.", confidence: verified }
    - { type: "UINT16", name: "Flags", notes: "Hardcore, expansion and ladder, from the creation screen's checkboxes. Easy to miss: it is 16 bits.", confidence: verified }
    - { type: "STRING", name: "Name", notes: "2 to 15 letters, with at most one `-` or `_`, not at either end.", confidence: verified }
  values:
    - name: "Classes"
      items:
        - { value: "0x00", meaning: "Amazon", confidence: verified }
        - { value: "0x01", meaning: "Sorceress", confidence: verified }
        - { value: "0x02", meaning: "Necromancer", confidence: verified }
        - { value: "0x03", meaning: "Paladin", confidence: verified }
        - { value: "0x04", meaning: "Barbarian", confidence: verified }
        - { value: "0x05", meaning: "Druid (*Lord of Destruction* only)", confidence: verified }
        - { value: "0x06", meaning: "Assassin (*Lord of Destruction* only)", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Created.", confidence: verified }
        - { value: "0x14", meaning: "A character with that name already exists. BNETDocs also lists this for reaching the character limit.", confidence: verified }
        - { value: "0x15", meaning: "Name, class or flags not allowed.", confidence: verified }
sources:
  - name: "Command Center: bnetccd realm server"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/realm.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---

**No `MCP_CHARLOGON` follows.** A real client that has just created a character goes straight on to `MCP_MOTD` and entering chat as that character. A realm should treat the new character as selected.

When the player ticks **Ladder**, the client shows its own ladder notice before sending this message. That notice isn't a server error.
