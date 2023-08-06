from pathlib import Path
from typing import List, Dict

from hathor.project.information.lua_file import LuaFile


class SourceRoot:
    _path: Path
    _properties: Dict
    _lua_files: List[LuaFile]

    def __init__(self, path: Path, properties: Dict):
        self._path = path.absolute()
        self._properties = properties
        self._lua_files = []

        self._scan()

    def _scan(self):
        self._lua_files.extend(map(lambda p: LuaFile(self._path, p), self._path.rglob("*.lua")))

    @property
    def lua_files(self) -> List[LuaFile]:
        return list(self._lua_files)

    @property
    def path(self):
        return self._path
