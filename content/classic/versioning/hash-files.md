---
title: "Hash files"
categories: ["Classic Battle.net", "Version checking"]
products: [STAR, SEXP, SSHR, JSTR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "The game files a version check reads, per game. This site documents them and never hosts them."
bnetdocs_documents: [47, 22]
sources:
  - name: "JBLS: util/Constants.java"
    url: "https://github.com/Davnit/JBLS/blob/develop/util/Constants.java"
    note: "the file set each game needs today, including the Lockdown screen dumps and version strings"
---

**Hash files** are copies of a game's own files that a version check reads. A game client already has them. A bot or a BNLS server that answers version checks for a game it isn't running needs its own copies.

## This site doesn't host them

These are Blizzard's copyrighted files. This site explains which files are needed and why, and never hosts them or links to copies. If you own the game, the files are in its install folder. Most bots today don't need them at all: they ask a [BNLS server](/classic/versioning/bnls/) to do the version check.

## Which files each game needs

A check reads up to three program files, in this order. Newer patches merged the support DLLs into the EXE, and then only the EXE is read.

| Game | File 1 | File 2 | File 3 | Lockdown screen dump |
|---|---|---|---|---|
| StarCraft, Brood War (`STAR`, `SEXP`) | `StarCraft.exe` | `Storm.dll` | `Battle.snp` (older patches) | `STAR.bin` |
| StarCraft Shareware (`SSHR`) | `Starcraft.exe` | `Storm.dll` | `Battle.snp` | unknown |
| StarCraft Japanese (`JSTR`) | `StarcraftJ.exe` | `Storm.dll` | `Battle.snp` | unknown |
| Warcraft II: Battle.net Edition (`W2BN`) | `Warcraft II BNE.exe` | `Storm.dll` | `Battle.snp` | `W2BN.bin` |
| Diablo (`DRTL`) | `Diablo.exe` | `Storm.dll` | `Battle.snp` | `DRTL.bin` |
| Diablo Shareware (`DSHR`) | `Diablo_s.exe` | `Storm.dll` | `Battle.snp` | unknown |
| Diablo II, Lord of Destruction (`D2DV`, `D2XP`), before 1.14 | `Game.exe` | `Bnclient.dll` | `D2Client.dll` ⚠️ | not used |
| Diablo II 1.14 and later | `Game.exe` | none | none | not used |
| Warcraft III (`WAR3`, `W3XP`), before 1.28 | `War3.exe` | `Storm.dll` | `Game.dll` | not used |
| Warcraft III 1.28 and later ⚠️ | `Warcraft III.exe` | none | none | not used |

File names are case-insensitive on Windows. When newer patches have no file for a slot, the game passes an empty slot to the check.

The **screen dump** (`.bin`) is only used by [Lockdown](/classic/versioning/lockdown/). It's a capture of the game's video memory, not a file from the install folder, so an implementation that answers Lockdown checks without running the game needs one captured from a real client.

## Games that need none

[Generations 3a and 3b](/classic/versioning/checkrevision/#generation-3a-the-version-number-only) only use the game's version number (and, for 3b, its signing certificate). A bot can answer them without any game files:

| Game | Generation | Version text |
|---|---|---|
| Diablo II 1.14d | 3a | `1.14.3.71` |
| Warcraft II, GOG edition | 3b | `2.0.2.1` ⚠️ |
| Diablo, GOG edition | 3b | `2001, 5, 18, 1` ⚠️ |

## Keeping them current

Hash files have to match the game version the server expects. When Blizzard patched a game, every bot and BNLS server needed new copies, and the [version byte](/classic/versioning/#the-exchange) changed too. A BNLS server saves each bot that work: its operator updates the files once, and bots also get the new version byte from it.
