import os
from maya import cmds
from functools import partial
import versionMaker.ux.vm_ui.applications.maya.vm_maya_ui


version_maker_path = os.path.dirname(os.path.abspath(__file__)).partition("versionMaker")[0]
if os.name == "nt":
    version_maker_path.replace("\\", "/")

logo_quarter_path = "{0}versionMaker/lib_vm/images/version_maker_logo_v01_quarter.png".format(version_maker_path)


def create():

    """

    :return:
    """

    menu_name = "versionMakerMenu"
    menu_label = "Version Maker"

    # delete it if it exists
    if cmds.menu(menu_name, exists=True):
        cmds.deleteUI(menu_name)

    cmds.setParent("MayaWindow")

    # Build a menu and parent under the Maya Window
    main_menu = cmds.menu(menu_name, parent="MayaWindow", tearOff=True, label=menu_label)

    # Animation
    cmds.menuItem("animationToolsDiveder", divider=True, parent=menu_name)
    cmds.menuItem(
        label="Import",
        image=logo_quarter_path,
        command=partial(versionMaker.ux.vm_ui.applications.maya.vm_maya_ui.vm_run),
        parent=main_menu
    )
    cmds.menuItem(
        label="Export",
        # image="out_timeEditorAnimSource.png",
        command=partial(versionMaker.ux.vm_ui.applications.maya.vm_maya_ui.vm_run),
        parent=main_menu
    )
