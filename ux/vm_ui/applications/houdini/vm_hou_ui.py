from ....vm_ui import vm_base
import utilities
import hou


def vm_run():

    """
    Run the versionMaker Ui for Houdini
    :return:
    """

    vm_hou = vm_base.VersionMakerWin(parent=utilities.get_houdini_window(), application="houdini")
    vm_hou.job_path = hou.getenv("JOB")
    vm_hou.setStyleSheet(hou.qt.styleSheet())
    vm_hou.setProperty("houdiniStyle", True)
    vm_hou.file_dialog.setStyleSheet(hou.qt.styleSheet())
    vm_hou()
    vm_hou.show()

    return vm_hou
