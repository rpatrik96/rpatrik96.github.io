#!/usr/bin/env python3
"""
Fetch recent publications from Google Scholar and save to _data/scholar_papers.yml

This script uses the scholarly library to scrape Google Scholar data.
Run this before building the Jekyll site to update the papers list.

Usage:
    pip install scholarly pyyaml
    python fetch_scholar.py

The script will:
1. Fetch the author profile from Google Scholar
2. Get the most recent publications (default: 5)
3. Fill in detailed information for each publication (authors, venue, date)
4. Save them to ../_data/scholar_papers.yml for Jekyll to use
"""

import os
import sys
import time
from datetime import datetime

import yaml

try:
    from scholarly import ProxyGenerator, scholarly
except ImportError:
    print("Error: scholarly library not installed.")
    print("Install it with: pip install scholarly")
    sys.exit(1)

# Configuration
SCHOLAR_AUTHOR_ID = "zIT0fdIAAAAJ"  # Your Google Scholar author ID
NUM_PAPERS = 5  # Number of recent papers to display
OUTPUT_FILE = "../_data/scholar_papers.yml"
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

# Month name to number mapping
MONTH_MAP = {
    'january': '01', 'jan': '01',
    'february': '02', 'feb': '02',
    'march': '03', 'mar': '03',
    'april': '04', 'apr': '04',
    'may': '05',
    'june': '06', 'jun': '06',
    'july': '07', 'jul': '07',
    'august': '08', 'aug': '08',
    'september': '09', 'sep': '09', 'sept': '09',
    'october': '10', 'oct': '10',
    'november': '11', 'nov': '11',
    'december': '12', 'dec': '12',
}


def setup_proxy():
    """Configure scholarly to use a free proxy to avoid rate limiting."""
    try:
        pg = ProxyGenerator()
        success = pg.FreeProxies()
        if success:
            scholarly.use_proxy(pg)
            print("Proxy configured successfully.")
            return True
        else:
            print("Warning: Could not set up proxy, proceeding without one.")
            return False
    except Exception as e:
        print(f"Warning: Proxy setup failed ({e}), proceeding without one.")
        return False


def parse_publication_date(bib: dict) -> str:
    """
    Parse publication date from bib entry and return in YYYY/MM format.
    Falls back to YYYY if month is not available.
    """
    year = bib.get('pub_year', '')

    if not year:
        return ''

    month = None

    if 'month' in bib:
        month_str = str(bib['month']).lower().strip()
        if month_str in MONTH_MAP:
            month = MONTH_MAP[month_str]
        elif month_str.isdigit() and 1 <= int(month_str) <= 12:
            month = month_str.zfill(2)

    if not month and 'publication_date' in bib:
        pub_date = str(bib['publication_date']).lower()
        for month_name, month_num in MONTH_MAP.items():
            if month_name in pub_date:
                month = month_num
                break

    if month:
        return f"{year}/{month}"
    return str(year)


def fetch_author_publications(author_id: str, num_papers: int = 5) -> list:
    """
    Fetch publications from Google Scholar for a given author ID.
    Fills in detailed information for each publication.
    """
    print(f"Fetching author profile for ID: {author_id}")

    author = scholarly.search_author_id(author_id)

    if author is None:
        raise RuntimeError("Google Scholar returned no author data (likely rate-limited)")

    author = scholarly.fill(author, sections=['publications'])

    if author is None:
        raise RuntimeError("Google Scholar returned no data when filling author profile")

    publications = author.get('publications', [])

    def get_year(pub):
        bib = pub.get('bib', {})
        year = bib.get('pub_year', '0')
        try:
            return int(year)
        except (ValueError, TypeError):
            return 0

    publications = sorted(publications, key=get_year, reverse=True)
    recent_pubs = publications[:num_papers]

    papers = []
    for pub in recent_pubs:
        try:
            filled_pub = scholarly.fill(pub)
            bib = filled_pub.get('bib', {})
        except Exception as e:
            print(f"  Warning: Could not fill publication details: {e}")
            bib = pub.get('bib', {})
            filled_pub = pub

        venue = (
            bib.get('venue', '')
            or bib.get('journal', '')
            or bib.get('conference', '')
            or bib.get('booktitle', '')
        )

        # Extract authors from bib entry
        authors = bib.get('author', '')

        paper = {
            'title': bib.get('title', 'Untitled'),
            'authors': authors,
            'year': bib.get('pub_year', ''),
            'venue': venue,
            'citations': filled_pub.get('num_citations', 0),
            'url': (
                f"https://scholar.google.com/citations?view_op=view_citation"
                f"&hl=en&user={author_id}"
                f"&citation_for_view={author_id}:"
                f"{pub.get('author_pub_id', '').split(':')[-1] if pub.get('author_pub_id') else ''}"
            ),
        }

        if filled_pub.get('pub_url'):
            paper['paper_url'] = filled_pub.get('pub_url')

        papers.append(paper)
        print(f"  - {paper['title']} ({paper['year']}) - {venue or 'No venue'}")

    return papers


def save_to_yaml(papers: list, output_path: str):
    """Save papers list to YAML file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    data = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'papers': papers
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nSaved {len(papers)} papers to {output_path}")


def main():
    print("=" * 60)
    print("Google Scholar Publication Fetcher")
    print("=" * 60)

    # Set up proxy to avoid Google Scholar rate limiting in CI
    setup_proxy()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            papers = fetch_author_publications(SCHOLAR_AUTHOR_ID, NUM_PAPERS)

            if papers:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                output_path = os.path.join(script_dir, OUTPUT_FILE)
                save_to_yaml(papers, output_path)
                print("\nDone! Now rebuild your Jekyll site to see the changes.")
                return 0
            else:
                print("No publications found.")
                return 0

        except Exception as e:
            print(f"Attempt {attempt}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

    print("\nAll attempts failed. Google Scholar may be rate-limiting this IP.")
    print("The existing data file will remain unchanged.")
    # Exit 0 so CI stays green — the data file is just unchanged
    return 0


if __name__ == "__main__":
    sys.exit(main())
