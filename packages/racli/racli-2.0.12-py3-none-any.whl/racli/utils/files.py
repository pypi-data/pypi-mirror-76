import os
from pathlib import Path

def find_file(filename, path=os.getcwd()):
    if os.path.dirname(path) == path:
        return None
    if os.path.exists(path + "/" + filename):
        return path + "/" + filename
    return find_file(filename, path=str(Path(path).parent))

def get_ctf_root():
    return find_file(".ctf.json").strip("/.ctf.json")

def get_cat_root():
    return find_file(".category.json").strip("/.category.json")