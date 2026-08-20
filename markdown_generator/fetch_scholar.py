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
import sys
from datetime import datetime

import requests
import yaml

# Configuration
OPENALEX_AUTHOR_ID = "A5034660028"  # OpenAlex author ID
OPENALEX_ORCID = "0000-0001-9861-0293"  # OpenAlex splits one person across profiles
NUM_PAPERS = 6  # Number of recent papers to display
OUTPUT_FILE = "../_data/scholar_papers.yml"
OVERRIDES_FILE = "../_data/venue_overrides.yml"  # Hand-verified venues
OPENALEX_EMAIL = "reizinger@tue.mpg.de"  # Polite pool for faster responses

API_BASE = "https://api.openalex.org"
CROSSREF_BASE = "https://api.crossref.org/works"

# Shown when no peer-reviewed venue can be established for a work
PREPRINT_VENUE = "arXiv preprint"


def normalize_title(title: str) -> str:
    """Key for matching the preprint and the published copy of the same paper."""
    stripped = "".join(c if c.isalnum() or c.isspace() else " " for c in title.lower())
    return " ".join(stripped.split())


def load_venue_overrides(path: str) -> dict:
    """Hand-verified venues for papers OpenAlex has no usable source for."""
    if not os.path.exists(path):
        return {}

    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    overrides = {}
    for entry in data.get("overrides", []):
        title = entry.get("title")
        venue = entry.get("venue")
        if title and venue:
            overrides[normalize_title(title)] = venue

    print(f"Loaded {len(overrides)} venue overrides")
    return overrides


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

    script_dir = os.path.dirname(os.path.abspath(__file__))
    overrides = load_venue_overrides(os.path.join(script_dir, OVERRIDES_FILE))

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

        # Extract venue: hand-verified override, then the published location,
        # then Crossref for published records OpenAlex has no source for.
        primary = work.get("primary_location") or {}
        doi = work.get("doi")
        is_arxiv_doi = bool(doi) and "10.48550/arxiv." in doi.lower()

        venue = overrides.get(title_key) or extract_venue(work)
        if not venue and doi and not is_arxiv_doi:
            venue = crossref_venue(doi)
        if not venue and (work.get("type") == "preprint" or is_arxiv_doi):
            venue = PREPRINT_VENUE

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
            "year": work.get("publication_year", ""),
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
