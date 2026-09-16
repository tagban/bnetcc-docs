---
title: "Battle.net 2.0"
bnetdocs_documents: [32]
sources:
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
    note: "the StarCraft II connection, Front RPC and Sunken records"
---

Battle.net 2.0 is the service behind *StarCraft II* and the Blizzard games that followed it. It replaced Classic Battle.net's single binary protocol with protobuf RPC over encrypted connections.

This section currently covers **StarCraft II**, which uses two connections:

| Connection | What it does | Format |
|---|---|---|
| **[Front](/bnet2/front/)** | Signs in to the regional Battle.net service and picks the StarCraft II game account | Protobuf RPC in WebSocket messages, over TLS on TCP port 1119 |
| **[Sunken](/bnet2/sunken/)** | Carries StarCraft II's own services: chat, matchmaking, profiles and more | Bit-packed records over a separate TCP connection, encrypted after sign-in |

## Start here

- [StarCraft II: signing in](/bnet2/sequences/starcraft-ii-logon/): the whole handoff from Front to Sunken, step by step.
- [Front RPC](/bnet2/front/): how Front messages are framed and routed.
- [Front messages](/bnet2/front-messages/): the protobuf messages used while signing in.
- [Sunken records](/bnet2/sunken/): how Sunken packs each record into bits.

**Signing in always requires a real Battle.net account.** Front hands account challenges, such as multi-factor authentication, to Blizzard's own web sign-in. There is no way around it, and these pages describe the protocol, not ways to avoid it.
