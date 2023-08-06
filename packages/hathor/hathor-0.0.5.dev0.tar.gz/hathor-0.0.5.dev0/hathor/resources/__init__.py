from pathlib import Path
from string import Template
from typing import Union, Dict

from cachetools import cached, LRUCache

HERE = Path(__file__).absolute().parent


@cached(cache=LRUCache(64))
def _read_text(path: Union[Path, str]) -> str:
    if isinstance(path, str):
        path = Path(path)

    with HERE.joinpath(path).open("r") as fp:
        return fp.read()


def hathor_loader():
    return _read_text("hathor_loader.lua")


def hathor_stub():
    return _read_text("hathor_stub.lua")


def hathor_run(modules_name: str, entry_point: str) -> str:
    template = Template(_read_text("hathor_run.lua"))

    return template.safe_substitute({
        "modules_name": modules_name,
        "entry_point": entry_point
    })


def gitignore_base():
    return _read_text("gitignore_base.txt")


def editorconfig_template(properties: Dict[str, str]) -> str:
    template = Template(_read_text("editorconfig_template.ini"))

    return template.safe_substitute(properties)
