import os
import shutil
import random

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

#  This function resizes all images in the given directory to 640x640 and puts them in a new directory named train640
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
    # Make basic folders
    imgs_dir = os.path.join(DATA_DIR, "images")
    if os.path.exists(imgs_dir):
        shutil.rmtree(imgs_dir)
    os.mkdir(imgs_dir)
    labels_dir = os.path.join(DATA_DIR, "labels")
    if os.path.exists(labels_dir):
        shutil.rmtree(labels_dir)
    os.mkdir(labels_dir)
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
    for idx, img_path in enumerate(img_path_list):
        try:
            if idx % 200 == 0:
                print(f"Processing {idx}/{len(img_path_list)} %")
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
    datasets_list = [ os.path.join(src_dir_path, name) for name in os.listdir(src_dir_path) if os.path.isdir(os.path.join(src_dir_path, name)) ]
    copy_labels_imgs_to_data(datasets_list, DATA_DIR)
    print("FINITOOOO")


def prepare_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

"""
This function accepts the path to a directory with dataset which only containt train and than splits the dataset into train, test and valid datasets
dataset_split is a list of 3 integers which represent the percentage of the dataset that will be used for train, test and valid datasets
"""
def split_dataset(DATA_DIR_SRC, DATA_DIR_TARGET, dataset_split=[70, 20, 10]):
    # Set up source dirs
    IMG_DIR = os.path.join(DATA_DIR_SRC, "images", "train")
    LABELS_DIR = os.path.join(DATA_DIR_SRC, "labels", "train")

    # Define target dirs for images and labels
    target_dirs = {subdir: (os.path.join(DATA_DIR_TARGET, "images", subdir),
                            os.path.join(DATA_DIR_TARGET, "labels", subdir))
                   for subdir in ['train', 'test', 'valid']}

    # Create/clean target directories
    for img_dir, label_dir in target_dirs.values():
        prepare_dir(img_dir)
        prepare_dir(label_dir)

    # Split dataset
    dir_list = os.listdir(IMG_DIR)
    random.shuffle(dir_list)

    train_split = dataset_split[0] * len(dir_list) // 100
    test_split = (dataset_split[0] + dataset_split[1]) * len(dir_list) // 100

    for idx, img_file in enumerate(dir_list):
        if idx % 500 == 0:
            print(f"Processing {idx}/{len(dir_list)}")

        img_path = os.path.join(IMG_DIR, img_file)
        label_file_name = os.path.splitext(img_file)[0] + ".txt"
        label_file_path = os.path.join(LABELS_DIR, label_file_name)

        if os.path.exists(label_file_path):
            if idx < train_split:
                target = 'train'
            elif idx < test_split:
                target = 'test'
            else:
                target = 'valid'

            shutil.copy(img_path, target_dirs[target][0])  # Copy image
            shutil.copy(label_file_path, target_dirs[target][1])  # Copy label
        else:
            print(f"No label file for: {img_file}")

    print("Finished splitting dataset")


def prepare_dir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)


