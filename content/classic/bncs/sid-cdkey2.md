---
title: "SID_CDKEY2"
layout: "packet"
protocol: "BNCS"
message_id: "0x36"
categories: ["BNCS", "Logon", "Historical"]
products: [W2BN]
status: "Historical."
summary: "Sends a hashed CD key in the older logon. *Warcraft II* uses it."
c2s:
  when: "After `SID_REPORTVERSION` passes."
  fields:
    - { type: "UINT32", name: "Spawn", confidence: verified }
    - { type: "UINT32", name: "Key length", confidence: verified }
    - { type: "UINT32", name: "Product value", notes: "Decoded from the key.", confidence: verified }
    - { type: "UINT32", name: "Public value", notes: "Decoded from the key.", confidence: verified }
    - { type: "UINT32", name: "Server token", notes: "From `SID_LOGONCHALLENGEEX`.", confidence: verified }
    - { type: "UINT32", name: "Client token", confidence: verified }
    - { type: "VOID", name: "Key hash (20 bytes)", notes: "Mixed with both tokens, so it changes every session.", confidence: verified }
    - { type: "STRING", name: "Key owner", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
    - { type: "STRING", name: "Key owner", confidence: verified }
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

**Token order.** In this message the server token comes **before** the client token, the opposite of the order in `SID_LOGONRESPONSE` and `SID_LOGONRESPONSE2`.
