# GitHub Portfolio Analyzer

## Présentation

GitHub Portfolio Analyzer est une application développée en **Python** avec **Streamlit** permettant d'analyser un profil GitHub public. Elle récupère les données via l'API GitHub, génère des statistiques, calcule un score de portfolio et propose des visualisations interactives ainsi que des exports au format CSV et PDF.

---

## Fonctionnalités

- Analyse d'un profil GitHub public
- Récupération des informations utilisateur
- Analyse des dépôts
- Calcul d'un score de portfolio
- Répartition des langages de programmation
- Graphiques interactifs avec Plotly
- Graphiques statistiques avec Matplotlib
- Export des données en CSV
- Génération d'un rapport PDF
- Interface moderne avec Streamlit
- Gestion des erreurs (utilisateur introuvable, limite API, erreurs réseau)

---


## Architecture du projet

```text
github-portfolio-analyzer/
│
├── api/
│   └── github_api.py
├── services/
│   └── analyzer.py
├── utils/
│   ├── charts.py
│   ├── plotly_charts.py
│   └── pdf_generator.py
├── assets/
├── app.py
├── requirements.txt
└── README.md
```

---

## Technologies

- Python
- Streamlit
- GitHub REST API
- Requests
- Pandas
- Plotly
- Matplotlib
- ReportLab

---

## Installation

```bash
git clone https://github.com/rayhanemokhtari2004-sudo/github-portfolio-analyzer.git

cd github-portfolio-analyzer

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py
```

---

## Utilisation

1. Lancez l'application.
2. Saisissez un nom d'utilisateur GitHub.
3. Cliquez sur **Analyser**.
4. Consultez les statistiques et les graphiques.
5. Téléchargez les résultats au format CSV ou PDF.

---

## Calcul du score

Le score du portfolio est calculé à partir de plusieurs indicateurs, notamment :

- Nombre de dépôts
- Nombre d'étoiles
- Nombre de forks
- Nombre d'abonnés
- Diversité des langages
- Activité globale du profil

---

## Exports

### CSV

- Dépôts
- Langages
- Étoiles
- Forks
- Visibilité
- URL

### PDF

- Informations du profil
- Statistiques
- Score du portfolio
- Répartition des langages
- Top dépôts
- Date de génération

---


