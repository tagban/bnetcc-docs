---
title: "SID_CLIENTID"
layout: "packet"
protocol: "BNCS"
message_id: "0x05"
categories: ["BNCS", "Logon", "Historical"]
products: [SSHR, JSTR, DRTL, DSHR, W2BN]
status: "Historical. Only the older logon uses it, and the registration fields are no longer used."
summary: "The client's first message in the oldest logon: registration numbers and the computer's LAN names."
c2s:
  when: "Sent right after the protocol byte by *StarCraft Shareware* and *StarCraft Japanese*. *Diablo* and *Warcraft II* send `SID_CLIENTID2` instead."
  fields:
    - { type: "UINT32", name: "Registration version", notes: "No longer used. May be `0`.", confidence: verified }
    - { type: "UINT32", name: "Registration authority", notes: "No longer used. May be `0`.", confidence: verified }
    - { type: "UINT32", name: "Account number", notes: "No longer used. May be `0`.", confidence: verified }
    - { type: "UINT32", name: "Registration token", notes: "No longer used. May be `0`.", confidence: verified }
    - { type: "STRING", name: "LAN computer name", notes: "The Windows computer name.", confidence: verified }
    - { type: "STRING", name: "LAN user name", notes: "The name of the Windows user who is logged in.", confidence: verified }
s2c:
  when: "Sent in reply to `SID_CLIENTID` or `SID_CLIENTID2`, before `SID_LOGONCHALLENGE` or `SID_LOGONCHALLENGEEX`."
  fields:
    - { type: "UINT32", name: "Registration version", notes: "`0`.", confidence: verified }
    - { type: "UINT32", name: "Registration authority", notes: "`0`.", confidence: verified }
    - { type: "UINT32", name: "Account number", notes: "`0`.", confidence: verified }
    - { type: "UINT32", name: "Registration token", notes: "`0`.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

Early Battle.net used these fields to hand out and check registration numbers for each copy of the game. The server once replied with new numbers when the client's were invalid. Today every registration field is zero in both directions, and only the two LAN names still carry data.
