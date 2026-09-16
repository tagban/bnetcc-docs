---
title: "StarCraft II: signing in"
layout: "sequence"
categories: ["Sequences", "Battle.net 2.0"]
products: [S2]
summary: "From opening Front to an encrypted Sunken connection: sign-in, choosing the game account, and handing the session over."
steps:
  - { section: "Front: connect" }
  - { from: client, raw: "TCP 1119 → TLS → WebSocket", transport: "v1.rpc.battle.net", note: "One WebSocket message per RPC message.", confidence: verified }
  - { from: client, raw: "ConnectionService / 1", note: "`ConnectRequest`. `service_id` 0, `token` 0, asking for bindless RPC.", confidence: single }
  - { section: "Front: sign in" }
  - { from: client, raw: "AuthenticationServer / 1", note: "`LogonRequest`: program `S2`, platform, locale, SDK identity. Includes the reusable credential if the client has one.", confidence: single }
  - { from: server, raw: "ChallengeNotify / 3", optional: true, note: "Only when needed: sends the client to Blizzard's web sign-in. No response.", confidence: single }
  - { from: client, raw: "Web sign-in", transport: "HTTPS", optional: true, note: "Blizzard's own sign-in page handles passwords, multi-factor authentication and CAPTCHA. It isn't part of the RPC protocol.", confidence: single }
  - { from: client, raw: "AuthenticationServer / 7", optional: true, note: "`VerifyWebCredentialsRequest` with the short-lived credential from the web sign-in.", confidence: single }
  - { from: server, raw: "AuthenticationClient / 5", note: "`LogonResult`: account, StarCraft II game accounts, region and a 64-byte session key.", confidence: single }
  - { from: client, raw: "AuthenticationServer / 8", note: "Asks for a new reusable credential for next time.", confidence: single }
  - { section: "Front: request the handoff" }
  - { from: client, raw: "GameUtilities / 1", note: "`ClientRequest` with the first StarCraft II game account and the session key.", confidence: single }
  - { from: server, raw: "GameUtilities / 1 response", note: "Sunken's address, a 64-byte session seed, and a bit-packed `LogonResponse3`.", confidence: single }
  - { section: "Sunken: take over the session" }
  - { from: client, raw: "New TCP connection to Sunken", transport: "TCP", note: "Opened before Front is closed.", confidence: single }
  - { from: client, raw: "WebSocket close", note: "Front is closed directly with a WebSocket close frame.", confidence: single }
  - { from: client, raw: "Auth / 1 ResumeRequest", note: "Sent in plain text once Front has closed. Its proof shows the client holds the session seed, binding the new connection to the account.", confidence: single }
  - { from: server, raw: "Resume proof", note: "The client must check the server's proof before going on.", confidence: single }
  - { from: client, raw: "Conn / 5 EnableEncryption", note: "Turns on RC4, with separate keys for each direction.", confidence: single }
  - { section: "Sunken: encrypted" }
  - { from: server, raw: "Service records", note: "Chat, matchmaking, profiles and every other StarCraft II service, as bit-packed records.", confidence: single }
sources:
  - name: "SC2Docs, by Warrior"
    url: "https://superiority-sc2docs.pages.dev/"
    note: "the full connection sequence"
  - name: "d4-bnet-mitm (a Diablo IV Battle.net proxy)"
    url: "https://github.com/cjbrigato/d4-bnet-mitm"
    note: "independent source used to cross-check the Front framing and RPC header"
---

Blizzard calls handing the session from Front to Sunken **Resume**. Front proves who the player is; Sunken then only needs proof that the new connection holds the session seed Front issued.

See [Front RPC](/bnet2/front/), [Front messages](/bnet2/front-messages/) and [Sunken records](/bnet2/sunken/) for the formats used in each step.
