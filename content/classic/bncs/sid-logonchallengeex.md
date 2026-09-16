---
title: "SID_LOGONCHALLENGEEX"
layout: "packet"
protocol: "BNCS"
message_id: "0x1D"
categories: ["BNCS", "Logon", "Historical"]
products: [DRTL, DSHR, W2BN]
status: "Historical. Newer games receive the server token in `SID_AUTH_INFO`."
summary: "Gives the client the UDP code and the server token for this session."
s2c:
  when: "Right after the server's `SID_CLIENTID` reply to `SID_CLIENTID2`."
  fields:
    - { type: "UINT32", name: "UDP token", notes: "The code the UDP test uses.", confidence: verified }
    - { type: "UINT32", name: "Server token", notes: "Mixed into the password proof in `SID_LOGONRESPONSE`.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---
