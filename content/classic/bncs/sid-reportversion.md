---
title: "SID_REPORTVERSION"
layout: "packet"
protocol: "BNCS"
message_id: "0x07"
categories: ["BNCS", "Logon", "Version checking"]
products: [SSHR, JSTR, DRTL, DSHR, W2BN]
status: "Historical. Newer games use `SID_AUTH_CHECK` for the same job."
summary: "Finishes the version check in the older logon: the client reports its EXE hash, and the server accepts or rejects it."
c2s:
  fields:
    - { type: "DWORD", name: "Platform code", notes: "Sent backwards, like every four-character code: `IX86` is `68XI`.", confidence: verified }
    - { type: "DWORD", name: "Product code", notes: "Sent backwards: `W2BN` is `NB2W`.", confidence: verified }
    - { type: "UINT32", name: "Version byte", confidence: verified }
    - { type: "UINT32", name: "EXE version", confidence: verified }
    - { type: "UINT32", name: "EXE hash", notes: "The result of running the formula from `SID_STARTVERSIONING`.", confidence: verified }
    - { type: "STRING", name: "EXE information", notes: "The executable's name, date and size.", confidence: verified }
s2c:
  fields:
    - { type: "UINT32", name: "Result", notes: "See the table below.", confidence: verified }
    - { type: "STRING", name: "Patch file", notes: "The patch to download when the version is old. Empty otherwise.", confidence: verified }
    - { type: "UINT8", name: "Unused", notes: "`0`. Some old clients misread the whole reply without this byte.", confidence: verified }
  values:
    - name: "Results"
      items:
        - { value: "0x00", meaning: "Version check failed.", confidence: verified }
        - { value: "0x01", meaning: "Game version too old. A patch file is named.", confidence: verified }
        - { value: "0x02", meaning: "Passed.", confidence: verified }
        - { value: "0x03", meaning: "Reinstall the game.", confidence: verified }
bnetdocs_documents: [10]
sources:
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/tree/master/src/Atlasd/Battlenet/Protocols/Game/Messages"
    note: "message handler used to cross-check the layout"
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "older logon tested with a real Warcraft II client"
---

The patch file field once carried leftover memory from the official server's buffers. That was fixed by a server update in 2017.
