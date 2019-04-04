import hou


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

        # Camera path is the scene path to the camera
        self.camera_path = ""

        self.build_from_hip_name = False
        self.output_directory = ""

    def create_arnold(self, name=""):

        """
        Creates a render node in the output context.
        :return:
        """

        if name == "":
            raise NameError("Must set name attribute when creating a node")

        self.rop_node = self.out_context.createNode("arnold", name)

        # set the start / end frames
        self.rop_node.parm("f1").set(self.start_frame)
        self.rop_node.parm("f2").set(self.end_frame)
        self.rop_node.parm("trange").set(1)

        # Try to set the camera path
        if self.camera_path != "":
            self.set_camera()

        # Set the output path
        self.rop_node.parm("ar_picture").set(self.output_directory)

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
    Creates a merge node for the
    :param string name:
    :return:
    """

    if not hou.node("/out/{0}".format(name)):
        return hou.node("/out").createNode("merge", name)
