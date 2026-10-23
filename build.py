#!/usr/bin/env python3
"""Builds the site from content/ into the repo root.

Run: python3 -I build.py          (pages only)
     python3 -I build.py --og     (pages, then re-render the share images with headless Chrome)
"""
import hashlib
import html
import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
CONTENT = ROOT / "content"
SITE = json.loads((CONTENT / "apps.json").read_text())
CONTACT = SITE["contact"]
GITHUB = SITE["github"]
LINKEDIN = SITE["linkedin"]
APPS = SITE["apps"]
SITE_URL = "https://gfranks.github.io"
YEAR = 2026
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

ROLE = "Mobile technical lead · iOS & Android"
INTRO = ("I lead mobile teams and build apps end to end, from the first sketch to the App Store: "
         "Swift and SwiftUI, Kotlin and Compose, and the web and backend behind them.")

NOW = [("Mobile technical lead", "Wahoo Fitness"), ("Founder", "C&F Solutions LLC")]

PAGES = [("privacy", "Privacy Policy"), ("terms", "Terms of Use"), ("support", "Support")]

SKILLS = [
    ("Apple platforms", ["Swift", "SwiftUI", "UIKit", "SwiftData", "CloudKit", "WidgetKit", "ActivityKit",
                         "App Intents", "MapKit", "StoreKit", "Swift Testing"]),
    ("Android", ["Kotlin", "Jetpack Compose", "Gradle"]),
    ("Web & backend", ["TypeScript", "Next.js", "React", "Fastify", "PostgreSQL", "Drizzle", "Docker",
                       "GitHub Actions"]),
    ("Product & leadership", ["Technical leadership", "Product design", "Accessibility", "Platform parity",
                              "App Store releases", "AI features with the Claude API"]),
]

ARROW = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 11 11 5M6 5h5v5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
NEXT = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
BACK = '<svg class="ic" viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

e = html.escape


def asset_version(name):
    return hashlib.sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]


def head(title, description, icon, extra_css, path, og_image, app_id=None, scripts=()):
    data_app = f' data-app="{app_id}"' if app_id else ""
    icon_type = "image/svg+xml" if icon.endswith(".svg") else "image/jpeg"
    touch = f'\n<link rel="apple-touch-icon" href="{icon}">' if icon.endswith(".jpg") else ""
    css = "".join(f'\n<link rel="stylesheet" href="/assets/{c}?v={asset_version(c)}">' for c in extra_css)
    js = "".join(f'\n<script src="/assets/{j}?v={asset_version(j)}" defer></script>' for j in scripts)
    image = f"{SITE_URL}/assets/og/{og_image}.jpg?v={asset_version(f'og/{og_image}.jpg')}"
    return f"""<!doctype html>
<html lang="en"{data_app}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Garrett Franks">
<meta property="og:url" content="{SITE_URL}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{image}">
<link rel="icon" type="{icon_type}" href="{icon}">{touch}{css}{js}
</head>
"""


def footer():
    linkedin = f' · <a href="{e(LINKEDIN)}">LinkedIn</a>' if LINKEDIN else ""
    return f"""
  <footer>
    <p><a href="/">Garrett Franks</a> · <a href="mailto:{CONTACT}">{CONTACT}</a> · <a href="{GITHUB}">GitHub</a>{linkedin}</p>
    <p class="fine">© {YEAR} Garrett Franks</p>
  </footer>

</body>
</html>
"""


def primary_link(app, cls):
    if app["appStore"]:
        return f'<a class="{cls}" href="{e(app["appStore"])}">View on the App Store {ARROW}</a>'
    if app["website"]:
        host = app["website"].split("//", 1)[1]
        return f'<a class="{cls}" href="{e(app["website"])}">{e(host)} {ARROW}</a>'
    return f'<span class="{cls} soon">Coming soon to the App Store</span>'


def chips(items, cls="chips", limit=None):
    shown = items[:limit] if limit else items
    more = f'<li class="more">+{len(items) - len(shown)}</li>' if limit and len(items) > limit else ""
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in shown) + more + "</ul>"


def profile_links():
    links = [f'<a class="cta primary" href="mailto:{CONTACT}">Email me {ARROW}</a>',
             f'<a class="cta" href="{GITHUB}">GitHub {ARROW}</a>']
    if LINKEDIN:
        links.append(f'<a class="cta" href="{e(LINKEDIN)}">LinkedIn {ARROW}</a>')
    return "".join(links)


