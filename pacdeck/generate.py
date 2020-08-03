import json
import os
import shlex
import subprocess
from tempfile import NamedTemporaryFile
from typing import Optional

from pacdeck.config import GlobalArgs
from pacdeck.pacman import pacman
from pacdeck.run_privileged import run_privileged


def generate(
    global_args: GlobalArgs,
    *,
    force: bool,
    command: Optional[str] = None,
    aur_command: Optional[str] = None,
):
    local = set(pacman.foreign_packages)
    conf = dict(
        installed=[
            {"source": "aur" if package in local else "official", "name": package}
            for package in pacman.installed_packages
        ],
    )
    if command is not None:
        conf["install_main"] = shlex.split(command)
    if aur_command is not None:
        conf["install_aur"] = shlex.split(aur_command)
    if not force and os.path.exists(global_args.config_path):
        config_name = os.path.basename(global_args.config_path)
        print(f"{config_name} already exists. Delete it or run with `-f`.")
        return
    with NamedTemporaryFile(mode="w") as tmp:
        tmp.write(json.dumps(conf, indent=4, sort_keys=True))
        run_privileged("install_config.py", tmp.name, global_args.config_path)
