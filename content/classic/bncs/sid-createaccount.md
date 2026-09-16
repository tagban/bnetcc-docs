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
        - { value: "0x00", meaning: "**Unresolved.** BNETDocs and the Atlas server say this means the account wasn't created. But an account created through Invigoration got `0x00` back with no problem. See the remarks.", confidence: unknown }
        - { value: "0x01", meaning: "Account created.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
---

**The result is reversed compared to `SID_CREATEACCOUNT2`.** Here `0x01` means created. In `SID_CREATEACCOUNT2`, `0x00` does.

**What `0x00` means is unresolved.** BNETDocs and the Atlas server both describe `0x00` as failure. In practice, a `0x00` reply hasn't caused problems: accounts created through Invigoration, a bot that also works on official Battle.net, got `0x00` back and logged on normally.

Invigoration, like many bots, doesn't read the value. It treats any reply as "account created", disconnects and logs on. So the safest reading today:

- **Clients** should treat either value as "account created", then confirm by logging on.
- **Servers** should send `0x01` for success, which every source agrees on.

A client that wants a reason for the failure can use `SID_CREATEACCOUNT2`, which any product may send.
