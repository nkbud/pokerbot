import math
import os

import time
import numpy as np
import cv2 as cv
import pyautogui

from b_learn.a_config.config import Config

basedir = "."
collectdir = os.path.join(basedir, "collect")


# we're going to try and get matchable templates for all the cards

def collect(config: Config):
    # search the central region of the game window
    wx, wy, ww, wh = config.window_xywh_tuple()
    wx += ww / 3
    wy += wh / 3
    ww -= 2 * ww / 3
    wh -= 2 * wh / 3
    
    # apply some filters
    thresh = config.card_threshold()
    blurwh = config.card_blurwh()
    
    # search for contour bounding boxes which are "card like"
    cw = config.card_width()
    ch = config.card_height()
    cb = config.card_brightness()
    
    # 50 screenshots ~ 80 cards ~ 13 unique cards most times.
    # It'd be cool if I could stop when I find 13. But, it's easier this way.
    os.makedirs(collectdir, exist_ok=True)
    
    screenshot_count = len(os.listdir(collectdir)) + 1
    screenshot_limit = screenshot_count + 100
    for i in range(1):
        time.sleep(1)
        print(f"Taking {screenshot_limit} screenshots to try and collect 13 unique cards")
        
    # track how many cards we're finding
    found, newfound, prevnewfound = 0, 0, 0
    while screenshot_count <= screenshot_limit:
        
        # find the contour bounding boxes
        rgb = np.array(pyautogui.screenshot(region=(wx, wy, ww, wh)))
        gray = cv.cvtColor(src=rgb, code=cv.COLOR_RGB2GRAY)
        bw = cv.threshold(src=gray, thresh=thresh, maxval=255, type=cv.THRESH_BINARY)[1]
        blur = cv.blur(src=bw, ksize=blurwh)
        blur = cv.add(blur, blur)
        contours = cv.findContours(blur, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]
        boundings = [cv.boundingRect(contour) for contour in contours]
        
        # select on the card-like ones
        idxs, imgs = [], []
        wtol, htol, btol = math.ceil(cw * 0.2), math.ceil(ch * 0.2), cb * 0.66
        for i in range(len(boundings)):
            bounding = boundings[i]
            bx, by, bw, bh = bounding[0:4]
            right_height = abs(bh - ch) <= htol
            right_width = abs(bw - cw) <= wtol
            if not right_height or not right_width:
                continue
            bounded = blur[by:(by + bh), bx:(bx + bw)]
            brightness = np.sum(bounded) / (255 * bw * bh)
            right_brightness = abs(brightness - cb) < btol
            if not right_brightness:
                continue
            imgs.append(bounded)
            idxs.append(i)
        
        # Check if we made any progress
        newfound = len(idxs)
        if newfound == 0:
            print(".", end="")
            time.sleep(1)
            continue
        if newfound == prevnewfound:
            print(",", end="")
            time.sleep(1)
            continue
        prevnewfound = newfound
        print("")
        
        # Only save the new cards
        newcards = []
        stage = "N/A"
        if newfound == 3:
            newcards = imgs
            stage = "Flop"
        if newfound == 4 or newfound == 5:
            selectedxs = [boundings[i][0] for i in idxs]
            sortedi = np.argsort(selectedxs)
            newesti = sortedi[len(sortedi) - 1]
            newcards = [imgs[newesti]]
            stage = "Turn" if newfound == 4 else "River"
        
        # save the new imgs
        for i in range(len(newcards)):
            cv.imwrite(f"{collectdir}/{found + i}.png", newcards[i])
        
        # print report, sleep, repeat
        found += len(newcards)
        progress = f"{screenshot_count} / {screenshot_limit}"
        print("%-5s | %-5s | %-9s |" % (progress, stage, f"{found} cards"))
        time.sleep(1)
        screenshot_count += 1
    
    # End.
    print(f"Collection complete.")
