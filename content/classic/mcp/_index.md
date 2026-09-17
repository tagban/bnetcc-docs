---
title: "MCP messages (Diablo II realm)"
layout: "protocol"
bnetdocs_prefix: "MCP_"
games: ["diablo-ii"]
---

MCP is the protocol of the *Diablo II* **closed realm**, the server that stores characters for Battle.net (closed) play. After logging on to Battle.net, the client opens a second connection to the realm. Each message has a one-byte ID and is written `MCP_NAME`.

**MCP is framed differently from BNCS.** There is no `FF` byte, and the length comes first:

```
BNCS   FF | message ID (1 byte) | length (2 bytes)
MCP         length (2 bytes)   | message ID (1 byte)
```

Both lengths include the header, and both are little-endian. The realm connection also starts with the protocol byte `0x01`, just like the Battle.net connection, which is why the two are easy to confuse. An empty MCP message is three bytes, such as `03 00 12` for `MCP_MOTD`.

See [Diablo II: closed realm logon](/classic/sequences/diablo-ii-realm-logon/) for the order messages are sent in.
