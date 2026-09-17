---
title: "SID_AUTH_ACCOUNTLOGONPROOF"
layout: "packet"
protocol: "BNCS"
message_id: "0x54"
categories: ["BNCS", "Logon", "NLS"]
products: [WAR3, W3XP]
summary: "Finishes a *Warcraft III* logon: each side proves it knows the password without sending it."
c2s:
  fields:
    - { type: "UINT8 × 20", name: "Client proof (M1)", notes: "See [NLS](/classic/nls/).", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Status", confidence: verified }
    - { type: "UINT8 × 20", name: "Server proof (M2)", confidence: verified }
    - { type: "STRING", name: "Error message", notes: "**Only with status `0x0F`.** Never send it otherwise; see below.", confidence: verified }
  values:
    - name: "Status"
      items:
        - { value: "0x00", meaning: "Logged on.", confidence: verified }
        - { value: "0x02", meaning: "Wrong password.", confidence: verified }
        - { value: "0x06", meaning: "Account closed.", confidence: single }
        - { value: "0x0E", meaning: "Logged on, but the account should have an email address. The client then sends `SID_SETEMAIL`.", confidence: verified }
        - { value: "0x0F", meaning: "Custom error. The message follows the proof and is shown to the player.", confidence: single }
sources:
  - name: "Command Center: WARCRAFT3-FIELD-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3-FIELD-NOTES.md"
    note: "observed from a real Warcraft III: The Frozen Throne client on September 11, 2026"
  - name: "Command Center: WARCRAFT3.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3.md"
---

**A successful reply must be exactly 24 bytes:** the status and the 20-byte proof, with nothing after them. BNETDocs lists a message string at the end, but a real *Warcraft III* client disconnects ("connection to Battle.net has been lost") if even one empty-string byte follows a success. Only the custom-error status `0x0F` carries a string.

```
Wrong (client disconnects):  00 00 00 00  <M2, 20 bytes>  00
Right:                       00 00 00 00  <M2, 20 bytes>
```
