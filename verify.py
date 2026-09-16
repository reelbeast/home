#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reelbeast satellite — link & SEO audit.

Run:  python verify.py     (or: py verify.py)

Enforces the routing contract:
  * every OUTBOUND link is exactly the affiliate URL
  * every INTERNAL link resolves to a file that exists
  * nothing links anywhere else (except the Google Fonts stylesheet)
Plus basic SEO hygiene: title, meta description, viewport, canonical,
image alt text, and no leaked '%%' from the templates.
"""

import os, re, io, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AFF = "https://vnstrf.com/d3f4MrnT"
ALLOWED_EXTERNAL = {
    "https://fonts.googleapis.com",
    "https://fonts.gstatic.com",
}

errors, warnings = [], []


def rel_of(path):
    return os.path.relpath(path, HERE).replace("\\", "/")


def html_files():
    for root, _dirs, files in os.walk(HERE):
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(root, f)


def main():
    stats = Counter()
    pages = sorted(html_files())

    for path in pages:
        rp = rel_of(path)
        src = io.open(path, encoding="utf-8").read()
        stats["pages"] += 1

        # ---- SEO hygiene -------------------------------------------------
        if not re.search(r"<title>[^<]{10,}</title>", src):
            errors.append("%s: missing or too-short <title>" % rp)
        m = re.search(r'<meta name="description" content="([^"]+)"', src)
        if not m:
            errors.append("%s: missing meta description" % rp)
        elif not (50 <= len(m.group(1)) <= 200):
            warnings.append("%s: meta description is %d chars (aim 120-160)"
                            % (rp, len(m.group(1))))
        if 'name="viewport"' not in src:
            errors.append("%s: missing viewport meta" % rp)
        if 'rel="canonical"' not in src:
            errors.append("%s: missing canonical" % rp)
        if len(re.findall(r"<h1[ >]", src)) != 1:
            errors.append("%s: expected exactly one <h1>, found %d"
                          % (rp, len(re.findall(r"<h1[ >]", src))))
        if "%%" in src:
            errors.append("%s: leaked '%%%%' from a template string" % rp)

        # ---- images ------------------------------------------------------
        for tag in re.findall(r"<img\b[^>]*>", src):
            stats["images"] += 1
            alt = re.search(r'alt="([^"]*)"', tag)
            if not alt:
                errors.append("%s: <img> with no alt attribute" % rp)
            elif len(alt.group(1).strip()) < 8:
                warnings.append("%s: thin alt text %r" % (rp, alt.group(1)))

        # ---- links -------------------------------------------------------
        for tag in re.findall(r"<a\b[^>]*>", src):
            href = re.search(r'href="([^"]*)"', tag)
            if not href:
                errors.append("%s: <a> with no href" % rp)
                continue
            h = href.group(1)

            if h.startswith("http://") or h.startswith("https://"):
                if h == AFF:
                    stats["affiliate"] += 1
                    for token in ("nofollow", "sponsored"):
                        if token not in tag:
                            warnings.append("%s: affiliate link missing rel=%s" % (rp, token))
                    if 'target="_blank"' not in tag:
                        warnings.append("%s: affiliate link missing target=_blank" % rp)
                elif any(h.startswith(a) for a in ALLOWED_EXTERNAL):
                    stats["external_allowed"] += 1
                else:
                    errors.append("%s: UNEXPECTED external link -> %s" % (rp, h))
            elif h.startswith("#") or h.startswith("mailto:"):
                stats["anchor"] += 1
            else:
                # internal — must resolve on disk
                stats["internal"] += 1
                target = os.path.normpath(
                    os.path.join(os.path.dirname(path), h.split("#")[0]))
                if os.path.isdir(target):
                    target = os.path.join(target, "index.html")
                if not os.path.exists(target):
                    errors.append("%s: BROKEN internal link -> %s" % (rp, h))

        # ---- stylesheet links (canonical/icon links are exempt) ----------
        for tag in re.findall(r"<link\b[^>]*>", src):
            if 'rel="stylesheet"' not in tag:
                continue
            l = re.search(r'href="([^"]+)"', tag)
            if not l:
                continue
            l = l.group(1)
            if l.startswith("http"):
                if any(l.startswith(a) for a in ALLOWED_EXTERNAL):
                    stats["external_allowed"] += 1
                else:
                    errors.append("%s: unexpected external stylesheet -> %s" % (rp, l))

    # ---- report ----------------------------------------------------------
    print("=" * 66)
    print("  Reelbeast satellite — audit")
    print("=" * 66)
    print("  HTML pages          %4d" % stats["pages"])
    print("  Affiliate links     %4d   (all -> %s)" % (stats["affiliate"], AFF))
    print("  Internal nav links  %4d" % stats["internal"])
    print("  Images (with alt)   %4d" % stats["images"])
    print("  Allowed external    %4d   (Google Fonts)" % stats["external_allowed"])
    print("-" * 66)

    if errors:
        print("  ERRORS (%d):" % len(errors))
        for e in errors:
            print("    x " + e)
    else:
        print("  ERRORS: none")

    if warnings:
        print("  WARNINGS (%d):" % len(warnings))
        for w in warnings[:25]:
            print("    ! " + w)
        if len(warnings) > 25:
            print("    ... and %d more" % (len(warnings) - 25))
    else:
        print("  WARNINGS: none")

    print("=" * 66)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
