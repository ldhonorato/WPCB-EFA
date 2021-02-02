#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 16:52:36 2020

@author: lhss
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker

original_size = (3280, 4928)


escala_area = (7/58)**2 #1 pixel corresponde a (7/58)² mm²

base_path = '/home/lhss/Documents/Artigo_PDI/database/PCB DSLR and Results/'

pcbs = list(['pcb' + str(p) for p in range(1, 166)])

areas = np.zeros((165,2))
for i, p in enumerate(pcbs):
    f_yolo_area = base_path + p + '/yolo_pixel_area.txt'
    f_gt_area = base_path + p + '/gt_pixel_area.txt'
    
    f = open(f_yolo_area, 'r')
    yolo_area = int(f.readline())
    f.close()
    
    f = open(f_gt_area, 'r')
    gt_area = int(f.readline())
    f.close()
    
    areas[i] = [gt_area*escala_area, yolo_area*escala_area]


df = pd.DataFrame(areas, index=list(range(1,166)), columns=['GT Area', 'YOLO Area'])

percentage_error = abs((df['GT Area'] - df['YOLO Area'])) / df['GT Area']
percentage_error = percentage_error.fillna(0)
percentage_error = percentage_error.replace(np.inf, 0)
rmse = ((df['GT Area'] - df['YOLO Area'])**2)**0.5
print(rmse.mean())
print(rmse.std())

us_per_grama = 0.0001 * 68.88/1000 + 0.013887 * 31.2/1000 + 0.00644 * 331.5/1000 + 0.0105 * 411.6/1000

df_gram = df * 2.358 / 1000

df_dolar = df_gram * us_per_grama

#===============================================================
#PLOT PCB/U$
#===============================================================
# ax = df_dolar.plot.bar(figsize=(50,25), rot=90, fontsize=35)


# plt.grid()
# plt.title("PCB's IC recycling ROI", fontsize=50)
# plt.legend(fontsize=40)
# plt.ylabel("U$", fontsize=40)
# plt.xlabel("PCBs", fontsize=40)
# plt.xticks(fontsize=20)


#===============================================================
#PLOT PCB/U$ HISTOGRAM
#===============================================================
# ax = df_dolar['GT Area'].hist()

# plt.grid()
# plt.title("PCB's IC recycling ROI Histogram")
# plt.ylabel("#PCBs")
# plt.xlabel("U$")


#===============================================================
#PLOT PCB/Area mm²
#===============================================================

# ax = df.plot.bar(figsize=(50,25), rot=90, fontsize=35)

# plt.grid()
# plt.title("IC area (mm²)", fontsize=50)
# plt.ylabel("Area (mm²)", fontsize=40)
# plt.xlabel("PCBs", fontsize=40)
# plt.xticks(fontsize=20)

#===============================================================
#PLOT PCB/RMSE
#===============================================================

ax2 = rmse.plot(style='.-', figsize=(50,25), linewidth=5, markersize=30)

plt.grid(linewidth=3)
plt.title("RMSE IC area (mm²)", fontsize=80)
plt.ylabel("Error (mm²)", fontsize=60)
plt.xlabel("PCBs", fontsize=60)
plt.xticks(fontsize=60)
plt.yticks(fontsize=60)

#===============================================================
#PLOT percentage error
#===============================================================

# ax2 = percentage_error.plot(style='.-', figsize=(50,25), linewidth=5, markersize=30)

# plt.grid(linewidth=3)
# plt.title("IC Area Percentual Error ", fontsize=80)
# plt.ylabel("Error (%)", fontsize=60)
# plt.xlabel("PCBs", fontsize=60)
# plt.xticks(fontsize=60)
# plt.yticks(fontsize=60)


#===============================================================
#PLOT RMSE HISTOGRAMA
#===============================================================


# ax = rmse.hist()

# #plt.grid()
# plt.title("RMSE Histogram")
# plt.ylabel("#PCBs")
# plt.xlabel("RMSE")

