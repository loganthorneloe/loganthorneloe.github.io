# Working on the personal site

- Read `README.md` and `DOMAIN_SETUP.md` before changing builds or hosting.
- Shared brand source is the `vendor/logan-style` submodule. Pull requested updates with `git submodule update --init --remote vendor/logan-style`, then run `python3 build.py --offline`. Fresh checkouts initialize without `--remote`.
- Edit shared styles in the central `logan-style` repository; keep page composition and app behavior here. Commit the submodule pointer, generated brand assets, and rebuilt pages together. Builds never fetch upstream.
- The Pages artifact workflow uses committed assets via `--prebuilt-brand` and excludes the private submodule source. Pages Source must be GitHub Actions.
- Run `python3 -m unittest discover -s tests` and `node --check static/app.js` for relevant changes. Inspect visual changes in both themes at mobile and desktop widths.
- Keep the retired, untracked `logan-tools/` archive out of commits and deployments.
