from secrets import refresh_token, base_64
from requests import post


class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        response = post(url="https://accounts.spotify.com/api/token",
                        data={"grant_type": "refresh_token",
                              "refresh_token": self.refresh_token},
                        headers={"Authorization": "Basic " + self.base_64}).json()

        return response["access_token"]
