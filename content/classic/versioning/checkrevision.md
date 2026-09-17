---
title: "CheckRevision"
categories: ["Classic Battle.net", "Version checking"]
products: [STAR, SEXP, SSHR, JSTR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Blizzard's version-check library, generation by generation: what the server sends, what the client calculates, and what it sends back."
bnetdocs_documents: [47]
sources:
  - name: "JBLS: CheckRevisionV1.java, V2, V4 and Constants.java"
    url: "https://github.com/Davnit/JBLS/tree/develop/Hashing"
    note: "independent implementation used to cross-check the constants, the operators, the padding and the SHA-1 generations (JBLS numbers the generations differently: its V2 is 1b, V3 is Lockdown and V4 is 3a and 3b)"
  - name: "Command Center: WARCRAFT3-FIELD-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3-FIELD-NOTES.md"
    note: "the real formula a stock server sends with `ver-IX86-1.mpq`"
---

Every generation returns the same three values, which the client sends in [`SID_AUTH_CHECK`](/classic/bncs/sid-auth-check/) or [`SID_REPORTVERSION`](/classic/bncs/sid-reportversion/):

| Value | Type | What it is |
|---|---|---|
| Version | `DWORD` | Which build of the game this is. |
| Checksum | `DWORD` | The result of the calculation. |
| EXE information | `STRING` | Extra text that depends on the generation. |

Marks follow [How to read these pages](/how-to-read/): ✅ verified, ⚠️ single source.

## Generations 1a and 1b: the formula

**Files:** `IX86ver0.mpq` to `IX86ver7.mpq` (1a) and `ver-IX86-0.mpq` to `ver-IX86-7.mpq` (1b). ✅

### Input

The server sends a **formula** as a text string: three starting values, a count, and that many steps. This is the real one a stock server sends with `ver-IX86-1.mpq`:

```
B=454282227 C=2370009462 A=2264812340 4 A=A^S B=B-C C=C-A A=A+B
```

The starting values can come in any order. The steps normally have this shape, with only the operators changing: `A=A?S B=B?C C=C?A A=A?B`. The operators are `+`, `-`, `*`, `/` and `^` (exclusive or). ✅

Don't assume exactly four steps in that order. Official servers have sent a short "default" formula, `A=0 B=0 C=0 4 A=A+S C=C+A`, which still says `4` but has two steps, for example to StarCraft clients older than 1.18. ✅

### Calculation

1. **Mix in the file number.** The digit in the MPQ's name (0 to 7) picks one of eight constants, which is XORed into `A` before any hashing: ✅

   | Digit | Constant |
   |---|---|
   | 0 | `0xE7F4CB62` |
   | 1 | `0xF6A14FFC` |
   | 2 | `0xAA5504AF` |
   | 3 | `0x871FCDC2` |
   | 4 | `0x11BF6A18` |
   | 5 | `0xC57292E6` |
   | 6 | `0x7927D27E` |
   | 7 | `0x2FEC8733` |

2. **Walk the files.** Read each game file in turn (the EXE first, then its support files: see [Hash files](/classic/versioning/hash-files/)) as a sequence of 32-bit little-endian numbers. For each number `S`, run all the steps in order. All arithmetic is 32-bit and wraps. ✅
3. **The checksum is `C`** when the last file is done. ✅

**The one difference in 1b** is padding: each file is extended to the next multiple of 1024 bytes, filled with bytes counting down from `0xFF` (`FF FE FD …`, wrapping back to `FF` after `00`). Generation 1a had a bug that crashed on systems with Data Execution Prevention, which is thought to be why 1b exists. ✅ (padding) ⚠️ (reason)

### Output

- **Version:** the product version from the EXE's version resource (`dwProductVersionMS` and `dwProductVersionLS`). ✅
- **EXE information:** the EXE's name, last-modified date (`MM/DD/YY`), time (`HH:MM:SS`, 24-hour) and size in bytes, separated by single spaces: `Game.exe MM/DD/YY HH:MM:SS size`. ✅

In May 2016 Blizzard signed the 1b DLLs, and StarCraft 1.17.0 and Diablo II 1.14d check that signature before running the DLL. ⚠️

## Generation 2: Lockdown

**Files:** `lockdown-IX86-00.mpq` to `lockdown-IX86-19.mpq`, and `psistorm-XMAC-…` / `psistorm-PMAC-…` on Mac. It hashes the game as it looks in memory, plus a dump of video memory, with a modified SHA-1. It has its own page: [Lockdown](/classic/versioning/lockdown/).

## Generation 3a: the version number only

**File:** `CheckRevision.mpq`. Served to Diablo II since January 4, 2019. ✅

This generation doesn't read the game files. It only proves the client knows its own version number, so a bot can calculate it without any game files.

### Input

A short base64 string (8 characters, sent as a 9-byte null-terminated `STRING`), different on every connection. Decoded, only its **first 4 bytes** are used; call them the seed. ✅

### Calculation

```
text     = seed ‖ ":" ‖ version ‖ ":" ‖ 0x01
result   = base64( SHA1(text) )                   standard SHA-1; 28 characters
checksum = first 4 characters of result, read as a little-endian DWORD
exeinfo  = the other 24 characters, null-terminated
```

`‖` means "followed by". `version` is the EXE's file version as dotted text. For Diablo II 1.14d it's `1.14.3.71`. ✅

### Output

- **Version:** always `0`. ✅
- **Checksum** and **EXE information:** as above. ✅

## Generation 3b: version number and certificate

**File:** `CheckRevisionD1.mpq`. Served only by `connect-forever.classic.blizzard.com`, to the GOG editions of Diablo (from March 7, 2019) and Warcraft II (from March 28, 2019). ✅

### Calculation

First, the whole of generation 3a, with the same seed. Then one more hash is added to the EXE information:

```
extra    = base64( SHA1( public key ‖ seed ) )
exeinfo  = (3a's 24 characters) ‖ ":" ‖ extra, null-terminated
```

`public key` is the public key from the certificate the game EXE is signed with. ⚠️ No open implementation we've seen includes the key itself, so this step hasn't been confirmed end to end.

### Output

- **Version:** always `6`. ✅
- **Version text for 3a's step:** GOG *Warcraft II* reports `2.0.2.1`. ⚠️ (JBLS lists it, and it matches what BNET.cc's operator remembers seeing; a capture would make it ✅.) GOG *Diablo* reports `2001, 5, 18, 1`, with commas, exactly as its version resource spells it. ⚠️

## History

| Date | Change |
|---|---|
| January 17, 1997 | The first version-check DLL (`ix86std.dll`) compiled. |
| March 3, 1997 | CheckRevision 1a compiled. |
| August 10, 2006 | CheckRevision 1b compiled. |
| Late 2006 | 1b served to Diablo II and Warcraft III; Lockdown served to StarCraft, Diablo and Warcraft II. |
| March 5, 2007 | CheckRevision updated. |
| April 21, 2016 | Generation 2 updated for Mac OS X (`XMAC`). |
| May 27, 2016 | 1b DLLs signed. |
| January 3, 2019 | CheckRevision 3a compiled. |
| January 4, 2019 | Server reset: Diablo II moves to 3a. |
| February 2, 2019 | CheckRevision 3b compiled. |
| March 7, 2019 | GOG releases *Diablo*; `connect-forever` serves it 3b. |
| March 28, 2019 | GOG releases *Warcraft II*; `connect-forever` serves it 3b. |
| February 25, 2020 | CheckRevision 3a recompiled. |

Dates are from the BNETDocs CheckRevision document.