def split_dataset_by_number(DATA_DIR_SRC, DATA_DIR_TARGET, valid_num, test_num):
    """
    Splits a dataset into training, validation, and test sets based on the specified number of images for validation and test sets.

    Args:
        DATA_DIR_SRC (str): Source directory containing the dataset.
        DATA_DIR_TARGET (str): Target directory where the split dataset will be saved.
        valid_num (int): Number of images to be assigned to the validation set.
        test_num (int): Number of images to be assigned to the test set.

    Raises:
        ValueError: If the sum of valid_num and test_num exceeds the total number of images in the dataset.

    The remaining images will be assigned to the training set.
    The directory structure will be:
        DATA_DIR_TARGET/
            images/
                train/
                test/
                valid/
            labels/
                train/
                test/
                valid/
    """

    # Set up source dirs
    IMG_DIR = os.path.join(DATA_DIR_SRC, "images", "train")
    LABELS_DIR = os.path.join(DATA_DIR_SRC, "labels", "train")

    # Define target dirs for images and labels
    target_dirs = {subdir: (os.path.join(DATA_DIR_TARGET, "images", subdir),
                            os.path.join(DATA_DIR_TARGET, "labels", subdir))
                   for subdir in ['train', 'test', 'valid']}

    # Create/clean target directories
    for img_dir, label_dir in target_dirs.values():
        prepare_dir(img_dir)
        prepare_dir(label_dir)

    # Get list of images and shuffle
    dir_list = os.listdir(IMG_DIR)
    random.shuffle(dir_list)

    total_images = len(dir_list)

    if valid_num + test_num > total_images:
        raise ValueError("Valid and test numbers exceed total dataset size")

    # Assign images to datasets
    valid_split = dir_list[:valid_num]
    test_split = dir_list[valid_num:valid_num + test_num]
    train_split = dir_list[valid_num + test_num:]

    # Helper function to copy files
    def copy_files(file_list, target):
        for img_file in file_list:
            img_path = os.path.join(IMG_DIR, img_file)
            label_file_name = os.path.splitext(img_file)[0] + ".txt"
            label_file_path = os.path.join(LABELS_DIR, label_file_name)

            if os.path.exists(label_file_path):
                shutil.copy(img_path, target_dirs[target][0])  # Copy image
                shutil.copy(label_file_path, target_dirs[target][1])  # Copy label
            else:
                print(f"No label file for: {img_file}")

    # Copy files to corresponding directories
    copy_files(valid_split, 'valid')
    copy_files(test_split, 'test')
    copy_files(train_split, 'train')

    print("Dataset split completed")

DIR_NAMES = ["images", "labels", "train", "val", "valid", "test"]
def longest_file_path(dir):
    print(os.getcwd())
    dir_list = os.listdir(dir)
    max_len = 0
    longest_str = ""
    for file_path in dir_list:
        if len(file_path) > max_len:
            longest_str = file_path
            max_len = len(file_path)
    return max_len, longest_str


# If the extension is not correct, delete file
def del_broken_files(dir, extenstion):
    dir_list = os.listdir(dir)
    count = 0
    for idx, file in enumerate(dir_list):
        if file.split(".")[-1] != extenstion:
            count += 1
            print(file)
            os.remove(os.path.join(dir, file))
    print(count)


# Change names of files that are too long (they are problematic lol weak os cant handle 256char len strings)
def rename_long_name_files(DATA_DIR, max_file_name_length=120):
    counter = 0
    err_counter = 0
    dir_path_imgs = os.path.join(DATA_DIR, "images", "train")
    dir_path_lab = os.path.join(DATA_DIR, "labels", "train")
    for file_name in os.listdir(dir_path_imgs):
        # print(len(file_name))
        if len(file_name) > max_file_name_length:
            old_file_name_lab = os.path.join(dir_path_lab, file_name[: -3]) + "txt"
            lable_file_new_name = file_name[-(max_file_name_length - 1): -3] + "txt"
            new_file_name_lab = os.path.join(dir_path_lab, lable_file_new_name)

            old_file_name_img = os.path.join(dir_path_imgs, file_name)
            new_file_name_img = os.path.join(dir_path_imgs, file_name[-(max_file_name_length - 1):])
            os.rename("\\\\?\\" + old_file_name_lab, new_file_name_lab)
            os.rename("\\\\?\\" + old_file_name_img, new_file_name_img)
            counter += 1
            #    err_counter += 1
    print(str(counter) + " files renamed           err_counter: " + str(err_counter))



# Changes all classes to 0 (if we only wanna detect leafs)
def change_classes_to_0(DATA_DIR):
    rename_long_name_files(DATA_DIR)  # change file names
    # start algo
    counter = 0
    dir_names = ["train/", "test/", "valid/"]
    for dir_name in dir_names:
        source_path = os.path.join(DATA_DIR, "labels", dir_name)
        try:
            dir_list = os.listdir(source_path)
            print("len dir_list: " + str(len(dir_list)))
            for idx, file_path in enumerate(dir_list):
                if idx % 300 == 0:
                    print(idx)
                # read file and than write to it
                file_name = file_path.split("/")[-1]
                file_source_path = source_path + file_name
                f = open(file_source_path, "r")
                f_lines = f.readlines()
                f.close()
                f2 = open(file_source_path, "w")

                # overwrite all annotations to class 0
                for idx, line in enumerate(f_lines):
                    annotation = line.split(" ")
                    if annotation[0] != '0':
                        counter += 1
                    annotation[0] = '0'
                    annotation_fixed = ""

                    # write annotation to file
                    for idx, i in enumerate(annotation):
                        if idx < len(annotation) - 1:
                            annotation_fixed += i + " "
                        else:
                            annotation_fixed += i
                    f2.write(annotation_fixed)
                f2.close()
        except:
            print("No directory: " + str(source_path))
    print("Changed classes for :" + str(counter) + " annotations")


