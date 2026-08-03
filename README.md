# 📊 GitHub Portfolio Analyzer

A modern, professional Python and **Streamlit** dashboard designed to analyze public GitHub profiles, evaluate portfolio health, visualize key repository metrics, and generate executive CSV and PDF reports.

---

## 🌟 Key Features

* **Profile Overview**: Displays avatar, bio, follower count, following count, and public repository counts.
* **Portfolio Metrics**: Calculates aggregate star count, fork count, and identifies the user's top-performing repository.
* **Portfolio Scoring Algorithm**: Evaluates profile quality on a 0–100 scale using repository count, star counts, follower engagement, and description completeness.
* **Actionable Recommendations**: Automatically highlights profile optimization opportunities.
* **Interactive & Static Visualizations**: Interactive Plotly charts (Language breakdown donut chart, Stars bar chart, Forks bar chart) alongside Matplotlib image exports.
* **CSV Export**: One-click download of all repository details encoded in UTF-8 format (`<username>_repositories.csv`).
* **Professional PDF Export**: Generates a PDF audit report featuring user details, avatar image, executive metrics summary, recommendations, and structured repository tables (`<username>_portfolio_report.pdf`).
* **Robust Error Handling**: Friendly error banners for missing usernames, 404 non-existent users, API rate limits, and network connection drops.
* **Performance Caching**: Uses Streamlit `@st.cache_data` caching to minimize redundant GitHub API calls.

---

## 🏗️ Project Architecture

```
github-portfolio-analyzer/
│
├── app.py                  # Main Streamlit web application & UI dashboard
├── main.py                 # CLI interface for command-line execution
├── requirements.txt        # Python package dependencies
├── README.md               # Project documentation
│
├── api/
│   └── github_api.py       # GitHub REST API client & session handler
│
├── services/
│   └── analyzer.py         # Business logic for portfolio scoring & analytics
│
├── utils/
│   ├── charts.py           # Matplotlib static chart generator
│   ├── plotly_charts.py    # Plotly interactive chart generator
│   └── pdf_generator.py    # ReportLab PDF report generation engine
│
└── images/                 # Saved chart image artifacts
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites

Ensure you have Python 3.9+ installed.

### 2. Installation

Clone the repository and install the required dependencies:

```bash
cd github-portfolio-analyzer
pip install -r requirements.txt
```

### 3. Run the Web Application

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

### 4. Run CLI Mode (Optional)

Alternatively, run the analyzer directly in your terminal:

```bash
python main.py
```

---

## 🛠️ Technologies Used

* **Frontend & Dashboard**: Streamlit, Custom CSS
* **Data Processing**: Pandas
* **API Integration**: Requests (GitHub REST API v3)
* **Visualization**: Plotly Express, Matplotlib
* **PDF Report Generation**: ReportLab
