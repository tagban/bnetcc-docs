---
title: "Diablo II: closed realm logon"
layout: "sequence"
categories: ["Sequences"]
products: [D2DV, D2XP]
summary: "How *Diablo II* 1.14d logs on to Battle.net, connects to the realm, picks a character and enters chat. Checked against a real *Lord of Destruction* 1.14d client."
bnetdocs_documents: [29, 10]
steps:
  - { section: "Battle.net connection: log on" }
  - { from: client, raw: "0x01", note: "Protocol byte: BNCS follows.", confidence: verified }
  - { from: client, packet: SID_AUTH_INFO, note: "Names the game (`D2DV` or `D2XP`). Version byte `0x0E` for 1.14d.", confidence: verified }
  - { from: server, packet: SID_PING, confidence: verified }
  - { from: server, packet: SID_AUTH_INFO, note: "Logon type `0x00` (X-SHA-1) and the version check.", confidence: verified }
  - { from: client, packet: SID_AUTH_CHECK, note: "*Lord of Destruction* sends two CD keys.", confidence: verified }
  - { from: server, packet: SID_AUTH_CHECK, confidence: verified }
  - { from: client, packet: SID_GETFILETIME, optional: true, note: "Terms of service. The client downloads them over BNFTP.", confidence: verified }
  - { from: server, packet: SID_GETFILETIME, optional: true, confidence: verified }
  - { from: client, packet: SID_LOGONRESPONSE2, note: "Or `SID_CREATEACCOUNT2` first, for a new account.", confidence: verified }
  - { from: server, packet: SID_LOGONRESPONSE2, confidence: verified }
  - { section: "Battle.net connection: find the realm" }
  - { from: client, packet: SID_QUERYREALMS2, confidence: verified }
  - { from: server, packet: SID_QUERYREALMS2, note: "The realms on offer.", confidence: verified }
  - { from: client, packet: SID_LOGONREALMEX, confidence: verified }
  - { from: server, packet: SID_LOGONREALMEX, note: "The realm's address and port, plus data to hand the realm.", confidence: verified }
  - { section: "Realm connection (a second TCP connection)" }
  - { from: client, raw: "0x01", note: "The same protocol byte, but MCP framing follows.", confidence: verified }
  - { from: client, packet: MCP_STARTUP, note: "The data from `SID_LOGONREALMEX`.", confidence: verified }
  - { from: server, packet: MCP_STARTUP, note: "`0x00` accepted.", confidence: verified }
  - { from: client, packet: MCP_CHARLIST2, confidence: verified }
  - { from: server, packet: MCP_CHARLIST2, note: "The character-select screen appears.", confidence: verified }
  - { section: "Either select a character…" }
  - { from: client, packet: MCP_CHARLOGON, optional: true, confidence: verified }
  - { from: server, packet: MCP_CHARLOGON, optional: true, note: "`0x00` selected.", confidence: verified }
  - { section: "…or create one, which selects it with no MCP_CHARLOGON" }
  - { from: client, packet: MCP_CHARCREATE, optional: true, confidence: verified }
  - { from: server, packet: MCP_CHARCREATE, optional: true, note: "`0x00` created.", confidence: verified }
  - { section: "Into the chat lobby" }
  - { from: client, packet: MCP_MOTD, note: "On the realm connection.", confidence: verified }
  - { from: server, packet: MCP_MOTD, confidence: verified }
  - { from: client, packet: SID_GETCHANNELLIST, note: "Back on the Battle.net connection.", confidence: verified }
  - { from: client, packet: SID_ENTERCHAT, note: "Name: the character. Statstring: `realm,character`.", confidence: verified }
  - { from: server, packet: SID_GETCHANNELLIST, confidence: verified }
  - { from: server, packet: SID_ENTERCHAT, note: "Unique name `Character*Account`, and the character's portrait statstring.", confidence: verified }
  - { from: client, packet: SID_NEWS_INFO, confidence: verified }
  - { from: server, packet: SID_NEWS_INFO, confidence: verified }
  - { from: client, packet: SID_JOINCHANNEL, note: "The *Diablo II* channel.", confidence: verified }
  - { from: server, packet: SID_CHATEVENT, confidence: verified }
  - { from: client, packet: SID_CHECKAD, note: "Repeated about every 15 seconds.", confidence: verified }
sources:
  - name: "Command Center: DIABLO2.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/DIABLO2.md"
    note: "observed from a real Diablo II: Lord of Destruction 1.14d client on September 13, 2026"
---

**Going back to character select.** The client sends `SID_LEAVECHAT`, then `SID_QUERYREALMS2`, then `MCP_CHARLIST2` on the realm connection it already has open.

**Creating and joining games** goes through the realm: `MCP_CREATEGAME`, then `MCP_JOINGAME`. On success the client closes the realm connection and connects to the game server on port 4000.

**One port or two.** Official Battle.net ran the realm on separate hosts. A server can also accept both connections on port 6112, because the next byte after `0x01` tells them apart: a BNCS message starts with `FF`, while an MCP message starts with its length.

**Open Battle.net** (characters kept on the player's computer) skips the realm entirely and logs on to chat like [StarCraft](/classic/sequences/starcraft-logon/).