# we chehck all labels are 0 --> only needed for leaf detection
def check_all_is_0_class(source_path):
    counter = 0
    source_pahts = [os.path.join(source_path, "labels", "train"), os.path.join(source_path, "labels", "val")]
    for path in source_pahts:
        print(path)
        dir_list = os.listdir(path)
        for idx1, file_path in enumerate(dir_list):
            if idx1 % 1000 == 0:
                print(idx1)
            file_name = file_path.split("/")[-1]
            file_source_path = os.path.join(path, file_name)
            f = open(file_source_path, "r")
            f_lines = f.readlines()
            for idx2, line in enumerate(f_lines):
                annotation = line.split(" ")
                if annotation[0] != '0':
                    counter += 1
            f.close()
    print("num of corrupt annotations:" + str(counter))


# We are splitting lables between "diseased" (0) and "healty" lables (1) --> we pass an input of an array of healty lables
def change_classes_to_0_1(DATA_DIR, healty_classes):
    # start algo
    for dir1_name in DIR_NAMES:
        for dir2_name in DIR_NAMES:
            source_path = os.path.join(DATA_DIR, dir1_name, dir2_name)
            if os.path.isdir(source_path):
                dir_list = os.listdir(source_path)
                if dir_list[0].split(".")[-1] == "txt":
                    # print("len dir_list: " + str(len(dir_list)))
                    for idx, file_path in enumerate(dir_list):
                        # read file and than write to it
                        file_name = file_path.split("/")[-1]
                        file_source_path = os.path.join(source_path, file_name)
                        f = open(file_source_path, "r")
                        f_lines = f.readlines()
                        f.close()
                        f2 = open(file_source_path, "w")

                        # overwrite all annotations to class 0 or 1
                        for idx, line in enumerate(f_lines):
                            annotation = line.split(" ")
                            annotation_class = int(annotation[0])
                            if annotation_class in healty_classes:
                                annotation[0] = '1'
                            else:
                                annotation[0] = '0'
                            annotation_fixed = ""

                            # write annotation to file
                            for idx, i in enumerate(annotation):
                                if idx < len(annotation) - 1:
                                    annotation_fixed += i + " "
                                else:
                                    annotation_fixed += i
                            f2.write(annotation_fixed)
                        f2.close()
    print("FINISHED CHANGE_CLASSES_0_1")

import os

# Counts how much of each class are in labels (how many times each class appears)
def each_class_count(DATA_DIR):
    annotation_lables_count = {}
    for dir1_name in DIR_NAMES:
        for dir2_name in DIR_NAMES:
            path = os.path.join(DATA_DIR, dir1_name, dir2_name)
            if os.path.isdir(path):
                dir_list = os.listdir(path)
                if dir_list[0].split(".")[-1] == "txt":
                    for idx1, file_path in enumerate(dir_list):
                        file_name = file_path.split("/")[-1]
                        file_source_path = os.path.join(path, file_name)
                        f = open(file_source_path, "r")
                        f_lines = f.readlines()
                        for idx2, line in enumerate(f_lines):
                            annotation_description = line.split(" ")
                            annotation_label = int(annotation_description[0])
                            if annotation_label not in annotation_lables_count:
                                annotation_lables_count[annotation_label] = 1
                            else:
                                annotation_lables_count[annotation_label] += 1
                        f.close()
    print(annotation_lables_count)
    print("FINISHED ANNOTATION LABELS COUNT")
    return annotation_lables_count


