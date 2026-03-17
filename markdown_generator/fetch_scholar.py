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
NUM_PAPERS = 5  # Number of recent papers to display
OUTPUT_FILE = "../_data/scholar_papers.yml"
OPENALEX_EMAIL = "reizinger@tue.mpg.de"  # Polite pool for faster responses

API_BASE = "https://api.openalex.org"


def fetch_publications(author_id: str, num_papers: int) -> list:
    """Fetch recent publications from OpenAlex, deduplicated by title."""
    print(f"Fetching publications for OpenAlex author: {author_id}")

    # Fetch extra to account for duplicates (preprint + published versions)
    fetch_count = num_papers * 4

    url = f"{API_BASE}/works"
    params = {
        "filter": f"author.id:{author_id}",
        "sort": "publication_year:desc,cited_by_count:desc",
        "per_page": fetch_count,
        "select": "id,title,publication_year,primary_location,cited_by_count,authorships,doi",
        "mailto": OPENALEX_EMAIL,
    }

    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    seen_titles: set[str] = set()
    papers = []

    for work in data.get("results", []):
        title = work.get("title", "Untitled")

        # Deduplicate by normalized title (OpenAlex has separate entries
        # for preprints and published versions)
        title_key = title.lower().strip()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)

        # Extract authors
        author_names = []
        for authorship in work.get("authorships", []):
            name = authorship.get("author", {}).get("display_name", "")
            if name:
                author_names.append(name)
        authors = " and ".join(author_names)

        # Extract venue
        primary = work.get("primary_location") or {}
        source = primary.get("source") or {}
        venue = source.get("display_name", "")

        # Build paper URL from DOI or landing page
        doi = work.get("doi")
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

        papers.append(paper)
        print(f"  - {paper['title']} ({paper['year']}) - {venue or 'No venue'}")

        if len(papers) >= num_papers:
            break

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
