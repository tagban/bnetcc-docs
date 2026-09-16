---
title: "Warcraft II: Battle.net Edition: logon to chat"
layout: "sequence"
categories: ["Sequences"]
products: [W2BN]
summary: "How *Warcraft II: Battle.net Edition* connects with the older logon, including its hashed CD key and the UDP test."
bnetdocs_documents: [10]
steps:
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: client, packet: SID_CLIENTID2, note: "Sent back to back with the next two messages.", confidence: single }
  - { from: client, packet: SID_LOCALEINFO, confidence: single }
  - { from: client, packet: SID_STARTVERSIONING, note: "Names the game (`W2BN`) and version byte.", confidence: verified }
  - { from: server, packet: SID_CLIENTID, note: "Registration fields, all zero.", confidence: verified }
  - { from: server, packet: SID_LOGONCHALLENGEEX, note: "UDP code and server token.", confidence: verified }
  - { from: server, packet: SID_PING, confidence: verified }
  - { from: client, packet: SID_PING, optional: true, confidence: single }
  - { from: server, packet: SID_STARTVERSIONING, note: "The version check to run.", confidence: verified }
  - { from: server, raw: "PKT_SERVERPING", transport: "UDP", note: "UDP test to the client's port 6112. The client doesn't probe first; it waits for this. Create and Join stay disabled until it arrives.", confidence: verified }
  - { from: client, packet: SID_REPORTVERSION, note: "EXE hash.", confidence: verified }
  - { from: server, packet: SID_REPORTVERSION, note: "`0x02` when the version passes.", confidence: verified }
  - { from: client, packet: SID_UDPPINGRESPONSE, note: "Confirms the UDP test over TCP.", confidence: verified }
  - { from: client, packet: SID_CDKEY2, note: "Hashed CD key.", confidence: single }
  - { from: server, packet: SID_CDKEY2, note: "`0x01` accepted.", confidence: single }
  - { section: "Optional: icons, terms of service and server list" }
  - { from: client, raw: "SID_GETICONDATA", optional: true, confidence: single }
  - { from: server, raw: "SID_GETICONDATA", optional: true, confidence: single }
  - { from: client, raw: "SID_GETFILETIME", optional: true, note: "For the icons file, `tos_USA.txt` and `bnserver.ini`.", confidence: single }
  - { from: server, raw: "SID_GETFILETIME", optional: true, note: "One reply for each request. Files are then downloaded over BNFTP.", confidence: single }
  - { section: "Only when the player creates a new account" }
  - { from: client, packet: SID_CREATEACCOUNT, optional: true, confidence: single }
  - { from: server, packet: SID_CREATEACCOUNT, optional: true, note: "`0x01` created.", confidence: single }
  - { section: "Logging on" }
  - { from: client, packet: SID_LOGONRESPONSE, confidence: verified }
  - { from: server, packet: SID_LOGONRESPONSE, note: "`0x01` logged on.", confidence: verified }
  - { section: "Entering chat" }
  - { from: client, packet: SID_ENTERCHAT, confidence: single }
  - { from: client, packet: SID_GETCHANNELLIST, confidence: single }
  - { from: client, packet: SID_JOINCHANNEL, note: "Flags `0x01` (first join).", confidence: single }
  - { from: server, packet: SID_ENTERCHAT, confidence: verified }
  - { from: server, packet: SID_GETCHANNELLIST, confidence: verified }
  - { from: server, packet: SID_CHATEVENT, confidence: verified }
sources:
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
    note: "UDP behaviour captured from a real Warcraft II client on September 9, 2026"
  - name: "BNETDocs Atlas server (MIT)"
    url: "https://github.com/BNETDocs/Atlas/blob/master/src/Atlasd/Battlenet/Protocols/Game/Messages/SID_CLIENTID2.cs"
---

**The GOG release is different.** The edition of *Warcraft II: Battle.net Edition* sold by GOG doesn't behave exactly like the original. This page describes the original. The GOG edition's differences will be added here once they're captured from a real client.
