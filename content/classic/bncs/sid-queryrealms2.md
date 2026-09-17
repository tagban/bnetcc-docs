---
title: "SID_QUERYREALMS2"
layout: "packet"
protocol: "BNCS"
message_id: "0x40"
categories: ["BNCS", "Diablo II realm"]
products: [D2DV, D2XP]
summary: "Asks which *Diablo II* realms this Battle.net server offers."
c2s:
  when: "After logging on, and again each time the player returns to character select."
s2c:
  fields:
    - { type: "UINT32", name: "Unused", notes: "`0`.", confidence: verified }
    - { type: "UINT32", name: "Number of realms", confidence: verified }
    - repeat: "For each realm"
      fields:
        - { type: "UINT32", name: "Unused", notes: "`1`.", confidence: verified }
        - { type: "STRING", name: "Realm name", confidence: verified }
        - { type: "STRING", name: "Description", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "tested with a real Diablo II: Lord of Destruction 1.14d client"
---
