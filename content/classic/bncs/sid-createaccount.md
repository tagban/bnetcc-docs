---
title: "SID_CREATEACCOUNT"
layout: "packet"
protocol: "BNCS"
message_id: "0x2A"
categories: ["BNCS", "Accounts"]
products: [SSHR, JSTR, DRTL, DSHR, W2BN]
summary: "Creates an account in the older logon. Same request as `SID_CREATEACCOUNT2`, but the reply is only success or failure."
c2s:
  fields:
    - { type: "VOID", name: "Password hash (20 bytes)", notes: "X-SHA-1 of the lowercase password, hashed **once**.", confidence: verified }
    - { type: "STRING", name: "Account name", notes: "Names longer than 15 characters are cut short.", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Account not created.", confidence: verified }
        - { value: "0x01", meaning: "Account created.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

**The result is reversed compared to `SID_CREATEACCOUNT2`.** Here `0x01` means created. In `SID_CREATEACCOUNT2`, `0x00` does.

**Many clients ignore the result.** Bots such as Invigoration treat any reply as "account created", disconnect and log on with the new account. Whether creation really worked only shows at that logon. A server that sends `0x00` for success still works with these clients, but a client that reads the value, as BNETDocs and Atlas describe it, would report a failure.

A client that wants a reason for the failure can use `SID_CREATEACCOUNT2`, which any product may send.
