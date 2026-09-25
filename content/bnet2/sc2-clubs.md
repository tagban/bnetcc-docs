---
title: "StarCraft II clans and groups"
categories: ["Battle.net 2.0"]
products: [S2]
summary: "Clubs on Sunken: a character's clans and groups, member lists and ranks, live member changes, descriptions, clan chat, and the requests that create and manage a clan, with every wire layout."
sources:
  - name: "StarCraft II 5.0.16.97563"
    note: "the club schema, from the metadata embedded in the client, and each scrambled struct's wire order, from the client's own generated reader and writer code"
  - name: "Superiority, by ncarrillo (MIT)"
    url: "https://github.com/ncarrillo/superiority"
    note: "the club list request and a reader for the summary, invitations, joining a club's chat, the scrambling rules, and retail captures"
  - name: "Invigoration"
    note: "confirmed live, 2026-09-25: the club list, member lists, name lookups, the roster subscription and the change notices it brings, and clan chat"
---

**A clan is a kind of club.** StarCraft II's clubs are clans, groups and teams, and they live on [Sunken](/bnet2/sunken/)'s club slot, **13**. A clan's chat is an ordinary chat channel, joined with the club's ID.

Marks on this page: ✅ **confirmed live** (Invigoration, 2026-09-25), ⚠️ from **one source** (named) or **inferred**, 📖 **from the client** (read from the game's own code, not tried live), 🛑 **unknown**. The notation (`u(n)`, `blob`, `opt`) is the one on [the chat page](/bnet2/sunken-chat/#notation).

## Scrambled structs

Most club structs are marked **obfuscated** in the game's schema. The schema still gives each field's name, type and width, but the wire can:

- **send the fields in a different order**, and
- **put filler bits between them**. The client skips filler without checking it.

So a struct's layout is written here as its wire sequence, for example `code, member, club, filler(11), result`. Everything not marked obfuscated goes in schema order.

**Widths always follow the schema.** A string's length counts UTF-8 **bytes**, two bits wider than the character count the schema declares: a club name (≤32 characters) has an 8-bit length, a tag (≤6) a 5-bit one. A struct that another struct "inherits" from (every request's base holds its token) is just its first field, and can land anywhere in the sequence. ✅ Every layout on this page that was tried live decoded to the exact end of its record.

**Filler, if you want to match the client bit for bit:** a 32-bit state starts at the struct's field count. Before each filler run, mix in what's been written so far, rotate left 8, and write the low bits. ⚠️ Superiority; the value isn't checked by the client.

```
bytes written so far   state becomes
0 (less than 1 byte)   NOT state
1                      state + last byte
2 or 3                 state + last u16 (little-endian)
4 or more              state + last u32 + last u16 (little-endian)
then                   rotate left 8
```

## Commands

Club slot 13. The numbers are the game's own `CommandID_S2Map` enum. ✅ from its schema.

| Cmd | Name | Direction | Status |
|---|---|---|---|
| 41 | CreateClub | both | 📖 |
| 42 | ModifyClub | both | 📖 |
| 43 | ModifyMember | both | 📖 |
| 44 | SetMemberRank | both | 📖 |
| 45 | GetRoster | both | ✅ |
| 46 | GetToonClubs | both | ✅ |
| 47 | ClubSubscribe | client → server | ✅ |
| 48 | ClubUnsubscribe | client → server | 📖 |
| 49 | ClubChangeNotification | server → client | ✅ |
| 50 | MemberChangeNotification | server → client | 📖 |
| 51 | SearchClubs | both | ⚠️ Superiority |
| 52 | SearchRoster | both | 📖 |
| 53 | GetMemberClanTags | both | 📖 |
| 54 | InviteAction | both | ✅ two sources |
| 55 | GetClubInfo | both | ⚠️ Superiority |
| 56 | GetMemberInfo | both | 📖 |
| 57 | ClubSettings | server → client, at sign-in | ✅ |
| 58–60 | FileUploadRequest, FileUploadPermit, FileUploadCancel | | 📖 |

A newer set (`CommandID_Toon`) lives on the Toon slot: **CREATE_CLUB_V2 20**, SUBSCRIBE_V2 21, UNSUBSCRIBE_V2 22, SNAPSHOT 23, SYNC 24, INVITE_RESPONSE 25, UPDATE 35. 📖 Which set the current client uses for what isn't known; everything tried live used slot 13.

