import cv2
import numpy as np

from glob import glob
from natsort import natsorted

filenames = glob('yolo/**/images/*', recursive=True)
#filenames = glob('desactivated/Luzignan//images/*', recursive=True)
filenames = natsorted(filenames)

colors = [
    (0,0,255),
    (255,0,0),
    (255,0,255),
]

for i, fname in enumerate(filenames):
    img = cv2.imread(fname)
    txt = fname[:-4].replace('images', 'labels') + '.txt'

    size = np.array(img.shape[:2])
    size = np.flip(size)
    print(i, fname)

    bboxes = np.loadtxt(txt)

    if len(bboxes) > 0:
        bboxes = np.atleast_2d(bboxes)
        for bbox in bboxes:
            print(bbox)
            bbox = bbox * np.hstack([1,size,size])
            bbox = bbox.astype('int')
            c,x,y,w,h = bbox
            w,h = w//2, h//2

            cv2.rectangle(img, (x-w, y-h), (x+w, y+h), colors[c], 2)

    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img', img)

    while cv2.waitKey() !=27:
        pass
