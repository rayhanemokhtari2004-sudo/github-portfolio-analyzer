"""GitHub Portfolio Analyzer Streamlit Dashboard Application.

Provides an interactive analytics dashboard for GitHub profiles, displaying user metadata,
repository statistics, interactive visualizations, portfolio scoring, actionable recommendations,
and export functionality (CSV and PDF).
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
import requests
import streamlit as st

from api.github_api import GitHubAPI
from services.analyzer import PortfolioAnalyzer
from utils.charts import Charts
from utils.plotly_charts import PlotlyCharts
from utils.pdf_generator import PDFReportGenerator


# ==========================================
# Page Configuration & Modern Theme Setup
# ==========================================

st.set_page_config(
    page_title="GitHub Portfolio Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Clean Custom CSS for Premium Dashboard Aesthetic
CUSTOM_CSS = """
<style>
    /* Global Font & Header Aesthetics */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Dashboard Header Banner */
    .dashboard-header {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        color: #FFFFFF;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
    .dashboard-header h1 {
        color: #FFFFFF !important;
        margin: 0 0 0.4rem 0 !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
    }
    .dashboard-header p {
        color: #C7D2FE !important;
        margin: 0 !important;
        font-size: 1.05rem !important;
    }
    
    /* Profile Hero Card */
    .profile-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    
    /* Custom Metric Cards */
    .metric-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.08);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4F46E5;
        margin-top: 0.2rem;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.35rem;
        font-weight: 700;
        color: #0F172A;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.5rem;
        margin-top: 1.8rem;
        margin-bottom: 1.2rem;
    }

    /* Custom Badges */
    .badge-public {
        background-color: #DEF7EC;
        color: #03543F;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .badge-private {
        background-color: #FDE8E8;
        color: #9B1C1C;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Footer Styling */
    .app-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.85rem;
        padding-top: 2rem;
        padding-bottom: 1rem;
        border-top: 1px solid #E2E8F0;
        margin-top: 3rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# Component Initialization & Helper Caching
# ==========================================

api = GitHubAPI()
analyzer = PortfolioAnalyzer()
charts = Charts()
plotly_charts = PlotlyCharts()
pdf_generator = PDFReportGenerator()


@st.cache_data(ttl=600, show_spinner=False)
def cached_get_user(username: str) -> Optional[Dict[str, Any]]:
    """Cached wrapper for fetching user details."""
    return api.get_user(username)


@st.cache_data(ttl=600, show_spinner=False)
def cached_get_repositories(username: str) -> List[Dict[str, Any]]:
    """Cached wrapper for fetching user repositories."""
    return api.get_repositories(username)


# ==========================================
# Sidebar Interface
# ==========================================

with st.sidebar:
    st.image("https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png", width=50)
    st.title("GitHub Analyzer")
    st.caption("Professional Portfolio Dashboard")
    st.markdown("---")

    username_input = st.text_input(
        "GitHub Username",
        placeholder="e.g. torvalds",
        help="Enter an exact GitHub username to analyze."
    )

    analyze_button = st.button(
        "🔍 Analyze Portfolio",
        type="primary",
        use_container_width=True
    )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info(
        "This tool audits GitHub profiles, calculates portfolio health metrics, "
        "generates interactive charts, and produces downloadable PDF & CSV reports."
    )


# ==========================================
# Main Dashboard Header
# ==========================================

st.markdown(
    """
    <div class="dashboard-header">
        <h1>📊 GitHub Portfolio Analyzer</h1>
        <p>Analyze any GitHub profile and discover actionable portfolio insights and metrics.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# Analysis Execution Logic
# ==========================================

if analyze_button or username_input.strip():
    clean_username = username_input.strip()

    if not clean_username:
        st.warning("⚠️ Please enter a GitHub username to begin analysis.")
        st.stop()

    with st.spinner(f"Fetching GitHub data for @{clean_username}..."):
        try:
            user = cached_get_user(clean_username)
        except requests.exceptions.ConnectionError:
            st.error("🌐 Network Error: Unable to connect to GitHub. Please check your internet connection.")
            st.stop()
        except requests.exceptions.RequestException as exc:
            st.error(f"⚠️ API Request Error: {exc}")
            st.stop()

        if not user:
            st.error(
                f"❌ GitHub user **'{clean_username}'** was not found. "
                "Please verify the username and try again."
            )
            st.stop()

        repositories = cached_get_repositories(clean_username)

    # ------------------------------------------
    # Section 1: User Profile Header
    # ------------------------------------------
    st.markdown('<div class="section-header">👤 Profile Overview</div>', unsafe_allow_html=True)

    profile_col1, profile_col2 = st.columns([1, 3])

    with profile_col1:
        st.image(
            user.get("avatar_url", "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"),
            width=160,
        )

    with profile_col2:
        st.subheader(f"{user.get('name') or user.get('login')}")
        st.markdown(f"**@{user.get('login')}**")
        if user.get("bio"):
            st.write(f"_{user.get('bio')}_")

        meta_col1, meta_col2, meta_col3 = st.columns(3)
        meta_col1.metric("Public Repositories", user.get("public_repos", 0))
        meta_col2.metric("Followers", user.get("followers", 0))
        meta_col3.metric("Following", user.get("following", 0))

    # ------------------------------------------
    # Section 2: Key Statistics
    # ------------------------------------------
    st.markdown('<div class="section-header">📊 Portfolio Statistics</div>', unsafe_allow_html=True)

    stat_col1, stat_col2, stat_col3 = st.columns(3)

    stat_col1.metric(
        "⭐ Total Stars",
        analyzer.total_stars(repositories)
    )

    stat_col2.metric(
        "🍴 Total Forks",
        analyzer.total_forks(repositories)
    )

    popular_repo = analyzer.most_popular_repository(repositories)
    if popular_repo:
        stat_col3.metric(
            "🏆 Best Repository",
            popular_repo.get("name", "N/A"),
            delta=f"{popular_repo.get('stargazers_count', 0)} stars"
        )
    else:
        stat_col3.metric("🏆 Best Repository", "N/A")

    # ------------------------------------------
    # Section 3: Interactive Visualizations
    # ------------------------------------------
    st.markdown('<div class="section-header">📈 Repository Analytics</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🌍 Programming Languages", "⭐ Repository Stars", "🍴 Repository Forks"])

    languages = analyzer.languages_used(repositories)

    # Generate Matplotlib charts in background for file compatibility
    charts.languages_chart(languages)
    charts.stars_chart(repositories)
    charts.forks_chart(repositories)

    with tab1:
        if languages:
            fig_lang = plotly_charts.languages_chart(languages)
            if fig_lang:
                st.plotly_chart(fig_lang, use_container_width=True)
            else:
                st.image("images/languages.png")
        else:
            st.info("No primary programming languages detected across public repositories.")

    with tab2:
        if repositories:
            fig_stars = plotly_charts.stars_chart(repositories)
            if fig_stars:
                st.plotly_chart(fig_stars, use_container_width=True)
            else:
                st.image("images/stars.png")
        else:
            st.info("No repositories available to display star statistics.")

    with tab3:
        if repositories:
            fig_forks = plotly_charts.forks_chart(repositories)
            if fig_forks:
                st.plotly_chart(fig_forks, use_container_width=True)
            else:
                st.image("images/forks.png")
        else:
            st.info("No repositories available to display fork statistics.")

    # ------------------------------------------
    # Section 4: Score & Recommendations
    # ------------------------------------------
    st.markdown('<div class="section-header">🏅 Portfolio Score & Recommendations</div>', unsafe_allow_html=True)

    score_col, rec_col = st.columns([1, 2])

    score = analyzer.portfolio_score(user, repositories)
    recommendations = analyzer.recommendations(user, repositories)

    with score_col:
        st.metric("Overall Score", f"{score} / 100")
        st.progress(score / 100)
        if score >= 80:
            st.caption("🟢 Status: Exceptional Portfolio")
        elif score >= 50:
            st.caption("🟡 Status: Good Portfolio (Room for Growth)")
        else:
            st.caption("🔴 Status: Needs Optimization")

    with rec_col:
        st.subheader("💡 Recommendations")
        if recommendations:
            for item in recommendations:
                st.warning(f"• {item}")
        else:
            st.success("🎉 Excellent GitHub profile! No major issues detected.")

    # ------------------------------------------
    # Section 5: Repositories Data Table
    # ------------------------------------------
    st.markdown('<div class="section-header">📂 Repositories Listing</div>', unsafe_allow_html=True)

    table_data = []
    for repo in repositories:
        table_data.append({
            "Repository": repo.get("name"),
            "Language": repo.get("language") or "N/A",
            "Stars": repo.get("stargazers_count", 0),
            "Forks": repo.get("forks_count", 0),
            "Visibility": "Private" if repo.get("private") else "Public"
        })

    df = pd.DataFrame(table_data)

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No public repositories found for this user.")

    # ------------------------------------------
    # Section 6: Data Exports (CSV & PDF)
    # ------------------------------------------
    st.markdown('<div class="section-header">📥 Export Reports</div>', unsafe_allow_html=True)

    export_col1, export_col2 = st.columns(2)

    with export_col1:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📄 Download CSV Report",
            data=csv_data,
            file_name=f"{clean_username}_repositories.csv",
            mime="text/csv",
            help="Download the repository listing table as a CSV file.",
            use_container_width=True
        )

    with export_col2:
        try:
            pdf_bytes = pdf_generator.generate_pdf(
                user=user,
                repositories=repositories,
                score=score,
                languages=languages,
                recommendations=recommendations
            )
            st.download_button(
                label="📕 Download PDF Report",
                data=pdf_bytes,
                file_name=f"{clean_username}_portfolio_report.pdf",
                mime="application/pdf",
                help="Download a complete PDF audit report.",
                use_container_width=True
            )
        except Exception as err:
            st.error(f"Could not generate PDF: {err}")

else:
    # Default State Banner when no username is submitted yet
    st.info("👆 Please enter a GitHub username in the sidebar and click **Analyze** to generate the portfolio dashboard.")

# Footer
st.markdown(
    """
    <div class="app-footer">
        GitHub Portfolio Analyzer &bull; Built with Streamlit & Python &bull; Refactored & Optimized
    </div>
    """,
    unsafe_allow_html=True
)