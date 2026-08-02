import matplotlib.pyplot as plt


class Charts:

    def languages_chart(self, languages):

        plt.figure(figsize=(8, 8))

        plt.pie(
            languages.values(),
            labels=languages.keys(),
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Languages Used")

        plt.savefig("images/languages.png")

        plt.close()

    def stars_chart(self, repositories):

        names = []
        stars = []

        for repo in repositories:
            names.append(repo["name"])
            stars.append(repo["stargazers_count"])

        plt.figure(figsize=(10, 5))

        plt.bar(names, stars)

        plt.title("Stars per Repository")
        plt.xlabel("Repositories")
        plt.ylabel("Stars")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig("images/stars.png")

        plt.close()