---
title: requiem
tagline: .http for Shortcuts
description: The HTTP client built for Apple Shortcuts. Build requests with chainable actions, send them, and view syntax-highlighted results.
status: v0.3.3
category: Developer Tools
platform: iOS · iPadOS · macOS
format: .http · .rest
appstore: https://apps.apple.com/us/app/requiem-http/id6751903685
---

The HTTP client built for Apple Shortcuts.

Build requests with chainable actions. Send them. View syntax-highlighted results. Share with a link.

## Shortcuts-First

requiem gives Apple Shortcuts real HTTP capabilities. Chainable actions let you build requests step by step — add headers, compose bodies, append paths, add query parameters — then send. Each action passes its result to the next.

*No scripting required. Just connect the blocks.*

![Shortcuts actions chained to build and send a request](img/shortcuts.png)

## The .http Standard

Requests live as `.http` files — the same format used by VS Code REST Client, JetBrains, and httpYac. Portable. Readable. Versionable. Not locked in a proprietary database. [Read the spec.](https://http-files.org)

```http
POST https://httpbin.org/post
Content-Type: application/json
Accept: application/json

{
  "name": "Alice",
  "role": "admin"
}
```

## Syntax Highlighting

Every element is color-coded: methods, URLs, headers, status codes by class. JSON, XML, HTML, and form bodies are parsed and highlighted individually. Long headers wrap to fit your screen.

![Syntax-highlighted request and response](img/detail.png)

## Share With a Link

Encode any request as a `req.to` URL. The full request — method, headers, body — is encoded in the URL itself. No account required. No server involved.

[🔗 Try it.](https://req.to/#UE9TVCBodHRwczovL2h0dHBiaW4ub3JnL3Bvc3QKQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi9qc29uCkFjY2VwdDogYXBwbGljYXRpb24vanNvbg.ewogICJuYW1lIjogIkFsaWNlIiwKICAicm9sZSI6ICJhZG1pbiIKfQ)

## Rich File Previews

`.http` files show custom thumbnails in Files, Spotlight, and Share Sheets — method, domain, headers, and body at a glance. QuickLook renders full syntax-highlighted content.

![Rich file preview in Messages](img/preview.png)

