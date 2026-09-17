---
title: "SID_AUTH_ACCOUNTLOGON"
layout: "packet"
protocol: "BNCS"
message_id: "0x53"
categories: ["BNCS", "Logon", "NLS"]
products: [WAR3, W3XP]
summary: "Starts a *Warcraft III* logon: the client sends its public key and the server answers with the account's salt and its own public key."
c2s:
  fields:
    - { type: "UINT8 × 32", name: "Client public key (A)", notes: "`g^a mod N` for a random `a`, 32 bytes little-endian.", confidence: verified }
    - { type: "STRING", name: "Account name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Status", confidence: verified }
    - { type: "UINT8 × 32", name: "Salt (s)", notes: "Zeros on failure.", confidence: verified }
    - { type: "UINT8 × 32", name: "Server public key (B)", notes: "Zeros on failure.", confidence: verified }
  values:
    - name: "Status"
      items:
        - { value: "0x00", meaning: "Account found. The client sends its proof next.", confidence: verified }
        - { value: "0x01", meaning: "No such account. The client offers to create it.", confidence: verified }
        - { value: "0x05", meaning: "The account must be upgraded first.", confidence: single }
sources:
  - name: "Command Center: WARCRAFT3-FIELD-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3-FIELD-NOTES.md"
    note: "observed from a real Warcraft III: The Frozen Throne client on September 11, 2026"
  - name: "Command Center: WARCRAFT3.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3.md"
---

**The reply is always 72 bytes,** even on failure: the status, then 32 zero bytes for the salt and 32 for the server key.
