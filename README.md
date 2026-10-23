# gfranks.github.io

Garrett Franks's site: the home page, and each app's page, privacy policy, terms of use and support page. Published by GitHub Pages at https://gfranks.github.io/.

## URLs

| App | Page | Privacy | Terms | Support |
|---|---|---|---|---|
| Arkive | `/arkive/` | `/arkive/privacy/` | `/arkive/terms/` | `/arkive/support/` |
| Tydé | `/tyde/` | `/tyde/privacy/` | `/tyde/terms/` | `/tyde/support/` |
| Whisper Court | `/whispercourt/` | `/whispercourt/privacy/` | `/whispercourt/terms/` | `/whispercourt/support/` |

These are the URLs to give App Store Connect. Don't rename an app's folder once it's live.

## Editing

The HTML pages are generated. Edit `content/`, then run `python3 -I build.py` and commit everything.

- `content/apps.json`: the contact email and, per app, its id (the folder name), name, kind, tagline, about text, facts and App Store link (`null` shows "Coming soon").
- `content/<app>/privacy.html`, `terms.html`, `support.html`: the page body. Update the `Last updated` line when a policy changes.
- `assets/themes.css`: each app's colors. `assets/legal.css`: app and legal pages. `assets/home.css`: the home page.
- `assets/icons/<app>.jpg`: the app icon, 512 px.

## Adding an app

1. Add it to `content/apps.json` and create `content/<id>/privacy.html`, `terms.html` and `support.html`.
2. Add its icon as `assets/icons/<id>.jpg` and its colors to `assets/themes.css` and `assets/home.css` (`.app[data-app="<id>"]`).
3. Run `python3 -I build.py`, commit and push.
