from json import *

class jsonUtils():
    def _get_json(self, name: str, path: list):
        pathstr = ""
        for i in path:
            pathstr+=i+"/"