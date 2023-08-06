import hashlib

from pyunique.configs import ConfigAlgo


def digest_file_bytes(filename: str) -> bytes:
    block_size = 65536
    hash_object = hashlib.new(ConfigAlgo.digest)
    with open(filename, 'rb') as file_handle:
        buf = file_handle.read(block_size)
        while len(buf) > 0:
            hash_object.update(buf)
            buf = file_handle.read(block_size)
    return hash_object.digest()
