import os
import cv2
import argparse
import torch
from multiprocessing import Pool
from tqdm import tqdm

# Define the threshold areas for big, medium, and small objects
big_thresh = 1850
medium_thresh = 756
small_thresh = 420

parser = argparse.ArgumentParser(description='Split dataset based on object size')
parser.add_argument('--img_dir', type=str, default='./images', help='path to directory containing images')
parser.add_argument('--ann_dir', type=str, default='./labels', help='path to directory containing annotations')
parser.add_argument('--num_workers', type=int, default=4, help='number of worker processes to use')
parser.add_argument('--device', type=str, default='cpu', help='device to use for processing (cpu or cuda)')
args = parser.parse_args()

# Create new directories for the output images and annotations
os.makedirs('output/big', exist_ok=True)
os.makedirs('output/medium', exist_ok=True)
os.makedirs('output/small', exist_ok=True)
os.makedirs('output/tiny', exist_ok=True)

# Initialize the device for processing images
if args.device == 'cuda' and torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

def process_image(file_path):
    root, img_file = file_path
    if img_file.endswith('.jpg') or img_file.endswith('.jpeg') or img_file.endswith('.png'):
        img_path = os.path.join(root, img_file)
        ann_path = os.path.join(args.ann_dir, os.path.basename(root), os.path.splitext(img_file)[0] + '.txt')
        if not os.path.isfile(ann_path):
            return

        # Read the image and its dimensions
        img = cv2.imread(img_path)
        height, width, _ = img.shape

        # Parse the annotation file and loop over each bounding box
        with open(ann_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            cls, x, y, w, h = map(float, line.strip().split())

            # Calculate the bounding box coordinates based on the percentage of the image dimensions
            x = int(x * width)
            y = int(y * height)
            w = int(w * width)
            h = int(h * height)

            # Calculate the area of the bounding box
            bbox_area = w * h

            # Classify the object based on its size
            if bbox_area > big_thresh:
                out_dir = 'output/big'
            elif bbox_area > medium_thresh:
                out_dir = 'output/medium'
            elif bbox_area > small_thresh:
                out_dir = 'output/small'
            else:
                out_dir = 'output/tiny'

            # Write the image and annotation to the appropriate output directory
            out_img_path = os.path.join(out_dir, os.path.basename(root), img_file)
            out_ann_path = os.path.join(out_dir, os.path.basename(root), os.path.splitext(img_file)[0] + '.txt')
            os.makedirs(os.path.dirname(out_img_path), exist_ok=True)
            os.makedirs(os.path.dirname(out_ann_path), exist_ok=True)
            cv2.imwrite(out_img_path, img)
            with open(out_ann_path, 'a') as f:
                f.write(f'{cls} {x} {y} {w} {h}\n')

# Loop over each image and its corresponding annotation file in parallel
with Pool(args.num_workers) as p:
    # Get the list of all image files
    all_files = []
    for root, dirs, files in os.walk(args.img_dir):
        all_files += [(root, img_file) for img_file in files]

    # Use tqdm to show a progress bar
    with tqdm(total=len(all_files), desc='Processing images') as pbar:
        for i, _ in enumerate(p.imap_unordered(process_image, all_files)):
            pbar.update()

