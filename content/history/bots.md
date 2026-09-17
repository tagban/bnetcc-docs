---
title: "Bots"
layout: "bots"
categories: ["History", "Bots"]
summary: "Programs that connect to Battle.net without the game: chat clients, channel moderators, game hosts and more. Every one we know of, what it's for, and where to find it."
bnetdocs_documents: [50]
sources:
  - name: "BNET.cc Files archive"
    url: "https://bnet.cc/files.php?cat=bots"
    note: "the files and versions linked below"
---

A **bot** is a program that logs on to Battle.net like a game does, but without the game. Most are chat clients that sit in a channel. Many also moderate the channel automatically, and some host games.

Bots that log on as a game still need to pass the [version check](/classic/versioning/). Most use a [BNLS server](/classic/versioning/bnls/) for that. On Blizzard's servers, a bot also needs a CD key for the game it logs on as.

**Know a bot that's missing, a version we don't have, or who wrote one marked unknown?** Edit this list (it's `data/bots.yaml` in the [repository](https://github.com/tagban/bnetcc-docs)), or tell us on [Discord](https://discord.gg/dR4djHweh3).

## What bots are used for

| Purpose | What it means |
|---|---|
| Chat | A window with the channel's messages, a box to type in, and the list of users in the channel. |
| Moderation | Keeps lists of users and words, and acts on them automatically: kicking, banning, greeting. |
| Extendable | Runs plug-ins or scripts, so its users can add features. |
| Host | Creates games and lets players join them, like a player hosting a game would. |
| Checker | Logs on to accounts so they don't expire from inactivity, or checks that logon details still work. |

Files in the BNET.cc archive are shared as they were found, for history and for use on community servers. Scan anything you download.
