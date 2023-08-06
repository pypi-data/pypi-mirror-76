import os
from dataclasses import dataclass
from typing import Tuple, List, Dict

from fs.base import FS

KindType = str


@dataclass()
class Kind:
    create: KindType = "ENTRY_CREATE"
    delete: KindType = "ENTRY_DELETE"
    modify: KindType = "ENTRY_MODIFY"


@dataclass()
class ChangeListEntry:
    id: str
    kind: KindType
    path: Tuple[str]
    isDirectory: bool
    isFile: bool
    fs: FS


@dataclass()
class Package:
    id: str
    changes: List[ChangeListEntry]


ONE_MEG = 1024 * 1024


@dataclass()
class PackageTakeout:
    content: Dict[str, str]
    remainingChanges: int = 0
    packageSize: int = 0
    content_size: int = 0
    size_limit = 4 * ONE_MEG

    def add_change(self, change: ChangeListEntry) -> bool:
        if change.kind != Kind.delete:
            with change.fs.open(os.path.sep.join(change.path), "r") as fp:
                data = fp.read()

        else:
            data = ""

        if len(data) + self.packageSize > self.size_limit:
            return False

        self.content[change.id] = data
        self.content_size += len(data)

        self.packageSize = len(self.content)

        return True
