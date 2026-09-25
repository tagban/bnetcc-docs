---
title: "Battle.net 2.0"
bnetdocs_documents: [32]
sources:
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
    note: "the StarCraft II connection, Front RPC and Sunken records"
---

Battle.net 2.0 is the service behind *StarCraft II* and the Blizzard games that followed it. It replaced Classic Battle.net's single binary protocol with protobuf RPC over encrypted connections.

This section covers **StarCraft II** sign-in in depth, and chat for **StarCraft II**, **StarCraft: Remastered**, **Diablo II: Resurrected** and **Diablo IV**.

It also covers **StarCraft: Remastered** sign-in and stats, and **StarCraft II** presence, friends, profiles and clans.

StarCraft II uses two connections:

| Connection | What it does | Format |
|---|---|---|
| **[Front](/bnet2/front/)** | Signs in to the regional Battle.net service and picks the StarCraft II game account | Protobuf RPC in WebSocket messages, over TLS on TCP port 1119 |
| **[Sunken](/bnet2/sunken/)** | Carries StarCraft II's own services: chat, matchmaking, profiles and more | Bit-packed records over a separate TCP connection, encrypted after sign-in |

## Start here

- [StarCraft II: signing in](/bnet2/sequences/starcraft-ii-logon/): the whole handoff from Front to Sunken, step by step.
- [Front RPC](/bnet2/front/): how Front messages are framed and routed.
- [Front messages](/bnet2/front-messages/): the protobuf messages used while signing in.
- [Sunken records](/bnet2/sunken/): how Sunken packs each record into bits.
- [StarCraft: Remastered: signing in](/bnet2/sequences/starcraft-remastered-logon/): Aurora, the classic server, the key-folded seed and the startup calls.
- [StarCraft: Remastered messages](/bnet2/scr-messages/): every classic service and method, with IDs and layouts: characters (including creating one), whispers, friends and stats.

## Chat, once signed in

| Game | Page | Carried on |
|---|---|---|
| StarCraft II | [StarCraft II chat on Sunken](/bnet2/sunken-chat/) | Bit-packed Sunken records |
| StarCraft: Remastered | [StarCraft: Remastered chat](/bnet2/scr-chat/) | LegacyChat RPC on a scrambled WebSocket |
| Diablo II: Resurrected, Diablo IV | [D2R and D4 chat](/bnet2/d2r-d4-chat/) | Front RPC, `ChannelService` and friends |

## StarCraft II: people

| Page | Covers |
|---|---|
| [StarCraft II presence](/bnet2/sc2-presence/) | Who is online, away, busy or in a game, and which game they're in |
| [StarCraft II friends](/bnet2/sc2-friends/) | The friends list, a friend's characters, and why Battle.net's friends service is closed to the game |
| [StarCraft II profiles and portraits](/bnet2/sc2-profiles/) | Profile reads, the portrait and other cosmetics, the portrait sheets, name lookups, what can be changed, and where ladder data lives |
| [StarCraft II clans and groups](/bnet2/sc2-clubs/) | A character's clans and groups, member lists and ranks, live changes, descriptions, clan chat, and creating and managing a clan |

## Still unknown

[Open questions](/bnet2/open-questions/) lists what isn't known yet: SC2 ladder data, emoticons, badges, other regions and more.

**Signing in always requires a real Battle.net account.** Front hands account challenges, such as multi-factor authentication, to Blizzard's own web sign-in. There is no way around it, and these pages describe the protocol, not ways to avoid it.
