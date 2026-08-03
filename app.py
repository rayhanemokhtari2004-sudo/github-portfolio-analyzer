import streamlit as st
import pandas as pd

from api.github_api import GitHubAPI
from services.analyzer import PortfolioAnalyzer


# Initialisation


api = GitHubAPI()
analyzer = PortfolioAnalyzer()

st.set_page_config(
    page_title="GitHub Portfolio Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GitHub Portfolio Analyzer")
st.write("Analyze any public GitHub profile.")

username = st.text_input("GitHub Username")


# Analyse


if st.button("Analyze"):

    if username.strip() == "":
        st.warning("Please enter a GitHub username.")
        st.stop()

    user = api.get_user(username)

    if not user:
        st.error("GitHub user not found.")
        st.stop()

    repositories = api.get_repositories(username)

   
    # Profile
   

    st.header("👤 Profile")

    st.write(f"**Name:** {user.get('name')}")
    st.write(f"**Login:** {user.get('login')}")
    st.write(f"**Bio:** {user.get('bio')}")

    col1, col2, col3 = st.columns(3)

    col1.metric("Repositories", user["public_repos"])
    col2.metric("Followers", user["followers"])
    col3.metric("Following", user["following"])

  
    # Statistics
  

    st.header("📊 Statistics")

    col1, col2 = st.columns(2)

    col1.metric(
        "⭐ Total Stars",
        analyzer.total_stars(repositories)
    )

    col2.metric(
        "🍴 Total Forks",
        analyzer.total_forks(repositories)
    )

    popular = analyzer.most_popular_repository(repositories)

    if popular:
        st.success(
            f"🏆 Most Popular Repository : {popular['name']}"
        )

    
    # Languages
    

    st.header("💻 Languages")

    languages = analyzer.languages_used(repositories)

    if languages:
        st.bar_chart(languages)
    else:
        st.info("No language information available.")

   
    # Repository Table
   

    st.header("📂 Repositories")

    repo_data = []

    for repo in repositories:

        repo_data.append(
            {
                "Repository": repo["name"],
                "Language": repo["language"],
                "Stars": repo["stargazers_count"],
                "Forks": repo["forks_count"],
            }
        )

    df = pd.DataFrame(repo_data)

    st.dataframe(
        df,
        use_container_width=True
    )

    
    # Repository Details
    

    st.header("📋 Repository Details")

    for repo in repositories:

        with st.expander(repo["name"]):

            st.write(f"**Description:** {repo['description']}")
            st.write(f"**Language:** {repo['language']}")
            st.write(f"**Stars:** ⭐ {repo['stargazers_count']}")
            st.write(f"**Forks:** 🍴 {repo['forks_count']}")
            st.write(f"**Default Branch:** {repo['default_branch']}")
            st.write(f"**Created At:** {repo['created_at']}")
            st.write(f"**Updated At:** {repo['updated_at']}")
            st.write(f"**Repository URL:** {repo['html_url']}")

    st.success("Analysis completed successfully!")