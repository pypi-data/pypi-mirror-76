from typing import List, Dict
from uuid import uuid4

from hathor.serve.models import ChangeListEntry, Package, PackageTakeout

CLIENTS = dict()
THREAD_INTERVAL = 2


def by_id(client_id: str):
    return CLIENTS.get(client_id, None)


class OnClientAdded:
    _listener: callable
    _listeners: List[callable] = []

    def __init__(self, listener: callable):
        self._listener = listener
        self._listeners.append(listener)

    def disconnect(self):
        self._listeners.remove(self._listener)

    @classmethod
    def fire(cls, client):
        for listener in cls._listeners:
            listener(client)


class OnClientRemoved:
    _listener: callable
    _listeners: List[callable] = []

    def __init__(self, listener: callable):
        self._listener = listener
        self._listeners.append(listener)

    def disconnect(self):
        self._listeners.remove(self._listener)

    @classmethod
    def fire(cls, client):
        for listener in cls._listeners:
            listener(client)


def _generate_client_id() -> str:
    return str(uuid4())


class Client:
    _id: str
    _name: str
    _changes: Dict[str, ChangeListEntry]
    _packages: Dict[str, Package]

    def __init__(self, name):
        self._id = _generate_client_id()
        self._name = name

        self._changes = dict()
        self._packages = dict()

        CLIENTS[self._id] = self
        OnClientAdded.fire(self)

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self):
        return self._name

    def add_changes(self, changes: List[ChangeListEntry]):
        for change in changes:
            self._changes[change.id] = change

    def remove(self):
        CLIENTS.pop(self._id)
        OnClientRemoved.fire(self)

    @property
    def changes(self) -> List[ChangeListEntry]:
        return list(self._changes.values())

    def delete_changes(self, changes: List[str]):
        for change in changes:
            if change in self._changes:
                self._changes.pop(change)

    def create_package(self, change_ids: List[str]) -> Package:
        package = Package(
            id=str(uuid4()),
            changes=list(
                map(lambda t: t[1],
                    filter(lambda t: t[0] in change_ids,
                           self._changes.items()
                           )
                    )
            )
        )

        self._packages[package.id] = package

        return package

    def create_takeout(self, package_id: str) -> PackageTakeout:
        package = self._packages[package_id]

        takeout = PackageTakeout(dict())

        for change in package.changes:
            if not takeout.add_change(change):
                break

            if change.id in self._changes:
                self._changes.pop(change.id)

        return takeout

    def delete_package(self, package_id):
        if package_id in self._packages:
            self._packages.pop(package_id)


def iter_clients():
    for client in CLIENTS.values():
        yield client