## Common types

| Type | Wire |
|---|---|
| Character handle | program u(32), region u(8), realm u(32), ID u(64) |
| Character full name | region u(8), program u(32), realm u(32), name: u(7) holding byte count − 2, align, bytes |
| Profile address | label u(32), record ID u(64) |
| Time | u(32) holding seconds + 2³¹ (a signed value, offset) |
| Cache handle | 40 bytes, byte-aligned, no length |

| Enum | Values |
|---|---|
| Club type (u8) | 1 group, 2 clan, 3 team |
| Category (u8) | 1 community, 2 barcraft, 3 esports teams, 4 coaching, 5 company, 6 region, 7 school, 8 shoutcast, 9 other, 10 esports leagues, 11 arcade, 12 IGR |
| Member rank (u8) | 0 none, 5 banned, 10 visitor, 13 rejected, 16 requested, 18 suggested, 20 invited, 24 benchwarmer, 25 honorary, 30 member, 40 officer, 50 owner |
| Member status (u8) | 0 offline, 1 online, 2 in a game, 3 in chat |
| Change type (u2) | 0 insert, 1 update, 2 remove, 3 sync |
| Subscription (u3) | 1 all, 2 events, 3 events (simple), 4 announcements, 5 announcements (simple), 6 message board, 7 roster |

## A character's clubs: GetToonClubs (46)

**Request.** ✅ Matches the request retail sends, byte for byte.

```
token      u(32)
character  handle
align
```

**Reply.**

```
result     u(1)          0 success, 1 failure: then error u(16)
 clubs     u(8) count, then per club: summary, then online counts
 ranks     u(8) count, then u(8) each: your rank in each club, same order
 last page bool
filler     31 bits
token      u(32)
align
```

**Club summary** (a scrambled struct):

```
locale        u(32)   FourCC, e.g. enUS
member count  u(32)
club ID       u(32)
category      u(8)
name          u(8) byte count, align, bytes
filler        6 bits
profile       profile address
flags         u(32)
type          u(8)
program       u(32)   S2
created       time
tag           opt: u(5) byte count, align, bytes
filler        25 bits
file handles  u(3) count, then per entry: opt{ cache handle }
```

**Online counts:** in chat u(32), in a game u(32), online u(32), in that order. ✅ Both retail replies Superiority captured, and live replies, decode to the exact end of their records.

## Member lists: GetRoster (45)

**Request.** ✅ Confirmed live.

```
club ID    u(32)
from       u(2) choice, then:
             0  offset u(32)
             1  character full name
             2  character handle
             3  offset u(32), lowest rank u(8), highest rank u(8)
token      u(32)
align
```

**Reply:**

```
result     u(1)   0 success, 1 failure: then error u(16)
 members   u(8) count (≤200), then per member: handle, rank u(8)
 last page bool
token      u(32)
align
```

**What Battle.net actually does:** ✅ Confirmed live

- **The last-page flag is always false.** Treat a page with fewer than 200 members as the last; asking again from an offset past the end returns an empty page forever.
- **The first request after signing in often comes back empty.** Asking again a moment later returns the members. The list probably wasn't loaded yet.
- **The reply only hands the token back.** To know whose members arrived, put the club ID in the token.

