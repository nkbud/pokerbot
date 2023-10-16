import os


mod: str = __name__
dirpath = "/".join(mod.split(".")[0:2])

def props(name: str):
    props = {}
    with open(os.path.join(dirpath, f"{name}.props")) as f:
        for line in f.readlines():
            k, v = line.split("=")
            props[k] = v.split("\n")[0]
    return props


def csv2bgr(csv: str):
    b, g, r = [int(x) for x in csv.split(",")][0:4]
    return b, g, r

def csv2xywh(csv: str):
    x,y,w,h = [int(x) for x in csv.split(",")][0:5]
    return x,y,w,h


class Config:
    
    def __init__(self):
        self.path = os.path.abspath(".")
        self.__bar = props("bar")
        self.__colorbgr = props("colorbgr")
        self.__card = props("card")
        self.__window = props("window")
    
    def ahk_cmd(self) -> str:
        return self.__window["ahk_cmd"]
    
    def ahk_exe(self) -> str:
        return self.__window["ahk_exe"]
    
    def ahk_class(self) -> str:
        return self.__window["ahk_class"]
    
    def bar_thresh(self) -> float:
        return float(self.__bar["bar_thresh"])
    
    def bgr_yellow(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["yellow"])
    
    def bgr_blue(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["blue"])
    
    def bgr_red(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["red"])
    
    def bgr_green(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["green"])
    
    def bgr_gray(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["gray"])
    
    def card_width(self) -> int:
        return int(self.__card["width"])
    
    def card_height(self) -> int:
        return int(self.__card["height"])
    
    def card_brightness(self) -> float:
        return float(self.__card["brightness"])
    
    def card_blurwh(self) -> (int, int):
        return int(self.__card["blurwidth"]), int(self.__card["blurheight"])
    
    def card_threshold(self) -> float:
        return float(self.__card["threshold"])
    
    def player_pathL(self) -> str:
        return self.__bar["playerL"]
    
    def player_pathR(self) -> str:
        return self.__bar["playerL"]
    
    def window_xywh_str(self) -> str:
        return self.__window["xywh"]
    
    def window_xywh_tuple(self) -> (int, int, int, int):
        return csv2xywh(self.__window["xywh"])


if __name__ == "__main__":
    config = Config()
