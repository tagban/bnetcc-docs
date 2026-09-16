---
title: "SID_CDKEY"
layout: "packet"
protocol: "BNCS"
message_id: "0x30"
categories: ["BNCS", "Logon", "Historical"]
products: [JSTR]
status: "Historical."
summary: "Sends a 13-character CD key **unhashed**. Only *StarCraft Japanese* used it."
c2s:
  when: "After `SID_REPORTVERSION` passes."
  fields:
    - { type: "UINT32", name: "Spawn", notes: "`1` for a spawned installation.", confidence: verified }
    - { type: "STRING", name: "CD key", notes: "The key itself, in plain text.", confidence: verified }
    - { type: "STRING", name: "Key owner", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
    - { type: "STRING", name: "Key owner", notes: "Can also carry the special values `TOO MANY SPAWNS` or `NO SPAWNING`.", confidence: single }
  values:
    - name: "Results"
      items:
        - { value: "0x01", meaning: "Accepted.", confidence: verified }
        - { value: "0x02", meaning: "Key not valid.", confidence: verified }
        - { value: "0x03", meaning: "Key is for a different game.", confidence: verified }
        - { value: "0x04", meaning: "Key banned.", confidence: verified }
        - { value: "0x05", meaning: "Key in use.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

Official servers reportedly IP-banned clients that sent a key of any other length through this message.
