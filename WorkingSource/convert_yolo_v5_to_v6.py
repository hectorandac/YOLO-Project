import os
import cv2
import argparse
from multiprocessing import Pool
from tqdm import tqdm

# set up command-line arguments
parser = argparse.ArgumentParser(description='Convert annotation format for YOLOv5')
parser.add_argument('--root', required=True, help='path to root directory')
args = parser.parse_args()

# set the path to the root directory
root = args.root

# set the subdirectories for the images and annotations
image_subdirs = ['images/train', 'images/test', 'images/val']
annotation_subdirs = ['labels/train', 'labels/test', 'labels/val']

def process_file(filename):
    # get the image path
    image_path = os.path.join(image_folder, filename)

    # get the annotation path
    annotation_filename = os.path.splitext(filename)[0] + '.txt'
    annotation_path = os.path.join(annotation_folder, annotation_filename)

    # check if the annotation file exists
    if os.path.exists(annotation_path):
        # open the annotation file
        with open(annotation_path, 'r') as f:
            lines = f.readlines()

        # open the annotation file for writing
        with open(annotation_path, 'w') as f:
            # get the image width and height for the annotation file
            image = cv2.imread(image_path)
            image_height, image_width, _ = image.shape

            for line in lines:
                # split the line into parts
                parts = line.strip().split(' ')

                # convert the first column to 0
                parts[0] = '0'

                # convert the x, y, w, h values to percentage values
                x_center = float(parts[1]) / image_width
                y_center = float(parts[2]) / image_height
                width = float(parts[3]) / image_width
                height = float(parts[4]) / image_height

                # write the modified line to the file
                f.write(' '.join([str(round(x, 6)) for x in [0, x_center, y_center, width, height]]) + '\n')

# loop through the subdirectories
for image_subdir, annotation_subdir in zip(image_subdirs, annotation_subdirs):
    # set the path to the folder containing the image files
    image_folder = os.path.join(root, image_subdir)

    # set the path to the folder containing the annotation files
    annotation_folder = os.path.join(root, annotation_subdir)

    # get a list of image files in the folder
    image_files = [filename for filename in os.listdir(image_folder) if filename.endswith('.png') or filename.endswith('.jpg')]

    # process the files in parallel
    with Pool() as p:
        list(tqdm(p.imap(process_file, image_files), total=len(image_files), desc=f"Processing {image_subdir} files", ncols=80))
