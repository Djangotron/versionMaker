import os
from stat import S_IREAD, S_IRGRP, S_IROTH

"https://stackoverflow.com/questions/28492685/change-file-to-read-only-mode-in-python"

def set_file_read_only(file_path):

    """
    Sets the file to have read only status.
    :param string file_path: absolute file path to your file
    :return:
    """


    os.chmod(filename, S_IREAD | S_IRGRP | S_IROTH)
