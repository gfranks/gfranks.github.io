# gfranks.github.io

Garrett Franks's site: the home page, and each app's page, privacy policy, terms of use and support page. Published by GitHub Pages at https://gfranks.github.io/.

## URLs

| App | Page | Privacy | Terms | Support |
|---|---|---|---|---|
| Arkive | `/arkive/` | `/arkive/privacy/` | `/arkive/terms/` | `/arkive/support/` |
| Tydé | `/tyde/` | `/tyde/privacy/` | `/tyde/terms/` | `/tyde/support/` |
| Pyllar | `/pyllar/` | (its own site) | | |
| Whisper Court | `/whispercourt/` | `/whispercourt/privacy/` | `/whispercourt/terms/` | `/whispercourt/support/` |
| Candidly | `/candidly/` | `/candidly/privacy/` | `/candidly/terms/` | `/candidly/support/` |

These are the URLs to give App Store Connect. Don't rename an app's folder once it's live.

## Editing

The HTML pages are generated. Edit `content/`, then run `python3 -I build.py` and commit everything. Run `python3 -I build.py --og` instead when anything on a share image changes (an app's name, kind, tagline or icon, or the role line); it re-renders `assets/og/*.jpg`, `favicon.ico` and `assets/apple-touch-icon.png` (from `assets/favicon.svg`) with headless Chrome.

- `content/apps.json`: contact email, GitHub and LinkedIn links, and per app its id (the folder name), name, kind, platforms, status, tagline, about text, highlights ("What I built"), stack, `screens` (the framed phones, each a `file` and its `alt` text, in display order: the first peeks out of the app's home page tile, the first two stand in its app page hero, and all of them fill its gallery), `screenStyle` (`"store"` shows finished App Store images unframed with rounded corners instead of framed captures), `featured` (one app gets the big home page tile; otherwise the first), App Store link or website, and whether it has legal pages here (`legal`).
- `build.py`: the role line, intro and the "What I work with" skills list.
- `assets/devices/<app>/<file>.webp`: each screen framed in an iPhone, made by `tools/frame_screens.py`.
- `content/<app>/privacy.html`, `terms.html`, `support.html`: the page body. Update the `Last updated` line when a policy changes.
- `assets/themes.css`: each app's colors. `assets/base.css`: shared by the home and app pages. `assets/home.css`: the home page. `assets/app.css`: the app pages. `assets/legal.css`: the privacy, terms and support pages. `assets/home.js`: the bento tiles rising into place and tilting toward the pointer (both off with Reduce Motion), used by the home and app pages.
- `assets/icons/<app>.jpg`: the app icon, 512 px.

## Adding an app

1. Add it to `content/apps.json` and, if it has `legal: true`, create `content/<id>/privacy.html`, `terms.html` and `support.html`.
2. Add its icon as `assets/icons/<id>.jpg`, its colors (including `--glow`) to `assets/themes.css` and `OG_CARDS` in `build.py`, its raw screenshot folder to `SOURCES` in `tools/frame_screens.py`, and at least two `screens` to `apps.json`; then run `python3 -I tools/frame_screens.py <id>`.
3. Run `python3 -I build.py --og`, commit and push.

## Framing screens

Every phone on the site is a real screen inside the ai-toolkit iPhone 17 Pro frame, framed by `tools/frame_screens.py` from the raw simulator screenshots listed in `SOURCES`. It reads each app's `screens` from `apps.json` and writes `assets/devices/<app>/<file>.webp` (transparent, 1100 px tall). For an app with `"screenStyle": "store"` (Candidly), `SOURCES` points at its finished App Store images, which are only resized. Read a screen before adding it: no real personal names, launch screens or half-loaded states.

```bash
python3 -I tools/frame_screens.py            # every app
python3 -I tools/frame_screens.py tyde       # one app
```

`tools/frame_media.py` makes store-style images with a caption above the phone (`assets/shots`, `assets/video`); the pages don't use those any more.
