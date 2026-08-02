from api.github_api import GitHubAPI


def main():
    api = GitHubAPI()

    username = input("Entrez un nom d'utilisateur GitHub : ")

    user = api.get_user(username)

    if user:
        print("\n Informations du profil ")
        print(f"Nom : {user.get('name')}")
        print(f"Login : {user.get('login')}")
        print(f"Bio : {user.get('bio')}")
        print(f"Dépôts publics : {user.get('public_repos')}")
        print(f"Followers : {user.get('followers')}")
        print(f"Following : {user.get('following')}")

        repositories = api.get_repositories(username)

        print("\n===== Dépôts =====")

        if repositories:
            for repo in repositories:
                print(f"Nom : {repo['name']}")
                print(f"Langage : {repo['language']}")
                print(f"⭐ Stars : {repo['stargazers_count']}")
                print("-" * 40)
        else:
            print("Aucun dépôt trouvé.")

    else:
        print("Utilisateur introuvable.")


if __name__ == "__main__":
    main()