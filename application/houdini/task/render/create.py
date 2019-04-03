import hou


class RenderSop(object):

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