def each_class_count_single_dir(dir_path):
    annotation_labels_count = {}
    if os.path.isdir(dir_path):
        dir_list = os.listdir(dir_path)
        if dir_list and dir_list[0].split(".")[-1] == "txt":
            for file_path in dir_list:
                file_name = file_path.split("/")[-1]
                file_source_path = os.path.join(dir_path, file_name)
                with open(file_source_path, "r") as f:
                    f_lines = f.readlines()
                    for line in f_lines:
                        annotation_description = line.split(" ")
                        annotation_label = int(annotation_description[0])
                        if annotation_label not in annotation_labels_count:
                            annotation_labels_count[annotation_label] = 1
                        else:
                            annotation_labels_count[annotation_label] += 1

    print("FINISHED ANNOTATION LABELS COUNT: ", annotation_labels_count, "    for path: ", dir_path)
    return annotation_labels_count



# COUNT NUMBER OF LABELS PER PICTURE (prints dict)
def count_labels_on_picture(DATA_DIR):
    LABELS_DIR = os.path.join(DATA_DIR, "labels", "train")
    num_of_labels_on_img = {}

    # read label.txt and count how many labels on image
    for idx, file_path in enumerate(os.listdir(LABELS_DIR)):
        file_name = file_path.split("/")[-1]
        file_source_path = os.path.join(LABELS_DIR, file_name)
        f = open(file_source_path, "r")
        f_lines = f.readlines()
        if len(f_lines) not in num_of_labels_on_img:
            num_of_labels_on_img[len(f_lines)] = 1
        else:
            num_of_labels_on_img[len(f_lines)] += 1
        f.close()

    # print number of labels per image dict
    print(dict(sorted(num_of_labels_on_img.items())))


# DELETES ALL IMAGES (AND THEIR LABELS.TXT) IF IT HAS LOWER THAN "min_num_of_labels" number of labels on the picture
def del_images_bellow_n_labels(DATA_DIR, min_num_of_labels):
    IMGS_DIR = os.path.join(DATA_DIR, "images", "train")
    LABELS_DIR = os.path.join(DATA_DIR, "labels", "train")
    err_counter = 0
    del_counter = 0

    # read label.txt and count how many labels on image
    for idx, file_path in enumerate(os.listdir(LABELS_DIR)):
        file_name = file_path.split("/")[-1]
        file_source_path = os.path.join(LABELS_DIR, file_name)
        # print(len(file_source_path))
        f = open(file_source_path, "r")
        f_lines = f.readlines()
        f.close()

        # if it has less than min_num_of_labels, delete picture and its labelse.txt
        if len(f_lines) < min_num_of_labels:
            file_name_split = file_name.split(".")
            file_name_split.pop()
            img_file_name = ".".join(file_name_split) + ".jpg"
            # print(len(img_file_name))
            os.remove(os.path.join(IMGS_DIR, img_file_name))
            os.remove(os.path.join(LABELS_DIR, file_name))
            del_counter += 1

    print("Deleted pictures: " + str(del_counter) + "      Err counter: " + str(err_counter))
    count_labels_on_picture(DATA_DIR)



# CONVERTS ALL CLASSES TO EITHER SICK(0) OR HEALTY
def run_change_classes_to_0_1(DATA_DIR, healty_classes):
    rename_long_name_files(DATA_DIR)
    each_class_count(DATA_DIR)
    change_classes_to_0_1(DATA_DIR, healty_classes)
    each_class_count(DATA_DIR)

import os

def delete_annotations_with_class_id(DATA_DIR, target_class_id):
    """
    Deletes all annotations with a specific class ID in annotation files.
    Args:
        DATA_DIR (str): Root directory containing subdirectories with annotation files.
        target_class_id (int): The class ID of annotations to delete.
    """
    for dir1_name in os.listdir(DATA_DIR):
        dir1_path = os.path.join(DATA_DIR, dir1_name)
        if not os.path.isdir(dir1_path):
            continue

        for dir2_name in os.listdir(dir1_path):
            source_path = os.path.join(dir1_path, dir2_name)
            if os.path.isdir(source_path):
                dir_list = os.listdir(source_path)
                if dir_list and dir_list[0].split(".")[-1] == "txt":
                    for file_name in dir_list:
                        file_source_path = os.path.join(source_path, file_name)

                        # Read the file lines
                        with open(file_source_path, "r") as f:
                            f_lines = f.readlines()

                        # Rewrite the file without the target class ID
                        with open(file_source_path, "w") as f2:
                            for line in f_lines:
                                annotation = line.split(" ")
                                annotation_class = int(annotation[0])
                                if annotation_class != target_class_id:
                                    f2.write(line)
    print("FINISHED DELETE_ANNOTATIONS_WITH_CLASS_ID")



