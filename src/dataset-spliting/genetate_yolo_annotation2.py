import cv2
import numpy as np

import os
import os.path
import argparse

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
#            text = '' if len(l) == 5 else ' '.join(l[5:])

#            sz = (rect[2]/87.4, rect[3]/87.4)
#            asp = max(sz[0], sz[1]) / min(sz[0], sz[1])
#            sz = sz[0]*sz[1]

            annotations.append((tuple(rect[0:2]), tuple(rect[2:4]), rect[4]))

        return annotations


def crop_mask(mask_path, img_path):
    '''
    Return (and cache) information for auto cropping a PCB image.
    rec: desired recording (see recordings()).
    '''
    
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    cnt, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(cnt) > 1:  # use largest region if there are multiple
        def cntsz(c):
            rr = cv2.minAreaRect(c)
            return rr[1][0]*rr[1][1]

        cnt = sorted(cnt, key=cntsz, reverse=True)

    cx, cy, cw, ch = cv2.boundingRect(cnt[0])
    ci = (cx, cy, cw, ch)
    
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    
    img = img[ci[1]:ci[1]+ci[3], ci[0]:ci[0]+ci[2]]
    
    return img
#    return  (cx, cy, cw, ch)


if __name__ == "__main__":
    # parse args

#    parser = argparse.ArgumentParser(description='Gera arquivo de anotacoes para YOLOv3')
#    parser.add_argument('--root', type=str, dest='root', required=True, help='Path para PCB DSLR dataset')
#    parser.add_argument('--out', type=str, dest='out', default='annotation.txt', help='Path para PCB DSLR dataset')
#    args = parser.parse_args()
#    
    fileoutput = '/home/lhss/Documents/Artigo_PDI/database/yolo_annotation2.txt'
    file = open(fileoutput,'w+')
    index = 0
    root = '/home/lhss/Documents/Artigo_PDI/database'
    list_folders = [os.path.join(root, 'cvl_pcb_dslr_'+str(i)) for i in range(1,9)]
    
    for folder in list_folders:
        pcb_folders = [os.path.join(folder, f) for f in os.listdir(folder) if f.startswith('pcb') and os.path.isdir(os.path.join(folder, f))]
        pcb_folders.sort()
        for p in pcb_folders:
            
            rec_ids = [int(os.path.splitext(r)[0][3:]) for r in os.listdir(p) if r.startswith('rec') and r.endswith('.jpg') and 'mask' not in r]
            
            for rec in rec_ids:
                rpath = os.path.join(p, 'rec{}.jpg'.format(rec))
                fpath = os.path.join(p, 'rec{}-annot.txt'.format(rec))
                
                img = cv2.imread(rpath, cv2.IMREAD_GRAYSCALE)
                img_dim = img.shape
                
                line = '{index} {path} {dim_x} {dim_y}'.format(index=index, 
                            path=rpath, 
                            dim_x = img_dim[1],
                            dim_y = img_dim[0])
                
                annotations = get_annotations(fpath)
                
                component = ''
                for n in annotations:
                    bp = cv2.boxPoints(n)
                    bp = np.int0(bp)
                    
                    max_x = bp[:,0].max()
                    min_x = bp[:,0].min()
                    
                    max_y = bp[:,1].max()
                    min_y = bp[:,1].min()
                    
                    component += ' {classe} {x_min} {y_min} {x_max} {y_max}'.format(classe = 0,
                                 x_min = min_x,
                                 y_min = min_y,
                                 x_max = max_x,
                                 y_max = max_y)
                    
                    
                
                index += 1
                if len(component) > 0:
                    line = line + component + '\r\n'
                    print(index)
                    file.write(line)
                    
                    
    file.close()
                    
#                rmaskpath = os.path.join(p, 'rec{}-mask.png'.format(rec))
                
#                img_cropped = crop_mask(rmaskpath, rpath)
#                filename = 'rec{}-masked.jpg'.format(rec)
#                cv2.imwrite(filename, img_cropped)
                
                
        
    
    