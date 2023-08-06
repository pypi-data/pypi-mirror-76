"""
All configurations for pyunique
"""
from pytconf import Config, ParamCreator
import hashlib


class ConfigScan(Config):
    folder = ParamCreator.create_existing_folder(
        help_string="Which folder to work on?",
        default=".",
    )


class ConfigAlgo(Config):
    digest = ParamCreator.create_choice(
        help_string="Which digest to use?",
        default="sha256",
        choice_list=list(hashlib.algorithms_available),
    )


class ConfigLMDB(Config):
    map_size = ParamCreator.create_int(
        help_string="Which size of mmap to use?",
        default=1000000000000,
    )
    encoding = ParamCreator.create_str(
        help_string="Which encoding to use?",
        default='utf-8',
    )
