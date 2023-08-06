from dataclasses import dataclass
from typing import List
from uuid import uuid4

CLIENTS = dict()


def _generate_client_id() -> str:
    return str(uuid4())


@dataclass
class ChangeListEntry:
    id: str
    kind: str
    path: List[str]
    isDirectory: bool
    isFile: bool


class Client:
    _id: str
    _name: str
    _changes: List[ChangeListEntry]

    def __init__(self, name):
        self._id = _generate_client_id()
        self._name = name
        self._changes = []

        CLIENTS[self._id] = self

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self):
        return self._name

    def add_changes(self, changes: List[ChangeListEntry]):
        self._changes.extend(changes)

    def remove(self):
        CLIENTS.pop(self._id)
