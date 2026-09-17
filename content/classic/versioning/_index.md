---
title: "Version checking"
categories: ["Classic Battle.net", "Version checking"]
products: [STAR, SEXP, SSHR, JSTR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Before a Classic client may log on, the server makes it prove it's running the right version of the game. This section explains how."
bnetdocs_documents: [47, 43, 41, 10]
bnetdocs_packets: [SID_OPTIONALWORK, SID_REQUIREDWORK, SID_EXTRAWORK]
sources:
  - name: "JBLS (Davnit/JBLS, develop branch)"
    url: "https://github.com/Davnit/JBLS/tree/develop/Hashing"
    note: "an independent implementation of every CheckRevision generation, used to cross-check each fact on these pages (no code copied)"
  - name: "Command Center: bnetccd session handling"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetccd/src/session.rs"
    note: "what a server sends, which file name each game expects, and failing open"
---

Every Classic game runs a **version check** right after connecting. The server names a small program for the client to run and gives it a random input. The client runs that program over its own game files and sends back the answer. If the answer is wrong, the server tells the client to upgrade, or disconnects it.

The program is Blizzard's **CheckRevision** library. It has changed several times, and each game is sent the generation its client understands.

## The exchange

| Step | Newer logon | Older logon |
|---|---|---|
| Client names its game, platform and version byte | [`SID_AUTH_INFO`](/classic/bncs/sid-auth-info/) | [`SID_STARTVERSIONING`](/classic/bncs/sid-startversioning/) |
| Server sends the file name, its timestamp and the input string | `SID_AUTH_INFO` reply | `SID_STARTVERSIONING` reply |
| Client downloads the file, if it doesn't already have that version | [`SID_GETFILETIME`](/classic/bncs/sid-getfiletime/), then BNFTP on a second connection | same |
| Client sends the result: version, checksum, EXE information | [`SID_AUTH_CHECK`](/classic/bncs/sid-auth-check/) | [`SID_REPORTVERSION`](/classic/bncs/sid-reportversion/) |
| Server accepts, or asks for an upgrade | `SID_AUTH_CHECK` reply | `SID_REPORTVERSION` reply |

The file is an MPQ archive holding one DLL. Its name tells the client which CheckRevision generation to run. The client uses the timestamp to decide whether its cached copy is current.

**Version byte.** Each game also sends a one-byte-wide version number (a `DWORD` on the wire). Blizzard raised it with each patch, and a server rejects a client whose byte is out of date. Bots usually ask a BNLS server for the current value: see [BNLS and JBLS](/classic/versioning/bnls/).

## Generations

| Generation | File name | Served to | Needs the game files? |
|---|---|---|---|
| **1a** | `IX86ver0.mpq` … `IX86ver7.mpq` | StarCraft, Diablo, Warcraft II, early Diablo II and Warcraft III | Yes |
| **1b** | `ver-IX86-0.mpq` … `ver-IX86-7.mpq` | Diablo II and Warcraft III, from late 2006 | Yes |
| **2 (Lockdown)** | `lockdown-IX86-00.mpq` … `lockdown-IX86-19.mpq` | StarCraft, Diablo, Warcraft II, from late 2006 | Yes, plus a screen dump |
| **3a** | `CheckRevision.mpq` | Diablo II, since the server reset of January 4, 2019 | No: only the version number |
| **3b** | `CheckRevisionD1.mpq` | The GOG editions of Diablo and Warcraft II, on `connect-forever.classic.blizzard.com` | No: the version number and the EXE's signing certificate |

Mac clients use their own platform codes in the file name (`XMAC`, `PMAC`), and Lockdown's Mac equivalent is called `psistorm`. Details of each generation are on the [CheckRevision](/classic/versioning/checkrevision/) page, and generation 2 has its own page: [Lockdown](/classic/versioning/lockdown/).

## What a server has to do

An official server computes the expected answer and compares it. A community server doesn't have to:

- **Failing open.** Command Center, and many PvPGN setups, never recompute the hash: any well-formed answer passes. The server still has to send a real file name and a formula the client can run, or the client can't finish its side.
- **Send the right name.** The client decides how to run the check from the file name alone, so a mismatch fails before hashing starts. Command Center sends `IX86ver1.mpq` to StarCraft, Diablo, Warcraft II and Warcraft III 1.26 or older (version byte `0x1A` or lower), and `ver-IX86-1.mpq` to Diablo II and Warcraft III 1.27 or newer.
- **Use Blizzard's own MPQ.** The client checks the archive's Blizzard digital signature and hangs up if it's missing, so a server can't build its own version-check file for these games. ⚠️ (Mac clients reportedly skip the check.)
- **Serve the file.** The client downloads the MPQ over BNFTP if it doesn't have it. Warcraft III uses BNFTP version 2, and keeps re-requesting until it gives up if it gets the wrong file.

## After the version check

- **ExtraWork.** Some servers followed a successful check with `SID_OPTIONALWORK` (`0x4A`) or `SID_REQUIREDWORK` (`0x4C`). Each names another MPQ, traditionally `IX86ExtraWork.mpq`. The client fetches it (`SID_GETFILETIME` request ID `0x80000005` for optional work, `0x80000006` for required work), runs the DLL inside, and returns the result in `SID_EXTRAWORK` (`0x4B`). It collected hardware information. Optional work only runs if `HKCU\Software\Battle.net\Optimize\SysDesc` is `1`. A community server has no reason to send either message.
- **Warden.** Switched off. See [Warden](/classic/versioning/warden/).

