import logging
from pathlib import Path
import shutil

from rpws.models import ModelInfo

from src.revit_project.functions import (
    control_workdir,
    get_all_models_in_revit_server,
    get_file_from_extention,
    get_model_for_mask,
    make_achive,
    pool_func,
)

from src.core.constants import (
    IFC_EXTENTION,
    NWC_EXTENTION,
    NWD_EXTENTION,
    NWF_EXTENTION,
    RVT_EXTENTION,
)
from src.revit_project import (
    RevitFileInLocal,
    RevitFileInRevitServer
)
from src.revit_project.directory import (
    ArchDirThree,
    FTPDirThree,
    ProjectDirThree,
)


class Project:
    def __init__(
        self,
        name: str,
        search_pattern: str,
        server_name: str,
        version_revit: int,
        project_dir_path: Path,
        arch_dir_path: Path,
        ftp_dir_path: Path,
    ) -> None:

        self.name: str = name
        self.search_pattern: str = search_pattern

        self.server_name: str = server_name
        self.version_revit: int = version_revit

        self.__project_dir_path: Path = project_dir_path
        self.__arch_dir_path: Path = arch_dir_path
        self.__ftp_dir_path: Path = ftp_dir_path

    @property
    def project_dir(self) -> ProjectDirThree:
        dir_object = ProjectDirThree(self.__project_dir_path, self.name)
        dir_object.create_dirs()
        return dir_object

    @property
    def arch_dir(self) -> ArchDirThree:
        dir_object = ArchDirThree(self.__arch_dir_path, self.name)
        dir_object.create_dirs()
        return dir_object

    @property
    def ftp_dir(self) -> FTPDirThree:
        dir_object = FTPDirThree(self.__ftp_dir_path, self.name)
        dir_object.create_dirs()
        return dir_object

    @property
    def revit_files_in_rs(self) -> list[RevitFileInRevitServer]:
        all_revit_models: list[ModelInfo] = get_all_models_in_revit_server(
            self.server_name
        )
        models_in_rs: list[ModelInfo] = get_model_for_mask(
            all_revit_models=all_revit_models,
            search_pattern=self.search_pattern,
        )
        result: list[RevitFileInRevitServer] = []

        for model in models_in_rs:
            result.append(
                RevitFileInRevitServer(
                    server_name=self.server_name,
                    model_info_for_rs=model,
                    backup_path=self.arch_dir.backup,
                    nwc_path=self.project_dir.nawis_nwc,
                    ftp_path=self.ftp_dir.revit_models,
                )
            )

        return result

    @property
    def revit_files(self) -> list[RevitFileInLocal]:
        models_in_rs_name: list[str] = [
            model_in_rs.name for model_in_rs in self.revit_files_in_rs
        ]

        result: list[RevitFileInLocal] = []
        models_local_path: list[Path] = get_file_from_extention(
            source_dir=self.ftp_dir.revit_models, extention=RVT_EXTENTION
        )

        for model_local_path in models_local_path:
            if model_local_path.name not in models_in_rs_name:
                revit_file_local: RevitFileInLocal = RevitFileInLocal(
                    model_path=model_local_path,
                    backup_path=self.arch_dir.backup,
                    nwc_path=self.project_dir.nawis_nwc,
                )
                result.append(revit_file_local)

        return result

    @property
    def backup_models(self) -> list[Path]:
        return get_file_from_extention(self.arch_dir.backup, RVT_EXTENTION)

    @property
    def ftp_models(self) -> list[Path]:
        return get_file_from_extention(
            self.ftp_dir.revit_models, RVT_EXTENTION
        )

    @property
    def nwf_models(self) -> list[Path]:
        return get_file_from_extention(
            self.project_dir.nawis_nwf, NWF_EXTENTION
        )

    @property
    def nwc_models(self) -> list[Path]:
        return get_file_from_extention(
            self.project_dir.nawis_nwc, NWC_EXTENTION
        )

    @property
    def nwd_models(self) -> list[Path]:
        return get_file_from_extention(
            self.project_dir.nawis_nwd, NWD_EXTENTION
        )

    @property
    def ifc_models(self) -> list[Path]:
        return get_file_from_extention(self.ftp_dir.ifc, IFC_EXTENTION)

    @property
    def arch_or_pub_items(self) -> dict[str:Path]:
        result = {}

        items: tuple[Path] = (
            self.backup_models,
            self.nwc_models,
            self.nwf_models,
            self.nwd_models,
            self.ifc_models,
        )
        for item in items:
            if item:
                extention: str = item[0].suffix[1:].upper()

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
