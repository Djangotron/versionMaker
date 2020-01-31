import os
from ..constants.film import hierarchy


def query_film_path():

    """
    Returns the current scene file's VersionMaker environment variables to your location
    :return:
    """

    _h = hierarchy.Hierarchy()
    _h()

    return _h


