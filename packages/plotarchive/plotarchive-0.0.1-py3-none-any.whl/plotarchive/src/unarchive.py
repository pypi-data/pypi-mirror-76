import dill
from . import files


def expand(filename, folder=None):

    data = dill.load(open(filename, 'rb'))
    file_dict = data['files']
    plotter = data['func']

    if 'args' in data:
        args = data['args']
        plotter(**data['args'])

    if folder is not None:
        files.write_files_from_dict(file_dict, folder)
