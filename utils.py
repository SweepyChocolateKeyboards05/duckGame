from json import *
from os import get_terminal_size

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

class DialougeInterface(JSONUtils):
    def visualizeTree(self, tree):
        text = ""
        size = get_terminal_size().columns
        nextLine = f" {tree[0]} "
        nextLine = f"/{nextLine.center(int(size/2), "-")}\\"
        nextLine = f"\n{nextLine.center(size, " ")}"
        text+=nextLine

        nextLine = f"{list(tree[1].keys())[0]}{" "* int(size/2 - len(list(tree[1].keys())[0])/2 - len(list(tree[1].keys())[1])/2)}{list(tree[1].keys())[1]}"
        text += f"\n{nextLine.center(int(size), " ")}"
        for _ in range(2):
            nextLine = f"|{" "* int(size/2)}|".center(int(size), " ")
            text += f"\n{nextLine}"

        tree1 = tree[1][list(tree[1].keys())[0]]
        tree2 = tree[1][list(tree[1].keys())[1]]
        size /= 2


        nextLine1 = f" {tree1[0]} "
        if isinstance(tree1[1], dict):
            nextLine1 = f"/{nextLine1.center(int(size/2), "-")}\\"
        nextLine1 = f"\n{nextLine1.center(int(size), " ")}"

        nextLine2 = f" {tree2[0]} "
        if isinstance(tree2[1], dict):
            nextLine2 = f"/{nextLine2.center(int(size/2), "-")}\\"
        nextLine2 = f"{nextLine2.center(int(size), " ")}"
        
        text+=(nextLine1+nextLine2)

        if isinstance(tree1[1], dict):
            nextLine1 = f"{list(tree1[1].keys())[0]}{" "* int(size/2 - len(list(tree1[1].keys())[0])/2 - len(list(tree1[1].keys())[1])/2)}{list(tree1[1].keys())[1]}"
        else:
            nextLine1 = str(tree1[1]).center(int(size), " ")
        if isinstance(tree2[1], dict):
            nextLine2 = f"{list(tree2[1].keys())[0]}{" "* int(size/2 - len(list(tree2[1].keys())[0])/2 - len(list(tree2[1].keys())[1])/2)}{list(tree2[1].keys())[1]}"
        else:
            nextLine2 = str(tree2[1]).center(int(size), " ")
        text += f"\n{nextLine1.center(int(size), " ")+nextLine2.center(int(size), " ")}"

        for _ in range(2):
            if isinstance(tree1[1], dict):
                nextLine1 = f"|{" "* int(size/2)}|".center(int(size), " ")
            else: nextLine1 = " "*int(size)
            if isinstance(tree2[1], dict):
                nextLine2 = f"|{" "* int(size/2)}|".center(int(size), " ")  
            else: nextLine2 = " "*int(size)
            text += f"\n{nextLine1 + nextLine2}"
        ends = []
        if isinstance(tree1[1], dict):
            ends.extend([tree1[1][list(tree1[1].keys())[0]],tree1[1][list(tree1[1].keys())[1]]])
        else:
            ends.extend(["",""])

        if isinstance(tree2[1], dict):
            ends.extend([tree2[1][list(tree2[1].keys())[0]],tree2[1][list(tree2[1].keys())[1]]])
        else:
            ends.extend(["",""])
        ends = [str(i) if isinstance(i, int) else "..." if i else "" for i in ends]

        nextLine = f"{ends[0]}{" "* int(size/2)}{ends[1]}".center(int(size), " ") + f"{ends[2]}{" "* int(size/2)}{ends[3]}".center(int(size), " ")
        text += f"\n{nextLine}"

        return text