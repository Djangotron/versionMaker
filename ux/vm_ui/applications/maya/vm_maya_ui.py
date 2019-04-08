from ....vm_ui import vm_base
import utilities


def vm_run():

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_maya = vm_base.VersionMakerWin(parent=utilities.get_maya_window())
    vm_maya.show()
