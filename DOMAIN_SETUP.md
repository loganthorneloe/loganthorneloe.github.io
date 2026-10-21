# Public domain setup

Canonical site: https://thorneloe.ai. GitHub Pages publishes this repository;
`CNAME`, canonical metadata, robots.txt, and sitemap.xml use that domain.

Pages Source must be **GitHub Actions**. The prepared workflow publishes an allowlisted artifact from
`package_site.py` and uses committed brand assets; it does not fetch the private
`logan-style` submodule. Branch-based Pages builds cannot fetch that dependency.

## Cloudflare DNS

- `thorneloe.ai`: proxied apex CNAME to `loganthorneloe.github.io` (flattened by Cloudflare).
- `www.thorneloe.ai`: proxied CNAME to `thorneloe.ai`.
- `loganthorneloe.com`: the existing four GitHub Pages A and four AAAA records are proxied.
- `www.loganthorneloe.com`: proxied CNAME to `loganthorneloe.github.io`.
- `aidevpass.com` and `www.aidevpass.com`: proxied A records to `192.0.2.1`; Cloudflare handles redirects before any origin request.
- The existing `thorneloe.ai` mail and verification records are unchanged.

## Permanent redirects

All rules below use HTTP 301 and preserve query strings:

| Zone | Matching hosts/paths | Destination |
| --- | --- | --- |
| thorneloe.ai | Host `www.thorneloe.ai`, any path | `concat("https://thorneloe.ai", http.request.uri.path)` |
| thorneloe.ai | Host `thorneloe.ai`, path `/roadmap` or `/roadmap/` | `https://learn.aiforswes.com/` |
| thorneloe.ai | Host `thorneloe.ai`, path `/devpass`, `/devpass/`, `/tinkerkit`, or `/tinkerkit/` | `https://www.aiforswes.com/perks` |
| aidevpass.com | Hosts `aidevpass.com` and `www.aidevpass.com`, any path | `https://www.aiforswes.com/perks` |
| loganthorneloe.com | Hosts `loganthorneloe.com` and `www.loganthorneloe.com`, any path | `concat("https://thorneloe.ai", http.request.uri.path)` |

The learning domain currently forwards onward to the existing AI foundations
GitHub repository. The former `thorneloe.ai` redirect to `loganthorneloe.com`
was replaced by the www-only canonical redirect. Do not restore it: that would
create a redirect loop with the old-domain rule.

## App routing

| Cloudflare Worker | Routes |
| --- | --- |
| stockboy | `thorneloe.ai/stockboy*` |
| ai-jobs | `thorneloe.ai/job*`, `thorneloe.ai/ai-jobs*`, `thorneloe.ai/aijobs*` |

Each Worker validates its exact supported paths after the prefix route match.
Stockboy normalizes `/stockboy` to `/stockboy/`. AI Jobs normalizes `/jobs` to
`/jobs/`; `/ai-jobs`, `/aijobs`, and `/job` are permanent aliases to `/jobs`,
including descendant paths and query strings. There are no Worker routes on
the retired link domain.

App source, deployment configuration, and tests live in the separate `stockboy`
and `ai-jobs` repositories. Their private R2 bindings and API protections are
unchanged. The migration deployed only the jobs Worker script and changed
routes, preserving the already-published app assets.

## Retired link domain

`logan.tools` is retired. Auto-renewal is off; the registration expires on
September 6, 2027. It must not redirect to or host any personal site or app.
The redirect rule, all six app routes, and the homepage custom domain were
removed. Keep this zone disconnected and do not reattach it during deployment.

The untracked `logan-tools/` directory is an inactive archive. Its Wrangler
configuration has no routes, no workers.dev URL, and no preview URLs. The
existing `logan-tools-home` Worker has no public domain or enabled Worker URL.

## IRONWAKE

The `ironwake` Cloudflare Worker serves `thorneloe.ai/ironwake*`. The bare `/ironwake` redirects to `/ironwake/`; the Worker handles only that path prefix and leaves other paths to the personal site. There is no database: random callsigns and saved mechs stay in browser storage. Source and deployments live in the separate public `loganthorneloe/ironwake` repository. The personal site publishes only its WIP link.
