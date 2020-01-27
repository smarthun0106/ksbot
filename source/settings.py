import os

DIR_PATH = ''
DIR_NAME = 'csv_file'
try:
    # Create target Directory
    os.mkdir(DIR_PATH+DIR_NAME)
    print("Directory " , DIR_PATH+DIR_NAME ,  " Created ")
except FileExistsError:
    pass
