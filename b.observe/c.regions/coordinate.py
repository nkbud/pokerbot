import os
import time

import cv2 as cv
import numpy as np
import pyautogui

from b_learn.a_config.config import Config

from b_learn.b_shapes.combine import combinedir

cards_csv = "cards.xywh"
cards_png = "cards.png"
regions_csv = "regions.csv"
regions_png = "regions.png"
groups_csv = "groups.csv"
groups_png = "groups.png"

def coordinate(config: Config):
    wx, wy, ww, wh = config.window_xywh_tuple()
    thresh = config.card_threshold()
    blurwh = config.card_blurwh()
    # a nice display of the found regions
    canvas = cv.cvtColor(np.array(pyautogui.screenshot(region=(wx, wy, ww, wh))), cv.COLOR_RGB2BGR)
    
    # read in all our images
    templs = {
        f: cv.cvtColor(cv.imread(os.path.join(combinedir, f)), cv.COLOR_BGR2GRAY)
        for f in os.listdir(combinedir)
    }
    with open(cards_csv, "w") as s:
        
        # look for cards
        seen = set()
        
        count, limit = 0, 500
        while count < limit:
            count += 1
            time.sleep(1)
            
            rgb = np.array(pyautogui.screenshot(region=(wx, wy, ww, wh)))
            gray = cv.cvtColor(src=rgb, code=cv.COLOR_RGB2GRAY)
            bw = cv.threshold(src=gray, thresh=thresh, maxval=255, type=cv.THRESH_BINARY)[1]
            blur = cv.blur(src=bw, ksize=blurwh)
            blur = cv.add(blur, blur)
            
            threshold = 0.9
            scores = {
                f: np.where(cv.matchTemplate(blur, img, method=cv.TM_CCOEFF_NORMED) > threshold)
                for f, img in templs.items()
            }
            for f, score in scores.items():
                img = templs[f]
                h, w = img.shape[0:2]
                for pt in zip(*score[::-1]):
                    x, y = pt[0:2]
                    xywh = f"{x},{y},{w},{h}"
                    
                    
                    if xywh not in seen:
                        seen.add(xywh)
                        print(xywh)
                        s.write(xywh + "\n")
                        cv.rectangle(canvas, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
    
    cv.imwrite(cards_png, canvas)


def consolidate(config: Config):
    wx, wy, ww, wh = config.window_xywh_tuple()
    canvas = cv.cvtColor(np.array(pyautogui.screenshot(region=(wx, wy, ww, wh))), cv.COLOR_RGB2BGR)
    
    # read in the cards
    with open(cards_csv, "r") as f:
        xywhs = [line.split(",") for line in f.readlines()]
        for i in range(len(xywhs)):
            x, y, w, h = xywhs[i][0:4]
            xywhs[i] = int(x), int(y), int(w), int(h)
    
    # find best matching group for each card
    card2group = {0: 0}
    numgroups = 1
    for i in range(1, len(xywhs)):
        x, y, w, h = xywhs[i]
        found = False
        for j in card2group.keys():
            x2, y2, w2, h2 = xywhs[j]
            dist = abs(x - x2) + abs(y - y2)
            if dist < config.card_width():
                card2group[i] = card2group[j]
                found = True
                break
        if not found:
            card2group[i] = numgroups
            numgroups += 1
    
    # invert groups --> cards
    group2cards = {}
    for card, group in card2group.items():
        if group not in group2cards:
            group2cards[group] = []
        group2cards[group].append(card)
    
    # combine into a single card + some wiggle room
    meh = config.card_width() // 5
    group2region = {}
    for group, cards in group2cards.items():
        minx, miny, maxx, maxy = 10000, 10000, 0, 0
        for card in cards:
            x, y, w, h = xywhs[card][0:4]
            x2, y2 = x + w, y + h
            minx = min(x - meh, minx)
            miny = min(y - meh, miny)
            maxx = max(x2 + meh, maxx)
            maxy = max(y2 + meh, maxy)
        group2region[group] = (minx, miny), (maxx, maxy)
    
    # split cards into 5 groups of y levels.
    y2groups = {}
    region = group2region[0]
    y2groups[region[0][1]] = [0]
    for i in range(1, len(group2region)):
        region = group2region[i]
        y = region[0][1]
        found = False
        for y2, cards in y2groups.items():
            if abs(y - y2) < config.card_height():
                y2groups[y2].append(i)
                found = True
                break
        if not found:
            y2groups[y] = [i]
    
    ysorted = np.sort([y for y in y2groups])
    assert len(ysorted) == 5
    
    # cards already group correctly
    v1cards = [group2region[i] for i in y2groups[ysorted[0]]]
    commcards = [group2region[i] for i in y2groups[ysorted[2]]]
    herocards = [group2region[i] for i in y2groups[ysorted[4]]]
    
    # cards that need one more split
    v23cards = [group2region[i] for i in y2groups[ysorted[1]]]
    v2cards, v3cards = [], []
    for card in v23cards:
        pt1, pt2 = card[0], card[1]
        x1 = pt1[0]
        if x1 < ww / 2:
            v2cards.append(card)
        else:
            v3cards.append(card)
    v45cards = [group2region[i] for i in y2groups[ysorted[3]]]
    v4cards, v5cards = [], []
    for card in v45cards:
        pt1, pt2 = card[0], card[1]
        x1 = pt1[0]
        if x1 < ww / 2:
            v4cards.append(card)
        else:
            v5cards.append(card)
    
    # now merge the regions
    cardsets = {
        "v1": v1cards,
        "v2": v2cards,
        "v3": v3cards,
        "v4": v4cards,
        "v5": v5cards,
        "hero": herocards,
        "comm": commcards
    }
    for key, cardset in cardsets.items():
        minx, miny, maxx, maxy = 10000, 10000, 0, 0
        for card in cardset:
            x1, y1 = card[0][0:2]
            x2, y2 = card[1][0:2]
            minx = min(x1 - meh, minx)
            miny = min(y1 - meh, miny)
            maxx = max(x2 + meh, maxx)
            maxy = max(y2 + meh, maxy)
        cv.rectangle(canvas, (minx, miny), (maxx, maxy), (0, 0, 255), 1)
        with open(groups_csv, "w") as f:
            f.write(f"{key},{minx},{miny},{maxx-minx},{maxy-miny}\n")
    
    draw_pot_region(canvas)
    cv.imwrite(groups_png, canvas)


def draw_pot_region(canvas):
    with open(groups_csv, "r") as f:
        for line in f.readlines():
            elems = line.split(",")
            key = elems[0]
            if key == "comm":
                x, y, w, h = int(elems[1]), int(elems[2]), int(elems[3]), int(elems[4])
                y = y - h
                x += w // 6
                w -= w // 6
                w -= w // 8
                with open("pot.xywh", "w") as f:
                    f.write(f"{x},{y},{w},{h}\n")
                cv.rectangle(canvas, (x, y), (x+w, y+h), (0, 255, 0), 1)
                return

    