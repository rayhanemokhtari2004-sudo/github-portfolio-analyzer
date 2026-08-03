class PortfolioAnalyzer:

    def total_repositories(self, repositories):
        return len(repositories)

    def total_stars(self, repositories):
        return sum(
            repo["stargazers_count"]
            for repo in repositories
        )

    def total_forks(self, repositories):
        return sum(
            repo["forks_count"]
            for repo in repositories
        )

    def most_popular_repository(self, repositories):
        if not repositories:
            return None

        return max(
            repositories,
            key=lambda repo: repo["stargazers_count"]
        )

    def languages_used(self, repositories):
        languages = {}

        for repo in repositories:
            language = repo["language"]

            if language:
                if language in languages:
                    languages[language] += 1
                else:
                    languages[language] = 1

        return languages

    def portfolio_score(self, user, repositories):
        score = 0

        # Nombre de dépôts publics (max 30 points)
        score += min(user["public_repos"] * 2, 30)

        # Nombre de followers (max 20 points)
        score += min(user["followers"], 20)

        # Nombre total d'étoiles (max 30 points)
        score += min(self.total_stars(repositories), 30)

        # Dépôts ayant une description (max 20 points)
        described = 0

        for repo in repositories:
            if repo["description"]:
                described += 1

        score += min(described * 2, 20)

        return score

    def recommendations(self, user, repositories):

        recommendations = []

        if user["public_repos"] < 5:
            recommendations.append(
                "Create more public repositories."
            )

        if user["followers"] < 10:
            recommendations.append(
                "Increase your GitHub visibility."
            )

        if self.total_stars(repositories) < 10:
            recommendations.append(
                "Work on projects that attract stars."
            )

        missing_description = False

        for repo in repositories:
            if not repo["description"]:
                missing_description = True
                break

        if missing_description:
            recommendations.append(
                "Add descriptions to all repositories."
            )

        return recommendations