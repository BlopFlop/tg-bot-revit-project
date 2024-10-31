from typing import Final
import getpass
import socket

import rpws
from rpws.server import RevitServer

RESTService: str = "/RevitServerAdminRESTService{}/AdminRESTService.svc"


class PatchRevitServer(RevitServer):
    """Revit server object, add support new version Revit."""

    PATCH_SROOTS: Final[dict[str: str]] = {
        str(version): RESTService.format(version)
        for version in range(2012, 2025)
    }

    def __init__(self, name, version, username=None, machine=None):

        if isinstance(version, int):
            version = str(version)

        if version not in self.PATCH_SROOTS:
            except_message = "Supported versions are: {}".format(
                [version for version in self.PATCH_SROOTS.keys()]
            )
            raise rpws.ServerVersionNotSupported(except_message)

        self.name = name
        self.version = version
        self._base_uri = "".join(
            ("http://", self.name, self.PATCH_SROOTS[self.version])
        )

        if username:
            self._huser = username
        else:
            self._huser = getpass.getuser()

        if machine:
            self._hmachine = machine
        else:
            self._hmachine = socket.gethostname()
