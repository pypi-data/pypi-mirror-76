import logging
from pathlib import Path

from fs.base import FS
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent
from watchdog.observers import Observer

from hathor.project.information.project import Project
from hathor.serve import change_tracker
from hathor.serve.change_tracker import FSChange
from hathor.serve.models import KindType, Kind

LOG = logging.getLogger(__name__)


class ChangeHandler(FileSystemEventHandler):
    _fs: FS
    _root: Path
    _project: Project

    def __init__(self, project: Project, fs: FS):
        self._project = project
        self._fs = fs
        self._root = Path(fs.root_path)

    def create_change_entry(self, kind: KindType, src_path: str):
        real_path = Path(src_path).absolute()
        relative_path = real_path.relative_to(self._root)

        change = FSChange(
            project=self._project,
            fs=self._fs,
            kind=kind,
            real_path=real_path,
            relative_path=relative_path
        )

        LOG.debug(change)

        change_tracker.notify(change)

    def on_created(self, event):
        if isinstance(event, FileCreatedEvent):
            self.create_change_entry(Kind.create, event.src_path)

    def on_deleted(self, event):
        if isinstance(event, FileDeletedEvent):
            self.create_change_entry(Kind.delete, event.src_path)

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            self.create_change_entry(Kind.modify, event.src_path)


def watch_files(project: Project):
    observer = Observer()

    for fs in project.source_file_systems:
        fs: FS = fs

        handler = ChangeHandler(project, fs)
        root_path = fs.root_path

        for path, info in fs.glob("**/*.lua"):
            absolute_path = Path(root_path, path.lstrip("/"))
            handler.create_change_entry(Kind.modify, absolute_path)

        observer.schedule(handler, root_path, recursive=True)

    observer.start()
