""" gdsfactory loads a configuration from 3 files, high priority overwrites low priority:

1. A config.yml found in the current working directory (highest priority)
2. ~/.gdsfactory/config.yml specific for the machine
3. the default_config is in this file (lowest priority)

`CONFIG` has all the paths that we do not care
`conf` has all the useful info
"""

__version__ = "1.3.2"
import os
import json
import subprocess
import pathlib
from pprint import pprint
import logging
from typing import Any

from omegaconf import OmegaConf

import numpy as np
from git import Repo


connections = {}  # global variable to store connections in a dict
home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent
home_path = pathlib.Path.home() / ".gdsfactory"
home_path.mkdir(exist_ok=True)

cwd_config = cwd / "config.yml"
module_config = module_path / "config.yml"
home_config = home_path / "config.yml"
config_base = OmegaConf.load(module_config)
try:
    config_cwd = OmegaConf.load(cwd_config)
except:
    config_cwd = OmegaConf.create()
try:
    config_home = OmegaConf.load(home_config)
except:
    config_home = OmegaConf.create()

conf = OmegaConf.merge(config_base, config_home, config_cwd)
conf.version = __version__

try:
    conf["git_hash"] = Repo(repo_path).head.object.hexsha
except Exception:
    conf["git_hash"] = None


CONFIG = dict(
    config_path=cwd_config.absolute(),
    repo_path=repo_path,
    module_path=module_path,
    font_path=module_path / "gds" / "alphabet.gds",
    masks_path=repo_path / "mask",
    version=__version__,
    home=home,
    cwd=cwd,
)

mask_name = "notDefined"

if conf.get("mask"):
    mask_name = conf["mask"]["name"]
    mask_config_directory = cwd
    build_directory = mask_config_directory / "build"
    CONFIG["devices_directory"] = mask_config_directory / "devices"
    CONFIG["mask_gds"] = mask_config_directory / "build" / "mask" / (mask_name + ".gds")
else:
    build_directory = home_path / "build"
    mask_config_directory = home_path / "build"

CONFIG["custom_components"] = conf.custom_components
CONFIG["gdslib"] = conf.gdslib or repo_path / "gdslib"
CONFIG["sp"] = CONFIG["gdslib"] / "sp"
CONFIG["gds"] = CONFIG["gdslib"] / "gds"
CONFIG["gdslib_test"] = home_path / "gdslib_test"

CONFIG["build_directory"] = build_directory
CONFIG["gds_directory"] = build_directory / "devices"
CONFIG["cache_doe_directory"] = build_directory / "cache_doe"
CONFIG["doe_directory"] = build_directory / "doe"
CONFIG["mask_directory"] = build_directory / "mask"
CONFIG["mask_gds"] = build_directory / "mask" / (mask_name + ".gds")
CONFIG["mask_config_directory"] = mask_config_directory
CONFIG["gdspath"] = build_directory / "gds.gds"
CONFIG["samples_path"] = module_path / "samples"
CONFIG["components_path"] = module_path / "components"

if "gds_resources" in CONFIG:
    CONFIG["gds_resources"] = CONFIG["masks_path"] / CONFIG["gds_resources"]

build_directory.mkdir(exist_ok=True)
CONFIG["gds_directory"].mkdir(exist_ok=True)
CONFIG["doe_directory"].mkdir(exist_ok=True)
CONFIG["mask_directory"].mkdir(exist_ok=True)
CONFIG["gdslib_test"].mkdir(exist_ok=True)


logging.basicConfig(
    filename=CONFIG["build_directory"] / "log.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)
logging.warning("This will get logged to a file")


def print_config(key=None):
    if key:
        if CONFIG.get(key):
            print(CONFIG[key])
        else:
            print(f"`{key}` key not found in {cwd_config}")
    else:
        pprint(CONFIG)


def complex_encoder(z):
    if isinstance(z, pathlib.Path):
        return str(z)
    else:
        type_name = type(z)
        raise TypeError(f"Object {z} of type {type_name} is not serializable")


def write_config(config, json_out_path):
    with open(json_out_path, "w") as f:
        json.dump(config, f, indent=2, sort_keys=True, default=complex_encoder)


def call_if_func(f: Any, **kwargs):
    return f(**kwargs) if callable(f) else f


def get_git_hash():
    """ Get the current git hash """
    try:
        with open(os.devnull, "w") as shutup:
            return (
                subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=shutup)
                .decode("utf-8")
                .strip("\n")
            )
    except subprocess.CalledProcessError:
        return "not_a_git_repo"


GRID_RESOLUTION = conf.tech.grid_resolution
GRID_PER_UNIT = conf.tech.grid_unit / GRID_RESOLUTION
GRID_ROUNDING_RESOLUTION = int(np.log10(GRID_PER_UNIT))
BEND_RADIUS = conf.tech.bend_radius
TAPER_LENGTH = conf.tech.taper_length
WG_EXPANDED_WIDTH = conf.tech.wg_expanded_width


if __name__ == "__main__":
    print(conf)
    # print_config("gdslib")
    # print_config()
    # print(CONFIG["git_hash"])
    # print(CONFIG)
