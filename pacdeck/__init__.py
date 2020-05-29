#!/usr/bin/env python
import argparse

from pacdeck.config import GlobalArgs
from pacdeck.generate import generate
from pacdeck.sync import sync


def main():
    parser = argparse.ArgumentParser(
        description="A transparent approach to declarative package management in Arch."
    )
    parser.add_argument(
        "--config", help="Configuration path", default="/etc/pacdeck.json"
    )
    parser.add_argument(
        "--noconfirm",
        help="Don't ask for confirmation; use default responses",
        action="store_true",
        default=False,
    )

    subparsers = parser.add_subparsers(title="Command", dest="action")

    com_gen = subparsers.add_parser(
        "generate",
        description="Generate configuration from current explicitly installed packages",
    )
    com_gen.add_argument(
        "-c", "--command", help="Install command",
    )
    com_gen.add_argument(
        "-ac", "--aur_command", help="AUR install command",
    )
    com_gen.add_argument(
        "-f",
        "--force",
        dest="force",
        help="Overwrite existing configuration",
        action="store_true",
        default=False,
    )

    subparsers.add_parser(
        "sync", description="Install, remove, and upgrade packages. Default command.",
    )

    args = parser.parse_args()

    global_args = GlobalArgs(config_path=args.config, confirm=not args.noconfirm)

    command = args.action
    if not command:
        command = "sync"

    if command == "generate":
        generate(
            global_args,
            command=args.command,
            aur_command=args.aur_command,
            force=args.force,
        )

    elif command == "sync":
        sync(global_args)


if __name__ == "__main__":
    main()
