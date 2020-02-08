import os
import hou
from ... import envrionment


class LookDevSop(object):

    def __init__(self, name=""):

        """
        Creates a simplistic rig to create render setups.
        """

        # get the obj path
        self.obj_context = hou.node("/obj")

        self.name = name
        self.geometry_sop = ""
        self.geometry_sop_obj = ""

    def create_geo_sop(self):

        """
        Creates a geometry sop in the obj context.
        :return:
        """

        self.geometry_sop = self.obj_context.createNode("geo", self.name, run_init_scripts=True)
        self.geometry_sop_obj = hou.node("/obj/{0}".format(self.name))

        # Create asset folder attribute


        # Create asset name attribute


        # Create


class RenderNode(object):

    def __init__(self):

        """
        Creates a render node.  It will create an arnold or mantra node.
        """

        # get the obj path
        self.out_context = hou.node("/out")

        # Frame commands
        self.start_frame = 1001.0
        self.end_frame = 1002.0

        # the output node
        self.render_node_name = ""
        self.rop_node = hou.RopNode

        self.image_file_type = "png"
        self._image_file_types = ("exr", "deepexr", "tiff", "png", "jpeg")

        # Camera path is the scene path to the camera
        self.camera_path = ""

        self.build_from_hip_name = False

        self.output_directory = ""
        self.output_name = ""
        self.output_path = ""

    def create_arnold(self, name=""):

        """
        Creates a render node in the output context.
        :return:
        """

        if name == "":
            raise NameError("Must set name attribute when creating a node")

        self.rop_node = self.out_context.createNode("arnold", name)

        # set the start / end frames
        self.rop_node.parm("f1").deleteAllKeyframes()
        self.rop_node.parm("f2").deleteAllKeyframes()

        # set the start / end frames
        self.rop_node.parm("f1").set(self.start_frame)
        self.rop_node.parm("f2").set(self.end_frame)
        self.rop_node.parm("trange").set(1)

        if self.image_file_type in self._image_file_types:
            self.rop_node.parm("ar_picture_format").set(self.image_file_type)

        # Try to set the camera path
        if self.camera_path != "":
            self.set_camera()

        # Set the output path
        self.rop_node.parm("ar_picture").set(self.output_path)

    def create_vm_render_node(self, name):

        """
        Creates a shot node and sets it's vales
        :return:
        """

        render_node = hou.node("/out").createNode("RenderNode", name)

        return render_node

    def format_output_path(self):

        """
        Once you have set an output path, this will make sure it is formatted for proper output with a houdini rop.
        :return:
        """

        if self.output_directory == "":
            raise NameError("Output directory not specified for ROP")

        formatted_path = envrionment.path_to_path_expression(path=self.output_directory, envrionment_key="JOB")
        self.output_path = "{0}/{1}.$F.{2}".format(formatted_path, self.output_name, self.image_file_type)

    def set_camera(self):

        """
        Sets the render nodes camera based on if it
        return:
        """

        if hou.node(self.camera_path) is None:
            raise RuntimeError("Camera path not set")

        self.rop_node.parm("camera").set(self.camera_path)


def create_render_merge(name=""):

    """
    Creates a merge node for the render output
    :param string name:
    :return:
    """

    if not hou.node("/out/{0}".format(name)):
        return hou.node("/out").createNode("merge", name)
    else:
        return hou.node("/out/{0}".format(name))
