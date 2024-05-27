import os
import shutil

from PIL import Image

def min_max_img_size(IMG_DIR):
    dir_list = os.listdir(IMG_DIR)
    sizes = [100000000,100000000,0,0]   # min_width, min_height, max_width, max_height
    for idx, img_file in enumerate(dir_list):
        if idx%1000 == 0:
            print(idx)
        img_path = os.path.join(IMG_DIR, img_file)
        img = Image.open(img_path)
        if img.width < sizes[0]:
            sizes[0] = img.width
        if img.height < sizes[1]:
            sizes[1] = img.height
        if img.width > sizes[2]:
            sizes[2] = img.width
        if img.height > sizes[3]:
            sizes[3] = img.height
    print(sizes)

def resize_images(DATA_DIR):
    # Set up dirs
    err_counter = 0
    IMG_DIR = os.path.join(DATA_DIR, "images", "train")
    LABELS_DIR = os.path.join(DATA_DIR, "labels", "train")
    RESIZE_IMG_DIR = os.path.join(DATA_DIR, "images", "train640")
    if os.path.exists(RESIZE_IMG_DIR):
        shutil.rmtree(RESIZE_IMG_DIR)
    if not os.path.exists(RESIZE_IMG_DIR):
        os.makedirs(RESIZE_IMG_DIR)

    # Resize all images
    dir_list = os.listdir(IMG_DIR)
    for idx, img_file in enumerate(dir_list):
        # logging
        if idx % 500 == 0:
            print(idx)
        # resizing
        img_path = os.path.join(IMG_DIR, img_file)
        img = Image.open(img_path)
        image_size_reduction_ratio = min(img.width, img.height)/640
        if image_size_reduction_ratio > 1:
            img = img.resize((round(img.width/image_size_reduction_ratio), round(img.height/image_size_reduction_ratio)), resample=Image.LANCZOS)
        try:
            img.save(os.path.join(RESIZE_IMG_DIR, img_file))
        except:
            err_counter += 1
        img.close()

    print("Num of errors: " + str(err_counter))

def del_imgs_no_label(IMG_DIR, LABEL_DIR):
    dir_list = os.listdir(IMG_DIR)
    counter = 0
    for img_file in dir_list:
        label_file_name = img_file.split(".")[0] + ".txt"
        label_file_path = os.path.join(LABEL_DIR, label_file_name)
        if not os.path.exists(label_file_path):
            img_file_path = os.path.join(IMG_DIR, img_file)
            os.remove(img_file_path)
            counter += 1

    print(counter)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.getcwd(), 'data')
    IMG_DIR = os.path.join(DATA_DIR, 'images', "train")
    LABEL_DIR = os.path.join(DATA_DIR, 'labels', "train")
    del_imgs_no_label(IMG_DIR, LABEL_DIR)