from pathlib import Path
from string import Template

from cachetools import cached, LRUCache

HERE = Path(__file__).absolute().parent


@cached(cache=LRUCache(64))
def _read_text(path: Path) -> str:
    with HERE.joinpath(path).open("r") as fp:
        return fp.read()


def hathor_loader():
    return _read_text(Path("hathor_loader.lua"))


def hathor_stub():
    return _read_text(Path("hathor_stub.lua"))


def hathor_run(modules_name: str, entry_point: str) -> str:
    template = Template(_read_text(Path("hathor_run.lua")))

    return template.safe_substitute({
        "modules_name": modules_name,
        "entry_point": entry_point
    })
