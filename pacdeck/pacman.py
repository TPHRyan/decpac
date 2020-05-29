import re
import subprocess
from typing import Iterable


class Pacman(object):
    @property
    def foreign_packages(self):
        yield from self._query_pacman("m")

    @property
    def installed_packages(self) -> Iterable[str]:
        yield from self._query_pacman("e")

    def _query_pacman(self, flags: str, root: bool = False):
        pacman_cmd = [*(["sudo"] if root else []), "pacman", f"-Q{flags}"]
        for line in (
            subprocess.run(pacman_cmd, capture_output=True, check=True)
            .stdout.decode("utf-8")
            .splitlines()
        ):
            yield re.search("([^ ]+)", line).group(1)


pacman = Pacman()
