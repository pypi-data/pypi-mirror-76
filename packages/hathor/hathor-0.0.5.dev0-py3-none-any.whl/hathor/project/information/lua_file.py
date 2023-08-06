import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Union

from hathor import resources

ENTRY_POINT_PTN = re.compile(r"---\s*@entrypoint\s+(\w+)\s+([\w\d.]+)")
REQUIRE_PTN = re.compile(r"require\([\"\']([\w\d\.]+)[\'\"]\)")
QUOTES = "'" + '"'


class EntryPointType:
    script = "Script"
    local_script = "LocalScript"


@dataclass
class EntryPointDefinition:
    line: str
    type: str
    game_location: str


@dataclass
class RequireDefinition:
    line: str
    require: str

    def __str__(self):
        return self.require


class LuaFile:
    _path: Path
    _entry_point: Union[None, EntryPointDefinition] = None
    _requires: List[RequireDefinition]
    _source_root_path: Path

    def __init__(self, source_root_path: Path, path: Path):
        self._source_root_path = source_root_path
        self._path = path.absolute()
        self._requires = []
        self._scan()

    def _scan(self):
        with self._path.open("r") as fp:
            for line in fp.readlines():
                if match := ENTRY_POINT_PTN.match(line):
                    self._entry_point = EntryPointDefinition(
                        line,
                        match.group(1).strip(),
                        match.group(2).strip()
                    )

                if match := REQUIRE_PTN.search(line.strip()):
                    self._requires.append(RequireDefinition(
                        line,
                        match.group(1).strip()
                    ))

    @property
    def is_entry_point(self):
        return self._entry_point is not None

    @property
    def require_alias(self) -> str:
        relative_path = self._path.relative_to(self._source_root_path)
        path_split = str(relative_path).split(os.path.sep)
        last = len(path_split) - 1
        file_name_split = path_split[last].split(".")
        path_split[last] = ".".join(file_name_split[:-1])

        return ".".join(path_split)

    @property
    def requires(self) -> List[RequireDefinition]:
        return list(self._requires)

    @property
    def name(self):
        return ".".join(self._path.name.split('.')[:-1])

    @property
    def entry_point_path(self) -> Path:
        assert self.is_entry_point, "File must be an entry point"

        return Path(*self._entry_point.game_location.split("."))

    def read(self):
        with self._path.open("r") as fp:
            contents = fp.read()

        return contents

    def processed_contents(self):
        contents = self.read()
        contents = resources.hathor_stub() + "\n" + contents

        processed_lines = []

        for line in contents.splitlines():
            if match := REQUIRE_PTN.search(line):
                proc_line = REQUIRE_PTN.sub(f"__require(\"{match.group(1)}\")", line)
                processed_lines.append(proc_line)

                continue

            processed_lines.append(line)

        contents = "\n".join(processed_lines)

        return contents

    def __str__(self):
        return self.require_alias