def home():
    cards = []
    for i, app in enumerate(APPS):
        a = app["id"]
        cards.append(f"""
      <article class="app" data-app="{a}" style="--i:{i}">
        <span class="spot" aria-hidden="true"></span>
        <a class="app-icon" href="/{a}/" aria-hidden="true" tabindex="-1">
          <img src="/assets/icons/{a}.jpg?v={asset_version(f'icons/{a}.jpg')}" alt="" class="glow" width="512" height="512">
          <img src="/assets/icons/{a}.jpg?v={asset_version(f'icons/{a}.jpg')}" alt="" width="512" height="512">
        </a>
        <div class="app-body">
          <p class="kind">{e(app["kind"])} <span class="status">{e(app["status"])}</span></p>
          <h3><a href="/{a}/">{e(app["name"])}</a></h3>
          <p class="tagline">{e(app["tagline"])}</p>
          {chips(app["stack"], "facts", 6)}
          <div class="actions">
            <a class="store" href="/{a}/">See how it's built {NEXT}</a>
            {primary_link(app, "secondary")}
          </div>
        </div>
      </article>""")

    groups = "".join(f"""
      <div class="skill">
        <h3>{e(title)}</h3>
        {chips(items, "skill-chips")}
      </div>""" for title, items in SKILLS)

    on_store = sum(1 for app in APPS if app["appStore"])
    now = "".join(f"<li><span>{e(role)}</span> {e(org)}</li>" for role, org in NOW)
    return head("Garrett Franks", f"{ROLE}. {INTRO}", "/assets/favicon.svg", ["home.css"], "/", "home",
                scripts=["home.js"]) + f"""<body class="home">

  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>

  <header class="intro">
    <p class="eyebrow">{ROLE}</p>
    <h1>Garrett Franks</h1>
    <p class="lead">{INTRO}</p>
    <ul class="now" aria-label="Currently">{now}</ul>
    <div class="ctas">{profile_links()}</div>
    <dl class="stats">
      <div style="--i:0"><dt>{len(APPS)}</dt><dd>Products</dd></div>
      <div style="--i:1"><dt>{on_store}</dt><dd>On the App Store</dd></div>
      <div style="--i:2"><dt>3</dt><dd>Platforms</dd></div>
      <div style="--i:3"><dt>0</dt><dd>Trackers</dd></div>
    </dl>
  </header>

  <main>
    <h2 class="section-title">Selected work</h2>
    <div class="apps">{"".join(cards)}
    </div>

    <section class="skills">
      <h2 class="section-title">What I work with</h2>
      <div class="skill-grid">{groups}
      </div>
    </section>

    <section class="contact">
      <h2>Let's talk</h2>
      <p>Hiring a mobile lead, or curious how something here was built? Email me and I'll get back to you.</p>
      <div class="ctas">{profile_links()}</div>
    </section>
  </main>
""" + footer()


def app_hero(app, subtitle, big=False):
    a = app["id"]
    extra = ""
    if big:
        extra = f"""
    <p class="hero-tagline">{e(app["tagline"])}</p>
    <div class="hero-actions">{primary_link(app, "hero-store")}<span class="hero-status">{e(app["status"])}</span></div>"""
    return f"""
  <div class="hero{' hero-big' if big else ''}">
    <a class="back" href="/">{BACK} Garrett Franks</a>
    <a href="/{a}/"><img src="/assets/icons/{a}.jpg?v={asset_version(f'icons/{a}.jpg')}" alt="{e(app["name"])} icon" width="512" height="512"></a>
    <h1>{e(app["name"])}</h1>
    <p>{e(subtitle)}</p>{extra}
  </div>
"""


def pillbar(app, current=None):
    if not app["legal"]:
        return ""
    current_attr = ' aria-current="page"'
    links = "".join(
        f'<a href="/{app["id"]}/{slug}/"{current_attr if slug == current else ""}>{title}</a>'
        for slug, title in PAGES)
    return f'\n  <nav class="pillbar">{links}</nav>\n'


