---
title: "BNCS messages"
layout: "protocol"
bnetdocs_prefix: "SID_"
---

BNCS (Battle.net Chat Server) is the protocol every Classic game uses for its main connection: logging on, chat, friends, clans and the game list. Each message has a one-byte ID and is written `SID_NAME`.

Every message is framed as `FF`, the message ID, and a 2-byte length that includes the 4-byte header. See [Connecting to a Classic server](/classic/connecting/) for framing and data types.
