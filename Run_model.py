import os
from ultralytics import YOLO


ROOT_DIR = '.'
DATA_DIR = os.path.join(ROOT_DIR,'datasets','data_fsb_wheat')

# Other model versions
# model = YOLO("yolov9e.yaml" -->  https://docs.ultralytics.com/models/yolov9/#performance-on-ms-coco-dataset

# Load Model
# model = YOLO('yolov9c.yaml').load(os.path.join(ROOT_DIR, "runs", "detect", "train10", "weights", "last.pt"))  # build from YAML and transfer weights

# Use the model
# model = YOLO("yolov9c.yaml")  # build a new model from scratch
# results = model.train(data=os.path.join(DATA_DIR, "config_data_fsb_wheat.yaml"), lr0=0.0001, lrf=0.001, epochs=500, patience=50, batch=16, save_period=42, dropout=0.25, degrees=90, translate=0.5, perspective=0.0005, flipud=0.3, mosaic=0.3, plots=True)  # train the model

# Resume learning
model = YOLO(os.path.join(ROOT_DIR, "runs", "detect", "train2", "weights", "last.pt"))  # load a model
results = model.train(resume=True)


# BEFORE THAT
# for download from google drive : gdown 1cvkVAGOCXErf25R1Wf-peUYkFvHGfEk7
# TO get gpu: salloc -p dev --gres=gpu:1   &&   srun --pty bash
#