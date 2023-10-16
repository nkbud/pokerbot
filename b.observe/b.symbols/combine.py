import os
import cv2 as cv
import numpy as np

from b_learn.b_shapes.collect import basedir
from b_learn.b_shapes.collect import collectdir

combinedir = os.path.join(basedir, "combine")


def pad(img, maxh, maxw):
    return cv.copyMakeBorder(src=img,
                             top=0, bottom=maxh - img.shape[0], left=0, right=maxw - img.shape[1],
                             borderType=cv.BORDER_CONSTANT, value=0)


def diff(img1, img2):
    return np.amin(cv.matchTemplate(img1, img2, cv.TM_SQDIFF_NORMED)[0])


def combine(config):
    print(f"Clustering found cards by similarity. Aggregating clusters to a single representative.")
    os.makedirs(combinedir, exist_ok=True)
    
    # read in all the collected images as grayscale
    collected = [
        cv.cvtColor(cv.imread(os.path.join(collectdir, entry)), cv.COLOR_BGR2GRAY)
        for entry in os.listdir(collectdir)
        if os.path.isfile(os.path.join(collectdir, entry))
    ]
    
    # pad imgs to equal height and width to allow distance function
    maxh = np.amax([img.shape[0] for img in collected])
    maxw = np.amax([img.shape[1] for img in collected])
    padded = [pad(img, maxh, maxw) for img in collected]
    
    # put similar images together into groups
    threshold = 0.05
    id2group = {0: 0}
    numgroups = 1
    for i in range(1, len(padded)):
        diffs = [diff(padded[i], padded[j]) for j in id2group.keys()]
        closest = np.argmin(diffs)
        if diffs[closest] < threshold:
            id2group[i] = id2group[closest]
        else:
            id2group[i] = numgroups
            numgroups += 1
    group2ids = {}
    for id, group in id2group.items():
        if group not in group2ids:
            group2ids[group] = []
        group2ids[group].append(id)
    
    # and then average each group to a single rep
    for group, ids in group2ids.items():
        groupimgs = [collected[i] for i in ids]
        maxhg = np.amax([img.shape[0] for img in groupimgs])
        maxwg = np.amax([img.shape[1] for img in groupimgs])
        paddedg = [pad(img, maxhg, maxwg) for img in groupimgs]
        canvas = np.zeros(paddedg[0].shape[0:2], float)
        for img in paddedg:
            cv.accumulate(img, canvas)
        canvas = (canvas / len(paddedg)).astype(np.uint8)
        
        # and write it to a file
        contour = cv.findContours(canvas, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)[0][0]
        cvx, cvy, cvw, cvh = cv.boundingRect(contour)
        found_box = canvas[cvy:(cvy + cvh), cvx:(cvx + cvw)]
        cv.imwrite(f"{combinedir}/{group}.png", found_box)
    
    # End.
    print(f"Combining complete. Found {len(group2ids)} clusters and averaged each to a single representative")
