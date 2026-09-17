---
title: "SID_NEWS_INFO"
layout: "packet"
protocol: "BNCS"
message_id: "0x46"
categories: ["BNCS", "Chat"]
products: [D2DV, D2XP, WAR3, W3XP]
summary: "Asks for Battle.net news and the message of the day, shown on the chat screen."
c2s:
  when: "After `SID_ENTERCHAT`."
  fields:
    - { type: "UINT32", name: "Since", notes: "Only news newer than this, in seconds since January 1, 1970 (UTC). `0` for everything.", confidence: verified }
s2c:
  fields:
    - { type: "UINT8", name: "Number of entries", confidence: verified }
    - { type: "UINT32", name: "Last logon", notes: "Seconds since 1970, UTC.", confidence: verified }
    - { type: "UINT32", name: "Oldest news", confidence: verified }
    - { type: "UINT32", name: "Newest news", confidence: verified }
    - repeat: "For each entry"
      fields:
        - { type: "UINT32", name: "Timestamp", notes: "`0` marks the message of the day.", confidence: single }
        - { type: "STRING", name: "Text", confidence: single }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
---

News can arrive in several replies; clients treat them as one list. A reply with zero entries lets the client's news panel finish loading.
