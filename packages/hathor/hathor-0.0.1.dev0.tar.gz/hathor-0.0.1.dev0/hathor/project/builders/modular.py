import os
import shutil

from hathor import resources
from hathor.project.information.project import Project
from hathor.project.information.requirement_explorer import RequirementExplorer


def build_modular(project: Project):
    build_root = project.build_directory.joinpath(project.path_compatible_name)
    if build_root.exists():
        shutil.rmtree(build_root)

    os.makedirs(build_root, exist_ok=True)

    for entry_point in project.entry_points:
        ep_path = build_root.joinpath(entry_point.entry_point_path)
        os.makedirs(ep_path.parent, exist_ok=True)

        modules_directory_name = entry_point.name + "_Modules"
        modules_directory = ep_path.parent.joinpath(modules_directory_name)
        os.makedirs(modules_directory, exist_ok=True)

        explorer = RequirementExplorer(project, entry_point)

        def emit_modules():
            to_emit = {
                entry_point.require_alias: entry_point
            }

            for link in explorer.links:
                for requirement in link.requirements:
                    to_emit[requirement.require_alias] = requirement

            for require_str, file in to_emit.items():
                path = modules_directory.joinpath(require_str + ".lua")

                with path.open("w+") as output_fp:
                    output_fp.write(file.processed_contents())

        def emit_loader():
            loader_path = modules_directory.joinpath("__HathorLoader.lua")
            with loader_path.open("w+") as fp:
                fp.write(resources.hathor_loader())

        def emit_runner():
            with ep_path.parent.joinpath(f"{entry_point.name}.Run.lua").open("w+") as fp:
                fp.write(resources.hathor_run(modules_directory_name, entry_point.require_alias))

        emit_modules()
        emit_loader()
        emit_runner()
