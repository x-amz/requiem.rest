---
title: Requiem
tagline: HTTP for Shortcuts
description: The HTTP client built for Apple Shortcuts. Build requests with chainable actions, send them, and view syntax-highlighted results.
status: v1.0
category: Developer Tools
platform: iOS
format: .http · .rest
appstore: #
---

The HTTP client built for Apple Shortcuts.

Build requests with chainable actions. Send them. View syntax-highlighted results. Share with a link. All from your iPhone.

## Shortcuts-First

Requiem gives Apple Shortcuts real HTTP capabilities. 13 chainable actions let you build requests step by step — set methods, add headers, compose bodies, append paths, add query parameters — then send. Each action passes its result to the next.

*No scripting required. Just connect the blocks.*

## The .http Standard

Requests live as `.http` files — the same format used by VS Code REST Client and JetBrains HTTP Client. Portable. Readable. Versionable. Not locked in a proprietary database.

```http
POST https://api.example.com/users
Content-Type: application/json
Authorization: Bearer token123

{
  "name": "Alice",
  "role": "admin"
}
```

## Syntax Highlighting

Every element is color-coded: methods, URLs, headers, status codes by class. JSON, XML, HTML, and form bodies are parsed and highlighted individually. Long headers wrap to fit your screen.

## Share With a Link

Encode any request as a `req.to` URL. The full request — method, headers, body — is encoded in the URL itself. No account required. No server involved.

## Rich File Previews

`.http` files show custom thumbnails in Files, Spotlight, and Share Sheets — method, domain, headers, and body at a glance. QuickLook renders full syntax-highlighted content.

## Pull to Send

Pull down on a request to send it. The response bounces in with a spring animation.
