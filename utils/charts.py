"""Matplotlib Charts Generator Module.

Provides static Matplotlib chart generation functions for saving profile
insights as image artifacts.
"""

import os
from typing import Any, Dict, List
import matplotlib.pyplot as plt


class Charts:
    """Utility class for generating static Matplotlib visualizations."""

    # Modern professional color palette
    PALETTE = [
        "#6366F1", "#3B82F6", "#14B8A6", "#10B981", "#F59E0B",
        "#EC4899", "#8B5CF6", "#64748B", "#06B6D4", "#F97316"
    ]

    def __init__(self) -> None:
        """Ensure images directory exists and set default plot aesthetics."""
        os.makedirs("images", exist_ok=True)
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    def languages_chart(self, languages: Dict[str, int]) -> None:
        """Generate pie chart for programming language distribution.

        Args:
            languages: Dictionary mapping language names to repository counts.
        """
        if not languages:
            return

        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        colors = self.PALETTE[:len(languages)] if len(languages) <= len(self.PALETTE) else self.PALETTE * (len(languages) // len(self.PALETTE) + 1)

        wedges, texts, autotexts = ax.pie(
            languages.values(),
            labels=languages.keys(),
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            textprops={"fontsize": 10, "color": "#1E293B"},
            wedgeprops={"edgecolor": "#FFFFFF", "linewidth": 1.5}
        )

        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_weight("bold")

        ax.set_title("Programming Languages Used", fontsize=14, pad=15, weight="bold", color="#0F172A")
        plt.tight_layout()
        plt.savefig("images/languages.png", bbox_inches="tight", transparent=False)
        plt.close(fig)

    def stars_chart(self, repositories: List[Dict[str, Any]]) -> None:
        """Generate bar chart for top repositories by stargazers count.

        Args:
            repositories: List of repository dictionaries.
        """
        if not repositories:
            return

        sorted_repos = sorted(
            repositories,
            key=lambda repo: repo.get("stargazers_count", 0),
            reverse=True
        )[:10]

        names = [repo.get("name", "Unknown") for repo in sorted_repos]
        stars = [repo.get("stargazers_count", 0) for repo in sorted_repos]

        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        bars = ax.bar(names, stars, color="#6366F1", edgecolor="#4F46E5", linewidth=1, width=0.6)
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#334155",
                weight="bold"
            )

        ax.set_title("Top Repositories by Stars", fontsize=14, pad=15, weight="bold", color="#0F172A")
        ax.set_xlabel("Repositories", fontsize=11, labelpad=10, color="#475569")
        ax.set_ylabel("Stars", fontsize=11, labelpad=10, color="#475569")
        ax.tick_params(colors="#475569", labelsize=10)
        plt.xticks(rotation=35, ha="right")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E2E8F0")
        ax.spines["bottom"].set_color("#E2E8F0")

        plt.tight_layout()
        plt.savefig("images/stars.png", bbox_inches="tight", transparent=False)
        plt.close(fig)

    def forks_chart(self, repositories: List[Dict[str, Any]]) -> None:
        """Generate bar chart for top repositories by forks count.

        Args:
            repositories: List of repository dictionaries.
        """
        if not repositories:
            return

        sorted_repos = sorted(
            repositories,
            key=lambda repo: repo.get("forks_count", 0),
            reverse=True
        )[:10]

        names = [repo.get("name", "Unknown") for repo in sorted_repos]
        forks = [repo.get("forks_count", 0) for repo in sorted_repos]

        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        fig.patch.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")

        bars = ax.bar(names, forks, color="#0EA5E9", edgecolor="#0284C7", linewidth=1, width=0.6)

        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#334155",
                weight="bold"
            )

        ax.set_title("Top Repositories by Forks", fontsize=14, pad=15, weight="bold", color="#0F172A")
        ax.set_xlabel("Repositories", fontsize=11, labelpad=10, color="#475569")
        ax.set_ylabel("Forks", fontsize=11, labelpad=10, color="#475569")
        ax.tick_params(colors="#475569", labelsize=10)
        plt.xticks(rotation=35, ha="right")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color("#E2E8F0")
        ax.spines["bottom"].set_color("#E2E8F0")

        plt.tight_layout()
        plt.savefig("images/forks.png", bbox_inches="tight", transparent=False)
        plt.close(fig)