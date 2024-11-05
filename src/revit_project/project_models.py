from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copy2

from rpws.models import ModelInfo

from src.core.constants import (
    LOCAL_NAWISWORKS_PATH, PATH_NAWIS_FTR, PATH_REVIT_RST
)
from src.revit_project.load_models import load_model_in_rs, export_rvt_to_nwc


class RevitFileBase(ABC):

    version: int

    local_path: Path
    backup_path: Path
    ftp_path: Path
    nwc_path: Path

    @abstractmethod
    def __str__(self):
        return self.name

    @property
    def name(self) -> str:
        return self.local_path.name

    @abstractmethod
    def load_backup(self) -> Path:
        pass

    @abstractmethod
    def load_ftp(self) -> Path:
        pass

    def load_nwc(self) -> Path:
        path_ftr: Path = PATH_NAWIS_FTR.format(self.version)

        return export_rvt_to_nwc(
            path_nawis_ftr=path_ftr,
            local_nawisworks_path=LOCAL_NAWISWORKS_PATH,
            source_path=self.backup_path,
            end_dir_path=self.nwc_path
        )


class RevitFileInRevitServer(RevitFileBase):

    def __init__(
        self,
        server_name: str,
        model_info_in_rs: ModelInfo,
        version_revit: int,
        local_path: Path,
        ftp_path: Path,
        nwc_path: Path,
    ) -> None:

        self.server_name = server_name
        self.__model_info_in_rs: ModelInfo = model_info_in_rs
        self.version = version_revit

        self.local_path = local_path / model_info_in_rs.name
        self.backup_path = local_path / model_info_in_rs.name
        self.ftp_path = ftp_path / model_info_in_rs.name
        self.nwc_path = nwc_path / model_info_in_rs.name

    @property
    def path_in_rs(self) -> Path:
        return Path(self.__model_info_in_rs.path[1:])

    def load_backup(self) -> Path:
        path_revit_rst: Path = Path(PATH_REVIT_RST.format(self.version))
        return load_model_in_rs(
            path_revit_rst=path_revit_rst,
            server_name=self.server_name,
            source_path_model=self.path_in_rs,
            end_path_model=self.backup_path
        )

    def load_ftp(self) -> Path:
        path_revit_rst: Path = Path(PATH_REVIT_RST.format(self.version))
        return load_model_in_rs(
            path_revit_rst=path_revit_rst,
            server_name=self.server_name,
            source_path_model=self.path_in_rs,
            end_path_model=self.ftp_path
        )

    def __str__(self) -> str:
        version: str = self.__model_info_in_rs.product_version
        return (
            f"{self.__class__} Server: {self.server_name} "
            f"Name: {self.name} Size: {version}"
        )


class RevitFileInFTP(RevitFileBase):
    def __init__(
        self,
        version_revit: int,
        local_path: Path,
        backup_path: Path,
        nwc_path: Path
    ) -> None:
        self.version = version_revit

        self.local_path = local_path
        self.backup_path = backup_path / local_path.name
        self.ftp_path = local_path
        self.nwc_path = nwc_path / local_path.name

    def load_backup(self) -> Path:
        if self.local_path.is_file():
            return copy2(self.local_path, self.backup_path)
        return self.backup_path

    def load_ftp(self) -> Path:
        return self.local_path

    def __str__(self) -> str:
        return (
            f"{self.__class__} Name: {self.name} Path: {self.local_path}"
        )
