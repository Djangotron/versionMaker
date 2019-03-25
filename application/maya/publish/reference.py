from maya import cmds


def query_referenced_assets():

    """
    Queries the loaded references and returns a list of dictionaries of file name / file path location.

    Returns a list of
    :return:
    """

    all_references = cmds.file(reference=True, query=True)

    reference_names = dict()
    for ref in all_references:

        node = cmds.referenceQuery(ref, namespace=True)[1:]  # Remove the first ':' from the namespace
        reference_names[node] = ref

    return reference_names
