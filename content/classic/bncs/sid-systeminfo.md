---
title: "SID_SYSTEMINFO"
layout: "packet"
protocol: "BNCS"
message_id: "0x2B"
categories: ["BNCS", "Logon", "Historical"]
products: [SSHR, JSTR]
status: "Historical. *StarCraft* and *Diablo* stopped sending it in version 1.07."
summary: "The client's hardware: processors, memory and free disk space."
c2s:
  when: "Optionally, early in the older logon. There is no reply."
  fields:
    - { type: "UINT32", name: "Number of processors", confidence: verified }
    - { type: "UINT32", name: "Processor architecture", confidence: verified }
    - { type: "UINT32", name: "Processor level", confidence: verified }
    - { type: "UINT32", name: "Processor timing", confidence: verified }
    - { type: "UINT32", name: "Total physical memory", confidence: verified }
    - { type: "UINT32", name: "Total page file", confidence: verified }
    - { type: "UINT32", name: "Free disk space", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---
