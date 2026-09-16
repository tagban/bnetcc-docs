---
title: "SID_LOCALEINFO"
layout: "packet"
protocol: "BNCS"
message_id: "0x12"
categories: ["BNCS", "Logon", "Historical"]
products: [DRTL, DSHR, W2BN, SSHR, JSTR]
status: "Historical. Newer games send this information inside `SID_AUTH_INFO`."
summary: "The client's clock, time zone, language and country."
c2s:
  when: "Right after `SID_CLIENTID` or `SID_CLIENTID2`. There is no reply."
  fields:
    - { type: "FILETIME", name: "System time", notes: "UTC.", confidence: verified }
    - { type: "FILETIME", name: "Local time", confidence: verified }
    - { type: "INT32", name: "Time zone bias", notes: "Minutes from UTC.", confidence: verified }
    - { type: "UINT32", name: "System locale ID", confidence: verified }
    - { type: "UINT32", name: "User locale ID", confidence: verified }
    - { type: "UINT32", name: "User language ID", confidence: verified }
    - { type: "STRING", name: "Language abbreviation", notes: "For example `ENU`.", confidence: verified }
    - { type: "STRING", name: "Country code", confidence: verified }
    - { type: "STRING", name: "Country abbreviation", notes: "For example `USA`.", confidence: verified }
    - { type: "STRING", name: "Country name", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

*Diablo* and *Warcraft II* always send this message. For *StarCraft Shareware* and *StarCraft Japanese* it is optional.
