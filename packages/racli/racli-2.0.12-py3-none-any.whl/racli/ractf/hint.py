from .abc import APIBaseObject
from .helpers.requests import post

class Hint(APIBaseObject):
    def __init__(self, object_id, challenge, ctf, data=None):
        self.id = object_id
        self.ctf = ctf
        self.challenge = challenge
        self.text = None
        super(Hint, self).__init__(ctf, data=data)

    def get_api_path(self):
        return f"hints/{self.id}/"

    def use(self):
        self._fill_attrs(data=post("hints/use/", self.ctf, json={"id": self.id})["d"])
