from .abc import APIBaseObject
from .helpers.requests import post
from .hint import Hint
from .file import File


class Challenge(APIBaseObject):
    def __init__(self, object_id, ctf, data=None):
        self.id = object_id
        self.unlocked = False
        self.ctf = ctf
        super(Challenge, self).__init__(ctf, data=data)
        if self.unlocked:
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