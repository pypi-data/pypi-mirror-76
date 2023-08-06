from dataclasses import dataclass
from typing import Dict, List

from hathor.project.information.lua_file import LuaFile
from hathor.project.information.project import Project


@dataclass
class RequireLink:
    file: LuaFile
    requirements: List[LuaFile]


class RequirementExplorer:
    _project: Project
    _entry_point: LuaFile
    _links: List[RequireLink]

    def __init__(self, project: Project, entry_point: LuaFile):
        self._project = project
        self._entry_point = entry_point
        self._links = []

        self._build()

    def _build(self):
        reference: Dict[str, LuaFile] = \
            dict(zip(map(lambda f: f.require_alias, self._project.lua_files), self._project.lua_files))

        def _process_file(file: LuaFile):
            requirements: List[LuaFile] = []

            for require_def in file.requires:
                if required_file := reference.get(require_def.require, None):
                    requirements.append(required_file)

                else:
                    raise RuntimeError(str(require_def))

            self._links.append(RequireLink(file, requirements))

            for requirement in requirements:
                _process_file(requirement)

        _process_file(self._entry_point)

    @property
    def links(self) -> List[RequireLink]:
        return list(self._links)