Members come as character handles. Their names come from the [profile name lookup](/bnet2/sc2-profiles/#names-for-character-handles), up to 32 per request. ✅

## Following changes: ClubSubscribe (47)

```
subscriptions  u(8) count, then per club:
  filler       11 bits
  club ID      u(32)
  what         u(3)   7: the roster (members and their status)
  since        time   0: now
align
```

✅ Confirmed live. Right after a roster subscription, Battle.net sends a **ClubChangeNotification (49)** for each club with its full summary and its **description**, both marked change type 3 (sync). A client that can't read command 49 loses whatever follows it in the stream.

**Member status isn't sent up front.** In the minute after subscribing, no member statuses arrived; they come as changes, when a member comes online, starts a game and so on. ⚠️ Inferred from one session.

## Member changes: MemberChangeNotification (50)

```
changes  u(8) count, then per change:
  info         u(1) choice: 0 rank: old u(8), new u(8); 1 status u(8)
  filler       5 bits
  club ID      u(32)
  filler       29 bits
  change type  u(2)
  member       handle
  stamp        u(64)
align
```

📖 From the client's code. A fixed-length skip, as some readers use, is wrong: the record is a list.

## Club changes: ClubChangeNotification (49)

```
changes  u(8) count, then per change:
  filler       6 bits
  club ID      u(32)
  info         u(4) choice, then the variant below
  change type  u(2)
  stamp        u(64)
align
```

| Info | Variant |
|---|---|
| 0 | summary deltas: u(6) count of changes (name, tag, type, category, locale, a flag, a club file) |
| 1 | full summary (the club summary above) ✅ |
| 2 | online status: nothing |
| 3, 7, 8 | announcement, **description** ✅, message board: user text |
| 4 | announcement (simple): created time only |
| 5 | event |
| 6 | event (simple): created, start, title (u(9) byte count, align, bytes), end |

**User text:** created (time), links (u(2) count of map links), text (u(13) byte count, align, bytes), author (u(64) profile record ID). **Event:** links, end, author, start, created, text.

## Settings: ClubSettings (57)

Sent at sign-in. ✅ Confirmed live.

```
tag rule      u(13) byte count, align, bytes    a regular expression
name rule     u(13) byte count, align, bytes    a regular expression
cache         4 × u(32)   info cache size, member cache size, info expiry, online-status expiry
event expiry  u(32)
align
```

Live, both rules were `^([\x{20}-\x{7F}\x{A0}-\x{FF}]+)$`: printable Latin-1. ✅

## Invitations: InviteAction (54)

```
code     u(2)    0 invited, 1 accepted, 2 declined
member   handle  zeros when answering
club ID  u(32)
filler   11 bits
result   u(16)
align
```

✅ Two sources: Superiority's retail capture of an invitation, and the client's code. Answer an invitation by sending it back with code 1 or 2.

## Clan chat

A club's chat is joined with the ordinary chat join request (Chat slot 5, command 0), using the club locator:

```
locator  u(2)   3: a club
         u(16)  0
club ID  u(32)
token    u(32)
align
```

✅ Superiority's retail capture, and confirmed live. The member list that follows is the usual one; club channels add each member's rank as a member status.

## Managing a club

📖 From the client's code; none of these has been sent live yet.

**SetMemberRank (44).** Inviting, promoting, demoting, banning and handing over ownership all look like rank changes. Kicking and leaving are probably rank "none". ⚠️ Inferred

```
old rank   u(8)
new rank   u(8)
token      u(32)
club ID    u(32)
member     character full name
member ID  u(64)
align
```

The reply is result u(16), 3 filler bits, token u(32).

**ModifyMember (43):** token u(32), then one member change as in command 50. The reply is result u(16), token u(32).

**ModifyClub (42):** one club change as in command 49 (summary deltas, the description, an announcement...), then token u(32). The reply is token u(32), result u(16).

**GetMemberClanTags (53):** the request is token u(32), character handle. The reply is 24 filler bits, result u(16), token u(32), then an optional tag and an optional club ID.

**GetClubInfo (55):** the request is token u(32), then a u(8) count of club IDs. The reply is result (0: a club list as in command 46, and a last-page bool; 1: error u(16)), then token u(32). ⚠️ Superiority

## Creating a club

📖 From the client's code; not tried live.

**CreateClub (41):**

```
flags      u(32)   privacy and other settings; which bit is which isn't known
filler     14 bits
token      u(32)
type       u(8)    2 for a clan
tag        opt: u(5) byte count, align, bytes
category   u(8)
name       u(8) byte count, align, bytes
locale     u(32)
align
```

The reply is 32 filler bits, token u(32), then result: 0 success (club ID u(32), profile address) or 1 failure (error u(16)).

**CreateClubV2 (Toon slot, command 20)** carries the same details plus the program and a subregion: 26 filler bits and the token, then 13 filler bits, flags u(8), type, program u(32), category, name, locale, tag, subregion u(8). Its reply is club ID u(32), result u(16), then 26 filler bits and the token.

**Rules:** names are up to 32 characters and tags up to 6, both matching the rules in ClubSettings. There's no way to reserve or check a name first; a taken one fails the create. The error codes are listed in Superiority's `errors.rs` (11000–11172). ⚠️ Superiority

## Showing members like the game

StarCraft II shows a member as `<TAG> Name`, with no `#123` code. The tag comes from the member's [presence](/bnet2/sc2-presence/#the-fields-that-matter) (field `0x50004`).
