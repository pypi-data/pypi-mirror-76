import os
from abc import ABCMeta, abstractmethod
from typing import Union

import lmdb

from pyunique.configs import ConfigLMDB, ConfigAlgo


class Archive(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def get_digest(self, filename: str) -> Union[bytes, None]:
        pass

    @abstractmethod
    def add_digest(self, filename: str, digest: bytes) -> None:
        pass

    @abstractmethod
    def start_read(self) -> None:
        pass

    @abstractmethod
    def end_read(self) -> None:
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

    @abstractmethod
    def yield_all_items(self):
        pass

    @abstractmethod
    def delete(self, filename: str) -> None:
        pass


class ArchiveLMDB(Archive):
    def __init__(self):
        super().__init__()
        filename = os.path.expanduser("~/.config/pyunique.lmdb")
        self.env = lmdb.open(
            path=filename,
            map_size=ConfigLMDB.map_size,
            subdir=False,  # default is True, for just one file
            writemap=True,  # default is False, for performance
            # lock=True,  # this is the default
        )
        self.txn = None

    def count(self) -> int:
        return self.env.stat()["entries"]

    def start_read(self) -> None:
        self.txn = self.env.begin(
            buffers=ConfigLMDB.buffers,
        )

    def end_read(self) -> None:
        self.txn.commit()

    def start_write(self) -> None:
        # write is False by default
        self.txn = self.env.begin(
            write=True,  # default is False
            buffers=ConfigLMDB.buffers,
        )

    def end_write(self) -> None:
        self.txn.commit()

    def get_digest(self, filename: str) -> Union[bytes, None]:
        return self.txn.get(key=filename.encode(ConfigAlgo.encoding))

    def add_digest(self, filename: str, digest: bytes) -> None:
        self.txn.put(
            key=filename.encode(ConfigAlgo.encoding),
            value=digest,
        )

    def close(self) -> None:
        self.env.close()

    def yield_all_items(self):
        with self.txn.cursor() as curs:
            for key, value in curs:
                yield key.decode(ConfigAlgo.encoding), value

    def delete(self, filename: str) -> None:
        self.txn.delete(key=filename.encode(ConfigAlgo.encoding))


def get_archive() -> Archive:
    """
    return correct archive using the currently configured algorithm
    (factory method)
    """
    return ArchiveLMDB()