def gallery(app):
    if not app["shots"]:
        return ""
    a = app["id"]
    shape = app["shotShape"]
    width, height = (1280, 900) if shape == "landscape" else (441, 960)
    shots = "".join(
        f'\n      <img src="/assets/shots/{a}/{n:02d}.jpg?v={asset_version(f"shots/{a}/{n:02d}.jpg")}" alt="{e(app["name"])} screenshot {n}" loading="lazy" width="{width}" height="{height}">'
        for n in range(1, app["shots"] + 1))
    return f'\n  <div class="gallery {shape}" tabindex="0" aria-label="{e(app["name"])} screenshots">{shots}\n  </div>\n'


def app_page(app):
    a = app["id"]
    highlights = "".join(f"\n        <li>{e(h)}</li>" for h in app["highlights"])
    tiles = ""
    if app["legal"]:
        tiles = "".join(f"""
        <a class="tile" href="/{a}/{slug}/"><span>{title}</span>{ARROW}</a>""" for slug, title in PAGES)
        tiles = f'\n    <div class="tiles">{tiles}\n    </div>'
    return head(f'{app["name"]} — Garrett Franks', f'{app["name"]}: {app["tagline"]}', f"/assets/icons/{a}.jpg",
                ["legal.css", "themes.css"], f"/{a}/", a, a) + \
        "<body>\n" + app_hero(app, f'{app["kind"]} · {app["platforms"]}', big=True) + pillbar(app) + \
        gallery(app) + f"""
  <main>
    <section class="card">
      <h2>About</h2>
      <p class="lede">{e(app["about"])}</p>
      {chips(app["stack"], "facts")}
    </section>

    <section class="card">
      <h2>What I built</h2>
      <ul class="built">{highlights}
      </ul>
    </section>
{tiles}
  </main>
""" + footer()


def legal_page(app, slug, title):
    a = app["id"]
    body = (CONTENT / a / f"{slug}.html").read_text().rstrip("\n")
    body = "\n".join(("      " + line) if line else "" for line in body.split("\n"))
    return head(f'{app["name"]} — {title}', f'{title} for {app["name"]}.', f"/assets/icons/{a}.jpg",
                ["legal.css", "themes.css"], f"/{a}/{slug}/", a, a) + \
        "<body>\n" + app_hero(app, title) + pillbar(app, slug) + f"""
  <main>
    <section class="card" id="{slug}">
      <h2>{title}</h2>
{body}
    </section>
  </main>
""" + footer()


def not_found():
    return head("Page not found — Garrett Franks", "Page not found.", "/assets/favicon.svg", ["home.css"],
                "/404.html", "home") + """<body class="home">

  <div class="aurora" aria-hidden="true"><span></span><span></span><span></span></div>

  <header class="intro">
    <p class="eyebrow">404</p>
    <h1>Not here</h1>
    <p class="lead">That page doesn't exist. Every app, with its privacy policy, terms and support, is on the home page.</p>
    <div class="ctas"><a class="cta primary" href="/">Back to Garrett Franks</a></div>
  </header>
""" + footer()


