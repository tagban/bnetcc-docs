---
title: "MCP_CREATEQUEUE"
layout: "packet"
protocol: "MCP"
message_id: "0x14"
categories: ["MCP", "Games"]
products: [D2DV, D2XP]
summary: "Tells the client its place in line to create a game, when the realm is busy."
s2c:
  fields:
    - { type: "UINT32", name: "Position", confidence: single }
---
