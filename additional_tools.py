from os import listdir
from os.path import isfile, isdir, join


def returnFilepaths(folder):
    """
    Creates list of filepaths to images from a folder and its subfolders.

    Parameters
    ----------
    folder : str

    Returns
    ----------
    out : list
    """
    paths = []
    for f in listdir(folder):
        p = join(folder, f)
        if isfile(p) & p.lower().endswith(('jpg', 'jpeg', 'png')):
            paths.append(p)
        elif isdir(p):
            paths += returnFilepaths(p)
    return paths
