#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reelbeast satellite — static site generator.

Run:  python build.py
Emits: index.html, bonuses.html, faq.html, terms.html,
       en/index.html, en/x1..x9/index.html,
       images/*.svg, robots.txt, sitemap.xml

Edit CONFIG below to rebrand / repoint. Everything else derives from it.
"""

import os, re, html, random

HERE = os.path.dirname(os.path.abspath(__file__))

# ============================================================================
# CONFIG  — the only block you normally need to touch
# ============================================================================
SITE       = "Reelbeast"
TAGLINE    = "Unleash the Reels"
DOMAIN     = "https://yard.example-domain.com"   # <-- your target domain, no trailing slash
AFF        = "https://vnstrf.com/d3f4MrnT"       # <-- every CTA points here
LOCALE     = "en"
BONUS_CASH = "1,500"
BONUS_CUR  = "EUR"
BONUS_SYM  = "\u20ac"
FREE_SPINS = "200"

# Affiliate anchor attributes: nofollow+sponsored keeps the link graph clean.
AFF_ATTRS = 'href="%s" target="_blank" rel="nofollow sponsored noopener noreferrer"' % AFF


# ============================================================================
# Internal navigation (these are the ONLY non-affiliate links on the site)
# ============================================================================
NAV = [
    ("index.html",   "Home",     "\U0001F3AE"),
    ("bonuses.html", "Bonuses",  "\U0001F381"),
    ("faq.html",     "FAQ",      "\U0001F4AC"),
    ("terms.html",   "Terms",    "\U0001F4C4"),
]

# Doorway pages under /en/. slug -> (nav label, keyword angle, H1, intro, bullets)
DOORS = [
    ("x1", "Welcome Bonus", "welcome bonus",
     "%s Welcome Bonus \u2014 %s%s + %s Free Spins" % (SITE, BONUS_SYM, BONUS_CASH, FREE_SPINS),
     "Your first deposit at %s is matched straight away, and the free spins land on the reels the moment the balance clears. No codes to hunt down, no hidden steps \u2014 just a bigger bankroll before your first spin." % SITE,
     ["100%% match up to %s%s on deposit one" % (BONUS_SYM, BONUS_CASH),
      "%s free spins released in daily batches" % FREE_SPINS,
      "35x wagering \u2014 published up front, never buried"]),

    ("x2", "Free Spins", "free spins",
     "Free Spins at %s \u2014 Daily Drops and Reload Rounds" % SITE,
     "Free spins are the fastest way to meet a new slot without touching your own balance. %s hands them out on signup, on reloads, and through the weekly drop \u2014 and the winnings are real, not locked behind a phantom cap." % SITE,
     ["Up to %s spins across the welcome sequence" % FREE_SPINS,
      "Weekly reload spins on the featured slot",
      "Winnings credited as bonus funds at 35x"]),

    ("x3", "Mobile Casino", "mobile casino",
     "%s Mobile Casino \u2014 Full Lobby in Your Browser" % SITE,
     "There is no app to sideload and no storage to sacrifice. The whole lobby runs in mobile Safari and Chrome at full speed, with portrait-first game frames and a cashier that works with one thumb.",
     ["Every slot playable in portrait orientation",
      "Session resumes exactly where you left it",
      "Face ID and fingerprint login supported"]),

    ("x4", "Live Casino", "live casino",
     "Live Casino at %s \u2014 Real Dealers, Real Time" % SITE,
     "Studio-streamed blackjack, roulette, baccarat and game shows run around the clock in HD. Tables start low enough for a casual session and stretch high enough for serious stakes.",
     ["Blackjack, roulette, baccarat and game shows",
      "Tables from %s0.50 to %s5,000 a hand" % (BONUS_SYM, BONUS_SYM),
      "Multi-camera HD streams with in-table chat"]),

    ("x5", "Megaways Slots", "megaways slots",
     "Megaways Slots at %s \u2014 Up to 117,649 Ways" % SITE,
     "Megaways reels change shape on every spin, so the number of winning ways shifts as you play. The mechanic pairs with cascading symbols and unlimited multipliers, which is why the format dominates the high-volatility charts.",
     ["Cascading reels with unlimited win multipliers",
      "Up to 117,649 ways to win on a single spin",
      "Feature buy available on selected titles"]),

    ("x6", "Fast Payouts", "fast payouts",
     "Fast Payouts at %s \u2014 Most Withdrawals Inside an Hour" % SITE,
     "A casino is only as good as its cashier. %s verifies once, up front, so approved withdrawals move as soon as they are requested rather than sitting in a queue for three working days." % SITE,
     ["E-wallets and crypto typically under 60 minutes",
      "Cards and bank transfer in 1\u20133 working days",
      "One-time KYC \u2014 verify once, withdraw freely"]),

    ("x7", "New Slots", "new slots",
     "New Slots at %s \u2014 Fresh Releases Every Week" % SITE,
     "The studios ship new titles constantly, and %s adds them the week they go live. The New Releases row is the first place to look if you want a mechanic nobody has solved yet." % SITE,
     ["New titles added every single week",
      "Demo mode on almost every release",
      "Launch-week free spins on featured slots"]),

    ("x8", "Jackpot Slots", "jackpot slots",
     "Jackpot Slots at %s \u2014 Progressive Pools That Keep Climbing" % SITE,
     "Progressive jackpots pool a slice of every stake across the whole network, so the headline figure grows until somebody triggers it. %s carries both the network giants and the faster local pools." % SITE,
     ["Network progressives climbing into seven figures",
      "Daily and hourly Must-Drop pools",
      "Live jackpot tickers on every eligible tile"]),

    ("x9", "VIP & Loyalty", "vip rewards",
     "%s VIP Club \u2014 Rewards That Scale With You" % SITE,
     "Every wager earns loyalty points automatically. Points move you up the tiers, and the tiers unlock cashback, faster withdrawals and a named host who actually answers.",
     ["Cashback rising from 5% to 15% by tier",
      "Priority withdrawal processing at Gold and above",
      "Dedicated VIP host from Platinum"]),
]

# ============================================================================
# Games — 15 popular slots. Tiles are original SVG placeholders.
# ============================================================================
GAMES = [
    ("Book of Dead",       "Play'n GO",      "#C9922E", "#6B3F0A", "\U0001F4D6", "hot"),
    ("Starburst",          "NetEnt",         "#7C5CFF", "#2A1370", "\u2726",     ""),
    ("Gonzo's Quest",      "NetEnt",         "#2FA36B", "#0C3A22", "\U0001F5FF", ""),
    ("Sweet Bonanza",      "Pragmatic Play", "#FF6FB5", "#7A1247", "\U0001F36D", "hot"),
    ("Gates of Olympus",   "Pragmatic Play", "#3E7BDC", "#10254F", "\u26A1",     "hot"),
    ("Big Bass Bonanza",   "Reel Kingdom",   "#2BA7C4", "#0B3B49", "\U0001F41F", ""),
    ("Wolf Gold",          "Pragmatic Play", "#D9A03C", "#4A2E08", "\U0001F43A", ""),
    ("Dead or Alive 2",    "NetEnt",         "#A6704A", "#3B2114", "\U0001F480", ""),
    ("Money Train 3",      "Relax Gaming",   "#C0453E", "#4A1210", "\U0001F682", "hot"),
    ("Bonanza Megaways",   "Big Time Gaming","#E0A93B", "#4C3208", "\u26CF",     ""),
    ("Reactoonz",          "Play'n GO",      "#43C9B0", "#0D423A", "\U0001F47E", ""),
    ("Fire Joker",         "Play'n GO",      "#E4562C", "#4C1608", "\U0001F525", ""),
    ("Jammin' Jars",       "Push Gaming",    "#E8C13C", "#4C3D06", "\U0001FAD9", ""),
    ("Razor Shark",        "Push Gaming",    "#2E6FA8", "#0A2440", "\U0001F988", ""),
    ("Legacy of Dead",     "Play'n GO",      "#B98A2F", "#452F06", "\U0001F3FA", ""),
]

def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# ============================================================================
# SVG placeholder assets
# ============================================================================
def write(path, content):
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def make_assets():
    made = []

    # Logo: beast eye inside a rounded badge + wordmark handled in HTML
    made.append(write("images/logo.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48" role="img" aria-label="%s logo">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#38E07B"/><stop offset="1" stop-color="#7C5CFF"/>
    </linearGradient>
  </defs>
  <rect width="48" height="48" rx="13" fill="url(#g)"/>
  <path d="M10 18c4-6 10-9 14-9s10 3 14 9c-4 7-9 11-14 11s-10-4-14-11z" fill="#070911" opacity=".9"/>
  <circle cx="24" cy="18" r="6" fill="#38E07B"/>
  <circle cx="24" cy="18" r="2.6" fill="#070911"/>
  <path d="M13 33c3 3 7 5 11 5s8-2 11-5" stroke="#070911" stroke-width="3" stroke-linecap="round" fill="none"/>
  <path d="M17 33l2.5 4M24 34v4.5M31 33l-2.5 4" stroke="#070911" stroke-width="2.4" stroke-linecap="round"/>
</svg>''' % SITE))

    made.append(write("images/favicon.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
  <rect width="48" height="48" rx="11" fill="#0B0E17"/>
  <circle cx="24" cy="22" r="11" fill="#38E07B"/>
  <circle cx="24" cy="22" r="4.6" fill="#0B0E17"/>
  <path d="M13 36c3 3 7 4.5 11 4.5S32 39 35 36" stroke="#38E07B" stroke-width="3.4" stroke-linecap="round" fill="none"/>
</svg>'''))

    # Hero artwork
    made.append(write("images/hero-slot-machine.svg", '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 400" width="520" height="400" role="img" aria-label="Illustration of a %s slot machine with three glowing reels">
  <defs>
    <linearGradient id="cab" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#2A1B52"/><stop offset="1" stop-color="#140B2C"/>
    </linearGradient>
    <linearGradient id="gl" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#38E07B"/><stop offset="1" stop-color="#FF3DA6"/>
    </linearGradient>
    <filter id="b"><feGaussianBlur stdDeviation="14"/></filter>
  </defs>
  <ellipse cx="260" cy="350" rx="170" ry="34" fill="#38E07B" opacity=".2" filter="url(#b)"/>
  <rect x="96" y="54" width="328" height="278" rx="30" fill="url(#cab)" stroke="url(#gl)" stroke-width="3"/>
  <rect x="128" y="92" width="264" height="24" rx="12" fill="#38E07B" opacity=".25"/>
  <g>
    <rect x="128" y="134" width="76" height="116" rx="12" fill="#070911"/>
    <rect x="222" y="134" width="76" height="116" rx="12" fill="#070911"/>
    <rect x="316" y="134" width="76" height="116" rx="12" fill="#070911"/>
    <text x="166" y="208" font-size="46" text-anchor="middle" fill="#FFC93C">7</text>
    <text x="260" y="208" font-size="46" text-anchor="middle" fill="#FFC93C">7</text>
    <text x="354" y="208" font-size="46" text-anchor="middle" fill="#FFC93C">7</text>
  </g>
  <rect x="128" y="270" width="264" height="40" rx="20" fill="url(#gl)"/>
  <text x="260" y="296" font-size="17" font-weight="700" text-anchor="middle" fill="#04210F">SPIN</text>
  <circle cx="446" cy="150" r="17" fill="#FFC93C"/>
  <rect x="438" y="150" width="16" height="96" rx="8" fill="#8C6A18"/>
</svg>''' % SITE))

    # Promo banner art
    for name, c1, c2, label in [
        ("promo-welcome", "#38E07B", "#7C5CFF", "WELCOME"),
        ("promo-reload",  "#FF3DA6", "#FFC93C", "RELOAD"),
    ]:
        made.append(write("images/%s.svg" % name, '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 260" width="640" height="260" role="img" aria-label="%s promotion banner">
  <defs><linearGradient id="p" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>
  <rect width="640" height="260" rx="22" fill="#0F1426"/>
  <circle cx="540" cy="60" r="130" fill="url(#p)" opacity=".28"/>
  <circle cx="90" cy="220" r="100" fill="url(#p)" opacity=".2"/>
  <text x="44" y="120" font-size="34" font-weight="800" fill="#EAF0FF">%s</text>
  <rect x="44" y="140" width="150" height="8" rx="4" fill="url(#p)"/>
</svg>''' % (label.title(), c1, c2, label)))

    # 15 game tiles
    for name, prov, c1, c2, glyph, _badge in GAMES:
        made.append(write("images/games/%s.svg" % slug(name), '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300" width="300" height="300" role="img" aria-label="%s slot by %s">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>
    </linearGradient>
    <radialGradient id="sh" cx="50%%" cy="34%%" r="62%%">
      <stop offset="0" stop-color="#ffffff" stop-opacity=".30"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="300" height="300" fill="url(#bg)"/>
  <rect width="300" height="300" fill="url(#sh)"/>
  <text x="150" y="168" font-size="104" text-anchor="middle">%s</text>
  <rect x="0" y="228" width="300" height="72" fill="#070911" opacity=".62"/>
  <text x="150" y="258" font-size="21" font-weight="700" text-anchor="middle" fill="#EAF0FF">%s</text>
  <text x="150" y="282" font-size="14" text-anchor="middle" fill="#8FA0C4">%s</text>
</svg>''' % (html.escape(name), html.escape(prov), c1, c2, glyph,
             html.escape(name[:20]), html.escape(prov))))

    return made


# ============================================================================
# Shared chrome
# ============================================================================
def rel(depth):
    """Relative path prefix for a page nested `depth` folders deep."""
    return "../" * depth


def head(title, desc, canonical, depth, extra_schema=""):
    p = rel(depth)
    return '''<!DOCTYPE html>
<html lang="%(loc)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(dom)s/%(canon)s">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0B0E17">
<meta name="rating" content="adult">

<meta property="og:type" content="website">
<meta property="og:site_name" content="%(site)s">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(dom)s/%(canon)s">
<meta property="og:image" content="%(dom)s/images/promo-welcome.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(desc)s">

<link rel="icon" type="image/svg+xml" href="%(p)simages/favicon.svg">
<link rel="apple-touch-icon" href="%(p)simages/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bungee&family=Inter:wght@400;600;700;800;900&display=swap">
<link rel="stylesheet" href="%(p)scss/style.css">
%(schema)s</head>
<body>
''' % dict(loc=LOCALE, title=html.escape(title), desc=html.escape(desc),
           dom=DOMAIN, canon=canonical, site=SITE, p=p, schema=extra_schema)


def header(active, depth):
    p = rel(depth)
    links = "".join(
        '<a href="%s%s"%s>%s</a>' % (p, href, ' aria-current="page"' if href == active else '', label)
        for href, label, _ic in NAV
    )
    return '''<header class="site-header">
  <div class="site-header__inner">
    <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="sidebar"><span></span></button>
    <a class="logo" href="%(p)sindex.html">
      <img src="%(p)simages/logo.svg" width="48" height="48" alt="%(site)s online casino logo">
      <span class="logo__text">Reel<b>beast</b></span>
    </a>
    <nav class="nav-main" aria-label="Primary">%(links)s</nav>
    <div class="header-search">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
      <label class="sr-only" for="q">Search games</label>
      <input id="q" type="search" placeholder="Search games\u2026" data-game-search autocomplete="off">
    </div>
    <div class="header-actions">
      <a class="btn btn--ghost" %(aff)s>Log In</a>
      <a class="btn btn--primary" %(aff)s>Register</a>
    </div>
  </div>
</header>
<div class="scrim"></div>
''' % dict(p=p, site=SITE, links=links, aff=AFF_ATTRS)


def sidebar(active, depth):
    p = rel(depth)
    main = "".join(
        '<a href="%s%s"%s><span class="ic" aria-hidden="true">%s</span>%s</a>'
        % (p, href, ' aria-current="page"' if href == active else '', ic, label)
        for href, label, ic in NAV
    )
    doors = "".join(
        '<a href="%sen/%s/"%s><span class="ic" aria-hidden="true">\u25B8</span>%s</a>'
        % (p, sl, ' aria-current="page"' if active == "en/%s/" % sl else '', label)
        for sl, label, _kw, _h1, _intro, _b in DOORS
    )
    return '''<aside class="sidebar" id="sidebar">
  <p class="sidebar__title">Casino</p>
  <nav aria-label="Site sections">%(main)s
    <a href="%(p)sen/"%(enc)s><span class="ic" aria-hidden="true">\U0001F5FA</span>All Guides</a>
  </nav>
  <p class="sidebar__title">Top Guides</p>
  <nav aria-label="Guides">%(doors)s</nav>
  <div class="sidebar__cta">
    <strong>%(sym)s%(cash)s + %(fs)s FS</strong>
    <p>New players only. 35x wagering. 18+</p>
    <a class="btn btn--accent btn--block" %(aff)s>Claim Bonus</a>
  </div>
</aside>
''' % dict(main=main, doors=doors, p=p, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS,
           aff=AFF_ATTRS, enc=' aria-current="page"' if active == "en/" else '')


def footer(depth):
    p = rel(depth)
    col_main = "".join('<a href="%s%s">%s</a>' % (p, h, l) for h, l, _ in NAV)
    col_doors_a = "".join('<a href="%sen/%s/">%s</a>' % (p, s, l) for s, l, _k, _h, _i, _b in DOORS[:5])
    col_doors_b = "".join('<a href="%sen/%s/">%s</a>' % (p, s, l) for s, l, _k, _h, _i, _b in DOORS[5:])
    return '''</div>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="logo" href="%(p)sindex.html">
          <img src="%(p)simages/logo.svg" width="48" height="48" alt="%(site)s logo">
          <span class="logo__text">Reel<b>beast</b></span>
        </a>
        <p>%(site)s is an independent information and comparison site covering online slots,
           casino bonuses and live dealer games. We may earn a commission when you sign up
           through links on this page \u2014 it never changes what you pay or what you are offered.</p>
      </div>
      <div class="footer-col">
        <h4>Casino</h4>
        <nav aria-label="Footer sections">%(main)s</nav>
      </div>
      <div class="footer-col">
        <h4>Guides</h4>
        <nav aria-label="Footer guides">%(da)s</nav>
      </div>
      <div class="footer-col">
        <h4>More Guides</h4>
        <nav aria-label="Footer guides continued">%(db)s
          <a href="%(p)sen/">All Guides</a>
        </nav>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> %(site)s. All rights reserved.
         Gambling can be addictive \u2014 please play responsibly and never stake more than you can afford to lose.
         Free help is available at BeGambleAware and Gamblers Anonymous.</p>
      <div class="rg">
        <div class="rg__18" aria-hidden="true">18+</div>
        <span>Over 18s only<br>Play responsibly</span>
      </div>
    </div>
  </div>
</footer>

<div class="sticky-cta">
  <a class="btn btn--primary btn--block btn--lg" %(aff)s>Claim %(sym)s%(cash)s + %(fs)s Free Spins</a>
</div>

<script src="%(p)sjs/main.js" defer></script>
</body>
</html>
''' % dict(p=p, site=SITE, main=col_main, da=col_doors_a, db=col_doors_b,
           aff=AFF_ATTRS, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS)


def page(title, desc, canonical, active, depth, body, schema=""):
    return (head(title, desc, canonical, depth, schema)
            + header(active, depth)
            + '<div class="shell">\n'
            + sidebar(active, depth)
            + '<main>\n' + body + '</main>\n'
            + footer(depth))


# ============================================================================
# Reusable body blocks
# ============================================================================
def games_grid(depth, limit=15, heading=True):
    p = rel(depth)
    tiles = []
    for name, prov, _c1, _c2, _g, badge in GAMES[:limit]:
        b = '<span class="game__badge game__badge--hot">Hot</span>' if badge == "hot" else ""
        tiles.append('''    <a class="game" %(aff)s data-name="%(name)s" data-provider="%(prov)s">
      %(badge)s<img src="%(p)simages/games/%(slug)s.svg" width="300" height="300" loading="lazy"
           alt="%(name)s online slot by %(prov)s \u2014 play at %(site)s">
      <span class="game__overlay"><span class="btn btn--primary">Play Now</span></span>
      <span class="game__info">
        <span class="game__name">%(name)s</span>
        <span class="game__prov">%(prov)s</span>
      </span>
    </a>''' % dict(aff=AFF_ATTRS, name=html.escape(name), prov=html.escape(prov),
                   badge=b, p=p, slug=slug(name), site=SITE))

    head_html = '''  <div class="section__head">
    <div>
      <h2>Popular Slots Right Now</h2>
      <p>The titles players open first \u2014 hand-picked from the full %s+ game lobby.</p>
    </div>
    <a class="btn btn--ghost" %s>See All Games</a>
  </div>
''' % ("4,000", AFF_ATTRS) if heading else ""

    return '''<section class="section" id="games">
%(head)s  <div class="grid-games" data-game-grid>
%(tiles)s
  </div>
  <p data-game-empty hidden style="color:var(--muted);margin-top:16px">No games match that search. Try another title or provider.</p>
</section>
''' % dict(head=head_html, tiles="\n".join(tiles))


def door_grid(depth, exclude=None):
    p = rel(depth)
    cards = []
    for sl, label, kw, _h1, intro, _b in DOORS:
        if sl == exclude:
            continue
        short = intro.split(".")[0] + "."
        cards.append('''    <a class="door" href="%sen/%s/">
      <span class="door__kicker">%s</span>
      <h3>%s</h3>
      <p>%s</p>
    </a>''' % (p, sl, html.escape(kw), html.escape(label), html.escape(short[:112])))
    return '''<section class="section">
  <div class="section__head">
    <div>
      <h2>Explore %s Guides</h2>
      <p>Deep dives on bonuses, payouts, mechanics and mobile play.</p>
    </div>
  </div>
  <div class="grid-doors">
%s
  </div>
</section>
''' % (SITE, "\n".join(cards))


def crumbs(depth, trail):
    p = rel(depth)
    out = ['<a href="%sindex.html">Home</a>' % p]
    for label, href in trail[:-1]:
        out.append('<a href="%s%s">%s</a>' % (p, href, html.escape(label)))
    out.append(html.escape(trail[-1][0]))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>\n' % '<span>/</span>'.join(out)


# ============================================================================
# Schema.org
# ============================================================================
def schema_org():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "%(dom)s/#organization",
      "name": "%(site)s",
      "url": "%(dom)s/",
      "logo": {"@type":"ImageObject","url":"%(dom)s/images/logo.svg","width":48,"height":48},
      "description": "%(site)s is an independent guide to online slots, casino bonuses and live dealer games.",
      "sameAs": []
    },
    {
      "@type": "WebSite",
      "@id": "%(dom)s/#website",
      "url": "%(dom)s/",
      "name": "%(site)s",
      "inLanguage": "en",
      "publisher": {"@id": "%(dom)s/#organization"}
    },
    {
      "@type": ["EntertainmentBusiness","Casino"],
      "@id": "%(dom)s/#casino",
      "name": "%(site)s Casino",
      "url": "%(dom)s/",
      "image": "%(dom)s/images/hero-slot-machine.svg",
      "description": "Online casino lobby with 4,000+ slots, live dealer tables and a %(sym)s%(cash)s welcome package plus %(fs)s free spins.",
      "priceRange": "%(sym)s10\u2013%(sym)s5000",
      "currenciesAccepted": "%(cur)s",
      "paymentAccepted": "Visa, Mastercard, Skrill, Neteller, Trustly, Bitcoin",
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
        "opens": "00:00", "closes": "23:59"
      },
      "areaServed": {"@type":"Place","name":"Online"},
      "makesOffer": {
        "@type": "Offer",
        "name": "Welcome Package",
        "description": "100%% match up to %(sym)s%(cash)s plus %(fs)s free spins on first deposit. 35x wagering. 18+."
      }
    }
  ]
}
</script>
''' % dict(dom=DOMAIN, site=SITE, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS, cur=BONUS_CUR)


def schema_faq(qa):
    items = ",\n".join('''    {"@type":"Question","name":%s,
     "acceptedAnswer":{"@type":"Answer","text":%s}}'''
        % (jstr(q), jstr(re.sub(r'<[^>]+>', '', a))) for q, a in qa)
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
%s
]}
</script>
''' % items


def schema_breadcrumb(trail):
    items = []
    for i, (label, href) in enumerate(trail, 1):
        items.append('{"@type":"ListItem","position":%d,"name":%s,"item":"%s/%s"}'
                     % (i, jstr(label), DOMAIN, href))
    return '''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[%s]}
</script>
''' % ",".join(items)


def jstr(s):
    return '"%s"' % s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').strip()
