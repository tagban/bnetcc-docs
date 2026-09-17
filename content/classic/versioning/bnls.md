---
title: "BNLS and JBLS"
categories: ["Classic Battle.net", "Version checking", "Bots"]
products: [STAR, SEXP, SSHR, JSTR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Community servers that answer version checks and logon math for bots, so a bot needs no game files. How they work, how to use one safely, and which are still up."
bnetdocs_documents: [22, 44, 48, 23, 16]
bnetdocs_packets: [BNLS_REQUESTVERSIONBYTE, BNLS_VERSIONCHECKEX2, BNLS_AUTHORIZE, BNLS_AUTHORIZEPROOF]
sources:
  - name: "JBLS (Davnit/JBLS)"
    url: "https://github.com/Davnit/JBLS"
    note: "the JBLS server still in use today; default port and supported version checks"
  - name: "This site's daily server check"
    url: "/servers/"
    note: "which BNLS servers answer today"
---

A **Battle.net Logon Server** (BNLS) is a community service, not a Blizzard one. A bot connects to it, hands over the version-check details it got from Battle.net, and gets back the answer it needs to send. The bot never needs [hash files](/classic/versioning/hash-files/) or a copy of the game.

- **BNLS** was the original, run by Skywing and Yoni of Valhalla Legends at `bnls.valhallalegends.com`. It supported 8 games.
- **JBLS** is a Java re-implementation, first run by Hdx. It added 3 more games (Diablo, Diablo Shareware and StarCraft Shareware), and it's what the BNLS servers still running today use.
- **BNLS#** added a twelfth product code, the Warcraft III demo.

## Servers today

Both use TCP port **9367**, the standard BNLS port.

| Host | Run by |
|---|---|
| `jbls.davnit.net:9367` | Davnit |
| `bnls.bnetdocs.org:9367` | BNETDocs |

Live status is on the [Servers](/servers/) page, checked once a day. Many older hosts have shut down: `jbls.org`, `hdx.jbls.org`, `bnls.net` and `bnls.valhallalegends.com` among them. BNETDocs keeps the full historical list.

## Protocol

A separate TCP connection. There's no protocol selector byte. Every message has a 3-byte header:

```
(UINT16) Length, including this header
(UINT8)  Message ID
(VOID)   Data
```

The server disconnects a connection that's idle for a minute; `BNLS_NULL` (`0x00`) keeps it open.

### Product codes

BNLS numbers games itself, instead of using Battle.net's four-letter codes:

| Code | Game | Code | Game |
|---|---|---|---|
| `0x01` | StarCraft | `0x07` | Warcraft III |
| `0x02` | StarCraft: Brood War | `0x08` | Warcraft III: The Frozen Throne |
| `0x03` | Warcraft II: Battle.net Edition | `0x09` | Diablo |
| `0x04` | Diablo II | `0x0A` | Diablo Shareware |
| `0x05` | Diablo II: Lord of Destruction | `0x0B` | StarCraft Shareware |
| `0x06` | StarCraft Japanese | `0x0C` | Warcraft III demo (BNLS# only) |

`0x00` in a reply means failure or an unsupported product.

### A bot's version check

1. **Get the version byte:** `BNLS_REQUESTVERSIONBYTE` (`0x10`) with the product code. The reply repeats the product code and adds the version byte, or returns product `0` on failure. Send the byte in `SID_AUTH_INFO`.
2. **Log on to Battle.net** and read the version-check file name, its timestamp and the input string from the `SID_AUTH_INFO` reply.
3. **Ask BNLS:** `BNLS_VERSIONCHECKEX2` (`0x1A`) with product code, flags (`0`), a cookie of your choice, the file timestamp, the file name and the input string, exactly as received.
4. **Read the reply:** a 32-bit success flag, then version, checksum, EXE information, your cookie and the current version byte. On failure, only the flag and cookie are sent.
5. **Send the version, checksum and EXE information** to Battle.net in `SID_AUTH_CHECK`.

`BNLS_VERSIONCHECKEX2` works out the generation from the file name, so the bot doesn't have to.

### Optional sign-in

`BNLS_AUTHORIZE` (`0x0E`) sends a bot name, and `BNLS_AUTHORIZEPROOF` (`0x0F`) answers the server's code with a checksum. Neither is required any more, but sending them is a courtesy to the server's operator. The checksum is a standard CRC-32 of the password followed by the server code as 8 uppercase hex digits.

## Use BNLS safely

BNLS isn't encrypted, and anyone can run a server.

- **Never send CD keys or passwords to a BNLS server.** BNLS has messages that hash them for you (`BNLS_CDKEY`, `BNLS_CDKEY_EX`, `BNLS_HASHDATA`, `BNLS_LOGONCHALLENGE` and others), but anyone watching the connection, or a dishonest operator, can keep them. Hash keys and passwords in the bot with an open-source library instead.
- **Use BNLS for the version check only.** It needs nothing secret: the input string and file name come from Battle.net in the clear anyway.
