#!/usr/bin/env python3
"""
Fetch recent publications from OpenAlex and save to _data/scholar_papers.yml

Uses the OpenAlex API (free, no auth, no rate-limit issues) to fetch
publication data. Replaces the previous Google Scholar scraping approach
which was unreliable in CI due to IP blocking.

Usage:
    pip install pyyaml requests
    python fetch_scholar.py
"""

import os
import re
import sys
import unicodedata
from datetime import datetime

import requests
import yaml

# Configuration
OPENALEX_AUTHOR_ID = "A5034660028"  # OpenAlex author ID
OPENALEX_ORCID = "0000-0001-9861-0293"  # OpenAlex splits one person across profiles
NUM_PAPERS = 6  # Number of recent papers to display
OUTPUT_FILE = "../_data/scholar_papers.yml"
BIB_URL = (  # His own CV bibliography is the source of truth for venues
    "https://raw.githubusercontent.com/rpatrik96/CV/main/publications.bib"
)
OPENALEX_EMAIL = "reizinger@tue.mpg.de"  # Polite pool for faster responses

API_BASE = "https://api.openalex.org"
CROSSREF_BASE = "https://api.crossref.org/works"

# Shown when no peer-reviewed venue can be established for a work
PREPRINT_VENUE = "arXiv preprint"


def normalize_title(title: str) -> str:
    """Key for matching the preprint and the published copy of the same paper."""
    stripped = "".join(c if c.isalnum() or c.isspace() else " " for c in title.lower())
    return " ".join(stripped.split())


ENTRY_RE = re.compile(r"@(\w+)\s*\{", re.M)

# Long official names as they appear in the .bib, mapped to what a homepage
# line can carry. Display only - the venue itself always comes from the .bib.
VENUE_ABBREVIATIONS = [
    ("international conference on machine learning", "ICML"),
    ("international conference on learning representations", "ICLR"),
    ("uncertainty in artificial intelligence", "UAI"),
    ("artificial intelligence and statistics", "AISTATS"),
    ("neural information processing systems", "NeurIPS"),
    ("association for computational linguistics", "ACL"),
    ("empirical methods in natural language processing", "EMNLP"),
    ("transactions on machine learning research", "TMLR"),
]


# Combining marks, so {\'e} comes back as an accented letter rather than a gap
ACCENTS = {
    "'": "\u0301", '"': "\u0308", "`": "\u0300",
    "^": "\u0302", "~": "\u0303", "=": "\u0304", ".": "\u0307",
}

# Commands that stand for a character; anything else is markup and just goes
TEXT_COMMANDS = {
    "textquoteright": "'", "textquoteleft": "'",
    "textendash": "\u2013", "textemdash": "\u2014",
    "ss": "ss", "&": "&",
}


def strip_latex(text: str) -> str:
    """Render the LaTeX a .bib carries as the plain text the page displays."""
    text = re.sub(r"\\color\s*\{[^}]*\}", "", text)  # drop the command AND its argument

    def accent(match):
        return unicodedata.normalize("NFC", match.group(2) + ACCENTS[match.group(1)])

    text = re.sub(r"\\(['\"`^~=.])\{?([a-zA-Z])\}?", accent, text)
    for command, char in TEXT_COMMANDS.items():
        text = text.replace("\\" + command, char)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = text.replace("{", "").replace("}", "").replace("\\", "")
    return " ".join(text.split())


