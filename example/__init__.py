import version.folder
import metadata.meta_data_file


def create():

    _ver = version.folder.Version()
    _ver.path_to_versions = "D:\\temp\\test"
    _ver.type_folder = "SH__0010__ni__animation"
    _ver.get_folder_versions()
    _ver.create_version()
    print _ver.version

    _meta_data = metadata.meta_data_file.WriteFile()
    _meta_data.publish_type = "animation"
    _meta_data.meta_data_file_path = "{0}\\SH__0010__ni__{1}.json".format(_ver.folder_version_path, _meta_data.publish_type)
    _meta_data.meta_data_folder_path = _ver.folder_version_path
    _meta_data.message = "testing a publish"
    _meta_data.folder_location = "{0}\\{1}.json".format(_ver.folder_version_path, _ver.type_folder)
    _meta_data.long_name = "SH__0010__ni__animation__v{0:04}".format(_ver.version)
    _meta_data.file_types = "alembic"
    _meta_data.application = "maya"

    print _ver.folder_version_path
    _meta_data.set_globals()
    _meta_data.create_file()
