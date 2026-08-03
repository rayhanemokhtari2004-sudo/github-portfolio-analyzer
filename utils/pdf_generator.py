"""PDF Generator Utility Module.

Generates professional PDF audit reports for GitHub user portfolios using ReportLab.
Includes user metadata, avatar image, portfolio score badge, metrics breakdown,
language summary, recommendations, repository table, and generation date.
"""

from datetime import datetime
import io
from typing import Any, Dict, List, Optional
import requests

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class PDFReportGenerator:
    """Utility class for generating structured PDF portfolio reports."""

    def __init__(self) -> None:
        """Initialize ReportLab styles."""
        self.styles = getSampleStyleSheet()

        # Custom Palette
        self.primary_color = colors.HexColor("#4F46E5")  # Indigo
        self.secondary_color = colors.HexColor("#0EA5E9")  # Sky Blue
        self.text_dark = colors.HexColor("#0F172A")  # Slate 900
        self.text_muted = colors.HexColor("#64748B")  # Slate 500
        self.bg_light = colors.HexColor("#F8FAFC")  # Slate 50

        # Custom Paragraph Styles
        self.title_style = ParagraphStyle(
            "DocTitle",
            parent=self.styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=self.primary_color,
            spaceAfter=4,
        )

        self.subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            textColor=self.text_muted,
            spaceAfter=12,
        )

        self.h2_style = ParagraphStyle(
            "SectionH2",
            parent=self.styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=self.text_dark,
            spaceBefore=14,
            spaceAfter=6,
        )

        self.body_style = ParagraphStyle(
            "BodyDark",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=self.text_dark,
        )

        self.body_muted = ParagraphStyle(
            "BodyMuted",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=self.text_muted,
        )

        self.table_header_style = ParagraphStyle(
            "TableHeader",
            parent=self.styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=11,
            textColor=colors.white,
        )

        self.table_cell_style = ParagraphStyle(
            "TableCell",
            parent=self.styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=self.text_dark,
        )

    def generate_pdf(
        self,
        user: Dict[str, Any],
        repositories: List[Dict[str, Any]],
        score: int,
        languages: Dict[str, int],
        recommendations: List[str],
    ) -> bytes:
        """Generate PDF report bytes for a given GitHub profile.

        Args:
            user: GitHub user metadata dictionary.
            repositories: List of repository dictionaries.
            score: Calculated portfolio score (0-100).
            languages: Language frequency mapping.
            recommendations: List of profile recommendations.

        Returns:
            Bytes representing the generated PDF file.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        story = []

        # Header Section
        story.append(Paragraph("GitHub Portfolio Report", self.title_style))
        gen_date = datetime.now().strftime("%B %d, %Y - %H:%M")
        story.append(Paragraph(f"Generated on {gen_date}", self.subtitle_style))
        story.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=colors.HexColor("#E2E8F0"),
                spaceAfter=15,
            )
        )

        # Profile Card Section
        avatar_img = None
        avatar_url = user.get("avatar_url")
        if avatar_url:
            try:
                resp = requests.get(avatar_url, timeout=5)
                if resp.status_code == 200:
                    img_data = io.BytesIO(resp.content)
                    avatar_img = Image(img_data, width=70, height=70)
            except Exception:
                avatar_img = None

        username = user.get("login", "Unknown")
        name = user.get("name") or "N/A"
        bio = user.get("bio") or "No bio provided."

        user_info_text = f"""
        <b>Name:</b> {name}<br/>
        <b>Username:</b> @{username}<br/>
        <b>Bio:</b> {bio}<br/>
        <b>Public Repositories:</b> {user.get('public_repos', 0)} | 
        <b>Followers:</b> {user.get('followers', 0)} | 
        <b>Following:</b> {user.get('following', 0)}
        """

        profile_paragraph = Paragraph(user_info_text, self.body_style)

        if avatar_img:
            profile_table_data = [[avatar_img, profile_paragraph]]
            col_widths = [80, 460]
        else:
            profile_table_data = [[profile_paragraph]]
            col_widths = [540]

        profile_table = Table(profile_table_data, colWidths=col_widths)
        profile_table.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), self.bg_light),
                ("PADDING", (0, 0), (-1, -1), 10),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ])
        )
        story.append(profile_table)
        story.append(Spacer(1, 15))

        # Executive Metrics Summary
        story.append(Paragraph("Key Metrics Summary", self.h2_style))

        total_stars = sum(r.get("stargazers_count", 0) for r in (repositories or []))
        total_forks = sum(r.get("forks_count", 0) for r in (repositories or []))

        metrics_data = [
            [
                Paragraph("<b>Portfolio Score</b>", self.table_header_style),
                Paragraph("<b>Total Stars</b>", self.table_header_style),
                Paragraph("<b>Total Forks</b>", self.table_header_style),
                Paragraph("<b>Public Repos</b>", self.table_header_style),
            ],
            [
                Paragraph(f"<b>{score} / 100</b>", self.table_cell_style),
                Paragraph(f"⭐ {total_stars}", self.table_cell_style),
                Paragraph(f"🍴 {total_forks}", self.table_cell_style),
                Paragraph(f"📂 {user.get('public_repos', 0)}", self.table_cell_style),
            ],
        ]
        metrics_table = Table(metrics_data, colWidths=[135, 135, 135, 135])
        metrics_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), self.primary_color),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BACKGROUND", (0, 1), (-1, 1), self.bg_light),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ])
        )
        story.append(metrics_table)
        story.append(Spacer(1, 15))

        # Languages & Recommendations Section
        if languages or recommendations:
            story.append(Paragraph("Languages & Recommendations", self.h2_style))

            lang_str = (
                ", ".join(
                    [f"{lang} ({count})" for lang, count in languages.items()]
                )
                if languages
                else "No languages detected."
            )
            lang_p = Paragraph(
                f"<b>Languages Used:</b> {lang_str}", self.body_style
            )
            story.append(lang_p)
            story.append(Spacer(1, 8))

            if recommendations:
                story.append(
                    Paragraph(
                        "<b>Profile Recommendations:</b>", self.body_style
                    )
                )
                for rec in recommendations:
                    story.append(
                        Paragraph(
                            f"• {rec}",
                            ParagraphStyle(
                                "RecItem",
                                parent=self.body_style,
                                leftIndent=12,
                                textColor=colors.HexColor("#C2410C"),
                            ),
                        )
                    )
            else:
                story.append(
                    Paragraph(
                        "✓ <b>Profile status:</b> Excellent GitHub profile with no major action items!",
                        ParagraphStyle(
                            "RecSuccess",
                            parent=self.body_style,
                            textColor=colors.HexColor("#15803D"),
                        ),
                    )
                )

            story.append(Spacer(1, 15))

        # Repositories Table
        story.append(Paragraph("Repository Details", self.h2_style))

        if repositories:
            repo_table_data = [
                [
                    Paragraph("<b>Repository</b>", self.table_header_style),
                    Paragraph("<b>Language</b>", self.table_header_style),
                    Paragraph("<b>Stars</b>", self.table_header_style),
                    Paragraph("<b>Forks</b>", self.table_header_style),
                    Paragraph("<b>Visibility</b>", self.table_header_style),
                ]
            ]

            for repo in repositories:
                name_p = Paragraph(
                    repo.get("name", "N/A"), self.table_cell_style
                )
                lang_p = Paragraph(
                    repo.get("language") or "N/A", self.table_cell_style
                )
                stars_p = Paragraph(
                    str(repo.get("stargazers_count", 0)), self.table_cell_style
                )
                forks_p = Paragraph(
                    str(repo.get("forks_count", 0)), self.table_cell_style
                )
                vis_p = Paragraph(
                    "Private" if repo.get("private") else "Public",
                    self.table_cell_style,
                )

                repo_table_data.append(
                    [name_p, lang_p, stars_p, forks_p, vis_p]
                )

            repo_table = Table(
                repo_table_data, colWidths=[180, 110, 75, 75, 100]
            )
            repo_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), self.secondary_color),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, self.bg_light]),
                    ("PADDING", (0, 0), (-1, -1), 6),
                ])
            )
            story.append(repo_table)
        else:
            story.append(
                Paragraph("No public repositories found.", self.body_muted)
            )

        # Footer
        story.append(Spacer(1, 20))
        story.append(
            HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.HexColor("#CBD5E1"),
                spaceAfter=10,
            )
        )
        story.append(
            Paragraph(
                "Generated by GitHub Portfolio Analyzer | Confidential & Proprietary",
                self.body_muted,
            )
        )

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
