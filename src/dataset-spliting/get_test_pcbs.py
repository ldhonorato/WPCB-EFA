#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 13:47:42 2020

@author: lhss
"""

f_test_path = '/home/lhss/Documents/Artigo_PDI/YOLOv3_TensorFlow/data/my_data/test.txt'

f = open(f_test_path, 'r')

lines = f.readlines()

pcbs_dic = {}
for l in lines:
    p = l.split()[1].split('/')[-2]
    
    
    pcbs_dic[p] = pcbs_dic.get(p, 0) + 1

print(sorted(pcbs_dic.keys()))
print(len(pcbs_dic.keys()))


f_test_path = '/home/lhss/Documents/Artigo_PDI/YOLOv3_TensorFlow/data/my_data/train.txt'

f = open(f_test_path, 'r')

lines = f.readlines()

pcbs_dic = {}
for l in lines:
    p = l.split()[1].split('/')[-2]
    
    
    pcbs_dic[p] = pcbs_dic.get(p, 0) + 1

print(sorted(pcbs_dic.keys()))
print(len(pcbs_dic.keys()))
