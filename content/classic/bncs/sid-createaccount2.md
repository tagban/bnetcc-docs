---
title: "SID_CREATEACCOUNT2"
layout: "packet"
protocol: "BNCS"
message_id: "0x3D"
categories: ["BNCS", "Accounts"]
products: [STAR, SEXP, D2DV, D2XP]
summary: "Creates an account using an X-SHA-1 password hash."
c2s:
  when: "When the player creates a new account, usually after `SID_LOGONRESPONSE2` reports that the account doesn't exist."
  fields:
    - { type: "VOID", name: "Password hash (20 bytes)", notes: "X-SHA-1 of the password converted to **lowercase**, hashed **once**.", confidence: verified }
    - { type: "STRING", name: "Account name", notes: "Names longer than 15 characters are cut short.", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Status", notes: "See the table below.", confidence: verified }
    - { type: "STRING", name: "Suggested name", notes: "May be empty.", confidence: single }
  values:
    - name: "Status"
      items:
        - { value: "0x00", meaning: "Account created.", confidence: verified }
        - { value: "0x02", meaning: "Name contains characters that aren't allowed.", confidence: single }
        - { value: "0x03", meaning: "Name contains a banned word.", confidence: single }
        - { value: "0x04", meaning: "An account with that name already exists.", confidence: verified }
        - { value: "0x06", meaning: "Name doesn't have enough letters or numbers.", confidence: single }
        - { value: "0x07", meaning: "Name has punctuation characters next to each other.", confidence: single }
        - { value: "0x08", meaning: "Name has too much punctuation.", confidence: single }
sources:
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
    note: "hashing rules, and the status codes confirmed so far"
---

**Lowercasing is the client's job.** The server only ever sees the hash, never the password, so it can't fix a client that forgets to lowercase first. An account created that way can only be logged on to by clients that make the same mistake. Blizzard's own clients always lowercase.

*Warcraft III* doesn't use this message. It creates accounts with `SID_AUTH_ACCOUNTCREATE`.
