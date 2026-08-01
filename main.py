from api.github_api import GitHubAPI


def main():
    api = GitHubAPI()

    username = input("Entrez un nom d'utilisateur GitHub : ")

    user = api.get_user(username)

    if user:
        print("\n===== Informations du profil =====")
        print(f"Nom : {user.get('name')}")
        print(f"Login : {user.get('login')}")
        print(f"Bio : {user.get('bio')}")
        print(f"Dépôts publics : {user.get('public_repos')}")
        print(f"Followers : {user.get('followers')}")
        print(f"Following : {user.get('following')}")
    else:
        print("Utilisateur introuvable.")


if __name__ == "__main__":
    main()