---
title: "Connect a game to BNET.cc"
categories: ["Guides"]
products: [STAR, SEXP, W2BN, DRTL, D2DV, D2XP, WAR3, W3XP]
summary: "Classic games find Battle.net servers through a list of gateways. Add BNET.cc's server, us.bnet.cc, to that list and pick it when you connect."
sources:
  - name: "Universal Battle.net Gateway Installer (PvPGN project, MIT)"
    url: "https://github.com/pvpgn/battle.net-gateway-installer"
    note: "registry locations and value format for StarCraft, Warcraft III and Diablo II"
  - name: "Command Center: DIABLO2.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/DIABLO2.md"
    note: "a retail Diablo II 1.14d client connecting through the `Diablo II Battle.net gateways` value, with no loader"
  - name: "Command Center: LEGAL.md §3"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/LEGAL.md"
    note: "why Warcraft III needs a modified client"
  - name: "Setting Battle.net gateways on Mac OS X"
    url: "http://www.chiark.greenend.org.uk/~ajlanes/free/bnetosx.html"
    note: "the Mac preferences file"
---

**BNET.cc's server:** `us.bnet.cc`, port `6112`.

Marks follow [How to read these pages](/how-to-read/): ✅ verified, ⚠️ single source or untested, 🛑 unknown.

Every Classic game keeps a list of **gateways**: the Battle.net servers it offers when you click **Battle.net**. Add `us.bnet.cc` to that list, choose it, and connect as normal. You create a BNET.cc account the first time, the same way you would on Blizzard's servers.

## Which games work

| Game | Version | Setup | Status |
|---|---|---|---|
| Diablo II, Lord of Destruction | 1.14d | Gateway list | ✅ Tested with a retail client, no loader needed |
| Diablo II | 1.13c and older | Gateway list | ⚠️ Should work, untested |
| Warcraft II: Battle.net Edition | original (not GOG) | Gateway list | ⚠️ Connects and runs the version check |
| StarCraft, Brood War | 1.16.1 | Gateway list | ⚠️ |
| Diablo | original (not GOG) | Gateway list | ⚠️ |
| Warcraft III, The Frozen Throne | 1.28 and older | Gateway list **and a modified client** | ⚠️ See below |
| GOG editions of Diablo and Warcraft II | | | 🛑 Not tested |

Tried one we haven't? Tell us on [Discord](https://discord.gg/dR4djHweh3).

## Windows: the gateway list

The list lives in the Windows registry, in your user's settings (`HKEY_CURRENT_USER`, `HKCU` for short):

| Game | Registry key | Value |
|---|---|---|
| StarCraft, Brood War | `HKCU\Software\Battle.net\Configuration` | `Battle.net Gateways` ✅ |
| Warcraft II, Diablo | `HKCU\Software\Battle.net\Configuration` | `Battle.net Gateways` ⚠️ (shared with StarCraft) |
| Diablo II | `HKCU\Software\Battle.net\Configuration` | `Diablo II Battle.net Gateways` ✅ |
| Warcraft III | `HKCU\Software\Blizzard Entertainment\Warcraft III` | `Battle.net Gateways` ⚠️ |

### Format

The value is a multi-line string (`REG_MULTI_SZ`):

```
1001            always this
01              which server is selected: 01 is the first, 02 the second, and so on
us.bnet.cc      server address
0               time zone number (not used to connect)
BNET.cc         the name shown in the game
…               three more lines for each further server
```

The format is ✅ verified; that the time zone isn't used to connect is ⚠️.

### Quickest way: a command

Close the game, open **Command Prompt**, and paste the line for your game. Each replaces the game's gateway list with BNET.cc only, and selects it.

StarCraft, Brood War, Warcraft II and Diablo:

```bat
reg add "HKCU\Software\Battle.net\Configuration" /v "Battle.net Gateways" /t REG_MULTI_SZ /d "1001\001\0us.bnet.cc\00\0BNET.cc" /f
```

Diablo II (two commands):

```bat
reg add "HKCU\Software\Battle.net\Configuration" /v "Diablo II Battle.net Gateways" /t REG_MULTI_SZ /d "1001\001\0us.bnet.cc\00\0BNET.cc" /f
reg add "HKCU\Software\Blizzard Entertainment\Diablo II" /v "BNETIP" /t REG_SZ /d "us.bnet.cc" /f
```

Warcraft III:

```bat
reg add "HKCU\Software\Blizzard Entertainment\Warcraft III" /v "Battle.net Gateways" /t REG_MULTI_SZ /d "1001\001\0us.bnet.cc\00\0BNET.cc" /f
```

`\0` separates the lines, so `1001\001\0us.bnet.cc` means `1001`, `01`, `us.bnet.cc`.

**Want to keep your other servers?** Use a gateway editor instead, or add BNET.cc to the end of the existing list with **Registry Editor** (`regedit`): double-click the value, add the three lines at the bottom, and change the second line to BNET.cc's position.

### Then connect

1. Start the game and choose **Battle.net**.
2. If the game shows a gateway or realm choice, pick **BNET.cc**.
3. Create an account, or log in.

## Warcraft III

Warcraft III checks that the server it connects to is signed by Blizzard, and no server other than Blizzard's can pass that check. As far as we know, every private Warcraft III server needs players to use a client modified to skip it. **This site doesn't provide or link to one.** Ask on the [BNET.cc Discord](https://discord.gg/dR4djHweh3) for current instructions.

## Mac

Mac versions keep the same gateway list in a preferences file instead of the registry: `Battle.net Preferences` in the Preferences folder. On Mac OS X it's in `~/Library/Preferences/`. The list sits inside the file's resource fork, so it's edited with ResEdit rather than a text editor. ⚠️ BNET.cc users on Mac OS 9 and early Mac OS X: please share the steps that work for you, and we'll add them here.

## Problems

- **Create and Join are greyed out** (Warcraft II and others). After logon the server tests whether it can reach your computer on **UDP** port 6112. If your router blocks that, the game won't let you host or join. Forward UDP port 6112 to your computer. ✅
- **"Unable to connect"**: check the address is exactly `us.bnet.cc` and that you picked the BNET.cc gateway. The [Servers](/servers/) page shows whether the server answered today's check.
- **Asked to upgrade, or disconnected during the version check**: the server expects a particular patch. For Diablo II, 1.14d is the tested version.