def read_braced(text: str, open_at: int) -> tuple:
    """Read one brace-balanced group, so nested {{...}} survives intact."""
    depth = 0
    for i in range(open_at, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[open_at + 1 : i], i + 1
    return "", len(text)


def parse_bib(text: str) -> list:
    """Minimal BibTeX reader: entry type plus the fields we display."""
    entries = []
    for match in ENTRY_RE.finditer(text):
        body, _ = read_braced(text, match.end() - 1)
        entry = {"type": match.group(1).lower()}
        for field in ("title", "booktitle", "journal", "year", "author", "url"):
            found = re.search(r"\b" + field + r"\s*=\s*", body)
            if not found:
                continue
            rest = body[found.end() :].lstrip()
            if rest.startswith("{"):
                value, _ = read_braced(body, body.index("{", found.end()))
            else:
                value = rest.split(",")[0]
            entry[field] = strip_latex(value).strip('"')
        if entry.get("title"):
            entries.append(entry)
    return entries


def shorten_venue(name: str) -> str:
    """Abbreviate the venues everyone knows by acronym; leave the rest alone."""
    low = name.lower()
    for needle, abbreviation in VENUE_ABBREVIATIONS:
        if needle in low:
            if "position paper" in low:
                return f"{abbreviation} Position Paper Track"
            if "workshop" in low:
                return f"{abbreviation} Workshop"
            return abbreviation
    return name


def load_bib_venues(url: str) -> dict:
    """Venue and year per title, read from his CV bibliography."""
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"Warning: could not read {url} ({exc}); falling back to OpenAlex")
        return {}

    venues = {}
    for entry in parse_bib(resp.text):
        container = entry.get("booktitle") or entry.get("journal") or ""
        year = entry.get("year", "")
        record = {
            "venue": PREPRINT_VENUE if entry["type"] == "misc" else shorten_venue(container),
            "year": int(year) if year.isdigit() else None,
            "title": entry["title"],
            "authors": entry.get("author", ""),
            "paper_url": entry.get("url", ""),
        }
        key = normalize_title(entry["title"])
        venues[key] = record
        # His position papers are titled "Position: ..." in the .bib; OpenAlex
        # indexes them without the prefix, so register both spellings.
        if key.startswith("position "):
            venues.setdefault(key[len("position ") :], record)

    print(f"Read {len(venues)} venues from the CV bibliography")
    return venues


def fetch_author_ids(orcid: str, fallback_id: str) -> list:
    """All OpenAlex author profiles for one ORCID (they get split over time)."""
    try:
        resp = requests.get(
            f"{API_BASE}/authors",
            params={"filter": f"orcid:{orcid}", "select": "id", "mailto": OPENALEX_EMAIL},
            timeout=30,
        )
        resp.raise_for_status()
        ids = [a["id"].rsplit("/", 1)[-1] for a in resp.json().get("results", [])]
    except Exception as e:
        print(f"  Could not resolve ORCID {orcid}: {e}")
        ids = []

    if fallback_id not in ids:
        ids.append(fallback_id)
    return ids


def is_preprint_venue(venue: str) -> bool:
    """True when a venue string carries no peer-reviewed information."""
    return not venue or venue == PREPRINT_VENUE


def extract_venue(work: dict) -> str:
    """Venue of the published copy, ignoring preprint repositories.

    OpenAlex stores the arXiv copy as a location whose source type is
    'repository'; reading primary_location blindly returns 'arXiv (Cornell
    University)' even when a journal or proceedings location is present.
    """
    locations = [work.get("primary_location")] + list(work.get("locations") or [])

    for location in locations:
        source = (location or {}).get("source") or {}
        name = source.get("display_name") or ""
        if name and source.get("type") != "repository":
            return name

    return ""


def crossref_venue(doi: str) -> str:
    """Venue from Crossref, for published records whose OpenAlex source is null.

    OpenAlex carries ACL Anthology, NeurIPS proceedings and IEEE records with
    `primary_location.source: null`, so the venue has to come from the DOI.
    """
    doi_suffix = doi.split("doi.org/", 1)[-1]

    try:
        resp = requests.get(
            f"{CROSSREF_BASE}/{doi_suffix}",
            params={"mailto": OPENALEX_EMAIL},
            timeout=30,
        )
        resp.raise_for_status()
        message = resp.json().get("message", {})
    except Exception as e:
        print(f"  Crossref lookup failed for {doi_suffix}: {e}")
        return ""

    container = message.get("container-title") or []
    if container:
        return container[0]
    return (message.get("event") or {}).get("name", "")


