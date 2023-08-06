"""
The default group of operations that pyunique has
"""
import os

import tqdm
from pytconf import register_endpoint, register_function_group

import pyunique.version
from pyunique.archive import get_archive
from pyunique.configs import ConfigScan, ConfigAlgo, ConfigLMDB
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
    configs=[
        ConfigScan,
        ConfigAlgo,
        ConfigLMDB,
    ],
)
def scan() -> None:
    """
    Scan a folder and register it's checksums
    """
    archive = get_archive()
    archive.start_write()
    logger = get_logger()
    logger.info("Scanning for number of files...")
    num_files = get_number_of_files(folder=ConfigScan.folder)
    with tqdm.tqdm(total=num_files) as progress_bar:
        for root, directories, files in os.walk(ConfigScan.folder):
            for file in files:
                filename = os.path.join(root, file)
                filename = os.path.abspath(filename)
                logger.debug(f"doing {filename}")
                if archive.get_digest(filename=filename) is None:
                    digest = digest_file_bytes(filename=filename)
                    archive.add_digest(filename=filename, digest=digest)
                progress_bar.update()
    archive.end_write()
    archive.close()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[
        ConfigScan,
        ConfigAlgo,
        ConfigLMDB,
    ],
)
def clean_db() -> None:
    """
    Scan the DB and remove any entries which are no longer valid
    """
    logger = get_logger()
    archive = get_archive()
    archive.start_write()
    count = archive.count()
    errors = 0
    with tqdm.tqdm(total=count) as progress_bar:
        for filename, _digest in archive.yield_all_items():
            if not os.path.isfile(filename):
                errors += 1
                logger.debug(f"problem with filename {filename}")
                archive.delete(filename=filename)
            progress_bar.update()
    archive.end_write()
    archive.close()
    logger.info(f"number of errors is {errors}")


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[
        ConfigScan,
        ConfigAlgo,
        ConfigLMDB,
    ],
)
def check_filenames() -> None:
    """
    Check filenames in a certain folder
    """
    logger = get_logger()
    errors = 0
    error_filenames = []
    logger.info("Scanning for number of files...")
    num_files = get_number_of_files(folder=ConfigScan.folder)
    with tqdm.tqdm(total=num_files) as progress_bar:
        for root, directories, files in os.walk(ConfigScan.folder):
            for file in files:
                filename = os.path.join(root, file)
                filename = os.path.abspath(filename)
                logger.debug(f"doing {filename}")
                try:
                    filename.encode(ConfigAlgo.encoding)
                except UnicodeEncodeError:
                    errors += 1
                    error_filenames.append(filename)
                progress_bar.update()
    logger.info(f"number of errors is {errors}")
    for error_filename in error_filenames:
        logger.info(error_filename)
