import logging
import shutil
from pathlib import Path

from abc import ABC, abstractmethod

from rpws.models import ModelInfo

from core.constants import (
    IFC_EXT,
    NWC_EXT,
    NWD_EXT,
    NWF_EXT,
    RVT_EXT,
)
from src.revit_project.project_models import (
    RevitFileBase, RevitFileInFTP, RevitFileInRevitServer
)
from src.revit_project.directory import (
    ArchDirThree,
    FTPDirThree,
    ProjectDirThree
)
from src.revit_project.functions import (
    control_workdir,
    get_models_in_revit_server,
    get_file_from_ext,
    get_model_for_mask,
    make_achive,
    pool_func,
)


class Builder(ABC, object):

    @abstractmethod
    def _build_project_structure(self):
        raise NotImplementedError()

    @abstractmethod
    def _build_arch_structure(self):
        raise NotImplementedError()

    @abstractmethod
    def _build_ftp_structure(self):
        raise NotImplementedError()

    @abstractmethod
    def _build_revit_models(self):
        raise NotImplementedError()

    @abstractmethod
    def create_project(self):
        raise NotImplementedError()

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()


class ProjectBuilder(Builder):

    def __init__(
        self,
        project_dir_path: Path,
        arch_dir_path: Path,
        ftp_dir_path: Path
    ) -> None:
        """_"""
        self.__project_dir_path = project_dir_path
        self.__arch_dir_path = arch_dir_path
        self.__ftp_dir_path = ftp_dir_path

    def _build_project_structure(self, name: str) -> ProjectDirThree:
        """_"""
        project_dir = ProjectDirThree(
            path_dir=self.__project_dir_path,
            name_project=name
        )
        project_dir.create_dirs()
        return project_dir

    def _build_arch_structure(self, name: str) -> ArchDirThree:
        """_"""
        arch_dir: ArchDirThree = ArchDirThree(
            path_dir=self.__arch_dir_path,
            name_project=name
        )
        arch_dir.create_dirs()
        return arch_dir

    def _build_ftp_structure(self, name: str) -> FTPDirThree:
        """_"""
        ftp_dir = FTPDirThree(
            path_dir=self.__ftp_dir_path,
            name_project=name
        )
        ftp_dir.create_dirs()
        return ftp_dir

    def _build_revit_models(
        self,
        server_name: str,
        version_revit: int,
        search_pattern: str,
        project_dir: ProjectDirThree,
        arch_dir: ArchDirThree,
        ftp_dir: FTPDirThree
    ) -> list[RevitFileBase]:
        """_"""
        all_revit_models_in_rs: list[ModelInfo] = get_models_in_revit_server(
            revit_server_name=server_name,
            version=version_revit
        )
        revit_models_in_rs: list[ModelInfo] = get_model_for_mask(
            all_revit_models=all_revit_models_in_rs,
            search_pattern=search_pattern
        )

        revit_items: dict[str: RevitFileBase] = {}

        for model_info in revit_models_in_rs:
            revit_object: RevitFileInRevitServer = RevitFileInRevitServer(
                server_name=server_name,
                model_info_in_rs=model_info,
                version_revit=version_revit,
                local_path=arch_dir.backup,
                ftp_path=ftp_dir.revit_models,
                nwc_path=project_dir.nawis_nwc
            )
            revit_items[revit_object.name] = revit_object

        for local_model in get_file_from_ext(ftp_dir.revit_models, RVT_EXT):
            revit_object: RevitFileInFTP = RevitFileInFTP(
                version_revit=version_revit,
                local_path=local_model,
                backup_path=arch_dir.backup,
                nwc_path=project_dir.nawis_nwc
            )
            if revit_object.name in revit_items:
                revit_items[revit_object.name] = revit_object

        return list(revit_items.values())

    def update_revit_models(self, project: "Project") -> list[RevitFileBase]:
        """_"""
        project.revit_models = self._build_revit_models(
            server_name=project.server_name,
            version_revit=project.version_revit,
            project_dir=project.project_dir,
            arch_dir=project.arch_dir,
            ftp_dir=project.ftp_dir
        )
        return project.revit_models

    def create_project(self,
        name: str,
        search_pattern: str,
        server_name: str,
        version_revit: int
    ) -> "Project":
        """_"""
        arch_dir = self._build_arch_structure(name=name)
        project_dir = self._build_project_structure(name=name)
        ftp_dir = self._build_ftp_structure(name=name)

        revit_models = self._build_revit_models(
            server_name=server_name,
            version_revit=version_revit,
            search_pattern=search_pattern,
            project_dir=project_dir,
            arch_dir=arch_dir,
            ftp_dir=ftp_dir
        )

        return Project(
            name=,
        )


    def __str__(self):
        return (
            f"Builder for Project. Name: {self.__name} "
            f"Version: {self.__version_revit}"
        )


