#!/usr/bin/env python3
"""
pdf_crawl: download PDFs for papers listed in a markdown roadmap.

Flow per paper:
  1. Crossref title-search -> DOI for strict metadata validation.
  2. Try verified open-access sources by default: arXiv, eLife, bioRxiv,
     and Semantic Scholar openAccessPdf.
  3. Publisher citation_pdf_url scraping is opt-in via --allow-publisher-pdf.
  4. Fuzzy Crossref matches are reported but not downloaded by default.

Stdlib only.
"""

import argparse
import ipaddress
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

UA_API = "pdf_crawl/1.0 (mailto:{email})"
UA_DOWNLOAD = "pdf_crawl/1.0 open-access downloader"
ARTICLES = {"a", "an", "the"}
YEAR_RE = re.compile(r"\b(1[89]\d\d|20\d\d|21\d\d)\b")

CITATION_PDF_RE = re.compile(
    r'<meta\s+[^>]*name=["\']citation_pdf_url["\'][^>]*content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
CITATION_PDF_RE_ALT = re.compile(
    r'<meta\s+[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']citation_pdf_url["\']',
    re.IGNORECASE,
)


# ---------- network safety (SSRF guard) ----------

def _url_is_public(url):
    """True if url is http(s) and resolves only to public, non-internal IPs.

    Blocks file/gopher/ftp/... schemes and any host that resolves (even partly)
    to private / loopback / link-local / reserved / multicast / unspecified
    ranges (169.254.169.254, 127.0.0.1, 10/8, etc.). Threat model: the OA-API
    JSON fields and publisher citation_pdf_url values we fetch are attacker-
    influencable, so every fetched URL is checked before connect."""
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return False
    host = parsed.hostname
    if not host:
        return False
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    if not infos:
        return False
    for _fam, _typ, _proto, _canon, sockaddr in infos:
        ip = ipaddress.ip_address(sockaddr[0])
        if (ip.is_private or ip.is_loopback or ip.is_link_local
                or ip.is_reserved or ip.is_multicast or ip.is_unspecified):
            return False
    return True


class _SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Refuse to follow a redirect whose target is not a public http(s) URL."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _url_is_public(newurl):
            raise urllib.error.URLError(
                f"refusing redirect to non-public url: {newurl}"
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


# One shared opener: redirect targets are validated by _SafeRedirectHandler.
urllib.request.install_opener(urllib.request.build_opener(_SafeRedirectHandler()))


def _assert_public(url):
    """Validate an about-to-be-fetched URL before connect; raise on internal target."""
    if not _url_is_public(url):
        raise urllib.error.URLError(f"refusing non-public url: {url}")


# ---------- markdown parsing ----------

def parse_md_tables(text):
    rows = []
    state = "out"  # out | target | other
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            state = "out"
            continue
        if state == "out":
            state = "target" if ("제목" in s and "저자" in s and "저널" in s) else "other"
            continue
        if re.match(r"^\|[\s\-:|]+\|?$", s):
            continue
        if state != "target":
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 5:
            continue
        _num, title, authors, journal, notes = cells[:5]
        if title and authors:
            rows.append((title, authors, journal, notes))
    return rows


def first_author_lastname(authors):
    first = authors.split(",")[0].strip()
    if not first:
        return "unknown"
    word = first.split()[0]
    return re.sub(r"[^a-z]", "", word.lower()) or "unknown"


def first_title_word(title):
    title = re.sub(r"[*_`]", "", title)
    for word in title.split():
        clean = re.sub(r"[^A-Za-z0-9]", "", word).lower()
        if not clean or clean in ARTICLES:
            continue
        return clean
    return "untitled"


def extract_year(notes):
    m = YEAR_RE.search(notes)
    return m.group(1) if m else None


def filename_for(title, authors, year):
    return f"{first_author_lastname(authors)}_{first_title_word(title)}_{year}.pdf"


# ---------- HTTP helpers ----------

def http_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get(url, timeout=60, extra_headers=None):
    """Plain HTTP GET for declared OA URLs. No cookie jar or browser impersonation."""
    _assert_public(url)
    headers = {
        "User-Agent": UA_DOWNLOAD,
        "Accept": "application/pdf,application/octet-stream,*/*;q=0.5",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers, r.geturl()


def looks_like_pdf(body, headers):
    if body[:5].startswith(b"%PDF"):
        return True
    ct = headers.get("Content-Type") or headers.get("content-type") or ""
    return "pdf" in ct.lower()


def title_overlap(a, b):
    a_tok = set(re.sub(r"\W+", " ", a.lower()).split())
    b_tok = set(re.sub(r"\W+", " ", b.lower()).split())
    if not a_tok or not b_tok:
        return 0.0
    return len(a_tok & b_tok) / len(a_tok | b_tok)


# ---------- step 1: Crossref ----------

def parse_journal(journal_field):
    """Extract a clean journal name from a 'Journal x:y' style field."""
    s = re.sub(r"[*_`]", "", journal_field or "").strip()
    # Strip trailing volume/page info: "Nature 497:113" -> "Nature"
    s = re.split(r"\s+\d", s, 1)[0].strip()
    return s or None


def _validate_crossref(item, title, author_last, year):
    """Return (score, reasons) — score in [0,3]. >=2 means accept."""
    score = 0
    cand_title = (item.get("title") or [""])[0]
    t_overlap = title_overlap(title, cand_title)
    if t_overlap >= 0.55:
        score += 1
    # Year check
    issued = item.get("issued", {}).get("date-parts") or [[None]]
    cand_year = issued[0][0] if issued and issued[0] else None
    try:
        if cand_year and year and abs(int(cand_year) - int(year)) <= 1:
            score += 1
    except Exception:
        pass
    # Author check
    authors = item.get("author") or []
    surnames = [(a.get("family") or "").lower() for a in authors]
    surnames_norm = [re.sub(r"[^a-z]", "", s) for s in surnames]
    if any(author_last in s or s in author_last for s in surnames_norm if s):
        score += 1
    return score, t_overlap


def _crossref_query(params, email):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    headers = {"User-Agent": UA_API.format(email=email)}
    try:
        data = http_json(url, headers=headers)
    except Exception:
        return []
    return data.get("message", {}).get("items", []) or []


def crossref_doi(title, author_last, year, journal, email):
    """Multi-strategy Crossref lookup with fuzzy fallback.
    Returns (doi, matched_title, quality) where quality is:
      'strict' — validation score >=2 (passes >=2 of: title overlap, year, author)
      'fuzzy'  — best candidate, overlap >=0.35 but didn't fully validate
      None     — no usable candidate found
    """
    year_str = str(year) if year and year != "0000" else None
    base_filter = "type:journal-article"
    if year_str:
        base_filter += f",from-pub-date:{int(year_str)-1},until-pub-date:{int(year_str)+1}"

    strategies = [
        {"query.bibliographic": f"{title} {author_last}", "filter": base_filter, "rows": "5"},
        {"query.title": title, "query.author": author_last, "filter": base_filter, "rows": "5"},
        {"query.title": title, "query.container-title": journal or "", "filter": base_filter, "rows": "5"} if journal else None,
        {"query.bibliographic": f"{title} {author_last}", "filter": "type:journal-article", "rows": "5"},
        {"query.bibliographic": f"{title} {author_last}", "rows": "5"},
        # Author-only fallback for very wrong titles
        {"query.author": author_last, "query.container-title": journal or "", "filter": base_filter, "rows": "10"} if (journal and year_str) else None,
    ]
    strategies = [s for s in strategies if s]

    best_overall = None
    best_overall_score = 0
    best_overall_overlap = 0.0
    for params in strategies:
        items = _crossref_query(params, email)
        for it in items:
            score, t_overlap = _validate_crossref(it, title, author_last, year)
            if score >= 2 and t_overlap >= 0.45:
                cand_title = (it.get("title") or [""])[0]
                return it.get("DOI"), cand_title, "strict"
            # Track best so far for fuzzy fallback
            combined = score + t_overlap
            if combined > best_overall_score + best_overall_overlap:
                best_overall_score = score
                best_overall_overlap = t_overlap
                best_overall = it
        time.sleep(0.2)

    if best_overall and best_overall_overlap >= 0.35:
        cand_title = (best_overall.get("title") or [""])[0]
        return best_overall.get("DOI"), cand_title, "fuzzy"
    return None, None, None


# ---------- step 2: arXiv ----------

def arxiv_pdf(title, author_last):
    q = f'ti:"{title[:120]}" AND au:{author_last}'
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": q, "max_results": "3"}
    )
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            text = r.read().decode("utf-8", errors="ignore")
    except Exception:
        return None
    for entry in re.findall(r"<entry>(.*?)</entry>", text, flags=re.DOTALL):
        m_id = re.search(r"<id>http://arxiv\.org/abs/(\S+?)</id>", entry)
        m_t = re.search(r"<title>(.*?)</title>", entry, flags=re.DOTALL)
        if not (m_id and m_t):
            continue
        cand = re.sub(r"\s+", " ", m_t.group(1)).strip()
        if title_overlap(title, cand) >= 0.6:
            return f"https://arxiv.org/pdf/{m_id.group(1)}.pdf"
    return None


# ---------- publisher-specific fast paths ----------

def elife_pdf(doi):
    """eLife API: returns canonical PDF URL for any 10.7554/eLife.NNNNN DOI."""
    m = re.match(r"10\.7554/elife\.(\d+)", doi.lower())
    if not m:
        return None
    api_url = f"https://api.elifesciences.org/articles/{m.group(1)}"
    try:
        req = urllib.request.Request(
            api_url, headers={"Accept": "application/vnd.elife.article-vor+json"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data.get("pdf")
    except Exception:
        return None


def biorxiv_pdf(doi):
    """bioRxiv: 10.1101/... -> https://www.biorxiv.org/content/{doi}.full.pdf"""
    if not doi.startswith("10.1101/"):
        return None
    return f"https://www.biorxiv.org/content/{doi}.full.pdf"


def semantic_scholar_pdf(doi):
    """Semantic Scholar Graph API: openAccessPdf field."""
    url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{urllib.parse.quote(doi)}?fields=openAccessPdf"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = json.loads(r.read().decode("utf-8"))
        oa = data.get("openAccessPdf") or {}
        return oa.get("url")
    except Exception:
        return None


# ---------- step 3: DOI -> publisher landing -> citation_pdf_url ----------

def find_pdf_meta(html, base_url):
    for rx in (CITATION_PDF_RE, CITATION_PDF_RE_ALT):
        m = rx.search(html)
        if m:
            return urllib.parse.urljoin(base_url, m.group(1))
    return None


def publisher_pdf_via_doi(doi):
    """Opt-in publisher lookup: resolve DOI and parse citation_pdf_url."""
    landing_url = f"https://doi.org/{urllib.parse.quote(doi)}"
    try:
        body, hdrs, final = http_get(landing_url)
    except Exception:
        return None, landing_url
    if looks_like_pdf(body, hdrs):
        return final, final
    html = body.decode("utf-8", errors="ignore")
    pdf_url = find_pdf_meta(html, final)
    return pdf_url, final


# ---------- download ----------

def download_pdf(url, dest, depth=0, allow_meta=False):
    """Fetch URL and save if PDF. HTML meta recursion is opt-in."""
    if depth > 2:
        return False, "redirect chain too deep"
    try:
        _assert_public(url)
    except Exception as e:
        return False, f"unsafe url: {e}"
    try:
        body, hdrs, final = http_get(url, timeout=120)
    except Exception as e:
        return False, f"fetch error: {e}"
    if looks_like_pdf(body, hdrs):
        dest.write_bytes(body)
        return True, None
    if allow_meta:
        html = body.decode("utf-8", errors="ignore")
        next_url = find_pdf_meta(html, final)
        if next_url and next_url != url:
            return download_pdf(next_url, dest, depth=depth + 1, allow_meta=True)
    ct = hdrs.get("Content-Type") or "?"
    return False, f"not a PDF (CT={ct}; final={final[:120]})"


# ---------- main loop ----------

def process_one(title, authors, year, journal, dest, email, allow_publisher_pdf=False):
    """Return (status, detail, match_quality, matched_title).
    status in {ok, fail, skip}; match_quality in {strict, fuzzy, None}."""
    if dest.exists() and dest.stat().st_size > 1024:
        return "skip", "already on disk", None, None
    title_clean = re.sub(r"[*_`]", "", title)
    author_last = first_author_lastname(authors)
    journal_clean = parse_journal(journal)

    doi, matched_title, match_quality = crossref_doi(
        title_clean, author_last, year, journal_clean, email
    )
    time.sleep(0.3)

    # Try sources in order. Each yields a candidate URL or None.
    attempts = []  # (source_label, url) — populated lazily

    arxiv_url = arxiv_pdf(title_clean, author_last)
    time.sleep(0.3)
    if arxiv_url:
        attempts.append(("arxiv", arxiv_url, False))

    landing = None
    doi_is_strict = bool(doi and match_quality == "strict")
    if doi and match_quality == "fuzzy":
        fuzzy_note = f"fuzzy Crossref match only: {(matched_title or '?')[:100]}"
    else:
        fuzzy_note = None

    if doi_is_strict:
        eu = elife_pdf(doi)
        if eu:
            attempts.append(("elife", eu, False))
            time.sleep(0.3)

        bu = biorxiv_pdf(doi)
        if bu:
            attempts.append(("biorxiv", bu, False))

        ss = semantic_scholar_pdf(doi)
        time.sleep(0.3)
        if ss:
            attempts.append(("s2-openAccessPdf", ss, False))

        if allow_publisher_pdf:
            pub_pdf, landing = publisher_pdf_via_doi(doi)
            time.sleep(0.3)
            if pub_pdf:
                attempts.append(("publisher-opt-in", pub_pdf, True))

    if not attempts:
        if fuzzy_note:
            reason = fuzzy_note + "; not downloaded without a strict DOI match"
        else:
            reason = "no strict DOI from Crossref" if not doi else f"no OA candidates; landing: {landing}"
        return "fail", reason, match_quality, matched_title

    last_err = None
    for label, url, allow_meta in attempts:
        ok, err = download_pdf(url, dest, allow_meta=allow_meta)
        if ok:
            reported_quality = None if label == "arxiv" and match_quality == "fuzzy" else match_quality
            return "ok", f"{label}: {url[:120]}", reported_quality, matched_title
        last_err = f"{label} failed -> {err}"
        time.sleep(0.3)
    return "fail", f"all {len(attempts)} candidates failed; last: {last_err}; landing: {landing}", match_quality, matched_title


def crawl(md_path, email, dry_run=False, limit=None, allow_publisher_pdf=False, yes_large=False):
    md_path = Path(md_path).resolve()
    text = md_path.read_text(encoding="utf-8")
    rows = parse_md_tables(text)
    pdf_dir = md_path.parent / "pdf"
    if not dry_run:
        pdf_dir.mkdir(exist_ok=True)

    # Dedup by filename, preserving first-seen order
    unique = {}
    for title, authors, journal, notes in rows:
        year = extract_year(notes) or "0000"
        fname = filename_for(title, authors, year)
        if fname not in unique:
            unique[fname] = (title, authors, year, journal)

    items = list(unique.items())
    if limit:
        items = items[:limit]

    print(f"[pdf_crawl] markdown: {md_path}")
    print(f"[pdf_crawl] output:   {pdf_dir}")
    print(f"[pdf_crawl] {len(rows)} rows, {len(unique)} unique, processing {len(items)}")
    if len(items) > 30 and not dry_run and not yes_large:
        print("[pdf_crawl] refusing to process more than 30 papers without a dry run first")
        print("[pdf_crawl] rerun with --dry-run, then use --yes-large if the plan is correct")
        return
    if dry_run:
        print("[pdf_crawl] DRY RUN — no network calls.\n")
        for fname, (title, _a, _y, _j) in items:
            print(f"  - {fname}  ::  {title[:90]}")
        return

    print()
    counts = {"ok": 0, "fail": 0, "skip": 0}
    failures = []
    fuzzy_matches = []  # (fname, original_title, matched_title)
    for fname, (title, authors, year, journal) in items:
        dest = pdf_dir / fname
        if year == "0000":
            print(f"[fail] {fname}  ::  no year in 비고")
            counts["fail"] += 1
            failures.append((fname, title, "no year"))
            continue
        status, detail, match_quality, matched_title = process_one(
            title, authors, year, journal, dest, email, allow_publisher_pdf=allow_publisher_pdf
        )
        counts[status] += 1
        tag = {"ok": "[ok]  ", "fail": "[fail]", "skip": "[skip]"}[status]
        fuzzy_marker = " [FUZZY]" if match_quality == "fuzzy" and status == "ok" else ""
        print(f"{tag}{fuzzy_marker} {fname}  ::  {detail}")
        if status == "fail":
            failures.append((fname, title, detail))
        elif status == "ok" and match_quality == "fuzzy":
            fuzzy_matches.append((fname, title, matched_title))
        time.sleep(0.4)

    print()
    print(f"[pdf_crawl] done: {counts['ok']} downloaded ({len(fuzzy_matches)} fuzzy), "
          f"{counts['skip']} already on disk, {counts['fail']} not found")
    print(f"[pdf_crawl] output: {pdf_dir}")

    if fuzzy_matches:
        print(f"\n[pdf_crawl] === FUZZY MATCHES — please verify these {len(fuzzy_matches)} ===")
        print("(downloaded the closest paper found; original info in roadmap may have a typo)")
        for fname, orig, matched in fuzzy_matches:
            print(f"  - {fname}")
            print(f"      roadmap: {orig[:110]}")
            print(f"      matched: {(matched or '?')[:110]}")

    if failures:
        print(f"\n[pdf_crawl] === NOT FOUND — manual download needed ({len(failures)}) ===")
        for fname, title, reason in failures:
            print(f"  - {fname}")
            print(f"      {title[:110]}")
            print(f"      {reason}")


def main():
    ap = argparse.ArgumentParser(description="Download PDFs from a markdown literature roadmap.")
    ap.add_argument("markdown")
    ap.add_argument("--email", default=os.environ.get("PDF_CRAWL_EMAIL", "research-agent@example.com"))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--allow-publisher-pdf", action="store_true",
                    help="Opt in to DOI landing-page citation_pdf_url lookup after OA sources fail.")
    ap.add_argument("--yes-large", action="store_true",
                    help="Allow processing more than 30 papers after reviewing a dry run.")
    args = ap.parse_args()
    crawl(args.markdown, args.email, dry_run=args.dry_run, limit=args.limit,
          allow_publisher_pdf=args.allow_publisher_pdf, yes_large=args.yes_large)


if __name__ == "__main__":
    main()
