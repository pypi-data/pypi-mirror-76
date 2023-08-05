from .abc import APIBaseObject
from .challenge import Challenge


class Category(APIBaseObject):
    def __init__(self, object_id, ctf, data=None):
        self.id = object_id
        self.ctf = ctf
        super(Category, self).__init__(ctf, data=data)
        self.convert_json_to_challenges()

    def get_api_path(self):
        return f"challenges/categories/{self.id}/"
    
    def convert_json_to_challenges(self):
        challenges = []
        for challenge in self.challenges:
            if isinstance(challenge, Challenge):
                continue
            challenges.append(Challenge(challenge["id"], self.ctf, challenge))
        self.challenges = challenges