import os

def delete_annotations_with_class_id(DATA_DIR, target_class_id):
    """
    Deletes all annotations with a specific class ID in annotation files.

    Args:
        DATA_DIR (str): Root directory containing subdirectories with annotation files, e.g., labels folder with subfolders of test, train, valid.
        target_class_id (int): The class ID of annotations to delete.
    """
    DATA_DIR = os.path.join(DATA_DIR, "labels")
    counter = 0

    for dir_name in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, dir_name)
        if not os.path.isdir(dir_path):
            continue

        for file_name in os.listdir(dir_path):
            if not file_name.endswith(".txt"):
                continue

            file_source_path = os.path.join(dir_path, file_name)

            # Read the file lines
            with open(file_source_path, "r") as f:
                f_lines = f.readlines()

            # Filter out lines containing the target class ID
            new_lines = []
            for line in f_lines:
                annotation = line.strip().split(" ")
                annotation_class = int(annotation[0])

                if annotation_class != target_class_id:
                    new_lines.append(line)
                else:
                    counter += 1

            # Rewrite the file only if changes were made
            if len(new_lines) != len(f_lines):
                with open(file_source_path, "w") as f2:
                    f2.writelines(new_lines)

    print(f"FINISHED DELETE_ANNOTATIONS_WITH_CLASS_ID: {target_class_id}. Number of deleted annotations: {counter}")




def change_class_id(DATA_DIR, old_class_id, new_class_id):
    """
    Changes all occurrences of a specific class ID in annotation files to another class ID.
    Args:
        DATA_DIR (str): Root directory containing subdirectories with annotation files. aka labels file with subfolders of test,train,valid
        old_class_id (int): The class ID to be replaced.
        new_class_id (int): The class ID to replace with.
    """
    DATA_DIR = DATA_DIR + "/labels"
    counter = 0
    for dir_name in os.listdir(DATA_DIR):
        dir_path = os.path.join(DATA_DIR, dir_name)
        print("dir path: ", dir_path)
        if not os.path.isdir(dir_path):
            print("dir path EMPTY: ", dir_path)
            continue

        if os.path.isdir(dir_path):
            annotations_files_list = os.listdir(dir_path)
            if annotations_files_list and annotations_files_list[0].split(".")[-1] == "txt":
                for file_name in annotations_files_list:
                    file_source_path = os.path.join(dir_path, file_name)

                    # Read the file lines
                    with open(file_source_path, "r") as f:
                        f_lines = f.readlines()

                    # Rewrite the file with updated class IDs
                    with open(file_source_path, "w") as f2:
                        for line in f_lines:
                            annotation = line.split(" ")
                            annotation_class = int(annotation[0])
                            if annotation_class == old_class_id:
                                annotation[0] = str(new_class_id)
                                counter += 1

                            # Reconstruct the annotation line
                            annotation_fixed = " ".join(annotation)
                            f2.write(annotation_fixed)
    print("FINISHED CHANGE_CLASS_ID from class: " , old_class_id, " to class: ", new_class_id, "    number of annotations changed: ", counter)


# Equalize classes to match the smallest class count
def equalize_classes(DATA_DIR):
    class_counts = each_class_count(DATA_DIR)
    min_class_count = min(class_counts.values())
    print(f"Equalizing classes to: {min_class_count} annotations per class")

    annotations_to_delete = {label: [] for label in class_counts.keys()}

    for dir1_name in DIR_NAMES:
        for dir2_name in DIR_NAMES:
            path = os.path.join(DATA_DIR, dir1_name, dir2_name)
            if os.path.isdir(path):
                dir_list = os.listdir(path)
                if dir_list and dir_list[0].split(".")[-1] == "txt":
                    for file_path in dir_list:
                        file_source_path = os.path.join(path, file_path)
                        with open(file_source_path, "r") as f:
                            f_lines = f.readlines()

                        for line in f_lines:
                            annotation = line.split(" ")
                            annotation_class = int(annotation[0])
                            annotations_to_delete[annotation_class].append((file_source_path, line))

    # Shuffle and delete excess annotations
    for class_id, annotations in annotations_to_delete.items():
        if len(annotations) > min_class_count:
            random.shuffle(annotations)
            excess_annotations = annotations[min_class_count:]
            for file_source_path, line in excess_annotations:
                with open(file_source_path, "r") as f:
                    lines = f.readlines()
                with open(file_source_path, "w") as f:
                    for l in lines:
                        if l != line:
                            f.write(l)
            print(f"Deleted {len(excess_annotations)} annotations of class {class_id}")

    print("FINISHED EQUALIZING CLASSES")
    each_class_count(DATA_DIR)



