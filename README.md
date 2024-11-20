# LED Defects Detection

This repository aims to provide a comprehensive solution for detecting defects in private LED datasets using multiple approaches. Currently, it supports YOLO and EfficientAD frameworks, but it is designed to be extensible, allowing for the integration of additional machine learning models and techniques in the future.
See [`JOURNAL.md`](./JOURNAL.md) for a detailed experiment log.

## Table of Contents

- [UltraLytics (YOLO family)](#ultralytics-yolo-family)
   - [Setup](#setup)
   - [Usage](#usage)
      - [Dataset Preparation](#1-dataset-preparation)
      - [Training](#2-training)
      - [Inference](#3-inference)
      - [Helper Scripts](#helper-scripts)
- [EfficientAD](#efficientad)
   - [Setup](#setup-1)
   - [Usage](#usage-1)
      - [Dataset Preparation](#1-dataset-preparation-1)
      - [Training](#2-training-1)
      - [Evaluation](#3-evaluation)
      - [Helper Scripts](#helper-scripts-1)

## UltraLytics (YOLO family)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/agbld/led-defects-detection.git
   cd led-defects-detection
   ```

2. Install PyTorch from the [official website](https://pytorch.org/get-started/locally/). For Ubuntu with CUDA 11.8, you can use the following command:
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
   (This is just an example, please refer to the official website for the exact command for your system)

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the required dataset. (The dataset is not included in this repository due to NDAs. Please contact the repository owner for access to the dataset)

### Usage

#### 1. Dataset Preparation

Use `prepare_dataset.py` to prepare a dataset for training.

Prepare a dataset for all classes:
```bash
python prepare_dataset.py --coco_json ../data/original/annotations/instance.json --images_dir ../data/original/images --yolo_dir ./yolo_dataset --train_ratio 0.8
```

Or, prepare a dataset for specific classes:
```bash
python prepare_dataset.py --coco_json ../data/original/annotations/instance.json --images_dir ../data/original/images --yolo_dir ./yolo_dataset --train_ratio 0.8 --included_classes particle flip Particle_Big tilt led_ng
```

Arguments:
- `--coco_json`: Path to COCO format JSON.
- `--images_dir`: Directory containing images.
- `--yolo_dir`: Directory to save YOLO formatted dataset.
- `--train_ratio`: Ratio for train-validation split (default: 0.8).
- `--included_classes`: Classes to include (default: `['led', 'particle', 'flip', ...]`).

#### 2. Training

Use `train.py` to train the YOLO model.

```bash
python train.py --data_config ./yolo_dataset/data.yaml --model yolo11x --epochs 500 --batch_size 16 --run_name experiment
```

Arguments:
- `--data_config`: Path to the dataset config YAML.
- `--model`: YOLO model type (default: `yolo11x`).
- `--epochs`: Number of training epochs (default: 50).
- `--batch_size`: Training batch size (default: 16).
- `--run_name`: Custom run name.

#### 3. Inference

Use `inference.py` to run inference on dataset.

```bash
python inference.py --weights runs/detect/experiment1/weights/best.pt --data_config yolo_dataset/data.yaml --split val --run_name experiment1
```

Arguments:
- `--weights`: Path to model weights file.
- `--data_config`: Path to data config YAML.
- `--split`: Dataset split to analyze (default: `val`).
- `--run_name`: Custom run name for analysis.
- `--save_dir`: Directory to save analysis results (default: `./runs/detect/`).
- `--classes`: List of class names to filter.

After running inference, the results will be saved in `./runs/detect/` directory. The results include:
- `per_class_stats.csv`: Per-class performance statistics.
- `cli-args.txt`: Command line arguments used for inference.
- (error samples with rendered annotations).jpg

#### Helper Scripts

See inlined documentation in the scripts for more information.

- [`ultralytics/generate_runs_report.py`](./ultralytics/generate_runs_report.py): Generate PDF reports of runs.
- [`data/visualize_dataset.py`](./data/visualize_dataset.py): Render annotations on images and export to `data/vis_images/`.
- [`data/select_dataset.py`](./data/select_dataset.py): Copy images with specific defects to `data/.tmp/`.

## EfficientAD

Unofficial implementation of paper https://arxiv.org/abs/2303.14535

**NOTE:** This is an integrated version from [agbld/EfficientAD](https://github.com/agbld/EfficientAD.git). For detailed changed from the [nelson1425/EfficientAD](https://github.com/nelson1425/EfficientAD.git), please see the commit history of [agbld/EfficientAD](https://github.com/agbld/EfficientAD.git).

[![PWC](https://img.shields.io/endpoint.svg?url=https://paperswithcode.com/badge/efficientad-accurate-visual-anomaly-detection/anomaly-detection-on-mvtec-loco-ad)](https://paperswithcode.com/sota/anomaly-detection-on-mvtec-loco-ad?p=efficientad-accurate-visual-anomaly-detection)

Huge thanks to the authors of both the paper and the unofficial implementation. This is a forked version with some modification for custom datasetsee. See here for the original unofficial implementation: https://github.com/nelson1425/EfficientAD.git

Please note that EfficientAD is a fully UNSUPERVISED learning approach that requires NO ANNOTATIONS. In the current setting, the model is trained using only HALF of the normal samples (and ZERO abnormal samples) and can be trained in UNDER 2 MINUTES on an RTX 4090.

### Setup

1. Create and activate a new conda environment:
   ```bash
   conda create -n effad python=3.8
   conda activate effad
   ```

2. Install PyTorch:
   - For Windows:
     ```bash
     pip install torch==1.13.0+cu116 torchvision==0.14.0+cu116 torchaudio==0.13.0+cu116 -f https://download.pytorch.org/whl/cu116/torch_stable.html
     ```
   - For Ubuntu:
     ```bash
     pip install torch==1.13.0+cu117 torchvision==0.14.0+cu117 torchaudio==0.13.0 --extra-index-url https://download.pytorch.org/whl/cu117
     ```

3. Install additional dependencies:
   ```bash
   pip install -r efficientad/requirements.txt
   ```

4. Download the required dataset. (The dataset is not included in this repository due to NDAs. Please contact the repository owner for access to the dataset)

### Usage

#### 1. Dataset Preparation
```bash
python prepare_dataset.py --annotations ../data/original/annotations/instance.json --labeled_dir ../data/original/images/ --unlabeled_dir ../data/original/normal/B/ --output_dir efficientad_dataset --train_ratio 0.8
```

Arguments:
- `--annotations`: Path to COCO format JSON.
- `--labeled_dir`: Directory containing labeled images.
- `--unlabeled_dir`: Directory containing unlabeled images.
- `--output_dir`: Directory to save EfficientAD formatted dataset.
- `--train_ratio`: Ratio for train-validation split (default: 0.8).

#### 2. Training
```bash
Train EfficientAD on custom dataset:
```bash
python train.py --dataset custom --custom_dataset_path efficientad_dataset --output_dir output/1 --model_size small --epochs 10 --batch_size 10
```

Arguments:
- `--dataset`: Dataset type (default: `mvtec`).
- `--custom_dataset_path`: Path to custom dataset.
- `--output_dir`: Directory to save training outputs.
- `--model_size`: Model size (default: `small`).
- `--epochs`: Number of training epochs (default: 10).
- `--batch_size`: Training batch size (default: 10).

#### 3. Evaluation
Evaluate EfficientAD on custom dataset:
```bash
python eval.py --dataset custom --custom_dataset_path efficientad_dataset --output_dir output/1 --model_size small --map_format jpg --threshold 15 --weights_dir output/1/trainings/custom
```

Arguments:
- `--dataset`: Dataset type (default: `mvtec`).
- `--custom_dataset_path`: Path to custom dataset.
- `--output_dir`: Directory to save evaluation outputs.
- `--model_size`: Model size (default: `small`).
- `--map_format`: Format of the mean anomaly map (default: `jpg`).
- `--threshold`: Threshold for anomaly detection (default: 15).
- `--weights_dir`: Directory containing model weights.

#### Helper Scripts

- [`efficientad/compare_mismatch.py`](./efficientad/compare_mismatch.py): Compare the mismatch between the ground truth and the predicted anomaly map.