import cv2, os
import numpy as np
import pandas as pd
import imagesize

from glob import glob

folders = glob('*')
folders = [i for i in folders if os.path.isdir(i)]

print(folders)

for folder in folders:
    filenames = glob(folder+'/*.txt')
    datas = []

    print(filenames)

    for fname in filenames:
        bboxes = np.loadtxt(fname)
        img_fname = fname.replace('.txt', '.jpg')
        file_stats = os.stat(img_fname)
        width, height = imagesize.get(img_fname)

        current = []

        for i,bbox in enumerate(bboxes):
            try:
                bbox = bbox[1:]
                bbox = bbox * np.array([width, height, width, height])
                ul = tuple(np.int32(bbox[:2]-bbox[2:4]/2+4))
                lr = tuple(np.int32(bbox[:2]+bbox[2:4]/2))
            except:
                print(bbox.shape)
                continue

            current.append({
                'filename': os.path.basename(img_fname),
                'file_size': file_stats.st_size,
                'file_attributes': '',
                'region_count': len(bboxes),
                'region_id': i,
                'region_shape_attributes': {
                    'name': 'rect',
                    'x': ul[0],
                    'y': ul[1],
                    'width': bbox[2]-4,
                    'height': bbox[3]-4,
                },
                'region_attributes': ''
            })

        datas += current

    datas = pd.DataFrame(datas)
    csv = datas.to_csv(index=False)
    csv = csv.replace('\'', '""')

    with open(folder+'.csv', 'w') as f:
        f.write(csv)
