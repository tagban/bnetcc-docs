---
title: "StarCraft Shareware and StarCraft Japanese: logon to chat"
layout: "sequence"
categories: ["Sequences", "Historical"]
products: [SSHR, JSTR]
summary: "The oldest logon, used by *StarCraft Shareware* and *StarCraft Japanese*. Both now require an update to a newer *StarCraft*."
bnetdocs_documents: [10]
steps:
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: client, packet: SID_CLIENTID, confidence: single }
  - { from: client, packet: SID_LOCALEINFO, optional: true, confidence: single }
  - { from: client, packet: SID_SYSTEMINFO, optional: true, confidence: single }
  - { from: client, packet: SID_STARTVERSIONING, note: "Names the game (`SSHR` or `JSTR`) and version byte.", confidence: single }
  - { from: server, packet: SID_CLIENTID, confidence: verified }
  - { from: server, packet: SID_LOGONCHALLENGE, note: "Server token only, with no UDP code.", confidence: single }
  - { from: server, packet: SID_PING, confidence: verified }
  - { from: client, packet: SID_PING, optional: true, confidence: single }
  - { from: server, packet: SID_STARTVERSIONING, confidence: single }
  - { from: client, packet: SID_REPORTVERSION, confidence: single }
  - { from: server, packet: SID_REPORTVERSION, note: "`0x02` when the version passes.", confidence: single }
  - { section: "*StarCraft Japanese* only" }
  - { from: client, packet: SID_CDKEY, note: "Plain-text CD key.", confidence: single }
  - { from: server, packet: SID_CDKEY, note: "`0x01` accepted.", confidence: single }
  - { section: "Logging on" }
  - { from: client, packet: SID_LOGONRESPONSE, confidence: single }
  - { from: server, packet: SID_LOGONRESPONSE, note: "`0x01` logged on.", confidence: single }
  - { from: client, packet: SID_UDPPINGRESPONSE, optional: true, confidence: single }
  - { section: "Entering chat" }
  - { from: client, packet: SID_ENTERCHAT, confidence: single }
  - { from: client, packet: SID_GETCHANNELLIST, confidence: single }
  - { from: client, packet: SID_JOINCHANNEL, confidence: single }
  - { from: server, packet: SID_ENTERCHAT, confidence: single }
  - { from: server, packet: SID_GETCHANNELLIST, confidence: single }
  - { from: server, packet: SID_CHATEVENT, confidence: single }
---

**Defunct on official servers.** Both games now show a required update to the free *StarCraft* 1.18, which no longer uses this logon.

**Which logon challenge.** BNETDocs recorded these clients receiving `SID_LOGONCHALLENGE`. The Atlas server sends `SID_LOGONCHALLENGEEX` in reply to `SID_CLIENTID` instead. A capture from a real client would settle which one they expect.
