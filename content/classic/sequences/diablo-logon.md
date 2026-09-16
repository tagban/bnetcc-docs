---
title: "Diablo: logon to chat"
layout: "sequence"
categories: ["Sequences"]
products: [DRTL, DSHR]
summary: "How *Diablo* and *Diablo Shareware* connect with the older logon. *Diablo* has no CD key, so there's no key check."
bnetdocs_documents: [10]
steps:
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: client, packet: SID_CLIENTID2, note: "Sent back to back with the next two messages.", confidence: single }
  - { from: client, packet: SID_LOCALEINFO, confidence: single }
  - { from: client, packet: SID_STARTVERSIONING, note: "Names the game (`DRTL` or `DSHR`) and version byte.", confidence: single }
  - { from: server, packet: SID_CLIENTID, note: "Registration fields, all zero.", confidence: verified }
  - { from: server, packet: SID_LOGONCHALLENGEEX, note: "UDP code and server token.", confidence: verified }
  - { from: server, packet: SID_PING, confidence: verified }
  - { from: client, packet: SID_PING, optional: true, confidence: single }
  - { from: server, packet: SID_STARTVERSIONING, note: "The version check to run.", confidence: single }
  - { from: client, packet: SID_REPORTVERSION, note: "EXE hash.", confidence: single }
  - { from: server, packet: SID_REPORTVERSION, note: "`0x02` when the version passes.", confidence: single }
  - { section: "Only when the player creates a new account" }
  - { from: client, packet: SID_CREATEACCOUNT, optional: true, note: "Password hashed once.", confidence: single }
  - { from: server, packet: SID_CREATEACCOUNT, optional: true, note: "`0x01` created.", confidence: single }
  - { section: "Logging on" }
  - { from: client, packet: SID_LOGONRESPONSE, note: "Salted password proof, using the token from `SID_LOGONCHALLENGEEX`.", confidence: single }
  - { from: server, packet: SID_LOGONRESPONSE, note: "`0x01` logged on.", confidence: single }
  - { from: client, packet: SID_UDPPINGRESPONSE, optional: true, note: "See the note below: unresolved for *Diablo*.", confidence: unknown }
  - { section: "Entering chat" }
  - { from: client, packet: SID_ENTERCHAT, confidence: single }
  - { from: client, packet: SID_GETCHANNELLIST, confidence: single }
  - { from: client, packet: SID_JOINCHANNEL, note: "Flags `0x01` (first join).", confidence: single }
  - { from: server, packet: SID_ENTERCHAT, confidence: single }
  - { from: server, packet: SID_GETCHANNELLIST, confidence: single }
  - { from: server, packet: SID_CHATEVENT, note: "`EID_CHANNEL`, then `EID_SHOWUSER` for each user.", confidence: single }
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/blob/master/src/Atlasd/Battlenet/Protocols/Game/Messages/SID_CLIENTID2.cs"
    note: "the server's three replies to `SID_CLIENTID2`, in order"
---

**Not yet checked against a real Diablo client.** Most steps are marked ⚠️ because this order comes from one source, BNETDocs' record of official clients. The server's first three replies are confirmed by a second source, the Atlas server. A capture from a real *Diablo* client would settle the rest.

**UDP.** BNETDocs lists *Diablo* among games that confirm the UDP test with `SID_UDPPINGRESPONSE`. It also notes that official Battle.net always showed *Diablo* users with the No UDP flag. Command Center currently assumes *Diablo* never runs the test. Treat this as unresolved.
