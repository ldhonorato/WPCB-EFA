#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 19:42:35 2020

@author: lhss
"""

import numpy as np
import cv2
import os
import argparse

parser.add_argument('--base_path', type=str, dest='base_path', required=True, help='Path dataset with results')
args = parser.parse_args()
#base_path = '/home/lhss/Documents/Artigo_PDI/database/PCB DSLR and Results/pcb'
base_path = args.base_path

original_size = (3280, 4928)

def get_annotations(fpath):
        '''
        Returns a list of IC chips as a list from annotation file.
        '''

        if not os.path.isfile(fpath):
            raise Exception('"{}" is not a file'.format(fpath))

        lines = None
        with open(fpath) as f:
            lines = [l.strip().split() for l in f.readlines()]

        annotations = []
        for l in lines:
            l = [x.strip() for x in l]
            if len(l) < 5:
                raise Exception('Failed to parse line "{}"'.format(l))

            rect = [float(s) for s in l[:5]]

            annotations.append((tuple(rect[0:2]), tuple(rect[2:4]), rect[4]))

        return annotations


for i in range(1, 166):
    bb_path = base_path + str(i) + '/'
    
    frame = np.zeros(original_size)
    original_image = cv2.imread(bb_path + 'rec1.jpg', cv2.IMREAD_UNCHANGED)
    
    annotation_path = bb_path + 'rec1-annot.txt'
    
    annotations = get_annotations(annotation_path)
    
    for a in annotations:
        #print(l)
        bp = cv2.boxPoints(a)
        bp = np.int0(bp)
        cv2.drawContours(original_image, [bp], 0, (0, 255, 0), 2)
        cv2.drawContours(frame, [bp], -1, (255), -1)
    
    # cv2.imshow('Detection result', original_image)
    cv2.imwrite(bb_path + 'ground_truth.jpg', original_image)
    cv2.imwrite(bb_path + 'ground_truth_bw.jpg', frame)
    
    # cv2.waitKey(0)

    # cv2.destroyAllWindows()
    
    pixel_area = np.sum(frame/255)
    
    print(str(i) + ' - pixel area = ' + str(int(pixel_area)))
    
    f = open(bb_path + 'gt_pixel_area.txt', 'w')
    f.write(str(int(pixel_area)))
    f.close()

