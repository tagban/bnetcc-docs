---
title: "StarCraft II friends"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "The friends list on Sunken, asking for a friend's characters, the unknown Friends command 28, and why the Battle.net friends service is closed to the game."
sources:
  - name: "Superiority, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/superiority"
    note: "the FriendsListNotify5 and ToonsOfFriends decoders, and ToonsOfFriendsRequest"
  - name: "novares"
    note: "independent source for the layouts of Friends 6 and 30"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-24: the friends list, ToonsOfFriends, Friends command 28, and FriendsService refusing an SC2 session"
---

**A StarCraft II client gets its friends list from [Sunken](/bnet2/sunken/)**, on the Friends slot (3). It doesn't get it from Battle.net's own friends service: that's closed to the game ([below](#the-battlenet-friends-service-is-closed)). Who is online comes separately, from [presence](/bnet2/sc2-presence/).

Marks on this page: ✅ **confirmed live** (Invigoration, 2026-09-24) or from two sources, ⚠️ from **one source** (named) or **inferred**, 🛑 **unknown**. The notation (`u(n)`, `blob`, `opt`) is the one on [the chat page](/bnet2/sunken-chat/#notation), which also has the short form of every Friends record.

## Two kinds of friend

| Kind | Identified by | What the record gives |
|---|---|---|
| **Account** (a Battle.net friend) | Account ID, u32 | Maybe a display name, maybe a real name, a profile address |
| **Character** (an SC2-only friend) | Character handle | The character's name and profile address |

**Account friends often arrive with no usable name.** ✅ Confirmed live. Name them from, in order:

1. the BattleTag in their presence (`0x1001E`, see [presence](/bnet2/sc2-presence/#the-fields-that-matter)),
2. the display name in the friend record,
3. their characters, from [ToonsOfFriends](#toonsoffriends),
4. the real name, only if the user has asked to see real names.

## Friends 30: FriendsListNotify5

The friends list, sent unprompted at sign-in and again when it changes. ✅ Two sources, and confirmed live

```
complete       opt{ bool }
count          u(7)                  (above 64: stop)
repeat count times:
    op         u(2)
      0  added:     a friend (below)
      2  changed:   a friend (below)
      1  removed:   u(1): 0 → account ID u(32)
                          1 → character handle
      3  stop
align
```

**A friend** starts with `arm u(2)`:

| Arm | Kind | Fields, in order |
|---|---|---|
| 0 | Character | character handle; name `blob(7, 2)`; profile address; note `opt{ blob(9) }` |
| 1 | Account | account ID `u(32)`; real name `opt{ blob(8), blob(8) }`; display name `opt{ blob(7) }`; profile address; custom message `opt{ s(32), blob(9) }`; note `opt{ blob(9) }`; last online `s(32)`; account serial `u(64)`; game account ID `u(32)` |
| 2 | Presence only | account ID `u(32)`; custom message `opt{ s(32), blob(9) }`; last online `s(32)` |
| 3 | | stop |

| Part | Layout |
|---|---|
| Character handle | program `u(32)`, region `u(8)`, realm `u(32)`, ID `u(64)`: 136 bits. Program comes **before** region here. |
| Profile address | label `u(32)`, record ID `u(64)` |
| Real name | Given name, then surname, each an 8-bit byte count and byte-aligned UTF-8. It's the friend's real name: keep it private unless the user asks for it. |
| `s(32)` | Stored with the sign bit flipped: read `u(32)`, then XOR `0x80000000`. ⚠️ Superiority |

Byte limits from Superiority: a character name is at most 100 bytes, a display name 108, a note or custom message 508. ⚠️ Superiority

**Byte example**, removing account 12345678:

```
5e 03 09 02 f1 85 0e
```

`5e 03` is the route (Friends slot 3, command 30). Then: no `complete`, a count of 1, op 1, the account choice (0), and the account ID. Built here from the layout above.

## ToonsOfFriends

**To find an account friend's SC2 characters, ask for them.** ✅ Confirmed live; layout from Superiority.

**ToonsOfFriendsRequest**, Friends slot 3, command 6, from the client:

```
account ID     u(32)
align
```

For account 12345678: `46 03 17 8c 29 06`.

**ToonsOfFriendsNotify**, Friends slot 3, command 6, from the server:

```
count          u(7)                  (above 100: stop)
repeat count times:
    region     u(8)
    program    u(32)
    realm      u(32)
    name       blob(7, 2)            the character name and code, e.g. Raynor#1234
    label      u(32)                 the character's profile address
    record ID  u(64)
    account ID u(32)                 the friend it belongs to
complete       bool
align
```

**Byte example**, one character: region 1, `S2`, realm 1, `Raynor#1234`, profile `0xCAFEBABE` / `0x12345678`, account 12345678:

```
46 03 01 01 00 14 cc 02 00 00 00 11 01
52 61 79 6e 6f 72 23 31 32 33 34        "Raynor#1234"
ca fe ba be 00 00 00 00 12 34 56 78     profile address
00 bc 61 4e                             account 12345678
01                                      complete
```

Built here from the layout. The first 12 bytes match Superiority's retail example, which has the same region, program and realm.

## Friends 28: probably FriendInvitationAdded

**Battle.net sent a Friends command 28 record at sign-in, unprompted.** Its layout isn't known, so a decoder that stops on unknown records stops here. 🛑

What was seen, in a 44-byte record: ✅ Confirmed live

- `5c 3b` is the route: command 28, Friends slot 3.
- The rest of the second byte held the value 7 (5 bits).
- Then a byte-aligned length, and **a BattleTag** in UTF-8: another player's, not the account's own.
- Then 27 bytes that aren't decoded. They probably include IDs and a time. ⚠️ Inferred

The same record came in four sign-ins in a row, then stopped coming in later sessions the same day. **It's most likely a pending friend invitation, sent at each sign-in until it's answered or withdrawn:** Battle.net's name for such a record is FriendInvitationAdded. ⚠️ Inferred, not confirmed. How to accept or decline an invitation is 🛑 unknown.

Invigoration drops the rest of the bytes it has buffered when it meets this record. That's only safe when it's the last record in the read; a full decoder would need its layout.

## Other Friends records

| Command | Record | Notes |
|---|---|---|
| 31 | AccountBlockNotify | The blocked-accounts list. Layout on [the chat page](/bnet2/sunken-chat/#friends-records). |
| 33 | ToonBlockNotify | The blocked-characters list. Each entry is the add/remove bit **first**, then region `u(8)`, program `u(32)`, realm `u(32)` and name `blob(7, 2)`. ⚠️ Single source: the one live record, which was cut short, reads cleanly this way |

## The Battle.net friends service is closed

**A StarCraft II session can't use Battle.net's own friends service.** ✅ Confirmed live

Invigoration kept [Front](/bnet2/front/) open after the handoff to Sunken and called **FriendsService.Subscribe**:

| | |
|---|---|
| Service | `bnet.protocol.friends.FriendsService`, hash `0xA3DDB1BD` |
| Method | 1, Subscribe |
| Body | `V(2, object ID)`: a listener ID of the client's choosing |

What happened:

1. The reply's status was **3025**, `ERROR_RPC_METHOD_DISABLED`.
2. At the same moment, Battle.net called ConnectionService (`0x65446991`) **method 4**, asking the client to disconnect. Its 22-byte body wasn't decoded.
3. Battle.net closed the Front WebSocket.

**Sunken and its chat carried on normally.** So an SC2 client should close Front after the handoff, as the game does, and take friends from Sunken. SC:R gets the Battle.net friends list another way, as [FriendUpdated calls](/bnet2/scr-chat/#friends) on its classic socket.
