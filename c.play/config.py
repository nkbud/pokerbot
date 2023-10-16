import os

config_filepath = os.path.abspath(__file__)
config_dirpath = os.path.dirname(config_filepath)+"/config"

def props(name: str):
    props = {}
    with open(os.path.join(config_dirpath,f"{name}.props")) as f:
        for line in f.readlines():
            k, v = line.split("=")
            props[k] = v.split("\n")[0]
    return props

def xywh(name: str):
    xywh = []
    with open(os.path.join(config_dirpath,f"{name}.xywh")) as f:
        for line in f.readlines():
            l = line.split("\n")[0]
            x,y,w,h = line.split(",")
            xywh.append((int(x),int(y),int(w),int(h)))
    return xywh

def csv2bgr(csv: str):
    b, g, r = [int(x) for x in csv.split(",")][0:4]
    return b, g, r

def csv2xywh(csv: str):
    x,y,w,h = [int(x) for x in csv.split(",")][0:5]
    return x,y,w,h


class Config:
    
    def __init__(self):
        self.path = os.path.abspath(".")
        self.__colorbgr = props("rgb")
        self.__card = props("card")
        self.__window = props("window")
        self.__comm = xywh("comm")
        self.__hero = xywh("hero")
        self.__vills = xywh("vills")
        self.__pot = xywh("pot")
    
    def ahk_cmd(self) -> str:
        return self.__window["ahk_cmd"]
    
    def ahk_exe(self) -> str:
        return self.__window["ahk_exe"]
    
    def ahk_class(self) -> str:
        return self.__window["ahk_class"]
    
    def bar_thresh(self) -> float:
        return float(self.__bar["bar_thresh"])
    
    def rgb_yellow(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["yellow"])
    
    def rgb_blue(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["blue"])
    
    def rgb_red(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["red"])
    
    def rgb_green(self) -> (int, int, int):
        return csv2bgr(self.__colorbgr["green"])
    
    def rgb_gray(self) -> (int, int, int):
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
    
    def window_xywh_str(self) -> str:
        return self.__window["xywh"]
    
    def window_xywh_tuple(self) -> (int, int, int, int):
        return csv2xywh(self.__window["xywh"])
    
    def hero_xywhs(self) -> [(int, int, int, int)]:
        return self.__hero
    
    def comm_xywhs(self) -> [(int,int,int,int)]:
        return self.__comm
    
    def vills_xywhs(self) -> [(int, int, int, int)]:
        return self.__vills
    
    def pot_xywh(self) -> (int, int, int, int):
        return self.__pot


if __name__ == "__main__":
    config = Config()
