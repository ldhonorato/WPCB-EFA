#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:52:36 2020

@author: lhss
"""

import numpy as np
import cv2

original_size = (3280, 4928)

score_threshold = 0.8

base_path = '/home/lhss/Documents/Artigo_PDI/database/original dataset pcbs/pcb'

for i in range(1, 166):
    bb_path = base_path + str(i) + '/'
    
    frame = np.zeros(original_size)
    
    f = open(bb_path + 'bb_file.csv', 'r')
    
    lines = f.readlines()
    
    for l in lines[1:]:
        #print(l)
        x0, y0, x1, y1, score = l.split(',')
        
        if float(score) > score_threshold:
            x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
            
            c1, c2 = (int(round(x0)), int(round(y0))), (int(round(x1)), int(round(y1)))
            
            cv2.rectangle(frame, c1, c2, (255), thickness=cv2.FILLED)
            
        #plot_one_box(frame, [x0, y0, x1, y1], label=None, color=(255), line_thickness=2)
    
        # x0, y0, x1, y1 = float(x0), float(y0), float(x1), float(y1)
        # x0, y0, x1, y1 = int(round(x0)), int(round(x1)), int(round(y0)), int(round(y1))
        # if float(score) > score_threshold:
        #     frame[x0:x1,y0:y1] = 255
            # cv2.rectangle(frame,(int(x0),int(y0)),(int(x1),int(y1)),(255,255,255),cv2.FILLED)
    
    #cv2.imshow('Detection result', frame)
    cv2.imwrite(bb_path + 'yolo_area.jpg', frame)
    
    
    pixel_area = np.sum(frame/255)
    
    print(str(i) + ' - pixel area = ' + str(int(pixel_area)))
    
    f = open(bb_path + 'yolo_pixel_area.txt', 'w')
    f.write(str(int(pixel_area)))
    f.close()
    

# cv2.waitKey(0)

# cv2.destroyAllWindows()
