# Public domain setup

Canonical site: https://thorneloe.ai. GitHub Pages publishes this repository;
`CNAME`, canonical metadata, robots.txt, and sitemap.xml use that domain.

## Cloudflare DNS

- `thorneloe.ai`: proxied apex CNAME to `loganthorneloe.github.io` (flattened by Cloudflare).
- `www.thorneloe.ai`: proxied CNAME to `thorneloe.ai`.
- `loganthorneloe.com`: the existing four GitHub Pages A and four AAAA records are proxied.
- `www.loganthorneloe.com`: proxied CNAME to `loganthorneloe.github.io`.
- `logan.tools`: existing `logan-tools-home` Worker custom domain stays attached as a fallback.
- `www.logan.tools`: proxied A record `192.0.2.1`, used only for the edge redirect.
- The existing mail and verification records are unchanged.

## Permanent redirects

All rules below use HTTP 301 and preserve query strings:

| Zone | Matching hosts/paths | Destination |
| --- | --- | --- |
| thorneloe.ai | Host `www.thorneloe.ai`, any path | `concat("https://thorneloe.ai", http.request.uri.path)` |
| thorneloe.ai | Host `thorneloe.ai`, path `/roadmap` or `/roadmap/` | `https://learn.aiforswes.com/` |
| loganthorneloe.com | Hosts `loganthorneloe.com` and `www.loganthorneloe.com`, any path | `concat("https://thorneloe.ai", http.request.uri.path)` |
| logan.tools | Hosts `logan.tools` and `www.logan.tools`, any path | `concat("https://thorneloe.ai", http.request.uri.path)` |

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
including descendant paths and query strings. The old logan.tools Worker routes
remain attached as a fallback, but the zone redirect runs before them.

App source, deployment configuration, and tests live in the separate `stockboy`
and `ai-jobs` repositories. Their private R2 bindings and API protections are
unchanged. The migration deployed only the jobs Worker script and changed
routes, preserving the already-published app assets.

The untracked `logan-tools/` directory is the retired homepage deployment;
it is not the canonical homepage or the public link source. Keep the zone
redirect in place if maintaining that fallback Worker.
