import glob
import os
dir_name = 'C:\pythonProjectpp'
list_of_files = filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) )
files_with_size = [ (file_name, os.stat(os.path.join(dir_name, file_name)).st_size)
                    for file_name in list_of_files  ]
for file_name, size in files_with_size:
    print(size, ' -->', file_name)