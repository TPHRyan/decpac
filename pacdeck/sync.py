import json
import os
import subprocess

from pacdeck.config import GlobalArgs
from pacdeck.pacman import pacman


def sync(global_args: GlobalArgs):
    with open(global_args.config_path, "r") as f:
        conf = json.load(f)
    print("Scanning current package state...")
    state = dict(installed=set(pacman.installed_packages),)
    add_official = set()
    add_aur = set()
    conf_names = set()

    # Group packages by source (official, aur, etc)
    for package in conf["installed"]:
        package_source = package["source"]
        package_name = package["name"]
        conf_names.add(package_name)
        if package_name not in state["installed"]:
            if package_source == "official":
                add_official.add(package_name)
            elif package_source == "aur":
                add_aur.add(package_name)
            else:
                raise RuntimeError(
                    f"Unknown package source {package_source} for {package_name}"
                )

    to_add = add_official | add_aur
    print(f"Installing {to_add}")
    to_remove = state["installed"] - conf_names
    print(f"Removing {to_remove}")
    if global_args.confirm and not input("Okay? (y/N) ") == "y":
        print("Aborting.")
        return
    print()

    # Add new packages or re-mark mismarked packages
    if to_add:
        mark = []
        for command, command_default, type_add in [
            ["install_main", ["sudo", "pacman", "--noconfirm", "-S"], add_official,],
            ["install_aur", None, add_aur,],
        ]:
            add_args = conf.get(command) or command_default
            _type_add, type_add = type_add, []
            for package in _type_add:
                if subprocess.run(["pacman", "-Q", package]).returncode != 0:
                    type_add.append(package)
                else:
                    mark.append(package)
            if type_add:
                if not add_args:
                    raise RuntimeError(
                        f"Field {command} missing from "
                        f"{os.path.basename(global_args.config_path)}"
                    )
                subprocess.run(add_args + type_add, check=True)

        # Hack for trizen which splits up packages which leads to
        # command line packages that are deps of others to be marked
        # as non-explicit.
        if mark:
            subprocess.run(
                ["sudo", "pacman", "--noconfirm", "-D", "--asexplicit"] + mark
            )
    else:
        print("No packages to install.")

    # Remove no longer listed packages
    if to_remove:
        subprocess.run(
            ["sudo", "pacman", "-D", "--asdeps", "--noconfirm"] + list(to_remove),
            check=True,
        )
        subprocess.run(
            ["sudo", "pacman", "-Rsu", "--noconfirm"] + list(to_remove), check=True
        )
    else:
        print("No packages to remove.")

    print("Done")
