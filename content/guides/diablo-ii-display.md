---
title: "Diablo II on modern and widescreen displays"
categories: ["Guides", "Diablo II"]
products: [D2DV, D2XP]
summary: "Diablo II runs at 800×600 and 25 frames a second, and often misbehaves on modern Windows. Two open-source wrappers fix that for 1.14d: D2DX and D2GL."
sources:
  - name: "D2DX (Jarcho's maintained version)"
    url: "https://github.com/Jarcho/d2dx"
    note: "features, supported versions, installation and launch options, from its README"
  - name: "D2DX (bolrog's original)"
    url: "https://github.com/bolrog/d2dx"
    note: "wiki and configuration documentation"
  - name: "D2GL"
    url: "https://github.com/bayaraa/d2gl"
    note: "features, supported versions and platforms, from its README"
---

The game's own limits are 800×600 (640×480 without the expansion) and 25 frames a second. D2DX and D2GL are free, open-source (GPL-3.0) wrappers that replace the game's graphics layer to lift those limits. Both support **1.14d**, and both keep the original look.

This page links to the projects' own sites, which have the downloads and full documentation. Check a project's page for its current release before installing.

## Which one?

| | D2DX | D2GL |
|---|---|---|
| **Draws with** | DirectX 11 | OpenGL 3.3 |
| **Runs on** | Windows 7 SP1 or newer (10 recommended) | Windows 7 to 11; Linux and macOS through Wine (Proton, Lutris, CrossOver) |
| **Needs** | a CPU with SSE4, and a DirectX 10.1 graphics card or integrated graphics | a graphics card with OpenGL 3.3 |
| **Higher resolutions and widescreen** | Yes, on 1.09d, 1.10, 1.12, 1.13c, 1.13d, 1.14c and 1.14d | Yes, upscaling with RetroArch shaders |
| **More than 25 fps** | Yes, with motion smoothing | Yes, using D2DX's motion prediction |
| **Also** | anti-aliasing of jagged edges, better full-screen and window switching (Alt+Enter), correct gamma | an in-game settings menu (Ctrl+O), sharper text and cursor, post-processing (sharpen, FXAA, color grading) |
| **Supported versions** | all, for basic drawing | 1.09d, 1.10f, 1.11, 1.11b, 1.12a, 1.13c, 1.13d, 1.14d |
| **Project** | [Jarcho/d2dx](https://github.com/Jarcho/d2dx) (maintained), originally [bolrog/d2dx](https://github.com/bolrog/d2dx) | [bayaraa/d2gl](https://github.com/bayaraa/d2gl) |

**Short version:** on Windows, either works, and D2DX's setup is just two files and a launch option. On a Mac or Linux through Wine, D2GL is the one that documents support.

## Setting up D2DX

1. Download the latest release from the [D2DX project](https://github.com/Jarcho/d2dx/releases).
2. Copy `glide3x.dll` and `d2fps.dll` into your Diablo II folder, next to `Game.exe`.
3. Start the game in **Glide mode**, which is what D2DX replaces. Any one of these does it:
   - add `-3dfx` to the shortcut: `Game.exe -3dfx`;
   - run `D2VidTst.exe` and choose **3dfx Glide**;
   - set `VideoConfig` to `3` in `HKCU\Software\Blizzard Entertainment\Diablo II`.
4. Press **Alt+Enter** to switch between a window and full screen.

If Windows complains about a missing runtime, install Microsoft's Visual C++ runtime (x86), linked from the D2DX README. Options, including a custom resolution, go in a `d2dx.cfg` file; the [D2DX wiki](https://github.com/bolrog/d2dx/wiki/) lists them.

**"Unsupported graphics mode."** The D2DX README says this happens with the version of Diablo II downloaded from blizzard.com, which needs changing to allow Glide mode. See the project's wiki and issues for current advice.

## Setting up D2GL

Follow the project's [installation guide](https://github.com/bayaraa/d2gl/wiki/Installation). Like D2DX it can run in Glide mode (`-3dfx`), and it can also replace DirectDraw. Press **Ctrl+O** in game for its settings.

## Online play

- A wider view shows more of the map around your character than the original 800×600 does. Private servers set their own rules about that; check before playing online.
- Don't use two wrappers at once, or combine them with another resolution mod: both projects document compatibility with other mods on their wikis.
