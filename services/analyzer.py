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