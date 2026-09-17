---
title: "SID_AUTH_ACCOUNTCREATE"
layout: "packet"
protocol: "BNCS"
message_id: "0x52"
categories: ["BNCS", "Accounts", "NLS"]
products: [WAR3, W3XP]
summary: "Creates a *Warcraft III* account. The client sends a salt and verifier, never the password."
c2s:
  when: "When the player creates an account, usually after `SID_AUTH_ACCOUNTLOGON` reports that it doesn't exist."
  fields:
    - { type: "UINT8 × 32", name: "Salt (s)", notes: "Random, chosen by the client.", confidence: verified }
    - { type: "UINT8 × 32", name: "Verifier (v)", notes: "`g^x mod N`, 32 bytes little-endian. See [NLS](/classic/nls/).", confidence: verified }
    - { type: "STRING", name: "Account name", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Status", confidence: verified }
  values:
    - name: "Status"
      items:
        - { value: "0x00", meaning: "Created. The client then logs on with `SID_AUTH_ACCOUNTLOGON`.", confidence: verified }
        - { value: "0x04", meaning: "Name already exists.", confidence: single }
        - { value: "0x07", meaning: "Name is too short or empty.", confidence: single }
        - { value: "0x08", meaning: "Name contains a character that isn't allowed.", confidence: single }
        - { value: "0x09", meaning: "Name contains a banned word.", confidence: single }
        - { value: "0x0A", meaning: "Name has too few letters or numbers.", confidence: single }
        - { value: "0x0B", meaning: "Name has punctuation characters next to each other.", confidence: single }
        - { value: "0x0C", meaning: "Name has too much punctuation.", confidence: single }
sources:
  - name: "Command Center: WARCRAFT3-FIELD-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3-FIELD-NOTES.md"
    note: "observed from a real Warcraft III: The Frozen Throne client on September 11, 2026"
  - name: "Command Center: WARCRAFT3.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3.md"
---

The server stores only the salt and verifier. Neither lets anyone log on without the password.
