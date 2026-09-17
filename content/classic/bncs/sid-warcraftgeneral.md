---
title: "SID_WARCRAFTGENERAL"
layout: "packet"
protocol: "BNCS"
message_id: "0x44"
categories: ["BNCS", "Warcraft III"]
products: [WAR3, W3XP]
summary: "*Warcraft III*'s multipurpose message for matchmaking, ladder profiles, tournaments and icons. The first byte picks the subcommand."
c2s:
  fields:
    - { type: "UINT8", name: "Subcommand", notes: "See the table below.", confidence: verified }
    - { type: "UINT32", name: "Cookie", notes: "Echoed by the reply. Most subcommands have one.", confidence: verified }
    - { type: "VOID", name: "Subcommand data", confidence: verified }
  values:
    - name: "Subcommands"
      items:
        - { value: "0x00", meaning: "`WID_GAMESEARCH`: start a matchmaking search (game type, maps, race).", confidence: verified }
        - { value: "0x02", meaning: "`WID_MAPLIST`: the ladder map list and game types, sent at logon.", confidence: verified }
        - { value: "0x03", meaning: "`WID_CANCELSEARCH`: stop searching.", confidence: verified }
        - { value: "0x04", meaning: "`WID_USERRECORD`: a player's ladder profile.", confidence: verified }
        - { value: "0x07", meaning: "`WID_TOURNAMENT`: tournament status. Sent on entering chat, then about every 11 minutes.", confidence: verified }
        - { value: "0x08", meaning: "`WID_CLANRECORD`: a clan's ladder profile.", confidence: verified }
        - { value: "0x09", meaning: "`WID_ICONLIST`: the icons the player may choose.", confidence: verified }
        - { value: "0x0A", meaning: "`WID_SETICON`: choose an icon.", confidence: verified }
s2c:
  fields:
    - { type: "UINT8", name: "Subcommand", confidence: verified }
    - { type: "UINT32", name: "Cookie", confidence: verified }
    - { type: "VOID", name: "Subcommand data", confidence: single }
sources:
  - name: "Command Center: bnetcc-proto w3general"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetcc-proto/src/w3general.rs"
---

A server without a ladder can still give truthful empty answers: no tournament, profiles with no ladder games, and no unlocked icons. Matchmaking searches and the map list need a real ladder. They'll be documented with *Warcraft III* matchmaking.
