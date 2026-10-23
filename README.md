# gfranks.github.io

Garrett Franks's site: the home page, and each app's page, privacy policy, terms of use and support page. Published by GitHub Pages at https://gfranks.github.io/.

## URLs

| App | Page | Privacy | Terms | Support |
|---|---|---|---|---|
| Arkive | `/arkive/` | `/arkive/privacy/` | `/arkive/terms/` | `/arkive/support/` |
| Tydé | `/tyde/` | `/tyde/privacy/` | `/tyde/terms/` | `/tyde/support/` |
| Pyllar | `/pyllar/` | (its own site) | | |
| Whisper Court | `/whispercourt/` | `/whispercourt/privacy/` | `/whispercourt/terms/` | `/whispercourt/support/` |

These are the URLs to give App Store Connect. Don't rename an app's folder once it's live.

## Editing

The HTML pages are generated. Edit `content/`, then run `python3 -I build.py` and commit everything. Run `python3 -I build.py --og` instead when anything on a share image changes (an app's name, kind, tagline or icon, or the role line); it re-renders `assets/og/*.jpg` with headless Chrome.

- `content/apps.json`: contact email, GitHub and LinkedIn links, and per app its id (the folder name), name, kind, platforms, status, tagline, about text, highlights ("What I built"), stack, screenshot count, App Store link or website, and whether it has legal pages here (`legal`).
- `build.py`: the role line, intro and the "What I work with" skills list.
- `assets/shots/<app>/01.jpg`…: screenshots for the app page gallery.
- `content/<app>/privacy.html`, `terms.html`, `support.html`: the page body. Update the `Last updated` line when a policy changes.
- `assets/themes.css`: each app's colors. `assets/legal.css`: app and legal pages. `assets/home.css`: the home page.
- `assets/icons/<app>.jpg`: the app icon, 512 px.

## Adding an app

1. Add it to `content/apps.json` and, if it has `legal: true`, create `content/<id>/privacy.html`, `terms.html` and `support.html`.
2. Add its icon as `assets/icons/<id>.jpg`, its colors to `assets/themes.css`, `assets/home.css` (`.app[data-app="<id>"]`) and `OG_CARDS` in `build.py`, and any screenshots.
3. Run `python3 -I build.py --og`, commit and push.
