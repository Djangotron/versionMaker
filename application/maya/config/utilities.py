import os


def return_maya_user_setup_location():

    return os.environ["MAYA_SCRIPT_PATH"].split(";")[1]
