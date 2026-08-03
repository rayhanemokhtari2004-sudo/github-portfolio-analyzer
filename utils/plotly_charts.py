import plotly.express as px


class PlotlyCharts:

    def languages_chart(self, languages):

        if not languages:
            return None

        fig = px.pie(
            values=list(languages.values()),
            names=list(languages.keys()),
            title="Programming Languages Used"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        return fig


    def stars_chart(self, repositories):

        if not repositories:
            return None

        repositories = sorted(
            repositories,
            key=lambda repo: repo["stargazers_count"],
            reverse=True
        )

        names = [
            repo["name"]
            for repo in repositories[:10]
        ]

        stars = [
            repo["stargazers_count"]
            for repo in repositories[:10]
        ]

        fig = px.bar(
            x=names,
            y=stars,
            title="Top 10 Repositories by Stars",
            labels={
                "x": "Repository",
                "y": "Stars"
            },
            text=stars
        )

        fig.update_traces(
            textposition="outside"
        )

        return fig


    def forks_chart(self, repositories):

        if not repositories:
            return None

        repositories = sorted(
            repositories,
            key=lambda repo: repo["forks_count"],
            reverse=True
        )

        names = [
            repo["name"]
            for repo in repositories[:10]
        ]

        forks = [
            repo["forks_count"]
            for repo in repositories[:10]
        ]

        fig = px.bar(
            x=names,
            y=forks,
            title="Top 10 Repositories by Forks",
            labels={
                "x": "Repository",
                "y": "Forks"
            },
            text=forks
        )

        fig.update_traces(
            textposition="outside"
        )

        return fig