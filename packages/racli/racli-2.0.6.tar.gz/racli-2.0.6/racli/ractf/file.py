from .abc import APIBaseObject
from .helpers.requests import get

class File(APIBaseObject):
    def __init__(self, object_id, challenge, ctf, data=None):
        self.id = object_id
        self.ctf = ctf
        self.challenge = challenge
        super(File, self).__init__(ctf, data=data)

    def get_api_path(self):
        return f"files/{self.id}/"

    def save(self, path):
        with open(path, "wb") as f:
            f.write(self.read())

    def read(self):
        return get(self.url, self.ctf)