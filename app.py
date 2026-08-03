import streamlit as st
import pandas as pd

from api.github_api import GitHubAPI
from services.analyzer import PortfolioAnalyzer
from utils.charts import Charts


# ==========================
# Initialization
# ==========================

api = GitHubAPI()
analyzer = PortfolioAnalyzer()
charts = Charts()


# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="GitHub Portfolio Analyzer",
    page_icon="📊",
    layout="wide"
)


# ==========================
# Sidebar
# ==========================

st.sidebar.title(
    "GitHub Portfolio Analyzer"
)

username = st.sidebar.text_input(
    "GitHub Username"
)

analyze = st.sidebar.button(
    "Analyze"
)


# ==========================
# Header
# ==========================

st.title(
    "GitHub Portfolio Analyzer"
)

st.write(
    "Analyze any GitHub profile and discover portfolio statistics."
)



# ==========================
# Analysis
# ==========================

if analyze:


    if username == "":

        st.warning(
            "Please enter a GitHub username."
        )

        st.stop()



    # ======================
    # Get GitHub Data
    # ======================

    user = api.get_user(
        username
    )


    if not user:

        st.error(
            "GitHub user not found."
        )

        st.stop()



    repositories = api.get_repositories(
        username
    )



    # ======================
    # Profile
    # ======================

    st.header(
        "👤 Profile"
    )


    col1, col2 = st.columns(
        [1, 3]
    )


    with col1:

        st.image(
            user["avatar_url"],
            width=170
        )


    with col2:

        st.subheader(
            user["login"]
        )


        if user.get("name"):

            st.write(
                user["name"]
            )


        if user.get("bio"):

            st.write(
                user["bio"]
            )


        st.write(
            f"Public repositories : {user['public_repos']}"
        )

        st.write(
            f"Followers : {user['followers']}"
        )

        st.write(
            f"Following : {user['following']}"
        )



    # ======================
    # Statistics
    # ======================

    st.header(
        "📊 Statistics"
    )


    col1, col2, col3 = st.columns(
        3
    )


    col1.metric(
        "⭐ Stars",
        analyzer.total_stars(
            repositories
        )
    )


    col2.metric(
        "🍴 Forks",
        analyzer.total_forks(
            repositories
        )
    )


    popular = analyzer.most_popular_repository(
        repositories
    )


    if popular:

        col3.metric(
            "🏆 Best Repository",
            popular["name"]
        )



    # ======================
    # Languages Chart
    # ======================

    st.header(
        "🌍 Programming Languages"
    )


    languages = analyzer.languages_used(
        repositories
    )


    if languages:


        charts.languages_chart(
            languages
        )


        st.image(
            "images/languages.png"
        )


    else:

        st.info(
            "No language detected."
        )



    # ======================
    # Stars Chart
    # ======================

    st.header(
        "⭐ Repository Stars"
    )


    charts.stars_chart(
        repositories
    )


    st.image(
        "images/stars.png"
    )



    # ======================
    # Forks Chart
    # ======================

    st.header(
        "🍴 Repository Forks"
    )


    charts.forks_chart(
        repositories
    )


    st.image(
        "images/forks.png"
    )



    # ======================
    # Portfolio Score
    # ======================

    st.header(
        "🏅 Portfolio Score"
    )


    score = analyzer.portfolio_score(
        user,
        repositories
    )


    st.metric(
        "Score",
        f"{score}/100"
    )


    st.progress(
        score / 100
    )



    # ======================
    # Recommendations
    # ======================

    st.header(
        "💡 Recommendations"
    )


    recommendations = analyzer.recommendations(
        user,
        repositories
    )


    if recommendations:


        for item in recommendations:

            st.warning(
                item
            )


    else:

        st.success(
            "Excellent GitHub profile!"
        )



    # ======================
    # Repository Table
    # ======================

    st.header(
        "📂 Repositories"
    )


    data = []


    for repo in repositories:


        data.append({

            "Repository": repo["name"],

            "Language": repo["language"],

            "Stars": repo["stargazers_count"],

            "Forks": repo["forks_count"],

            "Visibility":
                "Private"
                if repo["private"]
                else "Public"

        })



    df = pd.DataFrame(
        data
    )


    st.dataframe(
        df,
        use_container_width=True
    )