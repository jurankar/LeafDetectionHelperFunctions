import os
from ultralytics import YOLO


ROOT_DIR = '.'
DATA_DIR = os.path.join(ROOT_DIR,'datasets','data_fsb_wheat')

# Other model versions
# model = YOLO("yolov9e.yaml" -->  https://docs.ultralytics.com/models/yolov9/#performance-on-ms-coco-dataset

# Load Model
# model = YOLO('yolov9c.yaml').load(os.path.join(ROOT_DIR, "runs", "detect", "train10", "weights", "last.pt"))  # build from YAML and transfer weights

# Use the model
model = YOLO("yolov9c.yaml")  # build a new model from scratch
results = model.train(data=os.path.join(DATA_DIR, "config_data_fsb_wheat.yaml"), lr0=0.001, lrf=0.01, epochs=200, batch=16, optimizer="AdamW", save_period=42, dropout=0.25, degrees=90, translate=0.35, flipud=0.35, plots=True)  # train the model

# Resume learning
# model = YOLO(os.path.join(ROOT_DIR, "runs", "detect", "train23", "weights", "last.pt"))  # load a model
# results = model.train(resume=True)