def fetch_publications(author_id: str, num_papers: int) -> list:
    """Fetch recent publications from OpenAlex, deduplicated by title."""
    author_ids = fetch_author_ids(OPENALEX_ORCID, author_id)
    print(f"Fetching publications for OpenAlex author(s): {', '.join(author_ids)}")

    bib_venues = load_bib_venues(BIB_URL)

    # Fetch extra to account for duplicates (preprint + published versions)
    fetch_count = num_papers * 4

    url = f"{API_BASE}/works"
    params = {
        "filter": f"author.id:{'|'.join(author_ids)}",
        "sort": "publication_year:desc,cited_by_count:desc",
        "per_page": fetch_count,
        "select": "id,title,publication_year,publication_date,type,primary_location,locations,cited_by_count,authorships,doi",
        "mailto": OPENALEX_EMAIL,
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    by_title: dict[str, dict] = {}
    # A .bib record is registered under more than one spelling of its title,
    # so track the records themselves, not their keys.
    matched_bib: set[int] = set()
    pub_dates: dict[str, str] = {}
    papers = []

    for work in data.get("results", []):
        title = work.get("title", "Untitled")
        title_key = normalize_title(title)

        # Extract authors
        author_names = []
        for authorship in work.get("authorships", []):
            name = authorship.get("author", {}).get("display_name", "")
            if name:
                author_names.append(name)
        authors = " and ".join(author_names)

        # Extract venue: his CV bibliography first, then the published
        # location, then Crossref for records OpenAlex has no source for.
        primary = work.get("primary_location") or {}
        doi = work.get("doi")
        is_arxiv_doi = bool(doi) and "10.48550/arxiv." in doi.lower()

        bib_entry = bib_venues.get(title_key) or {}
        if bib_entry:
            matched_bib.add(id(bib_entry))
        venue = bib_entry.get("venue") or extract_venue(work)
        if not venue and doi and not is_arxiv_doi:
            venue = crossref_venue(doi)
        if not venue and (work.get("type") == "preprint" or is_arxiv_doi):
            venue = PREPRINT_VENUE

        # OpenAlex dates a work by the copy it holds, which for a paper indexed
        # only as a preprint is the year it was posted, not the year it appeared.
        year = bib_entry.get("year") or work.get("publication_year", "")

        # Build paper URL from DOI or landing page
        landing = primary.get("landing_page_url") or ""
        paper_url = ""
        if doi:
            paper_url = doi if doi.startswith("http") else f"https://doi.org/{doi}"
            # Convert arxiv DOI redirects to direct arxiv links
            if "10.48550/arxiv." in paper_url.lower():
                arxiv_id = paper_url.rsplit("arxiv.", 1)[-1]
                paper_url = f"https://arxiv.org/abs/{arxiv_id}"
        elif landing:
            paper_url = landing

        openalex_id = work.get("id", "")

        paper = {
            "title": title,
            "authors": authors,
            "year": year,
            "venue": venue,
            "citations": work.get("cited_by_count", 0),
            "url": openalex_id,
        }

        if paper_url:
            paper["paper_url"] = paper_url

        # OpenAlex keeps the preprint and the published version as separate
        # works: merge them so the published venue and the higher citation
        # count survive, whichever copy the API returns first.
        existing = by_title.get(title_key)
        if existing is not None:
            existing["citations"] = max(existing["citations"], paper["citations"])
            if is_preprint_venue(existing["venue"]) and not is_preprint_venue(venue):
                existing["venue"] = venue
                if paper_url:
                    existing["paper_url"] = paper_url
            continue

        pub_dates[title_key] = work.get("publication_date") or ""

        by_title[title_key] = paper
        papers.append(paper)

    # OpenAlex only indexes what has a DOI, so a paper at ICML, ICLR, UAI or
    # TMLR is invisible to it. Emit those straight from the bibliography.
    for key, record in bib_venues.items():
        if id(record) in matched_bib or key in by_title:
            continue
        if not record["year"] or not record["authors"]:
            continue
        matched_bib.add(id(record))
        paper = {
            "title": record["title"],
            "authors": record["authors"],
            "year": record["year"],
            "venue": record["venue"],
            "citations": 0,
            "url": record["paper_url"],
        }
        if record["paper_url"]:
            paper["paper_url"] = record["paper_url"]
        by_title[key] = paper
        papers.append(paper)

    # OpenAlex ties on cited_by_count:desc are arbitrary, so a batch of
    # uncited papers from the same year shuffles between runs. Order them
    # here instead: peer-reviewed venues first, then by publication date.
    papers.sort(
        key=lambda p: (
            p["year"] or 0,
            0 if is_preprint_venue(p["venue"]) else 1,
            pub_dates.get(normalize_title(p["title"]), ""),
            p["citations"],
        ),
        reverse=True,
    )

    papers = papers[:num_papers]
    for paper in papers:
        print(f"  - {paper['title']} ({paper['year']}) - {paper['venue'] or 'No venue'}")

    return papers


def save_to_yaml(papers: list, output_path: str):
    """Save papers list to YAML file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "papers": papers,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nSaved {len(papers)} papers to {output_path}")


def main():
    print("=" * 60)
    print("OpenAlex Publication Fetcher")
    print("=" * 60)

    try:
        papers = fetch_publications(OPENALEX_AUTHOR_ID, NUM_PAPERS)

        if papers:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, OUTPUT_FILE)
            save_to_yaml(papers, output_path)
            print("\nDone!")
            return 0
        else:
            print("No publications found.")
            return 0

    except Exception as e:
        print(f"Error fetching publications: {e}")
        print("The existing data file will remain unchanged.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
