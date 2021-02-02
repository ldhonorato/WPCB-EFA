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
import shutil

def del_and_create_folder(destPath):
    if os.path.exists(destPath) and os.path.isdir(destPath):
       shutil.rmtree(destPath)
    
    os.mkdir(destPath)

if __name__ == "__main__":
    # parse args

    parser = argparse.ArgumentParser(description='Gera pasta de para treino e teste')
    parser.add_argument('--root', type=str, dest='root', default='PCBs_512', help='Path para PCB DSLR dataset dividido')
    #parser.add_argument('--out', type=str, dest='fileoutput', default='full_base_quadrantes.txt', help='Path para PCB DSLR dataset')
    parser.add_argument('--testPCBs', type=str, dest='numberTestPCBs', default=33, help='Numero de PCBs para teste')
    #parser.add_argument('--testOut', type=str, dest='text_fileoutput', default='test_quadrantes.txt', help='Path para arquivo de teste')
    
    args = parser.parse_args()
#    
#    fileoutput = '/home/lhss/Documents/Artigo_PDI/database/yolo_annotation3.txt'
    root = args.root
    #root = '/home/lhss/Documents/Artigo_PDI/database/PCBs_512'
    
    list_folders = [os.path.join(root, name) for name in os.listdir(root) if os.path.isdir(os.path.join(root, name))]
    list_folders.sort()
    
    pcbs_test = random.choices(list_folders, k=args.numberTestPCBs)
    #pcbs_test = ['/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb130', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb139', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb35', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb49', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb156', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb100', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb113', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb46', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb94', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb92', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb157', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb73', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb73', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb158', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb49', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb77', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb29', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb83', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb65', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb11', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb109', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb103', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/Teste', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb56', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb118', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb140', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/Teste', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/Teste', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb80', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb161', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb87', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb103', 
    #              '/home/lhss/Documents/Artigo_PDI/database/PCBs_512/pcb136']
    
    print(pcbs_test)
    
    train_path = os.path.join(root, 'Treino')
    test_path = os.path.join(root, 'Teste')
    
    del_and_create_folder(train_path)
    del_and_create_folder(test_path)
    
    for folder in list_folders:
        pcb_imgs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.jpg') and 'annot' not in f]
#        pcb_folders.sort()
        for imgPath in pcb_imgs:
            annotPath = imgPath[:-3] + 'csv'
            
            if folder in pcbs_test:
                shutil.copy(imgPath, test_path)
                shutil.copy(annotPath, test_path)
                
            else:
                shutil.copy(imgPath, train_path)
                shutil.copy(annotPath, train_path)
                        
    
