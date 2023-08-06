import os
from configparser import ConfigParser
from shutil import copyfile


def parse_config(template="config.ini"):
    # Get paths.
    config_example_path = template
    config_path = os.getenv("CONFIG_PATH", template)
    # Read the config.
    cp = ConfigParser()
    try:
        cp.read(config_path)
    except FileNotFoundError:
        copyfile(config_example_path, config_path)
        cp.read(config_path)
    return cp