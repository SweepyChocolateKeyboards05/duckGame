from json import *

class Utils():
    def _navigate_dict(self, current:dict, keys:list):
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
        if "error" in res:
            return res
        return {"message": res["message"], "whole": content, "pathstr": pathstr}


    
    def _change_json(self, name: str, path: list, keys:list, add, remove:list):
        res = self._get_json(name = name, path = path, keys= keys)
        if "error" in res:
            return res

                
        if isinstance(res["message"], dict):
            if not isinstance(add, dict):
                return {"message": "failed", "error": "invalid data"}
            else:
                try:
                    res["message"].update(add)
                except:
                    return {"message":"failed", "error":"unknown"}

            for i in remove:
                if not i in res["message"]:
                    return {"message": "failed", "error": "key not in dict"}
                
            for i in remove:
                del res["message"][i]

                
        if isinstance(res["message"], list):
            if not isinstance(add, list):
                return {"message": "failed", "error": "invalid data"}
            else:
                try:
                    res["message"].extend(add)
                except:
                    return {"message":"failed", "error":"unknown"}

            for i in remove:
                if i >= len(res["message"]):
                    return {"message": "failed", "error": "index out of range"}

            for i in remove:
                del res["message"][i]

                    

        with open(res["pathstr"], "w") as f:
            try:
                dump(res["whole"], f, indent= 4)
            except:
                return {"message":"failed", "error":"unknown"}
        return {"message":"done"}