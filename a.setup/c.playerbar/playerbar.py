import os
import cv2 as cv
import numpy as np

# i've found that 215 seems safe. a more dynamic search would be nice.
threshold = 215

def create_threshold(file):
    bar = cv.imread(file)
    barg = cv.cvtColor(bar,cv.COLOR_BGR2GRAY)
    barbw = cv.threshold(barg,threshold,255,cv.THRESH_BINARY)[1]
    cv.imwrite(file.split(".")[0]+"_bw.png",barbw)
    return barbw

def find_threshold(active,inactive):
    a = create_threshold(active)
    i = create_threshold(inactive)
    
    # active we want to create a matchable template
    contours = [contour for contour in cv.findContours(a,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)[0]]
    boundings = [cv.boundingRect(contour) for contour in contours]
    imgh,imgw = a.shape[0:2]
    found = -1
    for i in range(len(boundings)):
        bounding = boundings[i]
        x,y,w,h = bounding[0:4]
        wide = w > imgw/3
        tall = h > imgh/3
        if wide and tall:
            found = i
            break
    if found < 0:
        print(f"Error. No bounding boxes found matching Width > {imgw/3} and Height > {imgh/3}")
        exit(1)
    # create an empty canvas and draw this contour onto it (and its x-flipped version)
    canvas = cv.threshold(a,0,0,cv.THRESH_BINARY)[1]
    cv.drawContours(canvas,contours,contourIdx=i,thickness=-1,color=255)
    bounding = boundings[found]
    x,y,w,h = bounding[0:4]
    bounded = canvas[y:(y+h),x:(x+w)]
    flipped = cv.flip(bounded,flipCode=1)
    
    # are we L or R?
    sumL = np.sum(canvas[y:(y+h),x:(x+int(w/2))])
    sumR = np.sum(canvas[y:(y+h),(x+int(w/2)):(x+w)])
    slf,oth = ("L","R") if sumL > sumR else ("R","L")
    player1 = active.split(".")[0]+slf+".png"
    player2 = active.split(".")[0]+oth+".png"
    cv.imwrite(player1,bounded)
    cv.imwrite(player2,flipped)
    with open("./bar.props","w") as f:
        f.write("bar_thresh="+str(threshold)+"\n")
        f.write(f"player{slf}="+player1+"\n")
        f.write(f"player{oth}="+player2+"\n")

if __name__ == "__main__":
    find_threshold("active.png","inactive.png")

