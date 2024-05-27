import csv
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
from PIL import Image
import os


def leaf_detection_dataset(csv_file_path, dataset_name="leaf_detection"):
    # format of csv file: img_id, img_width, img_height, bbox [annot_center_x, annot_center_y, annot_width, annot, height]
    with open(csv_file_path) as file:
        csv_file = csv.reader(file)
        for idx, line in enumerate(csv_file):
            if idx != 0:
                if idx == 1:
                    print(line)

                # convert to yolo annotatin
                img_width = float(line[1])
                img_height = float(line[2])

                annotation_array = []
                for idx, i in enumerate(line[3].split(', ')):
                    i = i.replace('[', '')
                    i = i.replace(']', '')
                    i = float(i)
                    annotation_array.append(i)

                # Fix leaf detection dataset
                if dataset_name == "leaf_detection":
                    annot_width = float(annotation_array[2])
                    annot_height = float(annotation_array[3])
                    annotation_array[0] = float(annotation_array[0]) + annot_width / 2     # annot_center_x
                    annotation_array[1] = float(annotation_array[1]) + annot_height / 2         # annot_center_y

                annotation = "0"
                for idx, i in enumerate(annotation_array):
                    # Fix dataset lables
                    if idx == 0 or idx == 2:
                        str_float = i/img_width
                    else:
                        str_float = i/img_height
                    annotation += " " + str(str_float)
                annotation += "\n"
                # print(annotation)

                # write to txt files
                img_name = line[0]
                txt_file_name ="img_anottations/" + img_name.split('.')[0] + ".txt"
                # print(txt_file_name)
                f = open(txt_file_name, "a")
                f.write(annotation)
                f.close()
def corn_disease_drone_images(csv_file_path, images_path, new_labels_path):
    # Corn dataset drone images
    # https://www.kaggle.com/datasets/alexanderyevchenko/corn-disease-drone-images

    # Import csv file
    # # format of csv file: img_name, x1,y1, x2, y2, ....
    # yolov9 format is: class x_center y_center width height

    if os.path.exists(new_labels_path):
        shutil.rmtree(new_labels_path)
    if not os.path.exists(new_labels_path):
        os.makedirs(new_labels_path)

    with open(csv_file_path) as file:
        csv_file = csv.reader(file)
        for idx, line in enumerate(csv_file):
            if idx % 3000 == 0:
                print(idx)
            if idx != 0:
                # Get lable values
                img_name = str(line[0])
                x1 = float(line[1])
                y1 = float(line[2])
                x2 = float(line[3])
                y2 = float(line[4])

                label_width = abs(x2-x1)
                label_height = abs(y2-y1)
                x_center = min(x1, x2) + label_width/2
                y_center = min(y1, y2) + label_height/2

                # Get img height and width
                img_path = os.path.join(images_path, img_name)
                img = Image.open(img_path)
                img_width = img.width
                img_height = img.height

                # Convert to yolov9 annotation
                converted_label = "0 " + str(x_center/img_width) + " " + str(y_center/img_height) + " " + str(label_width/img_width) + " " + str(label_height/img_height)

                # Write annotation to file
                label_file_name = img_name.split(".")[0] + ".txt"
                label_file_path = os.path.join(new_labels_path, label_file_name)
                file1 = open(label_file_path, "a")  # append mode
                file1.write(converted_label)
                file1.close()

def draw_squares_on_img(img_path, lables_path):
    # read image
    im = Image.open(img_path)
    img_width, img_height = im.size
    img_width = float(img_width)
    img_height = float(img_height)
    # Create figure and axes
    fig, ax = plt.subplots()
    ax.imshow(im)

    # read lables
    lables = []
    f = open(lables_path, "r")
    f_lines = f.readlines()
    f.close()

    for line in f_lines:
      annotation = line.replace("\n", "").split(" ")
      annot_width = float(annotation[3])*img_width
      annot_height = float(annotation[4])*img_height
      annot_center_x = (float(annotation[1])*img_width)
      annot_center_y = (float(annotation[2])*img_height)
      print(annotation) # [annot_center_x, annot_center_y, annot_width, annot_height]
      # draw squares
      rect = patches.Rectangle((annot_center_x-annot_width/2, annot_center_y-annot_height/2), annot_width, annot_height, linewidth=1, edgecolor='r', facecolor='none')
      # Add the patch to the Axes
      ax.add_patch(rect)
    plt.show()

def draw_squares_repository(img_dir="imgs/", lables_dir="img_anottations/"):
    dir_list = os.listdir(img_dir)
    for idx, file in enumerate(dir_list):
        file = file.replace(".jpg", "")
        file = file.replace(".JPG", "")
        draw_squares_on_img(img_dir + file + ".jpg", lables_dir + file + ".txt")
        if idx == 10:
            break

if __name__ == '__main__':
    DATA_DIR = os.path.join(os.getcwd(), 'data')
    IMG_DIR = os.path.join(DATA_DIR, 'images', "train")
    LABEL_DIR = os.path.join(DATA_DIR, 'labels', "train")
    corn_labels_csv = os.path.join(DATA_DIR, 'DRONE_IMAGES_ANNOTATION.csv')
    corn_disease_drone_images(corn_labels_csv, IMG_DIR, LABEL_DIR)