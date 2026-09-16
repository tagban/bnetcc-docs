---
title: "SID_LOGONRESPONSE"
layout: "packet"
protocol: "BNCS"
message_id: "0x29"
categories: ["BNCS", "Logon"]
products: [SSHR, JSTR, DRTL, DSHR, W2BN]
summary: "Logs on to an account in the older logon. Same proof as `SID_LOGONRESPONSE2`, but a simpler reply."
c2s:
  fields:
    - { type: "UINT32", name: "Client token", notes: "Chosen by the client.", confidence: verified }
    - { type: "UINT32", name: "Server token", notes: "From `SID_LOGONCHALLENGE` or `SID_LOGONCHALLENGEEX`.", confidence: verified }
    - { type: "VOID", name: "Password proof (20 bytes)", notes: "X-SHA-1 of: client token, server token, then X-SHA-1 of the lowercase password.", confidence: verified }
    - { type: "STRING", name: "Account name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Logon failed. The reply doesn't say whether the account is missing or the password is wrong.", confidence: verified }
        - { value: "0x01", meaning: "Logged on.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "older logon tested with a real Warcraft II client"
---

**The success value is reversed.** In this message `0x01` means success. In `SID_LOGONRESPONSE2`, `0x00` does.

**Which server token.** If a server never sends a logon challenge, older clients use `0` as the server token, and the proof must be checked with `0`.
