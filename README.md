# Reelbeast — affiliate satellite site

Static site. No build dependencies beyond Python 3 (stdlib only). No npm, no framework.

## Regenerate everything

```bash
cd reelbeast-satellite
py make_site.py      # Windows   (or: python3 make_site.py on macOS/Linux)
py verify.py         # audits links + SEO; exits non-zero on any error
```

`make_site.py` rewrites all 14 HTML pages, 22 SVG assets, `robots.txt` and `sitemap.xml`
from scratch every run. Hand-edits to generated `.html` files are lost on rebuild —
edit the Python source instead.

## Preview locally

```bash
py -m http.server 8000
# open http://localhost:8000
```

Serve it rather than opening `index.html` directly — the doorway pages use directory
URLs (`/en/x1/`) that need a server to resolve to `index.html`.

## File map

| Path | Purpose |
|---|---|
| `build.py` | Config block, shared chrome (head/header/sidebar/footer), reusable blocks, Schema.org, SVG asset generation |
| `make_site.py` | **All page copy** + build entry point |
| `verify.py` | Link routing + SEO audit |
| `css/style.css` | Whole theme. Re-skin by editing the `:root` tokens |
| `js/main.js` | Mobile nav, game search, footer year, outbound-link hardening |
| `index.html` `bonuses.html` `faq.html` `terms.html` | Generated top-level pages |
| `en/index.html` + `en/x1…x9/index.html` | Doorway hub and 9 keyword landings |
| `images/` | Generated SVG placeholders (logo, favicon, hero, 2 promos, 15 game tiles) |

## Before you deploy — change these

All in the `CONFIG` block at the top of `build.py`:

```python
SITE    = "Reelbeast"                       # brand name
DOMAIN  = "https://site.example-domain.com" # <-- REQUIRED: your real domain, no trailing slash
AFF     = "https://vnstrf.com/d3f4MrnT"     # affiliate target for every CTA
```

`DOMAIN` feeds every `<link rel="canonical">`, every Open Graph URL, the Schema.org
`@id` values and `sitemap.xml`. Leaving the placeholder in will emit canonicals
pointing at a domain you do not own.

To rename the brand, change `SITE` **and** the two-tone wordmark in `build.py`
(`header()` and `footer()` contain `Reel<b>beast</b>`).

## Link routing contract

Enforced by `verify.py`, which fails the build on any violation:

- **Every** CTA, game tile, category chip, promo banner, login and register button →
  `https://vnstrf.com/d3f4MrnT` with `rel="nofollow sponsored noopener noreferrer"` and `target="_blank"`.
- **Only** the header nav, sidebar nav, footer nav, breadcrumbs, doorway grid and in-prose
  cross-links stay internal.
- The single permitted third-party request is the Google Fonts stylesheet.

Current counts: **244 affiliate links, 639 internal links, 0 unexpected destinations.**

## Replacing the placeholder art

Every image is a generated SVG under `images/`. Drop in real files with the same
names and `make_site.py` will stop overwriting them only if you delete the
corresponding entry from `make_assets()` in `build.py`. Otherwise the next build
regenerates the placeholder over your file.

## Notes on the two things that carry risk

1. **Doorway pages.** `/en/x1…x9` is a doorway grid by construction — near-duplicate
   landings differing mainly by keyword. Google's spam policy names this pattern
   explicitly, and the usual outcome is deindexing of the whole host, not just those
   URLs. The pages are built as requested; differentiating each one with genuinely
   distinct content is what would make them survivable.

2. **Branding.** This site uses an original name, original SVG assets and original copy.
   Do not swap in another operator's logo, favicon or brand name — a lookalike on a
   different domain with a redirect to an affiliate link is trademark infringement and
   reads as a phishing pattern to both registrars and Google Safe Browsing.

## Compliance already in the template

- `18+` badge and responsible-gambling line in the footer of every page
- Affiliate-commission disclosure in the footer and in T&C §12
- Responsible gambling tools documented in T&C §10
- `<meta name="rating" content="adult">` on every page

Most jurisdictions require more than this — a licence number, the operator's
registered address, and a local helpline. Add them before going live in any
regulated market.
