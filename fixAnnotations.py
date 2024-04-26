import os

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



# Change names of files that are too long (they are problematic lol weak os cant handle 256char len strings)
def rename_long_name_files(DATA_DIR, max_file_name_length=130):
    counter = 0
    dir1_names = ["images", "labels"]
    dir2_names = ["train", "val"]
    for dir1_name in dir1_names:
      for dir2_name in dir2_names:
          dir_path = os.path.join(DATA_DIR, dir1_name, dir2_name)
          for file_name in os.listdir(dir_path):
              if len(file_name) > max_file_name_length:
                  counter += 1
                  old_file_name = os.path.join(dir_path, file_name)
                  new_file_name = os.path.join(dir_path, file_name[:(max_file_name_length-1)])
                  os.rename("\\\\?\\" + old_file_name, new_file_name)
    print(str(counter) + " files renamed")

def change_classes(DATA_DIR):
  rename_long_name_files(DATA_DIR)  # change file names
  # start algo
  counter = 0
  dir_names = ["train/", "val/"]
  for dir_name in dir_names:
    source_path = os.path.join(DATA_DIR, "labels", dir_name)
    dir_list = os.listdir(source_path)
    print("len dir_list: " + str(len(dir_list)))
    for idx, file_path in enumerate(dir_list):
      if idx%1000 == 0:
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
          if idx < len(annotation)-1:
            annotation_fixed += i + " "
          else:
            annotation_fixed += i
        f2.write(annotation_fixed)
      f2.close()
  print("Changed classes for :" + str(counter) + " annotations")


def check_all_is_0_class(source_path):
  counter  = 0
  source_pahts = [os.path.join(source_path, "labels", "train"), os.path.join(source_path, "labels", "val")]
  for path in source_pahts:
    print(path)
    dir_list = os.listdir(path)
    for idx1, file_path in enumerate(dir_list):
      if idx1%1000 == 0:
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


if __name__ == '__main__':
    # print(os.getcwd())
    DATA_DIR = os.path.join(os.getcwd(), 'dataBig')
    change_classes(DATA_DIR)
    check_all_is_0_class(DATA_DIR)