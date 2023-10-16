import os
from typing import List

import cv2
import numpy
import pyautogui
import threading

from c_play.config import Config,config_dirpath

templ_dirpath = config_dirpath+"/templs"

class Reader:
    """
    Screenshot the board and determine:
    v1:
    - cards:
        - community (0-5)
        - hero (0-2)
        - villain (down or up, 0-5)
    - pot size
        - via ocr
    - position
        - search dealer chip
    v2:
    - bet sizings
    v2.1
    - bet sizings past rounds

    Ideas that allow combination of all info?
    - sequence embeddings?

    """
    
    def __init__(self):
        self.config = Config()
        self.__load_templs()
        self.__load_regions()
        self.__load_colors()
        self.hero: List[str] = []
        self.comm: List[str] = []
        self.vills: List[bool] = []
        self.pot = -1
        self.__thread_hero_comm = threading.Thread(target=self.search_hero_and_comm)
        self.__thread_vills = threading.Thread(target=self.search_vills)
        self.__thread_pot = threading.Thread(target=self.search_pot)
    
    def __load_templs(self):
        self.templs = {
            f:cv2.cvtColor(cv2.imread(os.path.join(templ_dirpath,f)),cv2.COLOR_BGR2GRAY)
            for f in os.listdir(templ_dirpath)
        }
    
    def __load_colors(self):
        suits = {
            "d":self.config.rgb_blue(),
            "c":self.config.rgb_green(),
            "h":self.config.rgb_red(),
            "s":self.config.rgb_gray()
        }
        vill = self.config.rgb_yellow()
    
    def __load_regions(self):
        self.hero_xywhs = self.config.hero_xywhs()
        self.comm_xywhs = self.config.comm_xywhs()
        self.vills_xywhs = self.config.vills_xywhs()
    
    def __search_card(self,xywh):
        rgb = pyautogui.screenshot(region=xywh)
        colors = rgb.getcolors()
        
        pass
    
    def search_hero_and_comm(self):
        self.search_hero()
        self.search_comm()
    
    def search_hero(self):
        for xywh in self.hero_xywhs:
            self.__search_card(xywh)
        
        pass
    
    def search_comm(self):
        pass
    
    def search_vills(self):
        pass
    
    def search_pot(self):
        pass
    
    def __new_haystack(self,xywh: (int,int,int,int)):
        rgb = numpy.array(pyautogui.screenshot(region=xywh))
        gray = cv2.cvtColor(src=rgb,code=cv2.COLOR_RGB2GRAY)
        bw = cv2.threshold(src=gray,thresh=self.config.card_threshold(),maxval=255,type=cv2.THRESH_BINARY)[1]
        blur = cv2.blur(src=bw,ksize=self.config.card_blurwh())
        return cv2.add(blur,blur)
    
    def __match_template(self,haystack) -> str:
        threshold = 0.9
        for filename,templ in self.templs.items():
            result = cv2.matchTemplate(haystack,templ,method=cv2.TM_CCOEFF_NORMED)
            min_val,max_val,min_loc,max_loc = cv2.minMaxLoc(result)
            if max_val > threshold:
                return filename[0]
        return ""

if __name__ == "__main__":
    rgb = pyautogui.screenshot()
    h = rgb.getcolors(maxcolors=int(2^32-1))
    print(h)


