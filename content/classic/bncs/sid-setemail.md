---
title: "SID_SETEMAIL"
layout: "packet"
protocol: "BNCS"
message_id: "0x59"
categories: ["BNCS", "Accounts"]
products: [STAR, SEXP, D2DV, D2XP, WAR3, W3XP]
summary: "Asks the player to register an email address on their account, and carries the address back."
s2c:
  when: "After logon, when the account has no email address. No payload."
c2s:
  when: "Only after the server asks, either with this message or with `SID_AUTH_ACCOUNTLOGONPROOF` status `0x0E`."
  fields:
    - { type: "STRING", name: "Email address", confidence: single }
---

The message ID once belonged to a planned reconnect feature that Blizzard never finished, and was reused for email.
