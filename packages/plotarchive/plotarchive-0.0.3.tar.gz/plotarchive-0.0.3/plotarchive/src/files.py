import glob
import os


def create_file_dict():
    """
    Small helper function which reads all python files in the scope and saves the text to a dictionary.

    :return: dict where each key is the file path
    """
    python_files = {}
    python_files_list = glob.glob('./**/*.py', recursive=True)
    for f in glob.glob('./**/*.ipynb', recursive=True):
        python_files_list.append(f)
    for f in python_files_list:
        file = open(f, 'r')
        python_files[f] = file.read()
        file.close()
    return python_files


def write_files_from_dict(folder_dict: dict, new_folder_path=None):

    if new_folder_path is None:
        new_folder_path = 'sourcefiles/'

    cwd = os.getcwd()
    os.mkdir(new_folder_path)
    os.chdir(new_folder_path)


    for key in folder_dict:
        base_path, file_name = os.path.split(key)
        base_path = os.path.normpath(base_path)
        print(base_path+'/'+file_name)
        if base_path is not '.' and not os.path.exists(base_path):
            os.mkdir(base_path)
        text = folder_dict[key]
        file = open(base_path+'/'+file_name,'w')
        file.write(text)
        file.close()

    os.chdir(cwd)




