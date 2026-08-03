import os
import matplotlib.pyplot as plt


class Charts:

    def __init__(self):
        os.makedirs("images", exist_ok=True)


    def languages_chart(self, languages):

        if not languages:
            return

        plt.figure(figsize=(8, 8))

        plt.pie(
            languages.values(),
            labels=languages.keys(),
            autopct="%1.1f%%",
            startangle=90
        )

        plt.title("Programming Languages Used")

        plt.tight_layout()

        plt.savefig(
            "images/languages.png"
        )

        plt.close()



    def stars_chart(self, repositories):

        if not repositories:
            return

        names = []
        stars = []


        for repo in repositories[:10]:

            names.append(
                repo["name"]
            )

            stars.append(
                repo["stargazers_count"]
            )


        plt.figure(figsize=(10, 5))


        plt.bar(
            names,
            stars
        )


        plt.title(
            "Top Repositories by Stars"
        )

        plt.xlabel(
            "Repositories"
        )

        plt.ylabel(
            "Stars"
        )


        plt.xticks(
            rotation=45,
            ha="right"
        )


        plt.tight_layout()


        plt.savefig(
            "images/stars.png"
        )


        plt.close()



    def forks_chart(self, repositories):

        if not repositories:
            return


        names = []
        forks = []


        for repo in repositories[:10]:

            names.append(
                repo["name"]
            )

            forks.append(
                repo["forks_count"]
            )


        plt.figure(figsize=(10, 5))


        plt.bar(
            names,
            forks
        )


        plt.title(
            "Top Repositories by Forks"
        )

        plt.xlabel(
            "Repositories"
        )

        plt.ylabel(
            "Forks"
        )


        plt.xticks(
            rotation=45,
            ha="right"
        )


        plt.tight_layout()


        plt.savefig(
            "images/forks.png"
        )


        plt.close()