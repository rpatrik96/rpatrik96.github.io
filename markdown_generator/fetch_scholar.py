#!/usr/bin/env python3
"""
Fetch recent publications from Google Scholar and save to _data/scholar_papers.yml

This script uses the scholarly library to scrape Google Scholar data.
Run this before building the Jekyll site to update the papers list.

Usage:
    pip install scholarly pyyaml free-proxy
    python fetch_scholar.py

The script will:
1. Fetch the author profile from Google Scholar
2. Get the most recent publications (default: 5)
3. Fill in detailed information for each publication (authors, venue, date)
4. Save them to ../_data/scholar_papers.yml for Jekyll to use
"""

import multiprocessing
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
MAX_RETRIES = 2
RETRY_DELAY = 5  # seconds
FETCH_TIMEOUT = 90  # seconds per attempt (proxy setup + fetch combined)

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


def _worker(author_id, num_papers, use_proxy, result_queue):
    """Run in a subprocess so it can be killed on timeout."""
    try:
        if use_proxy:
            try:
                pg = ProxyGenerator()
                success = pg.FreeProxies()
                if success:
                    scholarly.use_proxy(pg)
                    print("  Proxy configured.")
                else:
                    print("  No proxy found, trying direct.")
            except Exception as e:
                print(f"  Proxy setup failed ({e}), trying direct.")

        author = scholarly.search_author_id(author_id)
        if author is None:
            result_queue.put({"error": "Scholar returned no author data (rate-limited)"})
            return

        author = scholarly.fill(author, sections=['publications'])
        if author is None:
            result_queue.put({"error": "Scholar returned no data filling profile"})
            return

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

        result_queue.put({"papers": papers})

    except Exception as e:
        result_queue.put({"error": str(e)})


def fetch_with_timeout(author_id, num_papers, use_proxy, timeout):
    """Fetch publications in a subprocess with a hard timeout."""
    result_queue = multiprocessing.Queue()
    proc = multiprocessing.Process(
        target=_worker,
        args=(author_id, num_papers, use_proxy, result_queue),
    )
    proc.start()
    proc.join(timeout=timeout)

    if proc.is_alive():
        proc.terminate()
        proc.join(timeout=5)
        if proc.is_alive():
            proc.kill()
            proc.join()
        raise TimeoutError(f"Fetch timed out after {timeout}s")

    if result_queue.empty():
        raise RuntimeError("Worker process exited without producing results")

    result = result_queue.get_nowait()
    if "error" in result:
        raise RuntimeError(result["error"])
    return result["papers"]


def save_to_yaml(papers, output_path):
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

    # Attempt 1: with proxy, Attempt 2: without proxy
    strategies = [
        ("with proxy", True),
        ("without proxy", False),
    ]

    for attempt, (desc, use_proxy) in enumerate(strategies, 1):
        try:
            print(f"\nAttempt {attempt}/{len(strategies)} ({desc})...")
            papers = fetch_with_timeout(
                SCHOLAR_AUTHOR_ID, NUM_PAPERS, use_proxy, FETCH_TIMEOUT
            )

            if papers:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                output_path = os.path.join(script_dir, OUTPUT_FILE)
                save_to_yaml(papers, output_path)
                print("\nDone!")
                return 0
            else:
                print("No publications found.")
                return 0

        except (TimeoutError, RuntimeError) as e:
            print(f"  Failed: {e}")
            if attempt < len(strategies):
                print(f"  Retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

    print("\nAll attempts failed. Google Scholar may be rate-limiting this IP.")
    print("The existing data file will remain unchanged.")
    return 0


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    sys.exit(main())
