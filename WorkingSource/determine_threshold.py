import os
import cv2
import argparse

parser = argparse.ArgumentParser(description='Calculate object size thresholds based on bounding box areas')
parser.add_argument('--img_dir', type=str, default='./images', help='Directory containing the images')
parser.add_argument('--ann_dir', type=str, default='./labels', help='Directory containing the annotation files')
args = parser.parse_args()

# Define the directories containing the images and annotations
img_dir = args.img_dir
ann_dir = args.ann_dir

# Initialize lists to store the bounding box areas
bbox_areas = []

# Recursively loop over each file in the directory tree
for root, dirs, files in os.walk(img_dir):
    for img_file in files:
        if img_file.endswith('.jpg') or img_file.endswith('.jpeg') or img_file.endswith('.png'):
            # Look for the annotation file in the corresponding annotations subdirectory
            img_dir_rel = os.path.relpath(root, img_dir)
            ann_dir_sub = os.path.join(ann_dir, img_dir_rel)
            img_file_without_ext = os.path.splitext(img_file)[0]
            ann_file = os.path.join(ann_dir_sub, img_file_without_ext + '.txt')
            if not os.path.isfile(ann_file):
                continue

            # Read the image and its dimensions
            img_path = os.path.join(root, img_file)
            img = cv2.imread(img_path)
            height, width, _ = img.shape

            # Parse the annotation file and loop over each bounding box
            with open(ann_file, 'r') as f:
                lines = f.readlines()
            for line in lines:
                cls, x_perc, y_perc, w_perc, h_perc = map(float, line.strip().split())

                # Convert percentage values to pixel values
                x = int(x_perc * width)
                y = int(y_perc * height)
                w = int(w_perc * width)
                h = int(h_perc * height)

                # Calculate the area of the bounding box and add it to the list
                bbox_area = w * h
                bbox_areas.append(bbox_area)

# Calculate the 25th, 50th, and 75th percentile of the bounding box areas
bbox_areas.sort()
num_bboxes = len(bbox_areas)
p25 = bbox_areas[num_bboxes // 4]
p50 = bbox_areas[num_bboxes // 2]
p75 = bbox_areas[(3 * num_bboxes) // 4]

# Set the size thresholds based on the percentiles
big_thresh = p75
medium_thresh = p50
small_thresh = p25

print(f'Big object threshold: {big_thresh}')
print(f'Medium object threshold: {medium_thresh}')
print(f'Small object threshold: {small_thresh}')
