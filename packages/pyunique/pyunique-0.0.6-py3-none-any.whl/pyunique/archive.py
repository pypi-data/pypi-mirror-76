import os
from abc import ABCMeta, abstractmethod
from typing import Union

import lmdb

from pyunique.configs import ConfigLMDB


class Archive(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_digest(self, filename: str) -> Union[bytes, None]:
        pass

    @abstractmethod
    def add_digest(self, filename: str, digest: bytes) -> None:
        pass

    @abstractmethod
    def start_write(self) -> None:
        pass

    @abstractmethod
    def end_write(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class ArchiveLMDB(Archive):
    def __init__(self):
        super().__init__()
        filename = os.path.expanduser("~/.config/pyunique.lmdb")
        self.env = lmdb.open(
            filename=filename,
            subdir=False,  # default is True
            map_size=ConfigLMDB.map_size,
            # lock=True,  # this is the default
        )
        self.txn = None

    def start_write(self) -> None:
        # write is False by default
        self.txn = self.env.begin(write=True)

    def get_digest(self, filename: str) -> Union[bytes, None]:
        return self.txn.get(key=filename.encode(ConfigLMDB.encoding))

    def add_digest(self, filename: str, digest: bytes) -> None:
        self.txn.put(
            key=filename.encode(ConfigLMDB.encoding),
            value=digest,
        )

    def end_write(self) -> None:
        self.txn.commit()

    def close(self) -> None:
        self.env.close()


def get_archive() -> Archive:
    """
    return correct archive using the currently configured algorithm
    (factory method)
    """
    return ArchiveLMDB()
