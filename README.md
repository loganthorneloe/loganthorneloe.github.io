# loganthorneloe.github.io

Personal website for https://thorneloe.ai.

The homepage contains projects and the five latest AI for Software Engineers articles. AI Jobs and Stockboy use `/jobs/` and `/stockboy/` on `thorneloe.ai`. `/roadmap` redirects to the existing learning site; the newsletter remains at `aiforswes.com`. Unpublished projects are not clickable. Only the newest article has a cover image.

`/now/` contains current work, experience, and principles. The shared navigation links directly to the Now page, and `/about/` redirects there. The legacy `projects.html` and `articles.html` URLs redirect to their homepage sections. `CNAME` sets the canonical personal domain to `thorneloe.ai`. Cloudflare permanently redirects `loganthorneloe.com` to its matching new URLs. The former tools domain is retired; the `logan-tools/` directory is an inactive archive.

## Edit and preview

Edit `templates/home.html`, `templates/now.html`, and the shared `templates/base.html`. Styling, scripts, fonts, and images live in `static/`. HTML pages are generated; edit templates rather than generated files.

```sh
python3 build.py --offline
python3 -m http.server 8768 --bind 127.0.0.1
```

Open http://127.0.0.1:8768/. The offline build uses the committed article cache and requires no network or additional Python packages.

```sh
python3 build.py
python3 -m unittest discover -s tests
```

A normal build refreshes the public newsletter RSS feed, caches five posts in `data/latest-articles.json`, and saves the first cover to `static/article-cover.jpg`. If the feed is unavailable, it retains cached articles. Styles and scripts use content hashes to invalidate browser caches. No GitHub API is used.

The existing GitHub Actions workflow runs on main pushes and daily at midnight UTC, rebuilds the pages, and commits changed generated pages, article metadata, and the cover image. Publishing still uses the repository's existing hosting setup.

## Shared brand kit

The site loads `static/vendor/logan-brand/{tokens,fonts,brand}.css` before its
own stylesheet. The shared kit supplies typography, colors, navigation,
controls, connected tiles, links, and numbered reading lists. Keep its files
unchanged; `static/styles.css` owns the hero artwork and page composition.
`static/app.js` preserves the `logan-theme` preference and mobile menu behavior.
The build hashes each imported stylesheet to refresh cached assets on updates.

```sh
python3 ../logan-style/scripts/install_web.py static/vendor/logan-brand --update
python3 ../logan-style/scripts/install_web.py static/vendor/logan-brand --check
python3 build.py --offline
python3 -m unittest discover -s tests
node --check static/app.js
```

After updates, check Home and Now in both themes at desktop and mobile sizes,
including the menu, keyboard focus, artwork, and linked tiles.

The public CV remains in [CV.md](CV.md).

Cloudflare DNS, redirects, and Worker ownership are documented in [domain setup](DOMAIN_SETUP.md).
