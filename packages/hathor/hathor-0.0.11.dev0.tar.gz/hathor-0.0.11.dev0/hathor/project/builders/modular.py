from fs.base import FS

from hathor import resources
from hathor.project.information.project import Project
from hathor.project.information.requirement_explorer import RequirementExplorer


def build_modular(project: Project, build_root: FS):
    build_root.makedirs("/", recreate=True)

    for entry_point in project.entry_points:
        epp = build_root.makedirs(str(entry_point.entry_point_path.parent), recreate=True)

        modules_directory_name = entry_point.name + "_Modules"
        modules_directory = epp.makedirs(modules_directory_name, recreate=True)

        explorer = RequirementExplorer(project, entry_point)

        def emit_modules():
            to_emit = {
                entry_point.require_alias: entry_point
            }

            for link in explorer.links:
                for requirement in link.requirements:
                    to_emit[requirement.require_alias] = requirement

            for require_str, file in to_emit.items():
                with modules_directory.open(require_str + ".lua", "w+") as fp:
                    fp.write(file.processed_contents())

        def emit_loader():
            with modules_directory.open("__HathorLoader.lua", "w+") as fp:
                fp.write(resources.hathor_loader())

        def emit_runner():
            with epp.open(f"{entry_point.name}.Run.lua", "w+") as fp:
                fp.write(resources.hathor_run(modules_directory_name, entry_point.require_alias))

        emit_modules()
        emit_loader()
        emit_runner()
