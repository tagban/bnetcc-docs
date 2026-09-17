---
title: "NLS: Warcraft III's password system"
categories: ["Classic Battle.net", "NLS"]
products: [WAR3, W3XP]
summary: "The New Logon System proves a player knows their password without ever sending it or anything that could replace it. It's a modified SRP-6."
bnetdocs_documents: [24]
sources:
  - name: "Command Center: WARCRAFT3.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3.md"
    note: "the algorithm, byte-order rules and test values, checked with an independent Python model"
  - name: "Command Center: WARCRAFT3-FIELD-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/WARCRAFT3-FIELD-NOTES.md"
    note: "the two mistakes that pass your own tests but fail a real client"
---

*Warcraft III* logs on with NLS (logon type `0x02` in `SID_AUTH_INFO`). The server stores a **salt** and a **verifier** for each account, never the password or a hash that could stand in for it. The messages are [`SID_AUTH_ACCOUNTCREATE`](/classic/bncs/sid-auth-accountcreate/), [`SID_AUTH_ACCOUNTLOGON`](/classic/bncs/sid-auth-accountlogon/) and [`SID_AUTH_ACCOUNTLOGONPROOF`](/classic/bncs/sid-auth-accountlogonproof/).

## Constants

| Name | Value |
|---|---|
| `g` | `47` (`0x2F`) |
| `N` | `0xF8FF1A8B619918032186B68CA092B5557E976C78C73212D91216F6658523C787` (256 bits) |
| Hash | **Standard SHA-1** everywhere. Not X-SHA-1. |

## The calculation

`C` is the account name, `P` the password, and `‖` means "followed by".

```
x  = SHA1( s ‖ SHA1( UPPER(C) ‖ ":" ‖ UPPER(P) ) )      read as a little-endian number
v  = g^x mod N                                           the verifier, stored with s
A  = g^a mod N                                           client; a is random for each logon
B  = (v + g^b mod N) mod N                               server; b is random for each logon
u  = first 4 bytes of SHA1(B)                            read as a BIG-endian number; never sent
S  = client: (B − v)^(a + u·x) mod N
     server: (A · v^u)^b mod N                           both sides get the same S
K  = SHA1 of S's even-numbered bytes and SHA1 of its odd-numbered bytes,
     interleaved byte by byte                            40 bytes
I  = SHA1(g) XOR SHA1(N)                                 a 20-byte constant
M1 = SHA1( I ‖ SHA1(UPPER(C)) ‖ s ‖ A ‖ B ‖ K )          the client's proof
M2 = SHA1( A ‖ M1 ‖ K )                                  the server's proof
```

## Byte order: where implementations go wrong

- **Every number is 32 bytes, little-endian, padded with zeros:** `s`, `v`, `A` and `B` on the wire, and whenever they are hashed. `K` is always 40 bytes.
- **Don't drop leading zero bytes.** Encoding a number at its natural length passes your own tests, but about one logon in 256 has a zero top byte, hashes a byte short, and fails. The result is "some accounts never work".
- **Uppercase the name and password,** in `x` and in `M1`. (Classic games lowercase instead; NLS is the opposite.)
- **`x` is read little-endian, but `u` is read big-endian.** Both are correct.
- **`I` hashes `N` in its little-endian form.** Its bytes are `6C0E97ED 0AF96BAB B15889EB 8BBA25A4 F08C01F8`.
- **NLS version 1** (logon type `0x01`, older clients) reverses the byte order of `N`.

**A useful shortcut:** if the server accepts the client's `M1`, its `M2` is automatically right. Both are built from the same `A` and `K`, so "the client rejects `M2`" is never a math bug. If the client disconnects after a successful proof, check the reply's *length* instead (see `SID_AUTH_ACCOUNTLOGONPROOF`).

## Test values

For account `Tagban`, password `hunter2`, salt bytes `00 01 02 … 1F`, `a` = bytes `01 02 … 20` and `b` = bytes `02 03 … 21` (both little-endian):

```
x  = 0x395e620c90a3919c75ede2fdd52aaf8cd6b28d39
v  = 7f2bf7dcd443e0f945a5a7bcbfec2f5e3fee8242d09b62aac46c194963dcafef
A  = f085e0261e42a247db6e0bb57ae40d56746b0c16783606718a2c500d3fed2594
B  = 423ac3a9427c556639f31804d59e3e2c409e182add1648440ed88622abb94580
u  = 0x672cb5c0
K  = 2eeb577075dfcbdd4ec5c17e13c8df4efc8bc573ce35f665c6a913bf0c6e2febf0b0c23a00428941
M1 = a4d99ac492f45207ce0ed8e1c9729f38a425d151
M2 = ba079a3bfcf36d706f1df1dd2934c3252aad086f
```

These come from a reference model whose client and server sides agree over random inputs. A real *Warcraft III* client has since logged on successfully with the same implementation.

## Server safety checks

The game doesn't require these, but a server should still refuse `A mod N = 0`, pick a fresh `b` for every logon, compare `M1` in constant time, and never reuse `b` after a failure.
