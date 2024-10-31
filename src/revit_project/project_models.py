from pathlib import Path

from rpws.models import ModelInfo


class RevitFileBase:

    __local_path: Path
    __backup_path: Path
    __ftp_path: Path
    __nwc_path: Path

    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self.__local_path.name

    @property
    def local_path(self) -> Path:
        return self.__local_path

    @property
    def backup_path(self) -> Path:
        return self.__backup_path / self.name

    @property
    def ftp_path(self) -> Path:
        return self.__ftp_path / self.name

    @property
    def nwc_path(self) -> Path:
        return self.__nwc_path / self.name


class RevitFileInRevitServer(RevitFileBase):

    def __init__(
        self,
        model_info_in_rs: ModelInfo,
        local_path: Path,
        ftp_path: Path,
        nwc_path: Path
    ) -> None:

        self.__model_info_in_rs: ModelInfo = model_info_in_rs

        self.__local_path = local_path
        self.__backup_path = local_path
        self.__ftp_path = ftp_path
        self.__nwc_path = nwc_path

    @property
    def local_path(self) -> Path:
        return self.__local_path / self.path_in_rs.name

    @property
    def path_in_rs(self) -> Path:
        return Path(self.__model_info_in_rs.path[1:])

    def load_model_from_revit_server(self):
        pass


class RevitFileInLocal(RevitFileBase):
    def __init__(
        self,
        local_path: Path,
        backup_path: Path,
        nwc_path: Path
    ) -> None:
        self.__local_path: Path = local_path
        self.__backup_path: Path = backup_path
        self.__ftp_path: Path = local_path
        self.__nwc_path: Path = nwc_path
