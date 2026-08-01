import requests


class GitHubAPI:
    BASE_URL = "https://api.github.com/users"

    def get_user(self, username):
        url = f"{self.BASE_URL}/{username}"

        response = requests.get(url)

        if response.status_code == 200:
            return response.json()

        return None