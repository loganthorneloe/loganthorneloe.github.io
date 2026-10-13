# loganthorneloe.github.io

Personal website for https://thorneloe.ai.

The homepage contains projects and the five latest AI for Software Engineers articles. AI Jobs and Stockboy use `/jobs/` and `/stockboy/` on `thorneloe.ai`. `/roadmap` redirects to the existing learning site; the newsletter remains at `aiforswes.com`. Unpublished projects are not clickable. Only the newest article has a cover image.

`/about/` contains Now, experience, and principles. The shared navigation links directly to the About page. The legacy `projects.html` and `articles.html` URLs redirect to their homepage sections. `CNAME` sets the canonical personal domain to `thorneloe.ai`. Cloudflare permanently redirects `loganthorneloe.com` and the former `logan.tools` links to their matching new URLs. The existing `logan-tools/` directory is separate from this personal-site build.

## Edit and preview

Edit `templates/home.html`, `templates/about.html`, and the shared `templates/base.html`. Styling, scripts, fonts, and images live in `static/`. HTML pages are generated; edit templates rather than generated files.

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

The public CV remains in [CV.md](CV.md).

Cloudflare DNS, redirects, and Worker ownership are documented in [domain setup](DOMAIN_SETUP.md).
