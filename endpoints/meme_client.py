import requests
from endpoints.endpoint import Endpoint


class AuthToken(Endpoint):

    def auth_token(self, payload):
        self.response = self.session.post(url=f"{self.url}/authorize", json=payload)
        self.response.raise_for_status()
        token = self.response.json()["token"]
        if not token:
            raise ValueError("Токен не найден")
        self.session.headers.update({"Authorization": f"{token}"})
        return token


class ToPostAPI(Endpoint):

    def post_meme(self, payload, token: str):
        self.response = self.session.post(f"{self.url}/meme", json=payload, headers={"Authorization": token})
        return self.response


class ToGetAPI(Endpoint):

    def get_memes(self, token):
        self.response = self.session.get(f"{self.url}/meme", headers={"Authorization": f"{token}"})
        return self.response

    def get_meme_by_id(self, idx: int, token: str):
        self.response = requests.get(f"{self.url}/meme/{idx}", headers={"Authorization": f"{token}"})
        return self.response


class ToDeleteAPI(Endpoint):

    def delete_meme(self, token: str, idx: int):
        self.response = requests.delete(f"{self.url}/meme/{idx}", headers={"Authorization": f"{token}"})
        return self.response


class ToPutAPI(Endpoint):

    def put_meme(self, token: str, payload, idx: int):
        self.response = self.session.put(f"{self.url}/meme/{idx}", json=payload, headers={"Authorization": f"{token}"})
        return self.response
