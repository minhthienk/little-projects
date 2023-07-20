
import pathlib
from sys import exit
import re
# read data from a file
def read_data(path):
    with open(path, "r", errors='ignore') as file_object:
        return file_object.read()



def get_paths_recursively(*folder_paths):
    '''
    get all files from a folder, 
    also check subfolders 
    '''

    # create a list to contain file paths
    file_paths = [] 
    while 1:
        '''
        this while loop will break only when no unchecked folders left
        '''
        temp_folder_paths = [] # this list collects folder paths each loop
        for folder_path in folder_paths: # iter all folder paths
            # convert path string to path type
            folder_path = pathlib.Path(folder_path)
            for path in folder_path.iterdir(): # iter all paths in each folder path
                if path.is_file(): # if path is file
                    file_paths.append(str(path)) # collect
                else: # folder
                    temp_folder_paths.append(path) # collect

        # assign the folder paths collect from this turn to folder_paths to run the next turn
        folder_paths = temp_folder_paths

        # if there is no folder paths left => done
        if folder_paths==[]: break
    return file_paths


def get_paths(root_path):
    '''
    get all files from a folder, 
    also check subfolders 
    '''

    # create a list to contain file paths
    file_paths = [] 
    folder_paths = []

    root_path = pathlib.Path(root_path)

    for path in root_path.iterdir(): # iter all paths in each folder path
        if path.is_file(): # if path is file
            file_paths.append(str(path)) # collect
        else: # folder
            folder_paths.append(str(path)) # collect

    for path in file_paths:
        print(path)

    for path in folder_paths:
        print(path)

    return file_paths


import shutil

root_path = r'/media/minhthienk/Data/English Coaching/0. Resources'
file_paths = get_paths_recursively(root_path)

count = 0
for path in file_paths:
    count += 1
    #print(count)
    #to_path = r'C:\Users\ThienNguyen\Desktop\New folder\14. Manythings\Source 2' + '\\' + re.sub(r'^.+\\','',path)
    print(re.sub(r'^.+\\','',path))
    #shutil.copy(str(path), str(to_path))


