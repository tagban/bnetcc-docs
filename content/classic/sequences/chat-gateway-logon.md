---
title: "Chat gateway: logon"
layout: "sequence"
categories: ["Sequences", "Historical"]
products: [CHAT]
summary: "The text handshake that logged a telnet user or gateway bot into chat. Every line ends with CR LF."
bnetdocs_documents: [17]
steps:
  - { from: client, raw: "0x03", note: "Protocol byte: chat gateway follows. No reply.", confidence: verified }
  - { from: client, raw: "0x04", note: "Followed by CR LF. Starts the logon.", confidence: single }
  - { from: server, raw: "Enter your login name and password.", confidence: single }
  - { from: client, raw: "<account name>", confidence: single }
  - { from: server, raw: "Username: <account name>", confidence: single }
  - { from: client, raw: "<password>", note: "**Plain text.** The server lowercases it before checking.", confidence: single }
  - { from: server, raw: "Password:", note: "Nothing follows the colon, not even a space.", confidence: single }
  - { section: "If the name or password is wrong" }
  - { from: server, raw: "Incorrect username/password.", optional: true, note: "The client starts again from the account name, without resending `0x04`.", confidence: single }
  - { section: "When logon succeeds" }
  - { from: server, raw: "Connection from [<address>]", note: "The client's address as the server sees it.", confidence: single }
  - { from: server, raw: "2010 NAME <unique name>", confidence: single }
  - { from: server, raw: "1007 CHANNEL \"<channel>\"", confidence: single }
  - { from: server, raw: "1001 USER <name> <flags> [CHAT]", note: "One for each user in the channel.", confidence: single }
  - { from: server, raw: "1018 INFO \"<text>\"", note: "Welcome and channel information.", confidence: single }
---

After this the client simply sends lines of text. See [Chat gateway (telnet)](/classic/chat-gateway/) for every message the server can send.
