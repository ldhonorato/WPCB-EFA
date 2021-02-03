# WPCB-EFA
Repository of Waste Printed Circuit Board Economic Feasibility Assessment (WPCB-EFA).

**A complete paper of WPCB-EFA will be available soon!**

TODO: Description of WPCB-EFA

## Dataset

This work uses the PCB DSRL public dataset. The PCB DSRL dataset can be downloaded [here](https://cvl.tuwien.ac.at/research/cvl-databases/pcb-dslr-dataset/). The following paper presents the dataset with more details:

C. Pramerdorfer and M. Kampel, “A dataset for computer-vision-based PCB analysis,” in 2015 14th IAPR International Conference on Machine Vision Applications (MVA), Tokyo, Japan, 2015, pp. 378–381, doi: 10.1109/MVA.2015.7153209 [Online]. Available: http://ieeexplore.ieee.org/document/7153209/.

### Data Preparation

The fist step is to apply a sliding window to split the original PCB DSLR dataset into small chunks. For this purpose, run the /src/pre-processing/split_dataset_images.py script. Use the help (-h) to see the script parameters and usage.

## Transfer learning from pre-training YOLO

This work uses YOLOv3 implementation that can be founded in https://github.com/wizyoung/YOLOv3_TensorFlow.
Fist step is to clone the repository and download and convert the weights as decribed [here](https://github.com/wizyoung/YOLOv3_TensorFlow#3-weights-convertion).

### Generate YOLO annotation

Use the script /src/dataset-spliting/generate_yolo_annotation.split.py to generate the YOLOv3 annotation files in a properly format. Check the script help for more specific details.

TODO: Finish this


## Running WPCB-EFA

With the IC object detetor trained, use the scipt /scr/post-processing/evaluate_full_pcb.py to apply the trained model into full size WPCB images from the PCB DSLR dataset. This script saves the raw image for each file and a csv file with coordinates and scores for each bouding box.

![](https://github.com/ldhonorato/WPCB-EFA/blob/main/example-pcb6/rec1.jpg | width=100 "Original PCB 6 iamge") !![](https://github.com/ldhonorato/WPCB-EFA/blob/main/example-pcb6/raw_yolo.jpg | width=100 "Raw YOLO Prediction")

The CSV file for the example above can be founded at /example/bb_file.csv

After IC detection is done, we need to calculate the IC pixel area. Use the sprit /src/post-processing/calulate_YOLO_PixelArea.py to calculate the pixel area of YOLO output. It uses the csv file described above and saves the calculated value into a text file (yolo_pixel_area.txt).

In order to compare with the ground truth area, we need to calculate the IC area with the annotation from the PCB DSLR dataset. To do this, use the script /src/post-processing/calculate_GT_IC_PixelArea.py. It works in a similar way of the scrit to calculate YOLO pixel area and it generates the ground truth bounding boxes applied to the image (ground_truth.jpg), the bounding boxes mask (ground_truth_bw.jpg) and a text file with the sum of the area from all bounding boxes.

## Evaluating WPCB-EFA

With all the outputs decribed above, the scrit /src/post-processing/compare_area_plot_grafics.py builds a dataframe with the calculated IC area from YOLO prediction and Ground Truth for each WPCB image form the PCB DSLR dataset. It alsos apply the image scale to convert to mm², convert the IC area to weight (using the estimated IC surface density), and build some graphics to evaluate the results.
