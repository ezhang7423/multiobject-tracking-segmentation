import sys
import os
import colorsys
import time
sys.path.insert(0, r"C:\Users\Victor\Desktop\resarch\cocoapi\PythonAPI")

import numpy as np
import matplotlib.pyplot as plt
import pycocotools.mask as rletools
from iot import load_sequences, load_seqmap, load_txt


def isOccluded(boxes):
    x0 = []
    xf = []
    y0 = []
    yf = []
    for x in range(len(boxes)):
        box = [i for i in boxes[x]]
        # x0 += [box[0]] move this to bottom of function
        # xf += [box[2]]
        x_index = [box[0], box[2]]
        for i in range(len(x0)):
            if x0[i] <= x_index[0] <= x0[i] + xf[i]:
                return True
            elif x0[i] <= x_index[1] <= x0[i] + xf[i]:
                return True
        x0.append(x_index[0])
        xf.append(x_index[1])

        y_index = [box[1], box[3]]
        for i in range(len(y0)):
            if y0[i] <= y_index[0] <= y0[i] + yf[i]:
                return True
            elif y0[i] <= y_index[1] <= y0[i] + yf[i]:
                return True
        y0.append(y_index[0])
        yf.append(y_index[1])
        # check if collision
    return False;


def returnBoxes(frame):
    frame128 = frame
    bBoxes = []
    for x in range(len(frame128)):
        if (frame128[x].class_id == 1 or frame128[x].class_id == 2):
            bBoxes.append(rletools.toBbox(frame128[x].mask))
    return bBoxes


def writeOcclusion(path):
    frames = load_txt(os.path.join(INSTANCE_PATH, path))
    occlusions = []
    for x in range(len(frames)):
        try:
            oc = isOccluded(returnBoxes(frames[x]))
            occlusions.append(oc)
            if oc:
                print("Occlusion at file", os.path.basename(path)[:-4], "frame", x)
        except KeyError:
            print('No data at frame', x)
            time.sleep(.1)
    filename = os.path.basename(path)[:-4] + "occlusions.txt"
    os.makedirs(os.path.join(INSTANCE_PATH, "occlusions"), exist_ok = True)
    with open(os.path.join(INSTANCE_PATH, "occlusions", filename), 'w') as fout:
        print("finished", filename)
        fout.write(str(occlusions))


if __name__ == "__main__":
    INSTANCE_PATH = r"C:\Users\Victor\Desktop\resarch\instances_txt"
    for file in os.listdir(INSTANCE_PATH):
        writeOcclusion(file)
    

