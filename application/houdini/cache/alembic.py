import os, sys
import hou
import _alembic_hom_extensions as hou_abc


class AlembicArchive(object):

    def __init__(self):

        """
        Import a camera into this scene.
        """

        self.obj_context = hou.node("/obj")
        self.archive = ""
        self.camera_node = hou.ObjNode
        self.name = ""

        self.cache_path = ""

    def create_from_abc_archive(self):

        """
        Creates the alembic archive node, sets the path and creates the archive
        :return:
        """

        if self.name == "":
            raise NameError("You must set the name attribute")

        child_names = [i.name() for i in self.obj_context.children()]
        if self.name in child_names:
            sys.stdout.write("Geometry object: '{0}' already exists".format(self.name))
            self.archive = self.obj_context.node(self.name)
        else:
            # Create Alembic archives
            self.archive = self.obj_context.createNode('alembicarchive', self.name)

        self.archive.parm('fileName').set(self.cache_path)
        self.archive.parm('loadmode').set('houdini')

        self.update_hierarchy()

    def return_cameras(self):

        """
        Returns any cameras that are in the hierarchy
        :param string abc_file_path:
        :return:
        """

        cameras = list()
        for child in self.archive.allSubChildren():

            if child.type() == hou.objNodeTypeCategory().nodeTypes()["cam"]:
                cameras.append(child)

        return cameras

    def update_hierarchy(self):

        """
        Presses the 'buildHierarchy' button!
        """

        self.archive.parm('buildHierarchy').pressButton()


def get_nodes(abc_file_path=""):

    """
    return all of the polymesh nodes from an alembic file.
    :param string abc_file_path: path to file
    :return:
    """

    # Handle the job environment variable
    if abc_file_path.find("$JOB") != -1:
        job_path = os.environ["JOB"]
        abc_file_path = abc_file_path.replace("$JOB", job_path)

    _abc, _abc_type, alembic_hierarchy = hou_abc.alembicGetSceneHierarchy(abc_file_path, "/")

    alembic_hierarchy_shapes = list()
    alembic_hierarchy_transforms = list()

    queue_alembic_hierarchy = list(alembic_hierarchy[::])

    # Loop through top level objects
    for xfrm, xfrm_type, children in queue_alembic_hierarchy:

        if xfrm_type == "cxform":
            alembic_hierarchy_transforms.append(xfrm)
        elif xfrm_type == "polymesh":
            alembic_hierarchy_shapes.append(xfrm)

        if children != tuple():
            queue_alembic_hierarchy.extend(children)

    return alembic_hierarchy_transforms, alembic_hierarchy_shapes


def get_geometry_nodes(abc_file_path):

    """
    return all of the polymesh nodes from an alembic file.
    :param string abc_file_path: path to file
    :return:
    """

    return get_nodes(abc_file_path=abc_file_path)[1]


def get_transform_nodes(abc_file_path):

    """
    return all of the polymesh nodes from an alembic file.
    :param string abc_file_path: path to file
    :return:
    """

    return get_nodes(abc_file_path=abc_file_path)[0]