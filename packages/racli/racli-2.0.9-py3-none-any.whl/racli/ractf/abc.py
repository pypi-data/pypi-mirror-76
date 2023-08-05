from abc import ABC, abstractmethod

from .helpers.requests import get, patch


class APIBaseObject(ABC):
    def __init__(self, ctf, data=None):
        self._ctf = ctf
        self._type = self.__class__.__name__
        self._fill_attrs(data=data)

    def __repr__(self):
        return f"<{self._type} [{self.id}]>"
    
    def __str__(self):
        return self.name

    @abstractmethod
    def get_api_path(self):
        raise NotImplementedError()

    def _set_attrs_on_remote(self, values):
        patch(self.get_api_path(), values, self._ctf)

    def _set_attr_on_remote(self, name, value):
        self._set_attrs({name: value})

    def _get_object(self):
        return get(self.get_api_path(), self._ctf)

    def _fill_attrs(self, data=None):
        if not data:
            data = self._get_object()
        for k, v in data.items():
            setattr(self, k, v)
