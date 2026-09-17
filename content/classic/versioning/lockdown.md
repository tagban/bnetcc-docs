---
title: "Lockdown"
categories: ["Classic Battle.net", "Version checking"]
products: [STAR, SEXP, W2BN, DRTL]
summary: "CheckRevision generation 2: twenty libraries that hash the game as it sits in memory, plus a dump of the screen, with a modified SHA-1."
bnetdocs_documents: [47]
sources:
  - name: "JBLS: CheckRevisionV3.java, lockdown_SHA1.java, lockdown_heap.java"
    url: "https://github.com/Davnit/JBLS/tree/develop/Hashing"
    note: "the only open implementation we know of; the order of the hashed data, the pads and the output shuffle come from reading it (no code copied)"
  - name: "Skywing, An Objective Analysis of the Lockdown Protection System for Battle.net (Uninformed)"
    url: "http://www.uninformed.org/?v=9&a=1"
    note: "the original reverse-engineering write-up, including the library's defences against tampering"
---

**Lockdown** is the Windows version of CheckRevision generation 2, served from late 2006 to *StarCraft*, *Diablo* and *Warcraft II*. The Mac version is called **psistorm**. It was built to be much harder to fake than [generations 1a and 1b](/classic/versioning/checkrevision/): instead of adding up bytes from files on disk, it hashes the game the way Windows loads it into memory, and includes a picture of the screen.

Marks follow [How to read these pages](/how-to-read/): ✅ verified, ⚠️ single source.

## Files

- **Twenty libraries:** `lockdown-IX86-00.mpq` to `lockdown-IX86-19.mpq`, each holding a DLL of the same name. The server picks one for each connection. ✅
- **Mac:** `psistorm-XMAC-00.mpq` … and `psistorm-PMAC-00.mpq` …. ✅
- Each library carries its own pair of constants, used while hashing. Implementations that don't run the DLL have to read them out of each of the twenty files. ⚠️

## What's hashed

Lockdown hashes with its own variant of SHA-1: different from standard SHA-1, and different from the X-SHA-1 that Classic games use for passwords. ✅

The server's input string (the "formula" field) isn't a formula here. It's the key. The client:

1. **Shuffles the input string into 16 bytes.** Each character is treated as a digit in a large number, which is rebuilt byte by byte. ✅ (that it's shuffled) ⚠️ (how)
2. **Builds two 64-byte pads.** One is filled with `0x36`, the other with `0x5C`, and the 16 key bytes are XORed into the start of each. This is the same shape as HMAC. ⚠️
3. **Inner hash.** Starting with the first pad, it hashes, in order: ⚠️
   1. the Lockdown DLL itself,
   2. the game EXE,
   3. the game's other hashed files, such as `Storm.dll` and `Battle.snp` (see [Hash files](/classic/versioning/hash-files/)),
   4. the **screen dump**: a capture of the game's video memory,
   5. two 4-byte values: `1`, meaning the library's return address checked out, and `0`, the module offset.
4. **Outer hash.** The second pad, then the 20-byte result of the inner hash. ⚠️

### Hashing a program "as loaded"

For each DLL and EXE, Lockdown doesn't hash the file's bytes as stored. It walks the Windows program (PE) format: ⚠️

- the headers, rounded up to the file alignment;
- each section as it would sit in memory, rounded up to the section alignment;
- writable sections as zeros, since their contents change while the game runs;
- addresses the Windows loader would adjust (relocations and imported functions) handled separately, using the library's own constants.

So a copy of the game files alone isn't enough to answer: the screen dump is needed too. ✅

## Output

- **Checksum:** the first 4 bytes of the outer hash, as a `DWORD`. ⚠️
- **EXE information:** the next 16 bytes of the hash, converted by another shuffle into a null-terminated string. The shuffle can shorten it, so it isn't always 16 bytes long. ✅
- **Version:** the EXE's version, as in generation 1. ✅

## For server authors

- Verifying a Lockdown answer requires the client's files, its screen dump and the twenty libraries. Failing open avoids all of that.
- These games also run generation 1a. Command Center sends `IX86ver1.mpq` to StarCraft, Diablo and Warcraft II instead, and a real Warcraft II client runs it.
- On Blizzard's side, the GOG editions of *Diablo* and *Warcraft II* use [generation 3b](/classic/versioning/checkrevision/#generation-3b-version-number-and-certificate) instead.