def og_home():
    icons = "".join(f'<img src="{ROOT}/assets/icons/{a["id"]}.jpg">' for a in APPS)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: #0D0C10; color: #F4EFE6; font-family: -apple-system, "SF Pro Display", sans-serif; position: relative; }}
  .b {{ position: absolute; border-radius: 50%; filter: blur(90px); opacity: .5; }}
  .b1 {{ background: #C97952; width: 620px; height: 620px; left: -200px; top: -320px; }}
  .b2 {{ background: #C2304A; width: 640px; height: 640px; right: -220px; top: -340px; }}
  .b3 {{ background: #1E4596; width: 520px; height: 520px; right: 120px; bottom: -420px; opacity: .45; }}
  .wrap {{ position: absolute; inset: 0; padding: 84px 88px; display: flex; flex-direction: column; }}
  .eyebrow {{ font-size: 22px; font-weight: 650; letter-spacing: .14em; text-transform: uppercase; color: #A8A095; }}
  h1 {{ font-size: 132px; font-weight: 700; letter-spacing: -.055em; line-height: .92; margin: 22px 0 0; }}
  .lead {{ font-size: 34px; font-weight: 500; letter-spacing: -.015em; line-height: 1.3; color: #CFC7BA; margin-top: 26px; max-width: 900px; }}
  .row {{ margin-top: auto; display: flex; align-items: center; gap: 20px; }}
  .row img {{ width: 92px; height: 92px; border-radius: 21px; box-shadow: 0 14px 34px rgba(0,0,0,.5); }}
  .url {{ margin-left: auto; font-size: 26px; font-weight: 600; color: #A8A095; }}
</style></head><body>
  <div class="b b1"></div><div class="b b2"></div><div class="b b3"></div>
  <div class="wrap">
    <div class="eyebrow">{e(ROLE)}</div>
    <h1>Garrett Franks</h1>
    <div class="lead">I lead mobile teams and build apps end to end.</div>
    <div class="row">{icons}<span class="url">gfranks.github.io</span></div>
  </div>
</body></html>"""


OG_CARDS = {
    "arkive": ("linear-gradient(135deg, #C97952 0%, #7A5540 52%, #3B2D23 100%)", "#FBF4EA"),
    "pyllar": ("linear-gradient(135deg, #3B6FD8 0%, #1E4596 50%, #0C1630 100%)", "#F2F6FF"),
    "tyde": ("linear-gradient(135deg, #FF6B7A 0%, #8E2F52 48%, #14121F 100%)", "#FBEEF0"),
    "whispercourt": ("linear-gradient(135deg, #5A4129 0%, #2C2017 50%, #120E0B 100%)", "#EFE3C8"),
}


def og_app(app):
    background, ink = OG_CARDS[app["id"]]
    icon = f'{ROOT}/assets/icons/{app["id"]}.jpg'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin: 0; width: 1200px; height: 630px; overflow: hidden; }}
  body {{ background: {background}; color: {ink}; font-family: -apple-system, "SF Pro Display", sans-serif; position: relative; }}
  body::after {{ content: ""; position: absolute; inset: 0; background: radial-gradient(110% 90% at 0% 0%, rgba(255,255,255,.18), transparent 55%); }}
  .wrap {{ position: absolute; inset: 0; z-index: 1; display: grid; grid-template-columns: 330px 1fr; gap: 64px; align-items: center; padding: 0 88px; }}
  .icon {{ position: relative; width: 330px; height: 330px; }}
  .icon img {{ position: absolute; inset: 0; width: 100%; height: 100%; border-radius: 74px; }}
  .icon .glow {{ filter: blur(40px) saturate(1.6); opacity: .75; transform: scale(1.08) translateY(14px); }}
  .icon .main {{ box-shadow: 0 24px 60px rgba(0,0,0,.45); }}
  .kind {{ font-size: 22px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; opacity: .8; }}
  h1 {{ font-size: 96px; font-weight: 700; letter-spacing: -.045em; line-height: .95; margin: 14px 0 22px; }}
  p {{ font-size: 34px; font-weight: 600; letter-spacing: -.015em; line-height: 1.25; margin: 0; }}
  .by {{ position: absolute; left: 88px; right: 88px; bottom: 44px; z-index: 1; font-size: 22px; font-weight: 600; opacity: .75; display: flex; justify-content: space-between; }}
</style></head><body>
  <div class="wrap">
    <div class="icon"><img class="glow" src="{icon}"><img class="main" src="{icon}"></div>
    <div><div class="kind">{e(app["kind"])}</div><h1>{e(app["name"])}</h1><p>{e(app["tagline"])}</p></div>
  </div>
  <div class="by"><span>Garrett Franks</span><span>gfranks.github.io/{app["id"]}</span></div>
</body></html>"""


def render_og():
    out = ROOT / "assets" / "og"
    out.mkdir(parents=True, exist_ok=True)
    jobs = [("home", og_home())] + [(app["id"], og_app(app)) for app in APPS]
    with tempfile.TemporaryDirectory() as tmp:
        for name, page in jobs:
            src = pathlib.Path(tmp) / f"{name}.html"
            src.write_text(page)
            png = pathlib.Path(tmp) / f"{name}.png"
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                            "--force-device-scale-factor=1", "--window-size=1200,630",
                            f"--screenshot={png}", src.as_uri()],
                           check=True, capture_output=True)
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "86", str(png),
                            "--out", str(out / f"{name}.jpg")], check=True, capture_output=True)
    print(f"Rendered {len(jobs)} share images.")


def write(path, text):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def main():
    if "--og" in sys.argv:
        render_og()
    write("index.html", home())
    write("404.html", not_found())
    for app in APPS:
        write(f'{app["id"]}/index.html', app_page(app))
        if app["legal"]:
            for slug, title in PAGES:
                write(f'{app["id"]}/{slug}/index.html', legal_page(app, slug, title))
    print(f"Built home, 404 and {len(APPS)} apps.")


if __name__ == "__main__":
    main()
