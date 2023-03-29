import os
import cv2
import argparse

parser = argparse.ArgumentParser(description='Convert image sequence to video')
parser.add_argument('--image_dir', type=str, required=True, help='Path to directory containing image sequence')
parser.add_argument('--prefix', type=str, default='', help='Prefix of the image file name (optional)')
parser.add_argument('--out_filename', type=str, required=True, help='Output file name (with extension)')
args = parser.parse_args()

# get the list of image files
image_files = sorted([os.path.join(args.image_dir, f) for f in os.listdir(args.image_dir) if f.startswith(args.prefix)])

# read the first image to get frame size
frame = cv2.imread(image_files[0])
height, width, channels = frame.shape

# initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(args.out_filename, fourcc, 15, (width, height))

# loop through the image files and write to video
for file in image_files:
    frame = cv2.imread(file)
    video_writer.write(frame)

# release resources
video_writer.release()
cv2.destroyAllWindows()
