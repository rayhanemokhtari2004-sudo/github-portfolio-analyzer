# GitHub Portfolio Analyzer

## Description

GitHub Portfolio Analyzer est une application développée en "Python" avec "Streamlit"permettant d'analyser un profil GitHub public à l'aide de l'API REST GitHub.

L'application récupère les informations d'un utilisateur, analyse ses dépôts publics, calcule un score de portfolio, génère des statistiques détaillées, crée des visualisations interactives et permet l'export des résultats aux formats CSV et PDF. Les résultats peuvent être exportés aux formats "CSV" et "PDF".

---

## Fonctionnalités

### Analyse du profil

- Analyse d'un profil GitHub public
- Récupération des informations utilisateur
- Analyse complète des dépôts
- Calcul d'un score de portfolio
- Classement des dépôts les plus populaires

### Statistiques

- Nombre de dépôts publics
- Nombre total d'étoiles
- Nombre total de forks
- Nombre de followers
- Langage principal
- Répartition des langages
- Activité globale du profil

### Visualisation

- Graphiques interactifs avec Plotly
- Graphiques statistiques avec Matplotlib

### Export

- Export des données au format CSV
- Génération d'un rapport PDF

### Gestion des erreurs

- Utilisateur GitHub introuvable
- Limite de requêtes de l'API GitHub
- Erreurs réseau
- Réponses API invalides

---

## Architecture

```text
github-portfolio-analyzer/
│
├── api/
│   └── github_api.py
│
├── services/
│   └── analyzer.py
│
├── utils/
│   ├── charts.py
│   ├── plotly_charts.py
│   └── pdf_generator.py
│
├── images/
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

### Description des dossiers

| Dossier | Description |
|----------|-------------|
| **api** | Communication avec l'API GitHub |
| **services** | Analyse des données et calcul du score |
| **utils** | Génération des graphiques et du rapport PDF |
| **images** | Images utilisées par l'application et le README |

---

## Technologies utilisées

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

### Cloner le projet

```bash
git clone https://github.com/rayhanemokhtari2004-sudo/github-portfolio-analyzer.git
```

### Accéder au dossier

```bash
cd github-portfolio-analyzer
```

### Créer un environnement virtuel

```bash
python -m venv venv
```

### Activer l'environnement

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Lancer l'application

```bash
streamlit run app.py
```

---

## Utilisation

1. Lancer l'application Streamlit.
2. Entrer un nom d'utilisateur GitHub.
3. Cliquer sur **Analyser**.
4. Consulter les statistiques et les graphiques.
5. Exporter les résultats au format CSV ou PDF.

---

## Calcul du score

Le score du portfolio est calculé à partir de plusieurs indicateurs :

- Nombre de dépôts publics
- Nombre total d'étoiles
- Nombre total de forks
- Nombre de followers
- Diversité des langages utilisés
- Activité globale du profil

Le score obtenu fournit une estimation globale de la qualité et de l'activité du portfolio GitHub.

---

## Rapport PDF

Le rapport généré contient :

- Informations du profil
- Statistiques principales
- Score du portfolio
- Répartition des langages
- Dépôts les plus populaires
- Date de génération

---

## Export CSV

Le fichier CSV contient notamment :

- Nom du dépôt
- Description
- Langage
- Nombre d'étoiles
- Nombre de forks
- Visibilité
- URL du dépôt

---
