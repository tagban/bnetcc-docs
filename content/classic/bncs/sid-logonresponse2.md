---
title: "SID_LOGONRESPONSE2"
layout: "packet"
protocol: "BNCS"
message_id: "0x3A"
categories: ["BNCS", "Logon"]
products: [STAR, SEXP, D2DV, D2XP]
summary: "Logs on to an account with a salted X-SHA-1 password proof."
c2s:
  when: "After `SID_AUTH_CHECK` passes."
  fields:
    - { type: "UINT32", name: "Client token", notes: "The same client token sent in `SID_AUTH_CHECK`.", confidence: verified }
    - { type: "UINT32", name: "Server token", notes: "The token from the server's `SID_AUTH_INFO`.", confidence: verified }
    - { type: "VOID", name: "Password proof (20 bytes)", notes: "X-SHA-1 of: client token, server token, then X-SHA-1 of the lowercase password.", confidence: verified }
    - { type: "STRING", name: "Account name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Status", notes: "See the table below.", confidence: verified }
    - { type: "STRING", name: "Reason", notes: "Only sent with status `0x06`.", confidence: single }
  values:
    - name: "Status"
      items:
        - { value: "0x00", meaning: "Logged on.", confidence: verified }
        - { value: "0x01", meaning: "No such account. The client offers to create it.", confidence: verified }
        - { value: "0x02", meaning: "Wrong password.", confidence: verified }
        - { value: "0x03", meaning: "Account data is damaged. *Diablo II* only.", confidence: single }
        - { value: "0x06", meaning: "Account closed. A reason string follows.", confidence: single }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
    note: "X-SHA-1 test vectors"
---

**Checking the proof.** The server stores X-SHA-1 of the lowercase password. To check a logon, it repeats the client's calculation using **the server token it issued itself**, never the token the client sends back. Using its own token is what stops an old proof from being replayed.

**Worked example.** With client token `0xDEADBEEF`, server token `0x12345678` and the password `password`, the proof (as five little-endian words) is `7488ad2d 82dc91a2 8aa43a7c 8d596822 a2920091`.

A client that gets a status it doesn't recognise shows a general error and disconnects.
