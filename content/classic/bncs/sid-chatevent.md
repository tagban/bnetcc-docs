---
title: "SID_CHATEVENT"
layout: "packet"
protocol: "BNCS"
message_id: "0x0F"
categories: ["BNCS", "Chat"]
products: [STAR, SEXP, JSTR, SSHR, W2BN, DRTL, DSHR, D2DV, D2XP, WAR3, W3XP]
summary: "Everything that happens in chat: joins, leaves, messages, whispers and server notices."
s2c:
  fields:
    - { type: "UINT32", name: "Event ID", notes: "What happened. See the table below.", confidence: verified }
    - { type: "UINT32", name: "User flags", notes: "For user events, the user's flags. For `EID_CHANNEL`, the channel's flags.", confidence: verified }
    - { type: "UINT32", name: "Ping", notes: "The user's latency in milliseconds.", confidence: verified }
    - { type: "UINT32", name: "IP address", notes: "No longer used. Always `0`.", confidence: single }
    - { type: "UINT32", name: "Account number", notes: "No longer used. Always `0`.", confidence: single }
    - { type: "UINT32", name: "Registration authority", notes: "No longer used. Always `0`.", confidence: single }
    - { type: "STRING", name: "Username", confidence: verified }
    - { type: "STRING", name: "Text", notes: "The message, the channel name, or the user's statstring, depending on the event.", confidence: verified }
  values:
    - name: "Event IDs"
      items:
        - { value: "0x01", meaning: "`EID_SHOWUSER`: a user already in the channel when you joined.", confidence: verified }
        - { value: "0x02", meaning: "`EID_JOIN`: a user joined.", confidence: verified }
        - { value: "0x03", meaning: "`EID_LEAVE`: a user left.", confidence: verified }
        - { value: "0x04", meaning: "`EID_WHISPER`: a whisper to you.", confidence: verified }
        - { value: "0x05", meaning: "`EID_TALK`: a message in the channel.", confidence: verified }
        - { value: "0x06", meaning: "`EID_BROADCAST`: a server-wide announcement.", confidence: verified }
        - { value: "0x07", meaning: "`EID_CHANNEL`: you are now in this channel.", confidence: verified }
        - { value: "0x09", meaning: "`EID_USERFLAGS`: a user's flags changed.", confidence: verified }
        - { value: "0x0A", meaning: "`EID_WHISPERSENT`: your whisper was delivered.", confidence: verified }
        - { value: "0x0D", meaning: "`EID_CHANNELFULL`: the channel is full.", confidence: verified }
        - { value: "0x0E", meaning: "`EID_CHANNELDOESNOTEXIST`: no such channel.", confidence: verified }
        - { value: "0x0F", meaning: "`EID_CHANNELRESTRICTED`: you may not join that channel.", confidence: verified }
        - { value: "0x12", meaning: "`EID_INFO`: an information message from the server.", confidence: verified }
        - { value: "0x13", meaning: "`EID_ERROR`: an error message from the server.", confidence: verified }
        - { value: "0x15", meaning: "`EID_IGNORE`: you are now ignoring (squelching) a user.", confidence: single }
        - { value: "0x16", meaning: "`EID_ACCEPT`: you stopped ignoring a user.", confidence: single }
        - { value: "0x17", meaning: "`EID_EMOTE`: an emote (`/me`).", confidence: verified }
        - { value: "0x08, 0x0B, 0x0C, 0x10, 0x11, 0x14", meaning: "Not known. Don't assume these are unused.", confidence: unknown }
    - name: "User flags"
      items:
        - { value: "0x01", meaning: "Blizzard representative", confidence: single }
        - { value: "0x02", meaning: "Channel operator", confidence: verified }
        - { value: "0x04", meaning: "Channel speaker", confidence: single }
        - { value: "0x08", meaning: "Battle.net administrator", confidence: single }
        - { value: "0x10", meaning: "No UDP support", confidence: verified }
        - { value: "0x20", meaning: "Squelched (ignored by you)", confidence: single }
        - { value: "0x40", meaning: "Special guest", confidence: single }
sources:
  - name: "Command Center: bnetcc-proto chat events"
    url: "https://github.com/tagban/bnet_command_center/blob/master/crates/bnetcc-proto/src/chat.rs"
  - name: "Command Center: PROTOCOL-NOTES.md"
    url: "https://github.com/tagban/bnet_command_center/blob/master/docs/PROTOCOL-NOTES.md"
---

**Relaying chat text.** A server must strip control characters from text before relaying it. A carriage return or line feed inside chat text makes real clients misbehave, and real Battle.net disconnected and briefly banned the sender.
