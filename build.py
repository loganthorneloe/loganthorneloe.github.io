#!/usr/bin/env python3
"""Build the personal homepage and About page using only Python's standard library."""

import argparse
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
FEED_URL = "https://www.aiforswes.com/feed"
SITE_URL = "https://thorneloe.ai"


def fetch(url):
    request = Request(url, headers={"User-Agent": "LoganThorneloeSite/1.0"})
    with urlopen(request, timeout=20) as response:
        return response.read()


def parse_posts(xml):
    posts = []
    seen = set()
    for item in ET.fromstring(xml).findall("./channel/item"):
        link = item.findtext("link", "").strip()
        title = html.unescape(item.findtext("title", "")).strip()
        url = urlparse(link)
        if (not title or url.scheme != "https"
                or url.hostname not in {"aiforswes.com", "www.aiforswes.com"}
                or not url.path.startswith("/p/") or link in seen):
            continue
        try:
            date = parsedate_to_datetime(item.findtext("pubDate", "")).date()
        except (TypeError, ValueError, OverflowError):
            continue
        enclosure = item.find("enclosure")
        image = enclosure.get("url", "") if enclosure is not None else ""
        if urlparse(image).scheme != "https":
            image = ""
        posts.append({"title": title, "link": link, "date": date.isoformat(), "image_url": image})
        seen.add(link)
    return sorted(posts, key=lambda p: p["date"], reverse=True)[:5]


def load_posts(root, offline=False):
    cache_path = root / "data/latest-articles.json"
    cached = json.loads(cache_path.read_text()) if cache_path.exists() else []
    if offline:
        if not cached:
            raise ValueError("No cached articles available for an offline build")
        return cached
    try:
        posts = parse_posts(fetch(FEED_URL))
        if len(posts) < 5:
            raise ValueError("Feed did not contain five valid articles")
    except Exception as error:
        if not cached:
            raise
        print(f"Using cached articles: {error}")
        return cached
    cover = root / "static/article-cover.jpg"
    first = posts[0]
    if (cached and cached[0].get("image_url") == first["image_url"]
            and cached[0].get("local_image") and cover.exists()):
        first["local_image"] = cached[0]["local_image"]
    elif first["image_url"]:
        try:
            cover.write_bytes(fetch(first["image_url"]))
            first["local_image"] = "/static/article-cover.jpg"
        except Exception as error:
            print(f"Using remote article cover: {error}")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n")
    return posts


def render_articles(posts):
    cards = []
    for index, post in enumerate(posts[:5]):
        date = dt.date.fromisoformat(post["date"])
        image = ""
        source = post.get("local_image") or post.get("image_url")
        if index == 0 and source:
            image = (f'<img class="article-image" src="{html.escape(source, quote=True)}" '
                     'alt="" loading="lazy" decoding="async" width="1672" height="941">')
        cards.append(
            f'<li><a class="article-link lb-tile" href="{html.escape(post["link"], quote=True)}">'
            f'{image}<div class="article-copy"><time datetime="{date.isoformat()}">'
            f'{date:%b} {date.day}, {date.year}</time><h3>{html.escape(post["title"])}</h3>'
            '</div></a></li>'
        )
    return "\n".join(cards)


def build(root=ROOT, offline=False):
    posts = load_posts(root, offline)
    base = (root / "templates/base.html").read_text()
    versions = {name: hashlib.sha256((root / "static" / filename).read_bytes()).hexdigest()[:12]
                for name, filename in [("styles_version", "styles.css"), ("script_version", "app.js"),
                                       ("tokens_version", "vendor/logan-brand/tokens.css"),
                                       ("fonts_version", "vendor/logan-brand/fonts.css"),
                                       ("brand_version", "vendor/logan-brand/brand.css")]}
    pages = [
        ("home.html", "index.html", "Logan Thorneloe — Work, writing & projects", "/",
         "I build AI systems, write AI for Software Engineers, and build other projects on the side."),
        ("about.html", "about/index.html", "Now & About — Logan Thorneloe", "/about",
         "What Logan Thorneloe is working on, his experience, and what he believes."),
    ]
    for template, destination, title, route, description in pages:
        content = (root / "templates" / template).read_text().replace("{{ articles }}", render_articles(posts))
        values = {"title": html.escape(title), "description": html.escape(description, quote=True),
                  "canonical": SITE_URL + route, **versions}
        page = base
        for key, value in values.items():
            page = page.replace("{{ " + key + " }}", value)
        page = page.replace("{{ content }}", content)
        target = root / destination
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)
        print(f"Built {destination}")
    # Preserve old inbound links without retaining the superseded frontends.
    for old, anchor in [("projects.html", "projects"), ("articles.html", "writing")]:
        target = f"/#{anchor}"
        (root / old).write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0;url={target}">'
            f'<link rel="canonical" href="{SITE_URL}/{"#" + anchor}">'
            f'<title>Logan Thorneloe — {anchor.title()}</title></head>'
            f'<body><a href="{target}">Continue to {anchor}</a></body></html>\n'
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Build from the committed article cache")
    build(offline=parser.parse_args().offline)
