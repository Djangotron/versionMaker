import os
from ....vm_ui import vm_base
import utilities


def vm_run():

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_maya = vm_base.VersionMakerWin(parent=utilities.get_maya_window(), application="houdini")

    if "SHOW" in os.environ:
        vm_maya.job_path = os.environ["SHOW"]

    vm_maya()
    vm_maya.show()
