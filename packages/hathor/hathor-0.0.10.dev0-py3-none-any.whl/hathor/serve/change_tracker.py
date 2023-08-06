import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from fs.base import FS

from hathor.project.information.project import Project
from hathor.serve.models import Kind, KindType

LOG = logging.getLogger(__name__)


@dataclass()
class FSChange:
    project: Project
    fs: FS
    kind: KindType
    real_path: Path
    relative_path: Path

    @property
    def path_string(self):
        return "/".join(self.relative_path.parts)


Changes = Dict[str, FSChange]


class State:
    changes: Changes = {}


def notify(change: FSChange):
    changes = State.changes
    path = change.path_string

    if change.kind == Kind.create or change.kind == Kind.modify:
        changes[path] = change

    elif change.kind == Kind.delete and path in changes:
        changes.pop(path)

    LOG.debug("--- CHANGES ---")
    for change in changes.values():
        LOG.debug((change.path_string, change.kind))


def take_changes():
    changes = State.changes
    State.changes = dict()

    return changes
