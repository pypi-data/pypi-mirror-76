import requests
from json.decoder import JSONDecodeError

from ..errors import APIError, PermissionsError


def _parse_resp(resp):
    if resp.status_code == 403:
        raise PermissionsError(resp.json())
    if resp.status_code != 200:
        raise APIError(resp.text)
    try:
        data = resp.json()
        if data["s"] != True:
            raise APIError(data["m"])
        return data
    except JSONDecodeError:
        return resp.content

def get(api_path, ctf, *args, **kwargs):
    if ctf.auth_token:
        kwargs["headers"] = {}
        kwargs["headers"]["authorization"] = ctf.auth_token
    resp = requests.get((ctf.api_base if not "http" in api_path else "") + api_path, *args, **kwargs)
    return _parse_resp(resp)


def post(api_path, ctf, *args, **kwargs):
    if ctf.auth_token:
        kwargs["headers"] = {}
        kwargs["headers"]["authorization"] = ctf.auth_token
    resp = requests.post((ctf.api_base if not "http" in api_path else "") + api_path, *args, **kwargs)
    return _parse_resp(resp)


def patch(api_path, values, ctf, *args, **kwargs):
    if ctf.auth_token:
        kwargs["headers"] = {}
        kwargs["headers"]["authorization"] = ctf.auth_token
    resp = requests.patch((ctf.api_base if not "http" in api_path else "") + api_path, values, *args, **kwargs)
    return _parse_resp(resp)
