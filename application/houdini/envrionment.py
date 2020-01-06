import os


def path_to_path_expression(path="", envrionment_key="JOB"):

    """
    Convert the alembic path to a relative path.

    :param string path:  Path to the file. The file does not have to exist.
    :param string envrionment_key:  The environment variable key, usually JOB or HIP
    :return: string - path_expression attribute
    """

    if envrionment_key not in os.environ:
        raise RuntimeError("Environment Key: '{0}' not in environment variables".format(envrionment_key))

    key_path = os.environ[envrionment_key]
    if key_path not in path:
        raise RuntimeError("JOB environment variables path: '{0}'\nNot in path: {1}".format(key_path, path))

    path_expression = path.replace(key_path, "${0}".format(envrionment_key))

    return path_expression
