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

"""
This function accepts the path to a datasets (list of paths) and than copies all the images and labels to our working directory in DATA_DIR
"""
def copy_labels_imgs_to_data(path_list, DATA_DIR):
    # Clean dirs
    imgs_dir = os.path.join(DATA_DIR, "images", "train")
    if os.path.exists(imgs_dir):
        shutil.rmtree(imgs_dir)
    os.mkdir(imgs_dir)

    labels_dir = os.path.join(DATA_DIR, "labels", "train")
    if os.path.exists(labels_dir):
        shutil.rmtree(labels_dir)
    os.makedirs(labels_dir)

    # get all dirs
    img_path_list = []
    label_path_list = []
    data_parts = ["train", "test", "valid"]
    for path in path_list:
        for data_part in data_parts:
            img_path_list.append(os.path.join(path, data_part, "images"))
            img_path_list.append(os.path.join(path, "images", data_part))
            label_path_list.append(os.path.join(path, data_part, "labels"))
            label_path_list.append(os.path.join(path, "labels", data_part))


    # Copy images from all dirs to data
    for img_path in img_path_list:
        try:
            img_list = os.listdir(img_path)
            for img in img_list:
                shutil.copy(os.path.join(img_path, img), imgs_dir)
            print("Finished: " + str(img_path))
        except:
            print("No directory: " + str(img_path))

    # Copy labels from all dirs to data
    for label_path in label_path_list:
        try:
            label_list = os.listdir(label_path)
            for label in label_list:
                shutil.copy(os.path.join(label_path, label), labels_dir)
            print("Finished: " + str(label_path))
        except:
            print("No directory: " + str(label_path))

"""
This function accepts the path to a directory with datasets and than copies all the images and labels from all datasets to our working directory in DATA_DIR
"""
def copy_directory_labels_imgs_to_data(src_dir_path, DATA_DIR):
    datasets = os.listdir(src_dir_path)
    datasets_list = []
    for dataset in datasets:
        datasets_list.append(os.path.join(src_dir_path,dataset))
    copy_labels_imgs_to_data(datasets_list, DATA_DIR)
    print("FINITOOOO")


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.getcwd(), 'data')
    IMG_DIR = os.path.join(DATA_DIR, 'images', "train")
    LABEL_DIR = os.path.join(DATA_DIR, 'labels', "train")
    # copy_directory_labels_imgs_to_data("D:\Sola\Magisterska\SlikeDataseti\DISEASE_DETECTION\CORN\CORN_DISEASE", DATA_DIR)
    resize_images(DATA_DIR)