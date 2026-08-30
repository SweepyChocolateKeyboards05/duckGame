from json import *

class Utils():
    def _navigate_dict(self, input_dict, keys:list):
        current = input_dict
        if not keys:
            return {"message":current}
        for key in keys:
            if (isinstance(current, list) and not isinstance(key, int) and key >= len(current)) or (isinstance(current, dict) and key not in current):
                return {"message": "failed", "error": "invalid key(s)"}
            current = current[key]
        return {"message":current}

class JSONUtils(Utils):
    def _get_json(self, name: str, path: list, keys:list):
        pathstr = ""
        if path:
            for i in path:
                pathstr+=i+"/"
        pathstr+=name+".json"
        try:
            with open(pathstr, "r") as f:
                content = load(f)
        except:
            return {"message":"failed", "error": "invalid path/name"}
        if keys:
            res = self._navigate_dict(content, keys)
        return res