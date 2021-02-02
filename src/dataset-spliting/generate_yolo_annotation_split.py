#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 17:32:24 2019

@author: lhss
"""

import cv2
import numpy as np

import os
import argparse
import random

if __name__ == "__main__":
    # parse args

    parser = argparse.ArgumentParser(description='Gera arquivo de anotacoes para YOLOv3 do dataset dividido')
    parser.add_argument('--root', type=str, dest='root', default='PCBs', help='Path para PCB DSLR dataset dividido')
    parser.add_argument('--out', type=str, dest='fileoutput', default='full_base_quadrantes.txt', help='Path para PCB DSLR dataset')
    parser.add_argument('--testPCBs', type=str, dest='numberTestPCBs', default=0, help='Numero de PCBs para teste')
    parser.add_argument('--testOut', type=str, dest='text_fileoutput', default='test_quadrantes.txt', help='Path para arquivo de teste')
    
    args = parser.parse_args()
#    
#    fileoutput = '/home/lhss/Documents/Artigo_PDI/database/yolo_annotation3.txt'
    root = args.root
#    root = '/home/lhss/Documents/Artigo_PDI/database/PCBs'
    
    list_folders = [os.path.join(root, name) for name in os.listdir(root) if os.path.isdir(os.path.join(root, name))]
    list_folders.sort()
    
    pcbs_test = random.choices(list_folders, k=args.numberTestPCBs)
    
    index = 0
    fileoutput = args.fileoutput
    file = open(fileoutput,'w+')
    
    if args.numberTestPCBs > 0:
        test_file = open(args.text_fileoutput,'w+')
    
    for folder in list_folders:
        pcb_imgs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.jpg') and 'annot' not in f]
#        pcb_folders.sort()
        for rpath in pcb_imgs:
            fpath = rpath[:-3] + 'txt'
            img = cv2.imread(rpath, cv2.IMREAD_GRAYSCALE)
            img_dim = img.shape
            line = '{index} {path} {dim_x} {dim_y}'.format(index=index, 
                path=rpath, 
                dim_x = img_dim[1],
                dim_y = img_dim[0])
            
            with open(fpath) as f:
                annotations = [l.strip().split() for l in f.readlines()]
                            
            component = ''
            for n in annotations:
                if len(n) != 4:
                    raise Exception('Failed to parse line "{}"'.format(fpath))
                
                component += ' {classe} {x_min} {y_min} {x_max} {y_max}'.format(classe = 0,
                             x_min = n[0],
                             y_min = n[1],
                             x_max = n[2],
                             y_max = n[3])
                
                
            
            index += 1
            if len(component) > 0:
                line = line + component + '\r\n'
                print(index)
                
                if folder in pcbs_test:
                    test_file.write(line)
                else:
                    file.write(line)
                        
    if args.numberTestPCBs > 0:
        test_file.close()        
    file.close()