class Project:
    def __init__(
        self,
        name: str,
        search_pattern: str,
        server_name: str,
        version_revit: int,
        revit_models: list[RevitFileBase],
        project_dir: ProjectDirThree,
        arch_dir: ArchDirThree,
        ftp_dir: FTPDirThree,
    ) -> None:

        self.name = name
        self.search_pattern = search_pattern

        self.server_name = server_name
        self.version_revit = version_revit

        self.revit_models = revit_models

        self.project_dir = project_dir
        self.arch_dir = arch_dir
        self.ftp_dir = ftp_dir

    @property
    def revit_models_in_rs(self) -> list[RevitFileInRevitServer]:
        filter_func = lambda model: isinstance(model, RevitFileInRevitServer)
        return list(filter(filter_func, self.revit_models))

    @property
    def revit_models_local(self) -> list[RevitFileInFTP]:
        filter_func = lambda model: isinstance(model, RevitFileInFTP)
        return list(filter(filter_func, self.revit_models))

    @property
    def backup_models(self) -> list[Path]:
        return get_file_from_ext(self.arch_dir.backup, RVT_EXT)

    @property
    def ftp_models(self) -> list[Path]:
        return get_file_from_ext(self.ftp_dir.revit_models, RVT_EXT)

    @property
    def nwf_models(self) -> list[Path]:
        return get_file_from_ext(self.project_dir.nawis_nwf, NWF_EXT)

    @property
    def nwc_models(self) -> list[Path]:
        return get_file_from_ext(self.project_dir.nawis_nwc, NWC_EXT)

    @property
    def nwd_models(self) -> list[Path]:
        return get_file_from_ext(self.project_dir.nawis_nwd, NWD_EXT)

    @property
    def ifc_models(self) -> list[Path]:
        return get_file_from_ext(self.ftp_dir.ifc, IFC_EXT)

    @property
    def arch_or_pub_items(self) -> dict[str: Path]:
        result: dict[str: list[Path]] = {}

        items: tuple[Path] = (
            self.backup_models,
            self.nwc_models,
            self.nwf_models,
            self.nwd_models,
            self.ifc_models,
        )

        for item in items:
            if not item:
                continue

            extention: str = item.suffix[1:].upper()

            if extention in result:
                result[extention].append(item)
            else:
                result[extention] = item
        return result

    def load_in_backup(self) -> None:
        # pool_items: list[RevitFileInRevitServer | RevitFileInLocal] = [
        #     *self.revit_files_in_rs,
        #     *self.revit_files,
        # ]
        pass

    def load_in_ftp(self) -> None:
        # pool_items: list[RevitFileInRevitServer] = self.revit_files_in_rs
        pass

    def load_in_nwc(self) -> None:
        pass

    def load_in_nwd(self) -> None:
        pass

    def load_in_arch(self, name_album: str = None) -> Path:
        # items = self.arch_or_pub_items

        # for extention, files in items.items():
        #     files: list[Path] = files

        #     if name_album:
        #         name_dir = "_".join((DATE_NOW, extention, name_album))
        #     else:
        #         name_dir = "_".join((DATE_NOW, extention))

        #     copy_dir = self.arch_dir.arch / name_dir

        #     copy_dir.mkdir(exist_ok=True)

        #     for file in files:
        #         path_copy_file = copy_dir / file.name
        #         shutil.copy2(file, path_copy_file)

        # return self.arch_dir.arch
        pass

    def load_in_publish(self) -> Path:
        # items: dict[str: list[Path]] = self.arch_or_pub_items

        # pub_dir: Path = self.ftp_dir.publish / (f"{self.name}_{DATE_NOW}")
        # with control_workdir(pub_dir) as new_dir:
        #     for extention, files in items.items():
        #         files: list[Path] = files

        #         copy_dir: Path = new_dir / extention
        #         copy_dir.mkdir()
        #         for file in files:
        #             path_copy_file = copy_dir / file.name
        #             shutil.copy2(file, path_copy_file)

        #     make_achive(new_dir, new_dir)

        # return pub_dir.parent
        pass
