import hashlib
import logging
import os
import time
import uuid
from threading import Thread
from typing import Dict, Callable, List

from fs.base import FS
from fs.info import Info
from fs.memoryfs import MemoryFS

from hathor.project.builders import Builder, get_builder
from hathor.project.information.project import Project
from hathor.serve import change_tracker
from hathor.serve.client import iter_clients, Client, OnClientAdded
from hathor.serve.models import ChangeListEntry, Kind, KindType

LOG = logging.getLogger(__name__)

ChangeList = Dict[str, ChangeListEntry]


def _tuple_path(p: str):
    return tuple(list(filter(lambda s: not not s.strip(), p.split(os.path.sep))))


def _append_change(change_list: ChangeList, build_root: FS, path: str, info: Info, kind: KindType):
    change_list[path] = ChangeListEntry(
        id=str(uuid.uuid4()),
        kind=kind,
        path=_tuple_path(path),
        isDirectory=info.is_dir,
        isFile=info.is_file,
        fs=build_root
    )


def _hash_string(s: str):
    h = hashlib.blake2b()
    h.update(s.encode("UTF-8"))

    digest = h.hexdigest()

    return digest.lower()


def _diff_hash_table(left, right) -> List[str]:
    diff = set()

    def go(left_table, right_table):
        for left_key, left_value in left_table.items():
            right_value = right_table.get(left_key)
            if left_value != right_value:
                diff.add(left_key)

    go(left, right)
    go(right, left)

    return list(diff)


class ProjectBuilderThread(Thread):
    _running: bool = True
    _project: Project
    _builder: Builder
    _interval: float

    _build_root: MemoryFS = None
    _hash_table: Dict[str, str] = None

    _name: str
    _log: logging.Logger

    _on_client_added_handle: OnClientAdded

    def __init__(self, project: Project, builder: Builder, interval: float):
        super().__init__()

        self._project = project
        self._builder = builder
        self._interval = float(interval)

        self._build_root = MemoryFS()
        self._hash_table = dict()

        self._name = f"Project builder for '{project.name}'"
        self.setName(self._name)

        self._log = logging.getLogger(self._name)

        self._on_client_added_handle = OnClientAdded(self._on_client_added)

    def _build(self):
        self._log.debug("Going to build the project")

        t0 = time.time()

        self._project.rescan()
        self._builder(self._project, self._build_root)

        dt = time.time() - t0
        LOG.debug(f"Building the project took {round(dt, 5)} seconds")

    def _iter_files(self, f: Callable[[str, Info], None]):
        if self._build_root:
            for path, info in self._build_root.glob("**/*"):
                if not self._build_root.isfile(path):
                    continue

                f(path, info)

    def _update_hash_table(self):
        self._hash_table = dict()

        def hash_file(path: str, info: Info):
            with self._build_root.open(path, "r") as fp:
                self._hash_table[path] = _hash_string(fp.read())

        self._iter_files(hash_file)

        return dict(self._hash_table)

    def _on_client_added(self, client: Client):
        change_list: ChangeList = dict()

        self._iter_files(lambda path, info: _append_change(
            change_list=change_list,
            build_root=self._build_root,
            path=path,
            info=info,
            kind=Kind.create
        ))

        client.add_changes(list(change_list.values()))

    def _prepare_changes(self) -> ChangeList:
        change_list: ChangeList = dict()

        self._iter_files(lambda path, info: _append_change(
            change_list=change_list,
            build_root=self._build_root,
            path=path,
            info=info,
            kind=Kind.delete
        ))

        return change_list

    def _distribute_changes(self, change_list: ChangeList):
        for client in iter_clients():
            client.add_changes(list(change_list.values()))

    def _clean(self):
        for f in self._build_root.listdir("/"):
            if self._build_root.isdir(f):
                self._build_root.removetree(f)

            elif self._build_root.isfile(f):
                self._build_root.remove(f)

    def run(self) -> None:
        self._log.debug("Running the project builder")

        def _wait(seconds: float, interval: float = 0.1):
            while seconds > 0 and self._running:
                time.sleep(interval)
                seconds -= interval

        while self._running:
            changes = change_tracker.take_changes()

            if len(changes) > 0:
                # Setup
                table_before = self._update_hash_table()
                change_list = self._prepare_changes()

                # Clean build in memory
                self._clean()
                self._build()

                # Undo all faux removals
                for path, change in dict(change_list).items():
                    if self._build_root.exists(path) and change.kind == Kind.delete:
                        change_list.pop(path)

                # Add all files from the memory fs
                self._iter_files(lambda p, info: _append_change(
                    change_list=change_list,
                    build_root=self._build_root,
                    path=p,
                    info=info,
                    kind=Kind.modify
                ))

                # Find all real changes
                table_after = self._update_hash_table()
                hash_table_changes = _diff_hash_table(table_before, table_after)

                # Filter out unchanged files using the hash table
                reduced_changelist: ChangeList = dict()
                for path, change in change_list.items():
                    if path in hash_table_changes:
                        reduced_changelist[path] = change

                # Distribute all changes
                self._distribute_changes(reduced_changelist)

            try:
                _wait(self._interval)

            except Exception as e:
                self._running = False
                self._log.info(f"time.sleep interrupt: {str(e)}")

    def stop(self):
        self._log.info("Stopping project builder")
        self._running = False

    def __del__(self):
        self._on_client_added_handle.disconnect()


class State:
    thread: ProjectBuilderThread = None


def stop():
    if State.thread:
        LOG.debug("at_exit handler is going to stop a project builder thread")
        State.thread.stop()
        LOG.debug("Joining that thread now")
        State.thread.join()


def configure(project: Project, builder: str, interval: int):
    assert State.thread is None, "The project builder is already configured"

    State.thread = ProjectBuilderThread(
        project,
        get_builder(builder),
        interval
    )

    State.thread.start()
