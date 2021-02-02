#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 16:49:07 2019

@author: lhss
"""

import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verifica quais PCBs nao possuem anotacoes')
    parser.add_argument('--pcbs', type=str, dest='pcbsPath', required=False, default='PCBs', help='Path para PCB DSLR dataset')
    parser.add_argument('--output', type=str, dest='file', required=False, default='empty_pcbs.txt', help='Arquivo de saída')
    args = parser.parse_args()
    
    base_path = args.pcbsPath
    pcbs_folders = [p for p in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, p))]
    
    empty_pcbs = []
    f = open(args.file, '+w')
    for p in pcbs_folders:
        if len(os.listdir(os.path.join(base_path, p))) == 0:
            empty_pcbs.append(p)
            f.write(p + '\r\n')
            
    f.write('\r\n' + str(len(empty_pcbs)))
    f.write(' PCBs sem anotacoes')
    
    f.close()
    
    
    
    print(empty_pcbs)