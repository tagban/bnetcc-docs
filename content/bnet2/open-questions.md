---
title: "Battle.net 2.0: open questions"
categories: ["Battle.net 2.0"]
products: [S2, S1, OSI, Fen]
summary: "What isn't known yet about StarCraft II, StarCraft: Remastered, Diablo II: Resurrected and Diablo IV on modern Battle.net, and where to look."
sources:
  - name: "Invigoration"
    note: "the questions left open by its live tests on 2026-09-24"
---

These are the gaps found while building native StarCraft II and SC:R chat on 2026-09-24. **If you capture any of them, please update the page it belongs on** and say how you confirmed it.

## StarCraft II: wins, scores and ladder rank

**Where a player's league, MMR, wins and ladder rank come from isn't known.** 🛑

- **Not in presence.** None of the 69 fields a live session announced carries them. See [presence](/bnet2/sc2-presence/#the-fields-that-matter). ✅ Confirmed live
- **Not in profile path `[0x14]`.** It returns only cosmetics: the portrait and 121 other keys. See [profiles](/bnet2/sc2-profiles/#other-keys-in-the-block). ✅ Confirmed live
- **Other profile-read paths are unknown**, and so are the record types a Start answer names (6145 was seen). The next step is to capture the game opening a player's profile or the ladder screen, and note the paths it reads.
- The current-season record (S2 master slot 10, command 27) is read past but not decoded. It may hold season and league data. ⚠️ Inferred

## Emoticons in chat

**How emoticons travel in chat isn't known for any Battle.net 2.0 game.** 🛑

- **StarCraft II:** a profile holds an `EMOT` key (0 in the one profile read), next to `PORT` and `BADG`. How an emoticon appears inside a Sunken chat message, and which ones a player owns, aren't known.
- **Diablo II: Resurrected** reportedly behaves like classic chat, even though it runs on the modern [channel service](/bnet2/d2r-d4-chat/). Not captured. ⚠️
- **Diablo III and Diablo IV** use the modern channel structure, so their emoticons are probably carried differently from D2R's. Not captured. ⚠️ Inferred

## StarCraft II badges and other cosmetics

- **`BADG` and the image it names.** There's a portrait catalog, but no known table from badge IDs to pictures. 🛑
- **The other 120 or so keys** in a profile block (`CSKI`, `Anim`, `GRBn`, `SPRY`, the per-unit `P`, `T` and `Z` keys…) have no confirmed meaning. See [profiles](/bnet2/sc2-profiles/#other-keys-in-the-block). 🛑
- **The packed number's dropped low bit**, and markers below `0xB0`. 🛑

## Other regions and gateways

- **SC:R gateways 20 (Europe), 30 (Korea) and 45 (Asia)** are announced to a U.S. account, but only 10 and 11 have been used. Whether a U.S. account can play on the others, and whether other Battle.net regions use another Aurora host, isn't known. 🛑
- **StarCraft II outside the Americas** hasn't been tested with these pages' records. 🛑

## StarCraft: Remastered

- **The six message callbacks' real layouts.** Chat still reads them by shape. See [StarCraft: Remastered chat](/bnet2/scr-chat/#legacychat-receiving). 🛑
- ~~Creating a character~~: answered. [GameAccount.CreateToon](/bnet2/scr-messages/#createtoon), confirmed live on 2026-09-24. What it answers for a taken or disallowed name is still open. 🛑
- **Two sessions at once on one account**, such as U.S. West and U.S. East together. Probably not possible. ⚠️ Inferred
- **The server calls during startup** with unknown hashes, listed on [signing in](/bnet2/sequences/starcraft-remastered-logon/#other-calls-during-startup). 🛑
- **What AuthSession's server proof proves.** 🛑
- **Friend invitations**, and the FriendUpdated fields thought to be away, busy and activity. ⚠️ Inferred
- **Whether a client that owns only the original StarCraft shows `STAR`** in the member list. 🛑

## StarCraft II records

- **Friends command 28**, probably a pending friend invitation. See [friends](/bnet2/sc2-friends/#friends-28-probably-friendinvitationadded). 🛑
- **Chat command 20**, seen once. It carried a character's name and code; it isn't decoded. 🛑
- **The body of ConnectionService method 4** that came with the 3025 refusal. See [friends](/bnet2/sc2-friends/#the-battlenet-friends-service-is-closed). 🛑

## Saved sign-ins across games

**GenerateWebCredentials takes a program**, so a signed-in SC:R session could, in principle, ask for a StarCraft II credential, and the other way round. Whether Battle.net issues one isn't confirmed. 🛑
