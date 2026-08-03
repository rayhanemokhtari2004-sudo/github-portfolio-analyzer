"""Portfolio Analyzer Service Module.

Calculates key metrics, portfolio scores, language statistics, and tailored
recommendations based on a user's GitHub profile and public repositories.
"""

from typing import Any, Dict, List, Optional


class PortfolioAnalyzer:
    """Service class for calculating metrics and scoring GitHub portfolios."""

    def total_repositories(self, repositories: List[Dict[str, Any]]) -> int:
        """Calculate the total number of repositories.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            Total count of repositories.
        """
        return len(repositories) if repositories else 0

    def total_stars(self, repositories: List[Dict[str, Any]]) -> int:
        """Calculate total stars across all repositories.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            Sum of stargazers count.
        """
        if not repositories:
            return 0
        return sum(repo.get("stargazers_count", 0) for repo in repositories)

    def total_forks(self, repositories: List[Dict[str, Any]]) -> int:
        """Calculate total forks across all repositories.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            Sum of forks count.
        """
        if not repositories:
            return 0
        return sum(repo.get("forks_count", 0) for repo in repositories)

    def most_popular_repository(
        self, repositories: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Identify the repository with the highest star count.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            The repository dict with max stars, or None if list is empty.
        """
        if not repositories:
            return None
        return max(repositories, key=lambda repo: repo.get("stargazers_count", 0))

    def languages_used(self, repositories: List[Dict[str, Any]]) -> Dict[str, int]:
        """Aggregate primary programming languages used across repositories.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            Dictionary mapping language name to frequency count.
        """
        languages: Dict[str, int] = {}
        if not repositories:
            return languages

        for repo in repositories:
            language = repo.get("language")
            if language:
                languages[language] = languages.get(language, 0) + 1

        return languages

    def portfolio_score(
        self, user: Dict[str, Any], repositories: List[Dict[str, Any]]
    ) -> int:
        """Calculate a portfolio score out of 100 based on profile metrics.

        Scoring Rules:
        - Public Repositories: 2 points per repo (max 30 pts)
        - Followers: 1 point per follower (max 20 pts)
        - Total Stars: 1 point per star (max 30 pts)
        - Described Repositories: 2 points per described repo (max 20 pts)

        Args:
            user: GitHub user dictionary.
            repositories: List of repository dictionaries.

        Returns:
            Calculated score between 0 and 100.
        """
        if not user:
            return 0

        score = 0
        repos_count = user.get("public_repos", 0)
        followers_count = user.get("followers", 0)

        # Public repositories (max 30 points)
        score += min(repos_count * 2, 30)

        # Followers count (max 20 points)
        score += min(followers_count, 20)

        # Total stars (max 30 points)
        score += min(self.total_stars(repositories), 30)

        # Repositories with descriptions (max 20 points)
        described_count = sum(
            1 for repo in (repositories or []) if repo.get("description")
        )
        score += min(described_count * 2, 20)

        return score

    def recommendations(
        self, user: Dict[str, Any], repositories: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate improvement recommendations for the user's GitHub profile.

        Args:
            user: GitHub user dictionary.
            repositories: List of repository dictionaries.

        Returns:
            List of recommendation string advice.
        """
        recs: List[str] = []
        if not user:
            return recs

        if user.get("public_repos", 0) < 5:
            recs.append("Create more public repositories.")

        if user.get("followers", 0) < 10:
            recs.append("Increase your GitHub visibility.")

        if self.total_stars(repositories) < 10:
            recs.append("Work on projects that attract stars.")

        missing_description = any(
            not repo.get("description") for repo in (repositories or [])
        )
        if missing_description:
            recs.append("Add descriptions to all repositories.")

        return recs