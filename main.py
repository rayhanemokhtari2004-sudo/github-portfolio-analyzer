from api.github_api import GitHubAPI
from services.analyzer import PortfolioAnalyzer
from utils.charts import Charts


def main():
    # Création des objets
    api = GitHubAPI()
    analyzer = PortfolioAnalyzer()
    charts = Charts()

    # Demande du nom d'utilisateur GitHub
    username = input("Entrez un nom d'utilisateur GitHub : ")

    # Récupération du profil
    user = api.get_user(username)

    if not user:
        print("Utilisateur introuvable.")
        return

    # ==========================
    # Informations du profil
    # ==========================
    print("\n========== PROFIL ==========\n")

    print(f"Nom : {user.get('name')}")
    print(f"Login : {user.get('login')}")
    print(f"Bio : {user.get('bio')}")
    print(f"Dépôts publics : {user.get('public_repos')}")
    print(f"Followers : {user.get('followers')}")
    print(f"Following : {user.get('following')}")

    # ==========================
    # Dépôts GitHub
    # ==========================
    repositories = api.get_repositories(username)

    print("\n========== DÉPÔTS ==========\n")

    if repositories:
        for repo in repositories:
            print(f"Nom : {repo['name']}")
            print(f"Langage : {repo['language']}")
            print(f"Stars : {repo['stargazers_count']}")
            print(f"Forks : {repo['forks_count']}")
            print("-" * 40)
    else:
        print("Aucun dépôt trouvé.")
        return

    # ==========================
    # Statistiques
    # ==========================
    print("\n========== STATISTIQUES ==========\n")

    print(f"Nombre de dépôts : {analyzer.total_repositories(repositories)}")
    print(f"Total des étoiles : {analyzer.total_stars(repositories)}")
    print(f"Total des forks : {analyzer.total_forks(repositories)}")

    popular = analyzer.most_popular_repository(repositories)

    if popular:
        print(
            f"Dépôt le plus populaire : "
            f"{popular['name']} ({popular['stargazers_count']} ⭐)"
        )

    # ==========================
    # Langages utilisés
    # ==========================
    print("\n========== LANGAGES ==========\n")

    languages = analyzer.languages_used(repositories)

    for language, count in languages.items():
        print(f"{language} : {count} dépôt(s)")

    # ==========================
    # Création des graphiques
    # ==========================
    charts.languages_chart(languages)
    charts.stars_chart(repositories)

    print("\nLes graphiques ont été enregistrés dans le dossier 'images'.")


if __name__ == "__main__":
    main()