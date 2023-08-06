from typing import Callable, Dict

from fs.base import FS

from hathor.project.builders.copy import build_copy
from hathor.project.builders.modular import build_modular
from hathor.project.information.project import Project

Builder = Callable[[Project, FS], None]

BUILDERS: Dict[str, Builder] = {
    "copy": build_copy,
    "modular": build_modular
}

DEFAULT_BUILDER: str = list(BUILDERS.keys())[0]


class BuilderNotFound(RuntimeError):
    def __init__(self, name: str):
        super().__init__(f"The builder '{name}' could not be found")


def get_builder(name: str) -> Builder:
    if builder := BUILDERS.get(name, None):
        return builder

    else:
        raise BuilderNotFound(name)