def equalize_classes_single_dir(dir_path):
    class_counts = each_class_count_single_dir(dir_path)
    min_class_count = min(class_counts.values())
    print(f"Equalizing classes to: {min_class_count} annotations per class")

    annotations_to_delete = {label: [] for label in class_counts.keys()}

    if os.path.isdir(dir_path):
        dir_list = os.listdir(dir_path)
        if dir_list and dir_list[0].split(".")[-1] == "txt":
            for file_path in dir_list:
                file_source_path = os.path.join(dir_path, file_path)
                with open(file_source_path, "r") as f:
                    f_lines = f.readlines()

                for line in f_lines:
                    annotation = line.split(" ")
                    annotation_class = int(annotation[0])
                    annotations_to_delete[annotation_class].append((file_source_path, line))

    # Shuffle and delete excess annotations
    for class_id, annotations in annotations_to_delete.items():
        if len(annotations) > min_class_count:
            random.shuffle(annotations)
            excess_annotations = annotations[min_class_count:]
            for file_source_path, line in excess_annotations:
                with open(file_source_path, "r") as f:
                    lines = f.readlines()
                with open(file_source_path, "w") as f:
                    for l in lines:
                        if l != line:
                            f.write(l)
            print(f"Deleted {len(excess_annotations)} annotations of class {class_id}")

    print("FINISHED EQUALIZING CLASSES")
    each_class_count_single_dir(dir_path)


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.getcwd())
    # IMG_DIR = os.path.join(DATA_DIR, 'images', "train")
    # LABEL_DIR = os.path.join(DATA_DIR, 'labels', "train")
    dataset_dir = os.path.join(DATA_DIR, "guava")
    DATA_DIR_target = os.path.join(os.getcwd(), 'data')
    DATA_DIR_target_split = os.path.join(DATA_DIR, 'data_split')
    DATA_DIR_DATA = os.path.join(os.getcwd(), 'data')
    # Create directories if they don't exist
    if not os.path.exists(DATA_DIR_target):
        os.makedirs(DATA_DIR_target)
    if not os.path.exists(DATA_DIR_target_split):
        os.makedirs(DATA_DIR_target_split)

    copy_labels_imgs_to_data([dataset_dir], DATA_DIR_target)
    # resize_images(DATA_DIR_target)
    
    each_class_count(DATA_DIR_DATA)
    delete_annotations_with_class_id(DATA_DIR_DATA, 1)
    delete_annotations_with_class_id(DATA_DIR_DATA, 3)
    delete_annotations_with_class_id(DATA_DIR_DATA, 4)
    delete_annotations_with_class_id(DATA_DIR_DATA, 5)
    change_class_id(DATA_DIR_DATA, 0, 1)
    change_class_id(DATA_DIR_DATA, 2, 0)
    each_class_count(DATA_DIR_DATA)


    # equalize_classes(DATA_DIR_DATA)
    
    # split_dataset(DATA_DIR_target, DATA_DIR_target_split, dataset_split=[70, 20, 10])
    split_dataset_by_number(DATA_DIR_target, DATA_DIR_target_split, valid_num=100, test_num=100)
    each_class_count_single_dir(os.path.join(DATA_DIR_target_split, "labels", "train"))
    equalize_classes_single_dir(os.path.join(DATA_DIR_target_split, "labels", "train")) # TOdo untested
    each_class_count_single_dir(os.path.join(DATA_DIR_target_split, "labels", "train"))
    each_class_count_single_dir(os.path.join(DATA_DIR_target_split, "labels", "valid"))
    each_class_count_single_dir(os.path.join(DATA_DIR_target_split, "labels", "test"))


