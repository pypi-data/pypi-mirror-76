import os

from fs.base import FS

from hathor.project.information.project import Project


def build_copy(project: Project, build_root: FS):
    build_root.makedirs("/", recreate=True)

    for lua_file in project.lua_files:
        build_root.makedirs(os.path.dirname(lua_file.path), recreate=True)

        with build_root.open(lua_file.path, "w+") as fp:
            fp.write(lua_file.read())
