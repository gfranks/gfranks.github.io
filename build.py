#!/usr/bin/env python3
"""Builds the site from content/ into the repo root. Run: python3 -I build.py"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SITE = json.loads((CONTENT / "apps.json").read_text())
CONTACT = SITE["contact"]
APPS = SITE["apps"]
YEAR = 2026

PAGES = [("privacy", "Privacy Policy"), ("terms", "Terms of Use"), ("support", "Support")]

ARROW = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 11 11 5M6 5h5v5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BACK = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

e = html.escape


def head(title, description, icon, extra_css, app_id=None):
    data_app = f' data-app="{app_id}"' if app_id else ""
    icon_type = "image/svg+xml" if icon.endswith(".svg") else "image/jpeg"
    touch = f'\n<link rel="apple-touch-icon" href="{icon}">' if icon.endswith(".jpg") else ""
    css = "".join(f'\n<link rel="stylesheet" href="/assets/{c}">' for c in extra_css)
    return f"""<!doctype html>
<html lang="en"{data_app}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<link rel="icon" type="{icon_type}" href="{icon}">{touch}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400..800;1,9..144,400..600&display=swap">{css}
</head>
"""


def footer():
    return f"""
  <footer>
    <p><a href="/">Garrett Franks</a> · <a href="mailto:{CONTACT}">{CONTACT}</a></p>
    <p class="fine">© {YEAR} Garrett Franks</p>
  </footer>

</body>
</html>
"""


def store_button(app, cls="store"):
    if app["appStore"]:
        return f'<a class="{cls}" href="{e(app["appStore"])}">View on the App Store {ARROW}</a>'
    return f'<span class="{cls} soon">Coming soon to the App Store</span>'


def facts(app):
    return "".join(f"<li>{e(f)}</li>" for f in app["facts"])


def home():
    cards = []
    for i, app in enumerate(APPS):
        a = app["id"]
        cards.append(f"""
      <article class="app" data-app="{a}" style="--i:{i}">
        <a class="app-icon" href="/{a}/" aria-hidden="true" tabindex="-1">
          <img src="/assets/icons/{a}.jpg" alt="" class="glow" width="512" height="512">
          <img src="/assets/icons/{a}.jpg" alt="" width="512" height="512">
        </a>
        <div class="app-body">
          <p class="kind">{e(app["kind"])}</p>
          <h3><a href="/{a}/">{e(app["name"])}</a></h3>
          <p class="tagline">{e(app["tagline"])}</p>
          <p class="about">{e(app["about"])}</p>
          <ul class="facts">{facts(app)}</ul>
          <div class="actions">
            {store_button(app)}
            <nav class="legal" aria-label="{e(app["name"])} pages">
              <a href="/{a}/privacy/">Privacy</a><a href="/{a}/terms/">Terms</a><a href="/{a}/support/">Support</a>
            </nav>
          </div>
        </div>
      </article>""")
    return head("Garrett Franks", "Apps for iPhone and iPad by Garrett Franks: Arkive, Tydé and Whisper Court.",
                "/assets/favicon.svg", ["home.css"]) + f"""<body class="home">

  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>

  <header class="intro">
    <p class="eyebrow">Independent apps for iPhone &amp; iPad</p>
    <h1>Garrett Franks</h1>
    <p class="lead">I make small, careful apps that do one thing well and leave you alone. No ads, no tracking, no accounts.</p>
    <ul class="principles">
      <li>No ads</li><li>No tracking</li><li>No accounts</li><li>Your data stays yours</li>
    </ul>
  </header>

  <main>
    <h2 class="section-title">Apps</h2>
    <div class="apps">{"".join(cards)}
    </div>

    <section class="contact">
      <h2>Say hello</h2>
      <p>Questions, bugs, or ideas for any of these apps go to one inbox, and I read every message.</p>
      <a class="mail" href="mailto:{CONTACT}">{CONTACT} {ARROW}</a>
    </section>
  </main>
""" + footer()


def app_hero(app, subtitle, big=False):
    a = app["id"]
    extra = f'\n    <p class="hero-tagline">{e(app["tagline"])}</p>\n    {store_button(app, "hero-store")}' if big else ""
    return f"""
  <div class="hero{' hero-big' if big else ''}">
    <a class="back" href="/">{BACK} Garrett Franks</a>
    <a href="/{a}/"><img src="/assets/icons/{a}.jpg" alt="{e(app["name"])} icon" width="512" height="512"></a>
    <h1>{e(app["name"])}</h1>
    <p>{e(subtitle)}</p>{extra}
  </div>
"""


def pillbar(app, current=None):
    current_attr = ' aria-current="page"'
    links = "".join(
        f'<a href="/{app["id"]}/{slug}/"{current_attr if slug == current else ""}>{title}</a>'
        for slug, title in PAGES)
    return f'\n  <nav class="pillbar">{links}</nav>\n'


def app_page(app):
    a = app["id"]
    tiles = "".join(f"""
        <a class="tile" href="/{a}/{slug}/"><span>{title}</span>{ARROW}</a>""" for slug, title in PAGES)
    return head(app["name"], f'{app["name"]}: {app["tagline"]}', f"/assets/icons/{a}.jpg", ["legal.css", "themes.css"], a) + \
        "<body>\n" + app_hero(app, app["kind"], big=True) + pillbar(app) + f"""
  <main>
    <section class="card">
      <h2>About</h2>
      <p class="lede">{e(app["about"])}</p>
      <ul class="facts">{facts(app)}</ul>
      <div class="tiles">{tiles}
      </div>
    </section>
  </main>
""" + footer()


def legal_page(app, slug, title):
    a = app["id"]
    body = (CONTENT / a / f"{slug}.html").read_text().rstrip("\n")
    body = "\n".join(("      " + line) if line else "" for line in body.split("\n"))
    return head(f'{app["name"]} — {title}', f'{title} for {app["name"]}.', f"/assets/icons/{a}.jpg",
                ["legal.css", "themes.css"], a) + "<body>\n" + app_hero(app, title) + pillbar(app, slug) + f"""
  <main>
    <section class="card" id="{slug}">
      <h2>{title}</h2>
{body}
    </section>
  </main>
""" + footer()


def not_found():
    return head("Page not found — Garrett Franks", "Page not found.", "/assets/favicon.svg", ["home.css"]) + \
        """<body class="home">

  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>

  <header class="intro">
    <p class="eyebrow">404</p>
    <h1>Not here</h1>
    <p class="lead">That page doesn't exist. Every app's privacy policy, terms and support live on the home page.</p>
    <p><a class="mail" href="/">Back to Garrett Franks</a></p>
  </header>
""" + footer()


def write(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    write("index.html", home())
    write("404.html", not_found())
    for app in APPS:
        write(f'{app["id"]}/index.html', app_page(app))
        for slug, title in PAGES:
            write(f'{app["id"]}/{slug}/index.html', legal_page(app, slug, title))
    print(f"Built home, 404 and {len(APPS)} apps.")


if __name__ == "__main__":
    main()
