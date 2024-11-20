"""
This script copies images and visualized images that contain specified classes to a temporary folder.

Example usage:
* `python select_dataset.py --included_classes tilt`
* `python select_dataset.py --included_classes led particle flip Particle_Big marked`
"""

import os
import json
import shutil
import argparse

# Define paths
json_file = './original/annotations/instance.json'
images_folder = './original/images'
vis_images_folder = './visualized'
tmp_folder = './selected'
tmp_images_folder = os.path.join(tmp_folder, 'original')
tmp_vis_folder = os.path.join(tmp_folder, 'visualized')

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Copy images with specified classes.')
parser.add_argument('--included_classes', nargs='+', required=True, help='List of class names to include.')
args = parser.parse_args()

included_classes = set(args.included_classes)

# Load the JSON data
with open(json_file, 'r') as f:
    data = json.load(f)

# If .tmp folder exists, delete it
if os.path.exists(tmp_folder):
    shutil.rmtree(tmp_folder)

# Create .tmp/images and .tmp/vis_images folders if they don't exist
os.makedirs(tmp_images_folder, exist_ok=True)
os.makedirs(tmp_vis_folder, exist_ok=True)

# Map category IDs to names and vice versa
category_id_to_name = {cat['id']: cat['name'] for cat in data['categories']}
category_name_to_id = {cat['name']: cat['id'] for cat in data['categories']}

# Filter category IDs based on included classes
included_category_ids = {category_name_to_id[name] for name in included_classes if name in category_name_to_id}

# Collect image IDs that contain the specified classes
image_ids_to_copy = set()
for ann in data['annotations']:
    if ann['category_id'] in included_category_ids:
        img_id = ann['image_id']
        image_ids_to_copy.add(img_id)

# Process each image
for img_info in data['images']:
    img_id = img_info['id']
    img_filename = img_info['file_name']

    if img_id not in image_ids_to_copy:
        continue

    # Paths to source and destination images
    img_path = os.path.join(images_folder, img_filename)
    tmp_image_path = os.path.join(tmp_images_folder, img_filename)

    # Copy image to .tmp/images
    if os.path.exists(img_path):
        shutil.copy(img_path, tmp_image_path)
    else:
        print(f"Image {img_filename} not found in {images_folder}, skipping...")

    # Paths to source and destination visualized images
    vis_img_path = os.path.join(vis_images_folder, img_filename)
    tmp_vis_image_path = os.path.join(tmp_vis_folder, img_filename)

    # Copy visualized image to .tmp/vis_images
    if os.path.exists(vis_img_path):
        shutil.copy(vis_img_path, tmp_vis_image_path)
    else:
        print(f"Visualized image {img_filename} not found in {vis_images_folder}, skipping...")

    print(f"Processed and copied image: {img_filename}")

print("Processing completed!")
