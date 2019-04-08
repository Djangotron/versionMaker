from functools import wraps
from maya import mel


def disable_viewport(func):

    @wraps(func)
    def viewport(*args, **kwargs):

        try:
            # viewport OFF
            mel.eval("paneLayout -e -manage false $gMainPane")
            return func(*args, **kwargs)

        finally:
            # viewport ON
            mel.eval("paneLayout -e -manage true $gMainPane")

    return viewport
