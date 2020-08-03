import argparse
import os
import shutil
import stat

if __name__ == "__main__":
    if os.getuid() != 0:
        print("This script is intended to be run as root!")
        print("By doing this, we isolate the commands that truly need privilege.")
        print("This script runs: cp, chmod (on only the input/output files)")
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("install_path")
    args = parser.parse_args()

    shutil.copy(args.config, args.install_path)
    config_file = args.install_path
    if os.path.isdir(config_file):
        config_file = os.path.join(config_file, os.path.basename(args.config))

    os.chmod(
        args.install_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
    )
    print("Config installed!")
