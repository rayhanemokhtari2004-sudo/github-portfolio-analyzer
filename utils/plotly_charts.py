"""Plotly Interactive Charts Generator Module.

Provides responsive, interactive Plotly chart objects for direct display within
the Streamlit dashboard interface.
"""

from typing import Any, Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go


class PlotlyCharts:
    """Utility class for building interactive Plotly visualizations."""

    # Curated modern color palette
    PALETTE = [
        "#6366F1", "#3B82F6", "#14B8A6", "#10B981", "#F59E0B",
        "#EC4899", "#8B5CF6", "#64748B", "#06B6D4", "#F97316"
    ]

    def languages_chart(self, languages: Dict[str, int]) -> Optional[go.Figure]:
        """Build interactive pie/donut chart for programming languages.

        Args:
            languages: Dictionary mapping language names to counts.

        Returns:
            Plotly Figure object or None if data is empty.
        """
        if not languages:
            return None

        fig = px.pie(
            values=list(languages.values()),
            names=list(languages.keys()),
            title="Programming Languages Distribution",
            color_discrete_sequence=self.PALETTE,
            hole=0.45
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>Repositories: %{value}<br>Share: %{percent}<extra></extra>",
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )

        fig.update_layout(
            margin=dict(t=50, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=13),
            title_font=dict(size=16, family="Inter, sans-serif")
        )

        return fig

    def stars_chart(self, repositories: List[Dict[str, Any]]) -> Optional[go.Figure]:
        """Build interactive bar chart for top repositories by stars.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            Plotly Figure object or None if data is empty.
        """
        if not repositories:
            return None

        sorted_repos = sorted(
            repositories,
            key=lambda repo: repo.get("stargazers_count", 0),
            reverse=True
        )[:10]

        names = [repo.get("name", "Unknown") for repo in sorted_repos]
        stars = [repo.get("stargazers_count", 0) for repo in sorted_repos]
        languages = [repo.get("language") or "N/A" for repo in sorted_repos]

        fig = px.bar(
            x=names,
            y=stars,
            title="Top 10 Repositories by Stars",
            labels={"x": "Repository Name", "y": "Star Count"},
            text=stars,
            color_discrete_sequence=["#6366F1"]
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Stars: %{y}<extra></extra>",
            marker=dict(line=dict(color="#4F46E5", width=1))
        )

        fig.update_layout(
            margin=dict(t=50, b=40, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=16, family="Inter, sans-serif"),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)", title=None)
        )

        return fig

    def forks_chart(self, repositories: List[Dict[str, Any]]) -> Optional[go.Figure]:
        """Build interactive bar chart for top repositories by forks.

        Args:
            repositories: List of repository dictionaries.

        Returns:
            Plotly Figure object or None if data is empty.
        """
        if not repositories:
            return None

        sorted_repos = sorted(
            repositories,
            key=lambda repo: repo.get("forks_count", 0),
            reverse=True
        )[:10]

        names = [repo.get("name", "Unknown") for repo in sorted_repos]
        forks = [repo.get("forks_count", 0) for repo in sorted_repos]

        fig = px.bar(
            x=names,
            y=forks,
            title="Top 10 Repositories by Forks",
            labels={"x": "Repository Name", "y": "Fork Count"},
            text=forks,
            color_discrete_sequence=["#0EA5E9"]
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Forks: %{y}<extra></extra>",
            marker=dict(line=dict(color="#0284C7", width=1))
        )

        fig.update_layout(
            margin=dict(t=50, b=40, l=20, r=20),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", size=12),
            title_font=dict(size=16, family="Inter, sans-serif"),
            xaxis=dict(showgrid=False, title=None),
            yaxis=dict(showgrid=True, gridcolor="rgba(148, 163, 184, 0.2)", title=None)
        )

        return fig