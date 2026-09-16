---
title: "SID_LOGONCHALLENGE"
layout: "packet"
protocol: "BNCS"
message_id: "0x28"
categories: ["BNCS", "Logon", "Historical"]
products: [SSHR, JSTR]
status: "Historical."
summary: "Gives the client the server token for this session, without a UDP code."
s2c:
  when: "Right after the server's `SID_CLIENTID` reply."
  fields:
    - { type: "UINT32", name: "Server token", notes: "Mixed into the password proof in `SID_LOGONRESPONSE`.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

BNETDocs' observed logon sequences show *StarCraft Shareware* and *StarCraft Japanese* receiving this message, and *Diablo* and *Warcraft II* receiving `SID_LOGONCHALLENGEEX` instead. BNETDocs' "used by" list for this message also names *Diablo* and *Warcraft II*, which may be out of date.
