import os
import re
from pathlib import Path
from typing import List, Dict, Union

import yaml

from hathor.project.information.lua_file import LuaFile
from hathor.project.information.source_root import SourceRoot


class Project:
    _root_directory: Path
    _config_path: Path
    _config: Dict = None
    _sources_root: List[SourceRoot]

    def __init__(self, config_file: Path):
        self._config_path = config_file
        self._root_directory = self._config_path.parent
        self._sources_root = []

        self._scan()

    @property
    def config(self) -> Dict:
        if self._config is None:
            with self._config_path.open("r") as fp:
                self._config = yaml.load(fp, yaml.FullLoader)

        return self._config

    @property
    def build_config(self) -> Dict:
        return self.config.get("build", {})

    @property
    def serve_config(self):
        return self.config.get("serve", {})

    def resolve_user_path(self, path: Union[str, Path]) -> Path:
        if isinstance(path, str):
            # *nix to host os
            if "/" in path:
                path = os.path.sep.join(path.split("/"))

        path = Path(path)
        if not path.is_absolute():
            path = self._root_directory.joinpath(path)

        return path

    def _scan(self):
        for source_path, properties in self.config["sources"].items():
            if not properties.get("enabled", False):
                continue

            path = self.resolve_user_path(source_path)
            self._sources_root.append(SourceRoot(path, properties))

    @property
    def lua_files(self) -> List[LuaFile]:
        files = []

        for root in self._sources_root:
            files.extend(root.lua_files)

        return files

    @property
    def entry_points(self) -> List[LuaFile]:
        return list(filter(lambda f: f.is_entry_point, self.lua_files))

    @property
    def name(self):
        return self.config["name"]

    @property
    def path_compatible_name(self):
        return re.subn(r"\W", "_", self.name.lower())[0]

    @property
    def build_directory(self) -> Path:
        v = self.build_config.get("directory", "build")
        return self.resolve_user_path(v)

    @property
    def source_directories(self) -> List[Path]:
        return list(map(lambda r: r.path, self._sources_root))


def find_projects(search_root: Path = None) -> List[Project]:
    search_root = search_root or Path(os.getcwd()).absolute()
    projects = []

    for project_config in search_root.rglob("hathor.project.yml"):
        projects.append(Project(project_config))

    return projects
