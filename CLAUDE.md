# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Marketing site for **requiem**, an HTTP client for Apple Shortcuts on iOS, iPadOS, and macOS. Hosted at `requiem.rest`. See `brand.md` for house style and terminology.

## Build

```
python3 build.py
```

No dependencies beyond Python 3 stdlib. Outputs `index.html`, `support/index.html`, and `privacy/index.html`.

## Architecture

`build.py` is a self-contained static site generator. Content is authored as Markdown with YAML frontmatter in `content/` and compiled to HTML.

- `content/index.md` — landing page content (frontmatter drives the masthead, meta block, and App Store link)
- `content/support.md`, `content/privacy.md` — doc pages built via `build_doc()`
- `style.css` — shared stylesheet, dark theme with gold/serif aesthetic
- `icon.png`, `requiem_aeternam.jpeg` — static assets
- `img/` — image assets: `appstore.svg` (App Store badge), `detail.png`, `preview.png`, `shortcuts.png` (screenshots/promo art)

New App Store marketing badges and assets can be generated at: https://toolbox.marketingtools.apple.com/en-us/app-store/us/app/6751903685

The build pipeline: `parse_frontmatter()` → `parse_blocks()` → `render_block()` / `inline()`. The landing page (`build_landing()`) has special handling for sections with `§` numbering, an abstract block, and CTA buttons. Doc pages (`build_doc()`) are simpler single-column layouts.

`highlight_http()` provides syntax highlighting for `.http` code blocks (methods, headers, JSON keys/values get CSS class spans).

## Conventions

- HTML output files are committed to the repo (the build output *is* the deployable site)
- After editing any `content/*.md` file or `build.py`, re-run the build and include the regenerated HTML in the commit
