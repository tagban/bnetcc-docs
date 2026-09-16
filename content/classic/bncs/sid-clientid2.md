---
title: "SID_CLIENTID2"
layout: "packet"
protocol: "BNCS"
message_id: "0x1E"
categories: ["BNCS", "Logon", "Historical"]
products: [DRTL, DSHR, W2BN]
status: "Historical. Only the older logon uses it."
summary: "A newer form of `SID_CLIENTID`, sent first by *Diablo* and *Warcraft II*."
c2s:
  when: "Right after the protocol byte, followed immediately by `SID_LOCALEINFO` and `SID_STARTVERSIONING`."
  fields:
    - { type: "UINT32", name: "Server version", notes: "Sets the order of the next two fields: `1` puts registration version first, `0` puts registration authority first.", confidence: verified }
    - { type: "UINT32", name: "Registration version or authority", notes: "Depends on the server version. No longer used.", confidence: verified }
    - { type: "UINT32", name: "Registration authority or version", notes: "Depends on the server version. No longer used.", confidence: verified }
    - { type: "UINT32", name: "Account number", notes: "No longer used.", confidence: verified }
    - { type: "UINT32", name: "Registration token", notes: "No longer used.", confidence: verified }
    - { type: "STRING", name: "LAN computer name", confidence: verified }
    - { type: "STRING", name: "LAN user name", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

The server answers with `SID_CLIENTID`, then `SID_LOGONCHALLENGEEX`, then `SID_PING`.
