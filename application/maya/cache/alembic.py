from maya import cmds, OpenMaya, mel
from ....version import utilities


def alembic_kwargs_to_jargs(**kwargs):
    """
    Convenience method for generating jobArgs for alembic import and export.
    :param kwargs:
    :return:
    """
    kwargs.setdefault('step', 1.0)
    kwargs.setdefault('attr', 'alembicID')
    paramsOrder = ['root',
                   'frameRange',
                   'step',
                   'uvWrite',
                   'writeVisibility',
                   'worldSpace',
                   'attr',
                   'file']

    params = []
    for param in paramsOrder:
        kwargs.setdefault(param, None)
        if param == "root":
            roots = kwargs[param].split()
            for root in roots:
                params.append('-{0} {1}'.format(param, root))
        elif kwargs[param] is None:
            params.append('-{0}'.format(param))
        else:
            params.append('-{0} {1}'.format(param, kwargs[param]))

    return ' '.join(params)


class AlembicCache(object):
    """Class to generate alembic cache commands"""

    # try:
    if not cmds.pluginInfo('AbcExport.mll', query=True, loaded=True):
        cmds.loadPlugin('AbcExport.mll')
    if not cmds.pluginInfo('AbcExport.mll', query=True, loaded=True):
        cmds.loadPlugin('AbcExport.mll')
    # except Exception:
    #     raise Exception("Cannot load Alembic Plugins")

    # Alembic Export Options
    '''
    // AbcExport [options]
    Options:
    -h / -help  Print this message.

    -prs / -preRollStartFrame double
    The frame to start scene evaluation at.  This is used to set the
    starting frame for time dependent translations and can be used to evaluate
    run-up that isn't actually translated.

    -duf / -dontSkipUnwrittenFrames
    When evaluating multiple translate jobs, the presence of this flag decides
    whether to evaluate frames between jobs when there is a gap in their frame
    ranges.

    -v / -verbose
    Prints the current frame that is being evaluated.

    -j / -jobArg string REQUIRED
    String which contains flags for writing data to a particular file.
    Multiple jobArgs can be specified.

    -jobArg flags:

    -a / -attr string
    A specific geometric attribute to write out.
    This flag may occur more than once.

    -df / -dataFormat string
    The data format to use to write the file.  Can be either HDF or Ogawa.
    The default is Ogawa.

    -atp / -attrPrefix string (default ABC_)
    Prefix filter for determining which geometric attributes to write out.
    This flag may occur more than once.

    -ef / -eulerFilter
    If this flag is present, apply Euler filter while sampling rotations.

    -f / -file string REQUIRED
    File location to write the Alembic data.

    -fr / -frameRange double double
    The frame range to write.
    Multiple occurrences of -frameRange are supported within a job. Each
    -frameRange defines a new frame range. -step or -frs will affect the
    current frame range only.

    -frs / -frameRelativeSample double
    frame relative sample that will be written out along the frame range.
    This flag may occur more than once.

    -nn / -noNormals
    If this flag is present normal data for Alembic poly meshes will not be
    written.

    -pr / -preRoll
    If this flag is present, this frame range will not be sampled.

    -ro / -renderableOnly
    If this flag is present non-renderable hierarchy (invisible, or templated)
    will not be written out.

    -rt / -root
    Maya dag path which will be parented to the root of the Alembic file.
    This flag may occur more than once.  If unspecified, it defaults to '|' which
    means the entire scene will be written out.

    -s / -step double (default 1.0)
    The time interval (expressed in frames) at which the frame range is sampled.
    Additional samples around each frame can be specified with -frs.

    -sl / -selection
    If this flag is present, write out all all selected nodes from the active
    selection list that are descendents of the roots specified with -root.

    -sn / -stripNamespaces (optional int)
    If this flag is present all namespaces will be stripped off of the node before
    being written to Alembic.  If an optional int is specified after the flag
    then that many namespaces will be stripped off of the node name. Be careful
    that the new stripped name does not collide with other sibling node names.

    Examples:
    taco:foo:bar would be written as just bar with -sn
    taco:foo:bar would be written as foo:bar with -sn 1

    -u / -userAttr string
    A specific user attribute to write out.  This flag may occur more than once.

    -uatp / -userAttrPrefix string
    Prefix filter for determining which user attributes to write out.
    This flag may occur more than once.

    -uv / -uvWrite
    If this flag is present, uv data for PolyMesh and SubD shapes will be written to
    the Alembic file.  Only the current uv map is used.

    -wcs / -writeColorSets
    Write all color sets on MFnMeshes as color 3 or color 4 indexed geometry
    parameters with face varying scope.

    -wfs / -writeFaceSets
    Write all Face sets on MFnMeshes.

    -wfg / -wholeFrameGeo
    If this flag is present data for geometry will only be written out on whole
    frames.

    -ws / -worldSpace
    If this flag is present, any root nodes will be stored in world space.

    -wv / -writeVisibility
    If this flag is present, visibility state will be stored in the Alembic
    file.  Otherwise everything written out is treated as visible.

    -wuvs / -writeUVSets
    Write all uv sets on MFnMeshes as vector 2 indexed geometry
    parameters with face varying scope.
    -wc / -writeCreases
    If this flag is present and the mesh has crease edges or crease vertices,
    the mesh (OPolyMesh) would now be written out as an OSubD and crease info will be stored in the Alembic
    file. Otherwise, creases info won't be preserved in Alembic file
    unless a custom Boolean attribute SubDivisionMesh has been added to mesh node and its value is true.

    -mfc / -melPerFrameCallback string
    When each frame (and the static frame) is evaluated the string specified is
    evaluated as a Mel command. See below for special processing rules.

    -mpc / -melPostJobCallback string
    When the translation has finished the string specified is evaluated as a Mel
    command. See below for special processing rules.

    -pfc / -pythonPerFrameCallback string
    When each frame (and the static frame) is evaluated the string specified is
    evaluated as a python command. See below for special processing rules.

    -ppc / -pythonPostJobCallback string
    When the translation has finished the string specified is evaluated as a
    python command. See below for special processing rules.

    Special callback information:
    On the callbacks, special tokens are replaced with other data, these tokens
    and what they are replaced with are as follows:

    #FRAME# replaced with the frame number being evaluated.
    #FRAME# is ignored in the post callbacks.

    #BOUNDS# replaced with a string holding bounding box values in minX minY minZ
    maxX maxY maxZ space seperated order.

    #BOUNDSARRAY# replaced with the bounding box values as above, but in
    array form.
    In Mel: {minX, minY, minZ, maxX, maxY, maxZ}
    In Python: [minX, minY, minZ, maxX, maxY, maxZ]

    Examples:

    AbcExport -j "-root |group|foo -root |test|path|bar -file /tmp/test.abc"
    Writes out everything at foo and below and bar and below to /tmp/test.abc.
    foo and bar are siblings parented to the root of the Alembic scene.

    AbcExport -j "-frameRange 1 5 -step 0.5 -root |group|foo -file /tmp/test.abc"
    Writes out everything at foo and below to /tmp/test.abc sampling at frames:
    1 1.5 2 2.5 3 3.5 4 4.5 5

    AbcExport -j "-fr 0 10 -frs -0.1 -frs 0.2 -step 5 -file /tmp/test.abc"
    Writes out everything in the scene to /tmp/test.abc sampling at frames:
    -0.1 0.2 4.9 5.2 9.9 10.2

    Note: The difference between your highest and lowest frameRelativeSample can
    not be greater than your step size.

    AbcExport -j "-step 0.25 -frs 0.3 -frs 0.60 -fr 1 5 -root foo -file test.abc"

    Is illegal because the highest and lowest frameRelativeSamples are 0.3 frames
    apart.

    AbcExport -j "-sl -root |group|foo -file /tmp/test.abc"
    Writes out all selected nodes and it's ancestor nodes including up to foo.
    foo will be parented to the root of the Alembic scene.
    '''

    # Alembic Import Options
    '''
    AbcImport  [options] File

    Options:
    -rpr/ reparent      DagPath
                        reparent the whole hierarchy under a node in the
                        current Maya scene
    -ftr/ fitTimeRange
                        Change Maya time slider to fit the range of input file.
    -rcs / recreateAllColorSets
                        IC3/4fArrayProperties with face varying scope on
                        IPolyMesh and ISubD are treated as color sets even if
                        they weren't written out of Maya.
    -ct / connect       string node1 node2 ...
                        The nodes specified in the argument string are supposed to be the names of top level nodes from the input file.
                        If such a node doesn't exist in the provided input file, awarning will be given and nothing will be done.
                        If Maya DAG node of the same name doesn't exist in the    current Maya scene,  a warning will be given and nothing will be done.
                        If such a node exists both in the input file and in the   current Maya scene, data for the whole hierarchy from the nodes down
                        (inclusive) will be substituted by data from the input file, and connections to the AlembicNode will be made or updated accordingly.
                        If string "/" is used as the root name,  all top level  nodes from the input file will be used for updating the current Maya scene.
                        Again if certain node doesn't exist in the current scene, a warning will be given and nothing will be done.
                        If a single node is specified and it exists in the Maya scene but doesn't exist in the archive, children of that node will be connected to the children of the archive.
    -crt/ createIfNotFound
                        Used only when -connect flag is set.
    -rm / removeIfNoUpdate
                        Used only when -connect flag is set.
    -sts/ setToStartFrame
                        Set the current time to the start of the frame range
    -m  / mode          string ("open"|"import"|"replace")
                        Set read mode to open/import/replace (default to import)
    -ft / filterObjects "regex1 regex2 ..."
                        Selective import cache objects whose name matches with
    -eft / excludeFilterObjects "regex1 regex2 ..."
                        Selective exclude cache objects whose name matches with
    the input regular expressions.
    -h  / help          Print this message
    -d  / debug         Turn on debug message printout
    '''

    def __init__(self):

        """
        Controls importing and exporting alembic caches in maya.

        Possible import modes: ("open"|"import"|"replace")
        """

        self.file_path = ""

        # Export controls
        self.export_command = ""
        self.cache_set = "cache_set"
        self.cache_objects = list()
        self.user_attributes = list()
        self.user_attributes_string = str()  # do not use this attr
        self.pre_roll_frame = 1
        self.start_frame = 1
        self.end_frame = 10
        self.step = 1
        self.frame_relative_samples = [-0.25, 0.25]
        self.renderable_only = False
        self.write_visibility = True
        self.root_geometries = str()

        # alembic import nodes
        self.alembic_node = str()
        self.alembic_heirarchy_top_nodes = list()

        # import controls
        self.import_command = ""
        self.fit_time_range = False
        self.import_mode = "import"
        self.import_parent = ""
        self.lock_exposed_transform_channels = True
        self.import_namespace = ""
        self.use_import_namespace = True
        self.add_meta_data_attributes = True

        self.alembic_verbose = False

        self.has_been_called = False

    def __call__(self):

        """
        compile the export command.
        :return:
        """

        # Print the cacheable objects
        if self.alembic_verbose:
            OpenMaya.MGlobal.displayInfo("{0}\tcache_objects:{1}".format(self.__module__, self.cache_objects))

        if not self.has_been_called:

            self.set_cache_geometries()
            self.append_user_attributes()
            self.set_export_command()

            self.has_been_called = True

    def append_user_attributes(self):

        """
        Append specific user attributes to the alembic cache
        :return:
        """

        for cache_obj in self.cache_objects:
            for attr in self.user_attributes:
                if cmds.attributeQuery(attr, node=cache_obj, exists=True):

                    attr_str = " -userAttr " + attr
                    self.user_attributes_string += attr_str

    def clean_up_alembic_hierarchy(self, top_transform=""):

        """
        Return the children of a top_transform
        :param string top_transform:
        :return:
        """

        descendants = cmds.listRelatives(top_transform, allDescendents=True, fullPath=True)
        if descendants is None:
            return list()

        descendants.insert(0, top_transform)

        type_list = list()
        non_type_list = list()
        for descendant in descendants:
            # check the object type.
            shape_type = cmds.objectType(descendant)

            if shape_type == "transform":
                type_list.append(descendant)
            else:
                non_type_list.append(descendant)

        # Lock the transforms
        if self.lock_exposed_transform_channels:
            for transform in type_list:
                for xform in ("t", "r", "s"):
                    for axis in ("x", "y", "z"):

                        transform_attr = "{0}.{1}{2}".format(transform, xform, axis)
                        # Pass if there is a transform connection
                        if cmds.listConnections(transform_attr, source=True, destination=False) is not None:
                            continue

                        # lock if there is no connection
                        if not cmds.getAttr(transform_attr, lock=True):
                            cmds.setAttr(transform_attr, lock=True)

        if self.add_meta_data_attributes:
            for descendant in descendants:
                cmds.addAttr(descendant, ln="originalName", dt="string")
                cmds.setAttr("{0}.originalName".format(descendant), descendant, lock=True, type="string")

        if self.use_import_namespace:
            cmds.namespaceinfo()

        self.alembic_heirarchy_top_nodes = cmds.listRelatives(top_transform, children=True)

        return self.alembic_heirarchy_top_nodes

    def export(self):
        """
        Run the export command.
        :return:
        """

        try:
            mel.eval(self.export_command)
        finally:
            OpenMaya.MGlobal.displayInfo(self.export_command)

    def get_cache_sets(self):

        """
        Returns and objects sets that have the name 'cache_set'
        :return:
        """

        return [i for i in cmds.ls(type="objectSet") if i.find(self.cache_set) != -1]

    def import_cache(self):

        """
        Imports an alembic cache into a maya scene.
        :return:
        """

        try:
            self.alembic_node = mel.eval(self.import_command)
        except RuntimeError:
            raise RuntimeError("Unable to import alembic cache")
        finally:
            OpenMaya.MGlobal.displayInfo(self.import_command)

        self.clean_up_alembic_hierarchy(top_transform=self.import_parent)

        return self.alembic_node

    def set_export_command(self):

        """
        Formats and creates the export command
        :return:
        """

        verbose = ""
        if self.alembic_verbose:
            verbose = " -v"

        if self.root_geometries == list():
            raise NameError("No root geometries set.")

        renderable_only = ""
        if self.renderable_only:
            renderable_only = " -renderableOnly"

        write_visibility = ""
        if self.write_visibility:
            write_visibility = " -writeVisibility"

        self.export_command = \
            'AbcExport -j{verbose} "-sn -frameRange {start} {end} -uvWrite -dataFormat ogawa -worldSpace{root}{renderable_only}{write_visibility}{user_attributes} -file \\"{file_path}\\""'.format(
                verbose=verbose,
                start=self.start_frame,
                end=self.end_frame,
                root=self.root_geometries,
                renderable_only=renderable_only,
                write_visibility=write_visibility,
                user_attributes=self.user_attributes_string,
                file_path=self.file_path
            )

    def set_import_command(self):

        """
        Formats and creates the export command
        :return:
        """

        reparent = ""
        if self.import_parent != "":
            reparent = ' -reparent \"{0}\"'.format(self.import_parent)

        fit_time_range = ""
        if self.fit_time_range:
            fit_time_range = " -fitTimeRange"

        self.import_command = \
            'AbcImport -mode {import_mode}{reparent}{fitTimeRange} \"{file_path}\";'.format(
                import_mode=self.import_mode,
                reparent=reparent,
                fitTimeRange=fit_time_range,
                file_path=self.file_path
            )

    def set_cache_geometries(self):

        """
        Caches out all geo in cache sets
        :return:
        """

        # cache_sets = self.get_cache_sets()
        #
        # for cache_set in cache_sets:
        #
        #     self.cache_objects = cmds.sets(cache_set, query=True)

        for obj in self.cache_objects:
            self.root_geometries += " -root {0}".format(obj)
