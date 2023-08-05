from .abc import APIBaseObject
from .helpers.requests import post, get
from .hint import Hint
from .file import File
from .errors import APIError


class Challenge(APIBaseObject):
    def __init__(self, object_id, ctf, data=None):
        self.id = object_id
        self.ctf = ctf
        self.challenge_metadata = {}
        super(Challenge, self).__init__(ctf, data=data)
        self.convert_json_to_hints()
        self.convert_json_to_files()

    def get_api_path(self):
        return f"challenges/{self.id}/"

    def convert_json_to_hints(self):
        hints = []
        for hint in self.hints:
            if isinstance(hint, Hint):
                continue
            hints.append(Hint(hint["id"], self, self.ctf, data=hint))
        self.hints = hints
    
    def convert_json_to_files(self):
        files = []
        for instance in self.files:
            if isinstance(instance, File):
                continue
            files.append(File(instance["id"], self, self.ctf, data=instance))
        self.files = files
    
    def submit_flag(self, flag):
        resp = post("challenges/submit_flag/", self.ctf, json={"challenge": self.id, "flag": flag})
        # again, bug
        # self._fill_attrs()
        return resp["m"] == "correct_flag"

    def get_challenge_server_instance(self):
        if not self.challenge_metadata.get('cserv_name'):
            raise APIError("Challenge has no instance attached")
        d = get(f"challengeserver/instance/{self.challenge_metadata.get('cserv_instance')}/")
        return f"{d['ip']}:{d['port']}"