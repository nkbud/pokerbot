import os

import cv2 as cv
import numpy as np

propsfile = "./_card.props"

if __name__ == "__main__":

    # read a file named "card" as a BGR (blue,green,red) image
    files = [f for f in os.listdir("../b.cards") if f.startswith("10.")]
    f = files[0]
    ext = f.split(".")[1]
    print(f"Found file: {f}")
    bgr = cv.imread(f)

    # i don't have a reliable way of searching for the correct
    blurheight = 3
    # but i do have a nice search for blurwidth, given the card is "10"
    for blurwidth in range(3, 50):

        # process the image
        threshold = 250
        gray = cv.cvtColor(bgr, cv.COLOR_BGR2GRAY)
        bw = cv.threshold(gray, threshold, 255, cv.THRESH_BINARY)[1]
        blur = cv.blur(bw, (blurwidth, blurheight))
        blur = cv.add(blur, blur)
        
        # if there exists a single significant contour that's wide enough to be both "1" and "0"
        # we found our minimum blur width
        significance = 0.2
        boundings = [cv.boundingRect(contour) for contour in
                     cv.findContours(blur, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0]]
        viables = [
            i for i in range(len(boundings))
            if np.product(boundings[i][2:4]) / np.product(blur.shape[0:2]) > significance and
               boundings[i][3] / boundings[i][2] < 1.2
        ]
        if len(viables) != 1:
            continue
        print(f"Found minimum horizontal blur: {blurwidth}")

        # get the bounding box and its properties. save them to a file.
        bounding = boundings[viables[0]]
        x, y, width, height = bounding[0:4]
        blurbounded = blur[y:(y + height), x:(x + width)]
        brightness = np.sum(blurbounded) / (255 * width * height)
        with open(propsfile, "w") as f:
            f.writelines([
                f"width={width}\n",
                f"height={height}\n",
                f"brightness={brightness}\n",
                f"blurwidth={blurwidth}\n",
                f"blurheight={blurheight}\n",
                f"threshold={threshold}\n"
            ])
        print(f"Saved bounding rectangle properties to file: {propsfile}")

        # show our intermediate steps
        cv.imwrite(f"./10_1." + ext, gray)
        cv.imwrite(f"./10_2." + ext, bw)
        cv.imwrite(f"./10_3." + ext, blur)
        cv.imwrite(f"./10_4." + ext, blurbounded)
        break
