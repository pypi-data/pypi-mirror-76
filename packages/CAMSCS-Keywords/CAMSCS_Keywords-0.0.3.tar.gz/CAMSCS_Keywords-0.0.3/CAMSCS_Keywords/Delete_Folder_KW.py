import os

def remove(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)  
    elif os.path.isdir(path):
        os.rmdir(path)  
    else:
        raise ValueError("file {} is not a file or dir.".format(path))