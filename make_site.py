#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reelbeast satellite — content + build entry point.

Run:  python make_site.py

All page copy lives here; all shared chrome lives in build.py.
"""

from build import *   # config, chrome, blocks, schema helpers


# ============================================================================
# HOME
# ============================================================================
BENEFITS = [
    ("⚡", "Withdrawals in Under an Hour",
     "E-wallet and crypto cashouts are approved and sent the same hour in most cases. One-time verification up front means no scramble when you finally hit a big one."),
    ("\U0001F3B0", "4,000+ Games in One Lobby",
     "Slots, Megaways, live dealer tables, game shows and instant wins from Pragmatic Play, NetEnt, Play'n GO, Push Gaming, Relax and thirty more studios."),
    ("\U0001F512", "Licensed and Independently Audited",
     "Segregated player funds, TLS encryption on every request, and RNG certificates renewed annually by an accredited testing lab."),
    ("\U0001F4AC", "Support That Answers in Minutes",
     "Live chat is staffed around the clock by people who can actually resolve a cashier issue, not a bot looping you through an FAQ."),
    ("\U0001F4F1", "Built Mobile-First",
     "The full lobby runs in your phone browser at desktop speed. Nothing to install, no storage to sacrifice, and your session survives a lock screen."),
    ("₿", "Cards, E-Wallets and Crypto",
     "Visa, Mastercard, Skrill, Neteller, Trustly and Bitcoin all supported, with no deposit fee from our side on any method."),
]

CATEGORIES = [
    ("\U0001F3B0", "Slots"), ("\U0001F3B4", "Live Casino"), ("♾", "Megaways"),
    ("\U0001F48E", "Jackpots"), ("\U0001F0CF", "Table Games"), ("\U0001F3AA", "Game Shows"),
    ("\U0001F6D2", "Bonus Buy"), ("✨", "New Releases"),
]

STEPS = [
    ("Create Your Account", "Register in under a minute — email, currency, password. No documents needed at this stage."),
    ("Make a First Deposit", "Minimum %s10. The match and your free spins are credited automatically, no bonus code required." % BONUS_SYM),
    ("Pick Your Game", "Filter by studio, volatility or RTP. Nearly every slot has a demo mode if you want a look first."),
    ("Withdraw Your Winnings", "Clear the 35x wagering, request a cashout, and watch it land — usually the same hour."),
]

HOME_FAQ = [
    ("Is %s safe to play at?" % SITE,
     "Yes. The operator runs under a recognised gaming licence, keeps player deposits in accounts segregated from operating capital, encrypts every request in transit, and submits its random number generator for annual certification by an independent testing laboratory."),
    ("How long do withdrawals take?",
     "E-wallets and cryptocurrency are typically processed within the hour. Debit cards and bank transfers take one to three working days, which is bank-side time rather than casino-side. Completing verification before your first withdrawal removes the most common source of delay."),
    ("Do I need a bonus code?",
     "No. The welcome match and free spins attach to your first qualifying deposit automatically. If a seasonal promotion ever does require a code, it is printed on the promotion itself."),
    ("Can I play without depositing?",
     "Most slots offer a demo mode that runs on play money, which is a sensible way to learn a mechanic before committing real funds. Demo play cannot produce withdrawable winnings."),
]

HOME_PROSE = '''<h2>Why Players Choose %(site)s</h2>
<p>There is no shortage of online casinos. What separates the ones worth a deposit from the ones
worth closing is rarely the size of the headline bonus — it is whether the cashier pays out
without an argument, whether the lobby has the games you actually want, and whether support
picks up when something goes wrong at two in the morning.</p>

<p><strong>%(site)s is built around those three things.</strong> The lobby carries more than 4,000
titles from the studios that matter, withdrawals are processed in hours rather than days, and the
bonus terms are printed in full on the <a href="bonuses.html">promotions page</a> rather than
buried in a footnote you find after you have already played.</p>

<h3>A Lobby Worth Browsing</h3>
<p>The slot catalogue spans everything from three-reel classics to 117,649-way Megaways monsters.
Pragmatic Play brings <em>Sweet Bonanza</em> and <em>Gates of Olympus</em>; NetEnt supplies
<em>Starburst</em> and <em>Dead or Alive 2</em>; Play'n GO covers the <em>Book of Dead</em> family;
Push Gaming handles the high-volatility end with <em>Razor Shark</em> and <em>Jammin' Jars</em>.
Filter by provider, volatility, RTP or release date, and sort a shortlist in seconds.</p>

<p>Beyond the reels, the live casino streams blackjack, roulette, baccarat and the full game-show
roster in HD from dedicated studios, with tables that start at %(sym)s0.50 and run up to
%(sym)s5,000 a hand. If you prefer something faster, the instant-win and crash section settles in
seconds.</p>

<h3>Bonuses You Can Actually Clear</h3>
<p>A %(sym)s5,000 headline with 60x wagering is worth less than a %(sym)s500 offer at 25x, and
most players work that out only after the fact. The %(site)s welcome package is
<strong>%(sym)s%(cash)s plus %(fs)s free spins at 35x</strong> — a mid-market figure attached
to terms that clear in a realistic number of sessions. Contribution rates, maximum bet while
wagering, and the expiry window are all stated up front. Read them on the
<a href="bonuses.html">bonuses page</a> before you opt in.</p>

<h3>Payments Without the Waiting Room</h3>
<p>Deposits are instant on every supported method. Withdrawals are where casinos reveal
themselves, and the policy here is deliberately simple: verify your identity once when you sign
up, and every subsequent cashout skips the document queue entirely. E-wallets and crypto usually
land inside sixty minutes; card and bank transfers follow standard banking timeframes of one to
three working days.</p>

<h3>Play Within Your Limits</h3>
<p>Gambling is entertainment with a cost, not an income strategy. Deposit limits, loss limits,
session reminders, cooling-off periods and permanent self-exclusion are all available in your
account settings and take effect immediately. If the game has stopped being fun, use them — and
if you need support beyond that, BeGambleAware and Gamblers Anonymous both offer free, confidential
help. See our <a href="terms.html">terms and conditions</a> for the full responsible gambling
policy.</p>
''' % dict(site=SITE, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS)


def build_home():
    benefits = "\n".join('''    <article class="benefit">
      <div class="benefit__ic" aria-hidden="true">%s</div>
      <h3>%s</h3>
      <p>%s</p>
    </article>''' % (ic, t, d) for ic, t, d in BENEFITS)

    chips = "\n".join('    <a class="chip" %s><span class="ic" aria-hidden="true">%s</span>%s</a>'
                      % (AFF_ATTRS, ic, label) for ic, label in CATEGORIES)

    steps = "\n".join('''    <article class="step">
      <h3>%s</h3>
      <p>%s</p>
    </article>''' % (t, d) for t, d in STEPS)

    faq = "\n".join('''  <details class="faq-item">
    <summary>%s</summary>
    <div class="faq-item__body"><p>%s</p></div>
  </details>''' % (html.escape(q), html.escape(a)) for q, a in HOME_FAQ)

    body = '''<section class="hero">
  <div class="hero__body">
    <span class="hero__eyebrow">New Player Package</span>
    <h1>%(tagline)s at <em>%(site)s</em></h1>
    <p>Claim <strong>%(sym)s%(cash)s in matched funds and %(fs)s free spins</strong>, then work
       through 4,000+ slots, live dealer tables and jackpot pools that never stop climbing.
       Withdrawals in under an hour. No bonus code needed.</p>
    <div class="hero__actions">
      <a class="btn btn--primary btn--lg" %(aff)s>Claim Your Bonus</a>
      <a class="btn btn--ghost btn--lg" %(aff)s>Play Now</a>
    </div>
    <div class="hero__meta">
      <span>✓ Licensed &amp; audited</span>
      <span>✓ Payouts under 1 hour</span>
      <span>✓ 24/7 live chat</span>
      <span>✓ 18+ only</span>
    </div>
  </div>
  <div class="hero__art">
    <img src="images/hero-slot-machine.svg" width="520" height="400" fetchpriority="high"
         alt="%(site)s slot machine showing three glowing sevens on the reels">
  </div>
</section>

<section class="section">
  <div class="section__head">
    <div>
      <h2>Why Play at %(site)s</h2>
      <p>Six things we get right that most casinos treat as optional.</p>
    </div>
  </div>
  <div class="grid-benefits">
%(benefits)s
  </div>
</section>

<section class="section">
  <div class="section__head">
    <div>
      <h2>Browse by Category</h2>
      <p>Jump straight into the format you came for.</p>
    </div>
  </div>
  <div class="chips">
%(chips)s
  </div>
</section>

%(games)s

<section class="section">
  <div class="section__head">
    <div>
      <h2>Live Promotions</h2>
      <p>Running right now — full terms on the bonuses page.</p>
    </div>
    <a class="btn btn--ghost" href="bonuses.html">All Promotions</a>
  </div>
  <div class="grid-promos">
    <a class="promo" %(aff)s>
      <span class="promo__amount">%(sym)s%(cash)s + %(fs)s FS</span>
      <h3>Welcome Package</h3>
      <p>A 100%% match on your first deposit plus %(fs)s free spins released in daily batches. 35x wagering, no code required.</p>
      <span class="btn btn--primary">Claim Now</span>
    </a>
    <a class="promo" %(aff)s>
      <span class="promo__amount">50%% up to %(sym)s400</span>
      <h3>Weekend Reload</h3>
      <p>Top up any Friday through Sunday and take half of it back as bonus funds, every single weekend.</p>
      <span class="btn btn--accent">Reload Now</span>
    </a>
  </div>
</section>

<section class="section">
  <div class="section__head">
    <div>
      <h2>Start Playing in Four Steps</h2>
      <p>From sign-up to first withdrawal.</p>
    </div>
  </div>
  <div class="steps">
%(steps)s
  </div>
  <p style="margin-top:22px">
    <a class="btn btn--primary btn--lg" %(aff)s>Register in 60 Seconds</a>
  </p>
</section>

%(doors)s

<section class="section card prose">
%(prose)s
</section>

<section class="section">
  <div class="section__head">
    <div>
      <h2>Quick Answers</h2>
      <p>The four questions new players ask most. <a href="faq.html">Full FAQ →</a></p>
    </div>
  </div>
%(faq)s
</section>
''' % dict(tagline=TAGLINE, site=SITE, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS,
           aff=AFF_ATTRS, benefits=benefits, chips=chips, steps=steps,
           games=games_grid(0), doors=door_grid(0), prose=HOME_PROSE, faq=faq)

    return page(
        title="%s Casino — %s%s Bonus + %s Free Spins | 4,000+ Slots" % (SITE, BONUS_SYM, BONUS_CASH, FREE_SPINS),
        desc="Play 4,000+ online slots and live dealer games at %s. Claim %s%s in matched funds plus %s free spins, with withdrawals processed in under an hour. 18+, T&Cs apply." % (SITE, BONUS_SYM, BONUS_CASH, FREE_SPINS),
        canonical="", active="index.html", depth=0, body=body,
        schema=schema_org() + schema_faq(HOME_FAQ))


# ============================================================================
# BONUSES
# ============================================================================
PROMOS = [
    ("Welcome Package", "%s%s + %s Free Spins" % (BONUS_SYM, BONUS_CASH, FREE_SPINS), "New players",
     "A 100%% match on your first deposit up to %s%s, plus %s free spins released in batches of 20 a day over ten days. Minimum deposit %s10. No bonus code needed — it attaches automatically."
     % (BONUS_SYM, BONUS_CASH, FREE_SPINS, BONUS_SYM), "primary"),
    ("Weekend Reload", "50%% up to %s400" % BONUS_SYM, "Every Fri–Sun",
     "Deposit any time between Friday 00:00 and Sunday 23:59 and claim half of it back as bonus funds. Claimable once per weekend, every weekend, with the same 35x terms as the welcome offer.", "accent"),
    ("Free Spins Friday", "Up to 100 Free Spins", "Weekly",
     "Deposit %s25 or more on a Friday to unlock a spin drop on that week's featured slot. The tier you land depends on the deposit size, and spins expire 72 hours after credit."
     % BONUS_SYM, "primary"),
    ("Cashback Club", "5% – 15% Weekly", "VIP tiers",
     "Every wager earns loyalty points, and points move you up the tiers. From Bronze to Diamond, weekly cashback rises from 5% to 15% of net losses — paid in cash, with no wagering attached.", "accent"),
]

BONUS_TABLE = [
    ("Welcome Match",   "100%% up to %s%s" % (BONUS_SYM, BONUS_CASH), "35x (bonus)", "%s10" % BONUS_SYM, "30 days"),
    ("Welcome Spins",   "%s free spins" % FREE_SPINS,                  "35x (winnings)", "%s10" % BONUS_SYM, "10 days"),
    ("Weekend Reload",  "50%% up to %s400" % BONUS_SYM,                "35x (bonus)", "%s20" % BONUS_SYM, "7 days"),
    ("Free Spins Friday","Up to 100 spins",                            "35x (winnings)", "%s25" % BONUS_SYM, "72 hours"),
    ("Weekly Cashback", "5%–15% of net losses",                   "None",        "—",            "—"),
]

BONUS_PROSE = '''<h2>How Wagering Requirements Actually Work</h2>
<p>A wagering requirement is the total amount you must stake before bonus funds convert into
withdrawable cash. At <strong>35x</strong>, a %(sym)s100 bonus means %(sym)s3,500 in total stakes
— not %(sym)s3,500 of your own money, but the cumulative value of every spin you place while
the bonus is active.</p>

<p>Three details decide whether a bonus is realistic or decorative, and all three are stated in
the table above:</p>

<ul>
  <li><strong>What the multiplier applies to.</strong> 35x on the bonus amount is standard.
      35x on <em>deposit plus bonus</em> is quietly double the work. Ours applies to the bonus
      only, or to free spin winnings only.</li>
  <li><strong>Game contribution.</strong> Slots contribute 100%%. Live dealer and table games
      contribute 10%%, because their house edge is far lower. Playing blackjack to clear a slots
      bonus takes ten times longer, which is exactly why the rate exists.</li>
  <li><strong>Maximum bet while wagering.</strong> %(sym)s5 per spin. Exceeding it can void the
      bonus and any winnings from it, and this is the single most common reason a withdrawal gets
      refused anywhere in this industry.</li>
</ul>

<h3>Bonus Funds Versus Cash Balance</h3>
<p>Your cash balance is always spent first, and it is always withdrawable. Bonus funds sit in a
separate pot and only become withdrawable once the requirement is met. If you request a withdrawal
while a bonus is still active, the unconverted bonus and anything won from it is forfeited — so
finish the wagering or cancel the bonus deliberately, never by accident.</p>

<h3>Should You Take the Bonus at All?</h3>
<p>Not always, and it is worth saying plainly. If you plan to deposit %(sym)s50 and play a couple
of sessions, a bonus adds obligation for little benefit and restricts your maximum bet along the
way. If you are settling in for a longer run on slots that contribute 100%%, the extra balance is
genuinely useful. Opting out is one click at the cashier, and it does not affect any future offer.</p>

<h3>One Account, One Offer</h3>
<p>Welcome offers are limited to one per person, household, IP address and payment method.
Duplicate accounts are closed and bonuses voided. Bonus abuse — low-risk betting patterns
designed purely to clear wagering, such as hedging opposite outcomes on roulette — is grounds
for forfeiture under the <a href="terms.html">terms and conditions</a>.</p>
''' % dict(sym=BONUS_SYM)


def build_bonuses():
    cards = "\n".join('''    <a class="promo" %(aff)s>
      <span class="promo__amount">%(amt)s</span>
      <h3>%(name)s</h3>
      <p><strong style="color:var(--venom)">%(who)s.</strong> %(desc)s</p>
      <span class="btn btn--%(style)s">Claim This Offer</span>
    </a>''' % dict(aff=AFF_ATTRS, amt=amt, name=name, who=who, desc=desc, style=style)
        for name, amt, who, desc, style in PROMOS)

    rows = "\n".join('''      <tr><td style="color:var(--text);font-weight:700">%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'''
                     % r for r in BONUS_TABLE)

    body = crumbs(0, [("Bonuses & Promotions", "bonuses.html")]) + '''
<h1>Bonuses &amp; Promotions at %(site)s</h1>
<p style="font-size:1.05rem;color:var(--muted);max-width:70ch">
  Every live offer, with the wagering requirement, minimum deposit and expiry window printed
  next to it. No asterisks, no terms you only discover at the cashier.
</p>

<p style="margin:22px 0 34px">
  <a class="btn btn--primary btn--lg" %(aff)s>Claim %(sym)s%(cash)s + %(fs)s Free Spins</a>
</p>

<section class="section">
  <div class="section__head"><div><h2>Current Offers</h2></div></div>
  <div class="grid-promos">
%(cards)s
  </div>
</section>

<section class="section">
  <div class="section__head">
    <div>
      <h2>Bonus Terms at a Glance</h2>
      <p>The numbers that decide whether an offer is worth taking.</p>
    </div>
  </div>
  <div class="table-wrap">
    <table>
      <caption class="sr-only">Comparison of %(site)s bonus offers, wagering requirements, minimum deposits and expiry windows</caption>
      <thead><tr><th scope="col">Offer</th><th scope="col">Value</th><th scope="col">Wagering</th><th scope="col">Min. Deposit</th><th scope="col">Expires</th></tr></thead>
      <tbody>
%(rows)s
      </tbody>
    </table>
  </div>
</section>

<section class="section card prose">
%(prose)s
</section>

<section class="section">
  <a class="promo" %(aff)s style="display:block;text-align:center">
    <span class="promo__amount">%(sym)s%(cash)s + %(fs)s Free Spins</span>
    <h3>Ready When You Are</h3>
    <p style="margin-inline:auto">Sign up, deposit from %(sym)s10, and the package credits automatically. 35x wagering. 18+. Play responsibly.</p>
    <span class="btn btn--primary btn--lg">Claim Bonus Now</span>
  </a>
</section>

%(games)s

%(doors)s
''' % dict(site=SITE, aff=AFF_ATTRS, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS,
           cards=cards, rows=rows, prose=BONUS_PROSE,
           games=games_grid(0, limit=10), doors=door_grid(0))

    return page(
        title="Casino Bonuses & Promotions — %s%s + %s Free Spins | %s" % (BONUS_SYM, BONUS_CASH, FREE_SPINS, SITE),
        desc="Every %s bonus in one place: a %s%s welcome match, %s free spins, weekend reloads and up to 15%% weekly cashback. Wagering and expiry shown for each. 18+, T&Cs apply." % (SITE, BONUS_SYM, BONUS_CASH, FREE_SPINS),
        canonical="bonuses.html", active="bonuses.html", depth=0, body=body,
        schema=schema_breadcrumb([("Home", ""), ("Bonuses & Promotions", "bonuses.html")]))


# ============================================================================
# FAQ
# ============================================================================
FAQ = [
    ("How do I create an account at %s?" % SITE,
     "Select Register, enter your email address, choose a username, password and account currency, and confirm you are over 18. The whole process takes under a minute and no documents are required at this stage. You can browse the lobby and play demo games immediately after signing up."),
    ("What is the minimum deposit?",
     "%s10, or the equivalent in your account currency, on every supported payment method. The welcome package requires a qualifying first deposit of at least %s10 to trigger." % (BONUS_SYM, BONUS_SYM)),
    ("Which payment methods are supported?",
     "Visa and Mastercard debit cards, Skrill, Neteller, Trustly instant bank transfer, standard bank transfer, and Bitcoin. Deposits are instant on every method and we do not add a processing fee — though your own bank or wallet provider may."),
    ("How long does a withdrawal take?",
     "E-wallet and cryptocurrency withdrawals are typically approved and sent within one hour. Debit card and bank transfer withdrawals take one to three working days once approved, which is banking-side time rather than casino processing. Withdrawals are paid back to the method you deposited with wherever regulations require it."),
    ("Why do I need to verify my identity?",
     "Licensing rules require every operator to confirm that players are who they say they are and are over 18. You will be asked for photo ID, a recent proof of address, and confirmation of the payment method you used. Verification is a one-time process — complete it when you sign up rather than when you first try to withdraw, and there is no delay later."),
    ("Do I need a bonus code to claim the welcome offer?",
     "No. The welcome match and free spins attach to your first qualifying deposit automatically. If a seasonal or email-only promotion ever requires a code, that code is printed on the promotion itself."),
    ("What does 35x wagering actually mean?",
     "It is the total stake volume required before bonus funds convert to withdrawable cash. A %s100 bonus at 35x requires %s3,500 in cumulative stakes. Slots contribute 100%% toward this, live dealer and table games contribute 10%%, and the maximum bet while wagering is %s5 per spin." % (BONUS_SYM, BONUS_SYM, BONUS_SYM)),
    ("Can I cancel a bonus once I have claimed it?",
     "Yes. Cancel an active bonus from the cashier at any time. Doing so forfeits the bonus funds and any winnings derived from them, but your own cash balance is untouched and remains fully withdrawable."),
    ("Are the games fair?",
     "Every slot outcome is produced by a random number generator that is tested and certified annually by an independent laboratory. Published RTP figures are set by the game studio, not the casino, and are visible in each game's info panel. Live dealer games use physical equipment streamed in real time from monitored studios."),
    ("Can I play on my phone?",
     "Yes, and there is nothing to install. The entire lobby runs in mobile Safari and Chrome, laid out for portrait orientation. Your session state, balance and any active bonus carry across devices automatically."),
    ("What limits can I set on my account?",
     "Deposit limits, loss limits, wager limits, session-time reminders, a cooling-off period from 24 hours to six weeks, and permanent self-exclusion. All are available in account settings. Tightening a limit takes effect immediately; loosening one is subject to a deliberate cooling-off delay."),
    ("What should I do if gambling stops feeling like entertainment?",
     "Use the deposit limits and cooling-off tools first — they work, and they take effect straight away. If you need more than that, BeGambleAware and Gamblers Anonymous both provide free, confidential support, and our support team can apply a permanent self-exclusion to your account on request at any time."),
]


def build_faq():
    items = "\n".join('''  <details class="faq-item">
    <summary>%s</summary>
    <div class="faq-item__body"><p>%s</p></div>
  </details>''' % (html.escape(q), html.escape(a)) for q, a in FAQ)

    body = crumbs(0, [("FAQ", "faq.html")]) + '''
<h1>Frequently Asked Questions</h1>
<p style="font-size:1.05rem;color:var(--muted);max-width:70ch">
  Accounts, deposits, withdrawals, bonus terms, fairness and player protection — answered
  directly. If yours is not here, live chat is staffed 24/7.
</p>

<section class="section" style="margin-top:28px">
%(items)s
</section>

<section class="section">
  <a class="promo" %(aff)s style="display:block;text-align:center">
    <span class="promo__amount">%(sym)s%(cash)s + %(fs)s Free Spins</span>
    <h3>Still Got Questions? Try the Demo First.</h3>
    <p style="margin-inline:auto">Nearly every slot has a free play mode. When you are ready, the welcome package is waiting.</p>
    <span class="btn btn--primary btn--lg">Register Now</span>
  </a>
</section>

%(games)s

%(doors)s
''' % dict(items=items, aff=AFF_ATTRS, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS,
           games=games_grid(0, limit=10), doors=door_grid(0))

    return page(
        title="FAQ — Deposits, Withdrawals & Bonus Terms | %s" % SITE,
        desc="Answers to the most common %s questions: minimum deposits, withdrawal times, verification, 35x wagering explained, game fairness and responsible gambling tools. 18+." % SITE,
        canonical="faq.html", active="faq.html", depth=0, body=body,
        schema=schema_faq(FAQ) + schema_breadcrumb([("Home", ""), ("FAQ", "faq.html")]))


# ============================================================================
# TERMS
# ============================================================================
TERMS_PROSE = '''<h2>1. Acceptance of These Terms</h2>
<p>By accessing %(site)s or registering an account, you agree to these terms in full. If you do not
accept them, do not use the site. We may revise these terms and will post the revised version here
with an updated effective date; continued use after that date constitutes acceptance.</p>

<h2>2. Eligibility</h2>
<ul>
  <li>You must be at least 18 years old, or the legal gambling age in your jurisdiction if it is higher.</li>
  <li>You must not be resident in a territory where online gambling is prohibited. It is your responsibility to know the law where you are.</li>
  <li>You must be acting on your own behalf, not as an agent for another person.</li>
  <li>You must not be self-excluded from this or any affiliated operator, and must not appear on any applicable exclusion register.</li>
</ul>

<h2>3. Accounts</h2>
<p>One account per person, household, shared device and IP address. Accounts must be registered in
your own legal name with accurate details. You are responsible for keeping your credentials secure
and for all activity that takes place under your login. Notify support immediately if you suspect
unauthorised access.</p>
<p>We reserve the right to suspend or close any account where information is inaccurate, where
duplicate accounts are identified, or where verification cannot be completed.</p>

<h2>4. Verification and Anti-Money-Laundering</h2>
<p>Licensing and AML obligations require identity verification. You may be asked for government
photo ID, proof of address dated within three months, and proof of ownership of the payment method
used. Withdrawals may be held until verification is complete. Providing falsified documents is
grounds for immediate closure and forfeiture of balance.</p>

<h2>5. Deposits and Withdrawals</h2>
<ul>
  <li>Minimum deposit: %(sym)s10. Minimum withdrawal: %(sym)s20.</li>
  <li>Withdrawals are returned to the original deposit method where regulation requires it.</li>
  <li>We charge no deposit or withdrawal fee. Your bank, card issuer or wallet provider may.</li>
  <li>Deposited funds must be wagered at least once before withdrawal. Depositing and immediately withdrawing without play is treated as a money-laundering risk and will be investigated.</li>
  <li>Player funds are held in accounts segregated from operating capital.</li>
</ul>

<h2>6. Bonuses and Promotions</h2>
<ul>
  <li>Welcome offers are limited to one per person, household, device, IP address and payment method.</li>
  <li>Default wagering is 35x the bonus amount, or 35x free spin winnings, unless a promotion states otherwise.</li>
  <li>Slots contribute 100%% toward wagering; live dealer and table games contribute 10%%. Some titles are excluded entirely and are listed in the cashier.</li>
  <li>Maximum bet while a bonus is active: %(sym)s5 per spin or hand. Exceeding it may void the bonus and associated winnings.</li>
  <li>Bonus funds expire 30 days after credit; free spins expire as stated on the individual promotion.</li>
  <li>Requesting a withdrawal while a bonus is active forfeits the unconverted bonus and any winnings from it.</li>
</ul>

<h2>7. Prohibited Conduct</h2>
<p>The following will result in forfeiture of bonuses and winnings and may result in account closure:</p>
<ul>
  <li>Operating multiple or duplicate accounts.</li>
  <li>Low-risk or hedged betting patterns designed solely to clear wagering requirements.</li>
  <li>Use of automated software, bots, or exploitation of a software fault.</li>
  <li>Collusion with other players, or use of another person's payment method.</li>
  <li>Chargebacks or payment disputes raised without first contacting support.</li>
</ul>

<h2>8. Game Rules, Fairness and Malfunction</h2>
<p>Outcomes are determined by a certified random number generator, independently tested annually.
Published RTP values are set by the game supplier. In the event of a malfunction, all affected
bets and payouts are void; where a game disconnects mid-round, the round is settled according to
the supplier's own rules on reconnection. Server-side records are the definitive record of play in
any dispute.</p>

<h2>9. Dormant Accounts</h2>
<p>An account with no login for 12 consecutive months is classified as dormant. A monthly
administration fee may be applied to a positive dormant balance, capped at the balance itself. We
will contact you at your registered email before any fee is applied.</p>

<h2>10. Responsible Gambling</h2>
<p>Gambling is entertainment and carries a cost. It is not a way to earn income or recover losses.
The following tools are available in your account settings and take effect immediately:</p>
<ul>
  <li><strong>Deposit, loss and wager limits</strong> — daily, weekly or monthly.</li>
  <li><strong>Session reminders</strong> — a periodic prompt showing elapsed time and net position.</li>
  <li><strong>Cooling-off</strong> — a lock from 24 hours to six weeks.</li>
  <li><strong>Self-exclusion</strong> — six months to permanent. This cannot be reversed early.</li>
</ul>
<p>Tightening a limit applies instantly. Loosening one is subject to a deliberate delay. If you are
concerned about your gambling, free and confidential support is available from BeGambleAware,
Gamblers Anonymous and GamCare.</p>

<h2>11. Privacy and Data</h2>
<p>We collect only the data required to operate your account, meet legal obligations and prevent
fraud. Data is encrypted in transit and at rest, retained for the period regulation requires, and
never sold. You may request a copy of your data or its deletion, subject to the record-keeping
obligations that apply to licensed operators.</p>

<h2>12. Affiliate Disclosure</h2>
<p>%(site)s is an independent information and comparison site. Some outbound links are affiliate
links, and we may receive a commission if you register or deposit through them. This never changes
the price you pay, the offer you receive, or the terms attached to it, and it does not influence
the factual accuracy of what is published here.</p>

<h2>13. Limitation of Liability</h2>
<p>The site is provided on an "as is" basis. To the fullest extent permitted by law, we exclude
liability for indirect or consequential loss, for loss arising from your own breach of these terms,
and for interruptions caused by circumstances outside our reasonable control. Nothing here excludes
liability that cannot lawfully be excluded.</p>

<h2>14. Complaints</h2>
<p>Contact live chat first — most issues are resolved in a single conversation. Unresolved
complaints are escalated internally and acknowledged within 24 hours, with a substantive response
within 8 working days. If you remain dissatisfied, you may refer the matter to the relevant
licensing authority or approved alternative dispute resolution provider.</p>

<h2>15. Governing Law</h2>
<p>These terms are governed by the laws of the jurisdiction in which the operating licence is held.
Nothing in this clause removes any mandatory consumer protection available to you under the law of
your own country of residence.</p>
''' % dict(site=SITE, sym=BONUS_SYM)


def build_terms():
    body = crumbs(0, [("Terms & Conditions", "terms.html")]) + '''
<h1>Terms &amp; Conditions</h1>
<p style="color:var(--muted)">Effective date: 1 January 2026 · Last reviewed: 1 January 2026</p>
<p style="font-size:1.02rem;color:var(--muted);max-width:70ch">
  Please read these terms carefully before registering or depositing. They set out the rules for
  accounts, payments, bonuses and dispute resolution, and they are binding once you create an account.
</p>

<section class="section card prose" style="margin-top:28px">
%(prose)s
</section>

<section class="section">
  <a class="promo" %(aff)s style="display:block;text-align:center">
    <span class="promo__amount">%(sym)s%(cash)s + %(fs)s Free Spins</span>
    <h3>Read and Ready to Play?</h3>
    <p style="margin-inline:auto">The welcome package applies to your first deposit from %(sym)s10. 35x wagering. 18+ only — please play responsibly.</p>
    <span class="btn btn--primary btn--lg">Register Now</span>
  </a>
</section>
''' % dict(prose=TERMS_PROSE, aff=AFF_ATTRS, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS)

    return page(
        title="Terms & Conditions | %s" % SITE,
        desc="Full %s terms and conditions covering eligibility, account rules, verification, deposits and withdrawals, bonus wagering, responsible gambling tools and complaints. 18+." % SITE,
        canonical="terms.html", active="terms.html", depth=0, body=body,
        schema=schema_breadcrumb([("Home", ""), ("Terms & Conditions", "terms.html")]))


# ============================================================================
# /en/ doorway hub + x1..x9 landings
# ============================================================================
def build_en_hub():
    body = crumbs(1, [("Guides", "en/")]) + '''
<h1>%(site)s Casino Guides</h1>
<p style="font-size:1.05rem;color:var(--muted);max-width:70ch">
  Nine focused guides covering the parts of an online casino that actually decide whether it is
  worth your deposit — bonus mechanics, payout speed, game formats and mobile play.
</p>

<p style="margin:22px 0 34px">
  <a class="btn btn--primary btn--lg" %(aff)s>Claim %(sym)s%(cash)s + %(fs)s Free Spins</a>
</p>

%(doors)s

%(games)s
''' % dict(site=SITE, aff=AFF_ATTRS, sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS,
           doors=door_grid(1), games=games_grid(1, limit=10))

    return page(
        title="Casino Guides — Bonuses, Payouts & Slot Formats | %s" % SITE,
        desc="Nine %s guides covering welcome bonuses, free spins, fast payouts, Megaways, jackpots, live casino, mobile play and VIP rewards. 18+, T&Cs apply." % SITE,
        canonical="en/", active="en/", depth=1, body=body,
        schema=schema_breadcrumb([("Home", ""), ("Guides", "en/")]))


def build_door(sl, label, kw, h1, intro, bullets):
    bl = "\n".join('''    <article class="benefit">
      <div class="benefit__ic" aria-hidden="true">✓</div>
      <p style="color:var(--text);font-weight:700;margin:0">%s</p>
    </article>''' % b for b in bullets)

    body = crumbs(2, [("Guides", "en/"), (label, "en/%s/" % sl)]) + '''
<h1>%(h1)s</h1>
<p style="font-size:1.05rem;color:var(--muted);max-width:70ch">%(intro)s</p>

<p style="margin:22px 0 30px">
  <a class="btn btn--primary btn--lg" %(aff)s>Claim %(sym)s%(cash)s + %(fs)s Free Spins</a>
</p>

<section class="section">
  <div class="grid-benefits">
%(bl)s
  </div>
</section>

<section class="section card prose">
  <h2>What to Know Before You Claim</h2>
  <p>%(intro)s The detail that matters is in the terms, not the headline, so here is the short
     version: the welcome package is <strong>%(sym)s%(cash)s plus %(fs)s free spins at 35x
     wagering</strong>, the minimum deposit is %(sym)s10, and the maximum bet while a bonus is
     active is %(sym)s5 a spin.</p>
  <p>Slots contribute 100%% toward wagering; live dealer and table games contribute 10%%. Bonus
     funds expire 30 days after credit. There is no bonus code — the offer attaches to your
     first qualifying deposit automatically. The complete rules are on the
     <a href="../../bonuses.html">bonuses page</a> and in the
     <a href="../../terms.html">terms and conditions</a>.</p>
  <h3>Is It Worth Taking?</h3>
  <p>If you are depositing small and playing briefly, a bonus adds obligation and caps your bet
     size for limited upside. If you are settling in on slots that contribute in full, the extra
     balance genuinely extends your session. Opting out is one click at the cashier and costs you
     nothing later. Either way, set a deposit limit first — it takes ten seconds and it is the
     single most effective thing you can do to keep this entertainment.</p>
  <p>New to the site? The <a href="../../faq.html">FAQ</a> covers deposits, verification and
     withdrawal times in detail.</p>
</section>

%(games)s

%(doors)s

<section class="section">
  <a class="promo" %(aff)s style="display:block;text-align:center">
    <span class="promo__amount">%(sym)s%(cash)s + %(fs)s Free Spins</span>
    <h3>Ready to Play?</h3>
    <p style="margin-inline:auto">Register in under a minute. 35x wagering. 18+ only — please play responsibly.</p>
    <span class="btn btn--primary btn--lg">Play Now</span>
  </a>
</section>
''' % dict(h1=html.escape(h1), intro=html.escape(intro), aff=AFF_ATTRS,
           sym=BONUS_SYM, cash=BONUS_CASH, fs=FREE_SPINS, bl=bl,
           games=games_grid(2, limit=10), doors=door_grid(2, exclude=sl))

    lead = intro.split(". ")[0].strip().rstrip(".")
    if len(lead) > 96:
        lead = lead[:93].rsplit(" ", 1)[0] + "…"

    return page(
        title="%s | %s" % (h1, SITE),
        desc="%s. %s%s + %s free spins, 35x wagering. 18+, T&Cs apply."
             % (lead, BONUS_SYM, BONUS_CASH, FREE_SPINS),
        canonical="en/%s/" % sl, active="en/%s/" % sl, depth=2, body=body,
        schema=schema_breadcrumb([("Home", ""), ("Guides", "en/"), (label, "en/%s/" % sl)]))


# ============================================================================
# robots.txt + sitemap.xml
# ============================================================================
def build_robots():
    return "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % DOMAIN


def build_sitemap():
    urls = [("", "1.0", "weekly"), ("bonuses.html", "0.9", "weekly"),
            ("faq.html", "0.7", "monthly"), ("terms.html", "0.3", "yearly"),
            ("en/", "0.8", "weekly")]
    urls += [("en/%s/" % sl, "0.6", "monthly") for sl, *_ in DOORS]
    items = "\n".join(
        '  <url><loc>%s/%s</loc><changefreq>%s</changefreq><priority>%s</priority></url>'
        % (DOMAIN, u, cf, pr) for u, pr, cf in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % items


# ============================================================================
# main
# ============================================================================
def main():
    made = make_assets()

    made.append(write("index.html",   build_home()))
    made.append(write("bonuses.html", build_bonuses()))
    made.append(write("faq.html",     build_faq()))
    made.append(write("terms.html",   build_terms()))
    made.append(write("en/index.html", build_en_hub()))

    for sl, label, kw, h1, intro, bullets in DOORS:
        made.append(write("en/%s/index.html" % sl, build_door(sl, label, kw, h1, intro, bullets)))

    made.append(write("robots.txt",  build_robots()))
    made.append(write("sitemap.xml", build_sitemap()))

    html_files = [m for m in made if m.endswith(".html")]
    print("Built %d files (%d HTML pages, %d assets)"
          % (len(made), len(html_files), len(made) - len(html_files)))
    for m in sorted(made):
        print("  " + m)


if __name__ == "__main__":
    main()
