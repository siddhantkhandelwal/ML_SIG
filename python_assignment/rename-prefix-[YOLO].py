import os, sys
paths = sys.argv[1:]
for path in paths:
    for dir_path, dir_names, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dir_path, filename)
            new_file_path = os.path.join(dir_path, '[YOLO]'+filename)
            os.rename(file_path, new_file_path)