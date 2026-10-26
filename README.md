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

The existing GitHub Actions workflow runs on main pushes and daily at midnight UTC, rebuilds the pages, and commits changed generated pages, article metadata, and the cover image. The workflow uploads only the public site files and deploys them with GitHub Pages Actions.

## Shared brand kit

The site loads `static/vendor/logan-brand/{tokens,fonts,brand}.css` before its
own stylesheet. The shared kit supplies typography, colors, navigation,
controls, connected tiles, links, and numbered reading lists. Keep its files
unchanged; `static/styles.css` owns the hero artwork and page composition.
Project icons have individual accents from the shared, theme-aware palette: blue jobs, red roadmap, teal watches, purple developer pass, amber IRONWAKE, green ML, and rose research. AI Dev Pass uses a code-ticket symbol to distinguish it from the jobs briefcase. These assignments live in `static/styles.css`; the existing newsletter and Stockboy logos retain their original artwork.

`static/app.js` preserves the `logan-theme` preference and mobile menu behavior.
The build hashes each imported stylesheet to refresh cached assets on updates.

```sh
git submodule update --init --remote vendor/logan-style
python3 build.py --offline
python3 -m unittest discover -s tests
node --check static/app.js
```

After updates, check Home and Now in both themes at desktop and mobile sizes,
including the menu, keyboard focus, artwork, and linked tiles.

The public CV remains in [CV.md](CV.md).

Cloudflare DNS, redirects, and Worker ownership are documented in [domain setup](DOMAIN_SETUP.md).

## Shared styling dependency

`vendor/logan-style` is a Git submodule pinned to a reviewed commit. To pull the latest shared style from `main`, run from this app:

```sh
git submodule update --init --remote vendor/logan-style
```

Then run the normal build or preview. To build just the assets explicitly:

```sh
python3 build.py --offline
```

The build runs the submodule's installer and verifies `static/vendor/logan-brand`. It refuses to overwrite locally edited brand files. Keep app-specific styles outside that directory. The generated assets remain committed for static hosting and existing checkout compatibility; include their diff and the changed submodule pointer together when committing an update. No background sync, cross-app registry, or automatic upstream fetch runs.

On a fresh checkout, `git submodule update --init vendor/logan-style` restores the pinned version without advancing it. The source repository requires authentication; use an account/key with read access. For a reproducible rollback, restore the previous submodule pointer, run `git submodule update --init vendor/logan-style`, and rebuild. Shared source changes must be committed and pushed in `logan-style` before apps can pull them.

The scheduled newsletter workflow uses `--prebuilt-brand` to retain the reviewed, committed styles without needing credentials for the private source repository. When updating the dependency locally, run the normal build without this flag and commit the generated styles/pages with the new pointer.

Set **Settings → Pages → Build and deployment → Source** to **GitHub Actions** when configuring hosting. Branch-based Pages builds cannot fetch the private submodule. The artifact workflow explicitly leaves submodules unchecked out and packages only public pages/assets, so it needs no new source-repository credential and never publishes the private kit source.

IRONWAKE is a playable work in progress linked from the homepage at `/ironwake/`. The game is maintained separately in `loganthorneloe/ironwake` and hosted by a Cloudflare Worker.

Garmin Watch Faces is a completed project linked from the homepage project grid to `loganthorneloe/garmin-watch`. The public repository houses Sector and Ember in separate face folders, with source, installable releases, and USB cable-install instructions for both.

AI for Software Engineers, AI Dev Pass, and AI Foundations Roadmap lead the homepage project grid. AI Dev Pass links to `/devpass`. Cloudflare permanently redirects `/devpass` and `/devpass/` to `https://www.aiforswes.com/perks`. Both `aidevpass.com` and `www.aidevpass.com` also redirect there, preserving query strings.
