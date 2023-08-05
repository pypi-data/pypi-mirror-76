from .challenge import Challenge
from .category import Category
from .helpers.requests import get, post

class CTF:
    def __init__(self, api_base):
        self.api_base = api_base
        self.auth_token = None

    def get_challenge(self, id):
        # There's currently a bug in RACTF that means we can't GET /challenges/:id, so this is a workaround
        return [challenge for challenge in self.get_challenges() if challenge.id == id][0]
        # return Challenge(id, self)

    def get_challenges(self):
        resp = get("challenges/categories/", self)
        challenges = []
        for category in resp["d"]:
            for challenge in category["challenges"]:
                challenges.append(Challenge(challenge["id"], self, data=challenge))
        return challenges
    
    def get_categories(self):
        resp = get("challenges/categories/", self)
        categories = []
        for category in resp["d"]:
            categories.append(Category(category["id"], self, data=category))
        return categories

    def get_config(self):
        return get("config/", self)["d"]
    
    def login(self, username, password, otp=None):
        self.auth_token = "Token " + post("auth/login/", self, json={"username": username, "password": password, "otp": otp})["d"]["token"]