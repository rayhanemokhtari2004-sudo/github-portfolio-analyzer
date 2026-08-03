"""GitHub API Integration Module.

Provides standard methods to interact with GitHub's REST API for fetching
user profile metadata and repository details with error handling.
"""

from typing import Any, Dict, List, Optional
import requests


class GitHubAPI:
    """Client for interacting with the public GitHub REST API."""

    BASE_URL = "https://api.github.com/users"

    def __init__(self, token: Optional[str] = None) -> None:
        """Initialize GitHubAPI client with optional authorization token.

        Args:
            token: Optional GitHub Personal Access Token for higher rate limits.
        """
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Portfolio-Analyzer/1.0"
        })
        if token:
            self.session.headers.update({"Authorization": f"token {token}"})

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Fetch GitHub user profile metadata by username.

        Args:
            username: The GitHub username to search for.

        Returns:
            Dict containing GitHub user metadata if found, or None if invalid/failed.
        """
        if not username or not username.strip():
            return None

        url = f"{self.BASE_URL}/{username.strip()}"
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except requests.RequestException:
            return None

    def get_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Fetch all public repositories for a given GitHub username.

        Args:
            username: The GitHub username to search for.

        Returns:
            List of repository dictionaries.
        """
        if not username or not username.strip():
            return []

        url = f"{self.BASE_URL}/{username.strip()}/repos"
        params = {"per_page": 100, "sort": "updated"}
        try:
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data if isinstance(data, list) else []
            return []
        except requests.RequestException:
            return []