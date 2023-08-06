"""
The default group of operations that pyunique has
"""
import os

import tqdm
from pytconf import register_endpoint, register_function_group

import pyunique.version
from pyunique.archive import get_archive
from pyunique.configs import ConfigScan
from pyunique.digest import digest_file_bytes
from pyunique.utils import get_logger, get_number_of_files

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyunique commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pyunique.version.VERSION_STR)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigScan],
)
def scan() -> None:
    """
    Scan a folder and register it's checksums
    """
    archive = get_archive()
    archive.start_write()
    logger = get_logger()
    num_files = get_number_of_files(folder=ConfigScan.folder)
    with tqdm.tqdm(total=num_files) as progress_bar:
        for root, directories, files in os.walk(ConfigScan.folder):
            for file in files:
                filename = os.path.join(root, file)
                logger.info(f"doing {filename}")
                if archive.get_digest(filename=filename) is None:
                    digest = digest_file_bytes(filename=filename)
                    archive.add_digest(filename=filename, digest=digest)
                    progress_bar.update()
    archive.end_write()
    archive.close()
