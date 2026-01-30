#!/usr/bin/env python3
"""
Fetch recent public repositories from GitHub and save to _data/github_projects.yml

This script uses the GitHub API (no authentication needed for public data).
Run this before building the Jekyll site to update the projects list.

Usage:
    pip install requests pyyaml
    python fetch_github.py

The script will:
1. Fetch the user's public repositories from GitHub
2. Sort by most recently updated
3. Save them to ../_data/github_projects.yml for Jekyll to use
"""

import os
import sys
from datetime import datetime

import requests
import yaml

# Configuration
GITHUB_USERNAME = "rpatrik96"
NUM_REPOS = 6  # Number of recent repos to display
OUTPUT_FILE = "../_data/github_projects.yml"

# GitHub API endpoint (no auth needed for public repos)
API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"


def fetch_github_repos(username: str, num_repos: int = 6) -> list:
    """
    Fetch public repositories from GitHub for a given username.
    Sorted by most recently updated.

    Args:
        username: GitHub username
        num_repos: Number of repos to fetch

    Returns:
        List of repository dictionaries
    """
    print(f"Fetching repositories for GitHub user: {username}")

    params = {
        "sort": "updated",
        "direction": "desc",
        "per_page": num_repos,
        "type": "owner",  # Only repos owned by user, not forks
    }

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Jekyll-GitHub-Fetcher",
    }

    response = requests.get(API_URL, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    repos_data = response.json()

    repos = []
    for repo in repos_data:
        # Skip forks
        if repo.get("fork", False):
            continue

        repo_info = {
            "name": repo["name"],
            "description": repo.get("description") or "",
            "url": repo["html_url"],
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language") or "",
            "updated_at": repo.get("updated_at", "")[:10],  # YYYY-MM-DD
            "topics": repo.get("topics", []),
        }

        repos.append(repo_info)
        print(f"  - {repo_info['name']} ({repo_info['language'] or 'No language'}) - {repo_info['stars']} stars")

    return repos[:num_repos]


def save_to_yaml(repos: list, output_path: str):
    """Save repos list to YAML file."""
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    data = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "github_url": f"https://github.com/{GITHUB_USERNAME}",
        "repos": repos,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nSaved {len(repos)} repositories to {output_path}")


def main():
    print("=" * 60)
    print("GitHub Repository Fetcher")
    print("=" * 60)

    try:
        repos = fetch_github_repos(GITHUB_USERNAME, NUM_REPOS)

        if repos:
            # Get absolute path relative to this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, OUTPUT_FILE)
            save_to_yaml(repos, output_path)
            print("\nDone! Now rebuild your Jekyll site to see the changes.")
            return 0
        else:
            print("No repositories found.")
            return 0

    except requests.exceptions.RequestException as e:
        print(f"Error fetching repositories: {e}")
        print("\nNote: GitHub API may rate-limit requests (60/hour unauthenticated).")
        print("If this persists, try again later.")
        # Exit gracefully for CI - don't fail the workflow
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
