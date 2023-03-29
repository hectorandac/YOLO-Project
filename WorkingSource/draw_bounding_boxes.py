import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Draw bounding boxes on an image based on YOLO format annotations.')
parser.add_argument('--image', required=True, help='Path to the input image file.')
parser.add_argument('--output', required=True, help='Path to the output image file.')
args = parser.parse_args()

# Load the input image
img = cv2.imread(args.image)

# Load the corresponding annotation file
ann_file = args.image.replace('.jpg', '.txt').replace('.jpeg', '.txt').replace('.png', '.txt')
with open(ann_file, 'r') as f:
    lines = f.readlines()

# Draw the bounding boxes on the image
for line in lines:
    cls, x, y, w, h = map(float, line.strip().split())
    height, width, _ = img.shape
    left = int((x - w/2))
    top = int((y - h/2))
    right = int((x + w/2))
    bottom = int((y + h/2))
    print(left)
    print(top)
    print(right)
    print(bottom)
    cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 3)

# Save the output image
cv2.imwrite(args.output, img)
