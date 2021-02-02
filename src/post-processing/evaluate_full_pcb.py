#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 10:59:51 2020

@author: lhss
"""

import numpy as np
import argparse
import cv2

from utils.misc_utils import parse_anchors, read_class_names
from utils.nms_utils import gpu_nms
from utils.plot_utils import plot_one_box
#from utils.data_aug import letterbox_resize

import tensorflow as tf

from model import yolov3

def sliding_window(image, y_offset=880, step=208, ws=(416,416)):
	# slide a window across the image
	for y in range(0, image.shape[0] - ws[0], step):
		for x in range(y_offset, image.shape[1] - ws[1], step):
			# yield the current window
			yield (x, y, image[y:y + ws[1], x:x + ws[0]])


parser = argparse.ArgumentParser(description="YOLO-V3 test full pcb image")
# parser.add_argument("input_image", type=str,
#                     help="The path of the input image.")
parser.add_argument("--anchor_path", type=str, default="./data/my_data/yolo_anchors.txt",
                    help="The path of the anchor txt file.")
parser.add_argument("--class_name_path", type=str, default="./data/my_data/data.names",
                    help="The path of the class names.")
parser.add_argument("--restore_path", type=str, default="./data/my_data/checkpoint/model-epoch_130_step_70084_loss_0.0919_lr_1e-05",
                    help="The path of the weights to restore.")
args = parser.parse_args()



args.anchors = parse_anchors(args.anchor_path)
args.classes = read_class_names(args.class_name_path)
num_class = 1


#path_image = '/home/lhss/Documents/Artigo_PDI/database/cvl_pcb_dslr_2/pcb24/rec1.jpg'
database_path = '/home/lhss/Documents/Artigo_PDI/database/original dataset pcbs/'

with tf.Session() as sess:
    
    input_data = tf.placeholder(tf.float32, [1, 416, 416, 3], name='input_data')
    yolo_model = yolov3(num_class, args.anchors)
    with tf.variable_scope('yolov3'):
        pred_feature_maps = yolo_model.forward(input_data, is_training=False, reuse=False)
            
    pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)

    pred_scores = pred_confs * pred_probs

    boxes, scores, labels = gpu_nms(pred_boxes, pred_scores, num_class, max_boxes=200, score_thresh=0.3, nms_thresh=0.45)

    saver = tf.train.Saver()
    saver.restore(sess, args.restore_path)
    
    for i in range(1,166):
        
        print(i)
        pcb_path = database_path + 'pcb' + str(i)
        
        image = cv2.imread(pcb_path + '/rec1.jpg')    
        all_boxes = []
        all_scores = []
        all_labels = []
        for (x, y, img_ori) in sliding_window(image):
            #print(img_ori.shape)
            img = img_ori.copy()
            # img = cv2.cvtpcb_pathColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = np.asarray(img, np.float32)
            img = img[np.newaxis, :] / 255.
            
            boxes_, scores_, labels_ = sess.run([boxes, scores, labels], feed_dict={input_data: img})
            #cv2.imshow('Detection result', img)
            #cv2.waitKey(0)
    
            if len(boxes_) > 0:
                # print("box coords:")
                # print(boxes_)
                # print('*' * 30)
                # print("scores:")
                # print(scores_)
                # print('*' * 30)
                # print("labels:")
                # print(labels_)
                
                # all_scores.append(scores_)
                # all_boxes.append(boxes_)
                # all_labels.append(labels_)
                
                for i in range(len(boxes_)):
                    x0, y0, x1, y1 = boxes_[i]
                    all_boxes.append((x0+x, y0+y, x1+x, y1+y))
                    all_scores.append(scores_[i])
                    all_labels.append(labels_[i])
                    
                    #plot_one_box(img_ori, [x0, y0, x1, y1], label=args.classes[labels_[i]] + ', {:.2f}%'.format(scores_[i] * 100), color=(255, 0, 0), line_thickness=2)
                
                # print(len(all_boxes))
                # if all_boxes == None:
                #     print('aqui!!!')
                #     all_boxes = tf.identity(boxes_)
                #     all_scores = tf.identity(scores_)
                #     all_labels = tf.identity(labels_)
                # else:
                #     all_boxes = tf.concat([all_boxes, boxes_], 0)
                #     all_scores = tf.concat([all_scores, scores_], 0)
                #     all_labels = tf.concat([all_labels, labels_], 0)
                # 
            #plot_one_box(img_ori, [x0, y0, x1, y1], label=args.classes[labels_[i]] + ', {:.2f}%'.format(scores_[i] * 100), color=color_table[labels_[i]])
            #cv2.imshow('Detection result', img_ori)
            #cv2.imwrite('detection_result.jpg', img_ori)
            #cv2.waitKey(0)
        
        #print(all_boxes)
        bb_file = open(pcb_path + '/bb_file.csv', 'w')
        bb_file.write('x0,y0,x1,y1,score\r\n')
        for i in range(len(all_boxes)):
            # print('='*20)
            # print(i)
            # print(all_boxes[i])
            x0, y0, x1, y1 = all_boxes[i]
            bb_file.write(str(x0) + ',' + str(y0) + ',' + str(x1) + ',' + str(y1) + ',' + str(all_scores[i]) + '\r\n')
            plot_one_box(image, [x0, y0, x1, y1], label=args.classes[all_labels[i]] + ', {:.2f}%'.format(all_scores[i] * 100), color=(255, 0, 0), line_thickness=2)
    
        bb_file.close() 
        #cv2.imshow('Detection result', image)
        cv2.imwrite(pcb_path + '/raw_yolo.jpg', image)
    
        #cv2.waitKey(0)
    
        #cv2.destroyAllWindows()