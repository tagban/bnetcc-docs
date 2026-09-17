---
title: "SID_CHECKAD"
layout: "packet"
protocol: "BNCS"
message_id: "0x15"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Asks which advertisement banner to show. Clients repeat it about every 15 seconds."
c2s:
  fields:
    - { type: "DWORD", name: "Platform code", confidence: verified }
    - { type: "DWORD", name: "Product code", confidence: verified }
    - { type: "UINT32", name: "Last banner shown", notes: "Its ad ID.", confidence: verified }
    - { type: "UINT32", name: "Current time", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Ad ID", confidence: verified }
    - { type: "UINT32", name: "File extension", notes: "The image format, as a four-character code.", confidence: verified }
    - { type: "FILETIME", name: "File time", notes: "When it changes, the client downloads the banner again over BNFTP.", confidence: verified }
    - { type: "STRING", name: "File name", confidence: verified }
    - { type: "STRING", name: "Link", notes: "Where clicking the banner goes.", confidence: verified }
sources:
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
---

Official Battle.net only replied when something in the request had changed since the last check. A server with no banners can simply not reply.
