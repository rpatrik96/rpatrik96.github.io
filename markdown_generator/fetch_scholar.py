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

import yaml
import os
import sys
import time
from datetime import datetime

try:
    from scholarly import scholarly
except ImportError:
    print("Error: scholarly library not installed.")
    print("Install it with: pip install scholarly")
    sys.exit(1)

# Configuration
SCHOLAR_AUTHOR_ID = "zIT0fdIAAAAJ"  # Your Google Scholar author ID
NUM_PAPERS = 5  # Number of recent papers to display
OUTPUT_FILE = "../_data/scholar_papers.yml"

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


def parse_publication_date(bib: dict) -> str:
    """
    Parse publication date from bib entry and return in YYYY/MM format.
    Falls back to YYYY if month is not available.

    Args:
        bib: Bibliography dictionary from scholarly

    Returns:
        Date string in YYYY/MM or YYYY format
    """
    year = bib.get('pub_year', '')

    if not year:
        return ''

    # Try to get month from various possible fields
    month = None

    # Check for explicit month field
    if 'month' in bib:
        month_str = str(bib['month']).lower().strip()
        # Try to map month name to number
        if month_str in MONTH_MAP:
            month = MONTH_MAP[month_str]
        # Check if it's already a number
        elif month_str.isdigit() and 1 <= int(month_str) <= 12:
            month = month_str.zfill(2)

    # Try to extract from publication date string if present
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

    Args:
        author_id: Google Scholar author ID
        num_papers: Number of recent papers to fetch

    Returns:
        List of publication dictionaries
    """
    print(f"Fetching author profile for ID: {author_id}")

    # Search for author by ID
    author = scholarly.search_author_id(author_id)

    # Fill in the author's publication details
    author = scholarly.fill(author, sections=['publications'])

    publications = author.get('publications', [])

    # Sort by year (most recent first)
    # Publications might not have year, so we handle that
    def get_year(pub):
        bib = pub.get('bib', {})
        year = bib.get('pub_year', '0')
        try:
            return int(year)
        except (ValueError, TypeError):
            return 0

    publications = sorted(publications, key=get_year, reverse=True)

    # Take only the top N papers
    recent_pubs = publications[:num_papers]

    papers = []
    for pub in recent_pubs:
        # Fill the publication to get detailed info (authors, venue, etc.)
        try:
            filled_pub = scholarly.fill(pub)
            bib = filled_pub.get('bib', {})
        except Exception as e:
            print(f"  Warning: Could not fill publication details: {e}")
            bib = pub.get('bib', {})
            filled_pub = pub

        # Extract relevant fields
        # Get venue from multiple possible fields
        venue = bib.get('venue', '') or bib.get('journal', '') or bib.get('conference', '') or bib.get('booktitle', '')

        paper = {
            'title': bib.get('title', 'Untitled'),
            'authors': authors,
            'year': bib.get('pub_year', ''),
            'venue': venue,
            'citations': filled_pub.get('num_citations', 0),
            'url': f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={author_id}&citation_for_view={author_id}:{pub.get('author_pub_id', '').split(':')[-1] if pub.get('author_pub_id') else ''}",
        }

        # Try to get the actual paper URL if available
        if filled_pub.get('pub_url'):
            paper['paper_url'] = filled_pub.get('pub_url')

        papers.append(paper)
        print(f"  - {paper['title']} ({paper['year']}) - {venue or 'No venue'}")

    return papers


def save_to_yaml(papers: list, output_path: str):
    """Save papers list to YAML file."""
    # Ensure directory exists
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

    try:
        papers = fetch_author_publications(SCHOLAR_AUTHOR_ID, NUM_PAPERS)

        if papers:
            # Get absolute path relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, OUTPUT_FILE)
            save_to_yaml(papers, output_path)
            print("\nDone! Now rebuild your Jekyll site to see the changes.")
            return 0
        else:
            print("No publications found.")
            return 0

    except Exception as e:
        print(f"Error fetching publications: {e}")
        print("\nNote: Google Scholar may rate-limit requests.")
        print("If this persists, try again later or use a proxy.")
        # Exit gracefully for CI - don't fail the workflow
        # The existing data file will remain unchanged
        return 1


if __name__ == "__main__":
    sys.exit(main())
