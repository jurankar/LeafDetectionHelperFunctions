import os


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


if __name__ == '__main__':
    DATA_DIR = os.path.join(os.getcwd(), 'data')
    DATA_DIR_target = os.path.join(os.getcwd(), 'data_split')
    # run_change_classes_to_0_1(DATA_DIR, [])
    # change_classes_to_0(DATA_DIR_target)

    each_class_count(DATA_DIR)
    count_labels_on_picture(DATA_DIR)

    # healty_classes = [3]
    # run_change_classes_to_0_1(DATA_DIR, healty_classes)
    # del_images_bellow_n_labels(DATA_DIR, 3)


