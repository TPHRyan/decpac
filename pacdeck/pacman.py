import re
from subprocess import check_output
from typing import Iterable


class Pacman(object):
    @property
    def foreign_packages(self):
        for line in check_output(["pacman", "-Qm"]).decode("utf-8").splitlines():
            yield re.search("([^ ]+)", line).group(1)

    @property
    def installed_packages(self) -> Iterable[str]:
        for line in check_output(["pacman", "-Qe"]).decode("utf-8").splitlines():
            yield re.search("([^ ]+)", line).group(1)


pacman = Pacman()
