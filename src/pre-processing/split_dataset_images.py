#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:32:00 2019

@author: lhss
"""

import numpy as np
import os
import cv2
import json

def get_annotations(fpath):
        '''
        Returns a list of IC chips as a list from annotation file.
        rec: desired recording (see recordings()).
        cropped: whether to return coordinates for cropped images (see image_masked()).
        size: (min, max) size of returned ICs in cm^2, disregarding the scale factor (0 = all).
        aspect: (min, max) aspect ratio of returned ICs (0 = all).
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
        
        vertices = [cv2.boxPoints(n) for n in annotations]
        vertices = np.array(vertices)
        vertices = np.int0(vertices)
        
        return annotations, vertices


def calculateIntersection_1D(a0, a1, b0, b1):
    if a0 >= b0 and a1 <= b1: # Contained
        intersection = a1 - a0
    elif a0 < b0 and a1 > b1: # Contains
        intersection = b1 - b0
    elif a0 < b0 and a1 > b0: # Intersects right
        intersection = a1 - b0
    elif a1 > b1 and a0 < b1: # Intersects left
        intersection = b1 - a0
    else: # No intersection (either side)
        intersection = 0

    return intersection


def has_intersection(img_piece_points, annotation_vertice, offset=0.3):
    '''
    Returns a True if the percentage of intersection between image crop and annotation is bigger than offset.
    img_piece_points: tuple (start_x, start_y, end_x, end_y)
    annotation_vertice: numpy.ndarray (4,2) - 4 points, each point with 2 dimentions
    '''
    
    (start_x, start_y, end_x, end_y) = img_piece_points
    
    obj_max_x = annotation_vertice[:,0].max()
    obj_min_x = annotation_vertice[:,0].min()
    
    obj_max_y = annotation_vertice[:,1].max()
    obj_min_y = annotation_vertice[:,1].min()
    
    obj_area = (obj_max_x - obj_min_x) * (obj_max_y - obj_min_y)
    
    x_intersection = calculateIntersection_1D(start_x, end_x, obj_min_x, obj_max_x)
    y_intersection = calculateIntersection_1D(start_y, end_y, obj_min_y, obj_max_y)
    
    intersection_area = x_intersection * y_intersection
    
    return (intersection_area/obj_area) > offset
    

def get_new_vertices(img_piece_points, annotation_vertice):
    (start_x, start_y, end_x, end_y) = img_piece_points
    
    obj_max_x = annotation_vertice[:,0].max()
    obj_min_x = annotation_vertice[:,0].min()
    
    obj_max_y = annotation_vertice[:,1].max()
    obj_min_y = annotation_vertice[:,1].min()
    
    dim_x = end_x - start_x
    dim_y = end_y - start_y
    
    #calculate x
    new_min_x = max(obj_min_x - start_x, 0)
    new_max_x = min(obj_max_x - start_x, dim_x)
    
    #calculate y
    new_min_y = max(obj_min_y - start_y, 0)
    new_max_y = min(obj_max_y - start_y, dim_y)
    
    start_point = (new_min_x, new_min_y)
    end_point = (new_max_x, new_max_y)
    return start_point, end_point
    
def image_split(img_path, annot_vertices ,dim=(416,416), stride=(208,208), new_dataset_dir='PCBs_splited_416'):
#def image_split(img_path, annot_vertices ,dim=(512,512), stride=(256,256), new_dataset_dir='PCBs_splited_512'):
    pcb_id = img_path.split('/')[-2]
    new_dataset_dir = os.path.join(new_dataset_dir, pcb_id)
    
    if not os.path.exists(new_dataset_dir):
        os.makedirs(new_dataset_dir)
    
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
    print(pcb_id)
    
    index = 1
    for y in range(0, img.shape[0], stride[0]):
        for x in range(0, img.shape[1], stride[1]):
            y_inicial = y
            x_inicial = x
            
            y_final = y_inicial + dim[0]
            x_final = x_inicial + dim[1]
            
            if(y_final > img.shape[0]):
                y_final = img.shape[0]
                y_inicial = y_final-dim[0]
            
            if(x_final > img.shape[1]):
                x_final = img.shape[1]
                x_inicial = x_final-dim[1]
            
#            print('================================================')
#            print('Index = ', index)
#            print('x_inicial = ', x_inicial)
#            print('x_final = ', x_final)
#            print('y_inicial = ', y_inicial)
#            print('y_final = ', y_final)
            
            img_piece_points = (x_inicial, y_inicial, x_final, y_final)
            
            crop = img[y_inicial:y_final,x_inicial:x_final,:]
            imagem_com_retangulos = np.copy(crop)
            
            
            new_vertices = []
            
            for v in annot_vertices:
                if has_intersection(img_piece_points, v):
                    start_point, end_point = get_new_vertices(img_piece_points, v)
                    imagem_com_retangulos = cv2.rectangle(imagem_com_retangulos, start_point, end_point, (0, 255, 255), 2)
                    new_vertices.append([start_point, end_point])
#                    print(v)
            
            
            data = {}
            data['version'] = "1.0"
            data['flags'] = {}
            data['shapes'] = []
           
            data['imageHeight'] = dim[0]
            data['imageWidth'] = dim[1]
            #csv_header = "filename,width,height,class,xmin,ymin,xmax,ymax\r\n"
            if len(new_vertices) > 0:
                file_name = pcb_id +'_' + str(index)
                data['imagePath'] = file_name + '.jpg'
                annotation_file = file_name + '.txt'
                #csv_annotation_fie = file_name + '.csv'
                
                #csv_file = open(os.path.join(new_dataset_dir, csv_annotation_fie),'w+')
                #csv_file.write(csv_header)
                file = open(os.path.join(new_dataset_dir, annotation_file),'w+')
                for v in new_vertices:
                    #print(v)
                    x_min=v[0][0]
                    y_min=v[0][1]
                    x_max = v[1][0]
                    y_max = v[1][1]
                    
                    shape = {}
                    shape['label'] = "IC"
                    shape['line_color'] = None
                    shape['fill_color'] = None
                    shape['points'] = [ [int(x_min), int(y_min)], [int(x_max), int(y_max)] ]
                    shape["shape_type"] = "rectangle"
                    shape["flags"] = {}
                    line = '{x_min} {y_min} {x_max} {y_max}\r\n'.format(
                            x_min=v[0][0], 
                            y_min=v[0][1], 
                            x_max = v[1][0],
                            y_max = v[1][1])
                    
                    file.write(line)
                    #csv_annotation_str = '{filename},{width},{height},{classe},{x_min},{y_min},{x_max},{y_max}\r\n'.format(
                    #        filename = data['imagePath'], 
                    #        width = data['imageWidth'], 
                    #        height = data['imageHeight'],
                    #        classe = "IC",
                    #        x_min = x_min, 
                    #        y_min = y_min, 
                    #        x_max = x_max,
                    #        y_max = y_max)
                    #csv_file.write(csv_annotation_str)
                    
                    data['shapes'].append(shape)
                file.close()
                #csv_file.close()
                
                
                #annotation_file = file_name + '.json'
                #outfile = open(os.path.join(new_dataset_dir, annotation_file),'w+')
                #with open(os.path.join(new_dataset_dir, annotation_file),'w+') as outfile:
                    #json.dump(data, outfile, indent=4, sort_keys=True)
                
                
                cv2.imwrite(os.path.join(new_dataset_dir, file_name + '.jpg'), crop)
                #cv2.imwrite(os.path.join(new_dataset_dir, file_name + '_annot.jpg'), imagem_com_retangulos)
                
                index += 1

if __name__ == "__main__": 
    root = '/home/lhss/Documents/Artigo_PDI/database/PCB DSLR'
    
    list_folders = [os.path.join(root, 'cvl_pcb_dslr_'+str(i)) for i in range(1,9)]
    
    for folder in list_folders:
        pcb_folders = [os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('pcb') and os.path.isdir(os.path.join(folder, f))]
        pcb_folders.sort()
        for p in pcb_folders:
            
            rpath = os.path.join(p, 'rec1.jpg')
            fpath = os.path.join(p, 'rec1-annot.txt')
            
            _, annot_vertices = get_annotations(fpath)
            image_split(rpath, annot_vertices)
            
#    img_path = 'cvl_pcb_dslr_1/pcb2/rec1.jpg'
#    fpath = 'cvl_pcb_dslr_1/pcb2/rec1-annot.txt'
#    _, annot_vertices = get_annotations(fpath)
#    image_split(img_path, annot_vertices)
