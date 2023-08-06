from typing import List, Dict

from fs.base import FS

from hathor.project.information.lua_file import LuaFile


class SourceRoot:
    _fs: FS
    _properties: Dict
    _lua_files: List[LuaFile]

    def __init__(self, fs: FS, properties: Dict):
        self._fs = fs
        self._properties = properties
        self._lua_files = []

        self._scan()

    def _scan(self):
        self._lua_files.extend(map(lambda gm: LuaFile(self._fs, gm.path), self._fs.glob("**/*.lua")))

    @property
    def lua_files(self) -> List[LuaFile]:
        return list(self._lua_files)

    @property
    def path(self):
        return self._path

    @property
    def fs(self):
        return self._fs
