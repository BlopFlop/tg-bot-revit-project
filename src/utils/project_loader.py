import logging
from pathlib import Path
from typing import Final

from cmd_revit_program.core.exceptions import DirectoryNotFoundError

from src.utils.functions import (
    control_workdir,
    get_or_create_dir,
    command_run_export_rvt_to_nwc,
    command_run_model_in_rs,
    get_all_models_in_revit_server,
    get_file_from_extention,
    get_model_for_mask,
    make_achive,
    pool_func,
    run_load_nwd,
    start_backup_process_from_pool,
    start_ftp_process_from_pool,
    start_nwc_process_from_pool,
)

import logging
import shutil
from pathlib import Path

from rpws.models import ModelInfo

from cmd_revit_program.core.constants import (
    DATE_NOW,
    IFC_EXTENTION,
    NWC_EXTENTION,
    NWD_EXTENTION,
    NWF_EXTENTION,
    PATH_WORKDIR_NAWIS,
    RVT_EXTENTION,
)
from cmd_revit_program.loader.dit_three import (
    ArchDirThree,
    FTPDirThree,
    ProjectDirThree,
)


class DirThreeMixin:
    def __init__(self, path_dir: Path, name_project: str) -> None:
        self.base_dir = self.check_dir_project(path_dir)
        self.name_project = name_project

    def check_dir_project(self, path_dir: Path) -> Path:
        if path_dir.is_dir():
            return path_dir
        except_message: str = f"Базовой директории не существует {str(path_dir)}"
        logging.error(except_message, stack_info=True)
        raise DirectoryNotFoundError(except_message)

    @property
    def project(self) -> Path:
        return self.base_dir / self.name_project


class ArchDirThree(DirThreeMixin):
    _ARCH_DIR: str = "02_Arch"
    _BACKUP_DIR: str = "01_Backup"

    def check_dir_project(self, path_dir: Path):
        arch_dir: Path = path_dir / self._ARCH_DIR
        backup_dir: Path = path_dir / self._BACKUP_DIR

        if not path_dir.is_dir():
            except_message: str = f"Базовой директории не существует {str(path_dir)}"
            logging.error(except_message, stack_info=True)
            raise DirectoryNotFoundError(except_message)
        elif not arch_dir.is_dir():
            except_message: str = f"Архивной директории не существует {str(arch_dir)}"
            logging.error(except_message, stack_info=True)
            raise DirectoryNotFoundError(except_message)
        elif not backup_dir.is_dir():
            except_message: str = f"Бэкап директории не существует {str(backup_dir)}"
            logging.error(except_message, stack_info=True)
            raise DirectoryNotFoundError(except_message)
        return path_dir

    @property
    def arch(self) -> Path:
        return self.base_dir / self._ARCH_DIR / self.name_project

    @property
    def backup(self) -> Path:
        return self.base_dir / self._BACKUP_DIR / self.name_project

    def create_dirs(self) -> list[Path]:
        items_: tuple[Path] = self.arch, self.backup
        return list(map(get_or_create_dir, items_))


class ProjectDirThree(DirThreeMixin):
    _DOCS: Final[str] = "01_Docs"
    _FAMILY: Final[str] = "02_Families"
    _TEMPLATES: Final[str] = "03_Templates"
    _SCRIPTS: Final[str] = "04_Scripts"
    _NAWISWORKS: Final[str] = "05_Navis"
    _NAWISWORKS_NWC: Final[str] = "01_NWC"
    _NAWISWORKS_NWF: Final[str] = "02_NWF"
    _NAWISWORKS_NWD: Final[str] = "03_NWD"
    _SUPPORT_MODELS: Final[str] = "06_SupportModels"
    _DWG_FILES: Final[str] = "07_DWG"

    @property
    def documents(self) -> Path:
        return self.project / self._DOCS

    @property
    def family(self) -> Path:
        return self.project / self._FAMILY

    @property
    def templates(self) -> Path:
        return self.project / self._TEMPLATES

    @property
    def scripts(self) -> Path:
        return self.project / self._SCRIPTS

    @property
    def nawisworks(self) -> Path:
        return self.project / self._NAWISWORKS

    @property
    def nawis_nwc(self) -> Path:
        return self.nawisworks / self._NAWISWORKS_NWC

    @property
    def nawis_nwf(self) -> Path:
        return self.nawisworks / self._NAWISWORKS_NWF

    @property
    def nawis_nwd(self) -> Path:
        return self.nawisworks / self._NAWISWORKS_NWD

    @property
    def support_models(self) -> Path:
        return self.project / self._SUPPORT_MODELS

    @property
    def dwg_files(self) -> Path:
        return self.project / self._DWG_FILES

    def create_dirs(self) -> list[Path]:
        items_: tuple[Path] = (
            self.project,
            self.documents,
            self.family,
            self.templates,
            self.scripts,
            self.nawisworks,
            self.nawis_nwc,
            self.nawis_nwf,
            self.nawis_nwd,
            self.support_models,
            self.dwg_files,
        )
        return list(map(get_or_create_dir, items_))


class FTPDirThree(DirThreeMixin):
    _SHARED: Final[str] = "10_Shared"
    _NAWISWORKS_NWC: Final[str] = "01_NWC"
    _NAWISWORKS_NWF: Final[str] = "02_NWF"
    _NAWISWORKS_NWD: Final[str] = "03_NWD"
    _IFC: Final[str] = "04_IFC"
    _RVT: Final[str] = "05_RVT"
    _TSCS: Final[str] = "06_TSKS"
    _PUBLISH: Final[str] = "20_Publish"
    _DOCS: Final[str] = "30_Docs"

    @property
    def shared(self) -> Path:
        return self.project / self._SHARED

    @property
    def nawis_nwc(self) -> Path:
        return self.shared / self._NAWISWORKS_NWC

    @property
    def nawis_nwf(self):
        return self.shared / self._NAWISWORKS_NWF

    @property
    def nawis_nwd(self):
        return self.shared / self._NAWISWORKS_NWD

    @property
    def ifc(self):
        return self.shared / self._IFC

    @property
    def revit_models(self):
        return self.shared / self._RVT

    @property
    def tasks(self):
        return self.shared / self._TSCS

    @property
    def publish(self):
        return self.project / self._PUBLISH

    @property
    def documents(self):
        return self.project / self._DOCS

    def create_dirs(self) -> list[Path]:
        items_: list[Path] = [
            self.project,
            self.shared,
            self.nawis_nwc,
            self.nawis_nwf,
            self.nawis_nwd,
            self.ifc,
            self.revit_models,
            self.tasks,
            self.publish,
            self.documents,
        ]
        return list(map(get_or_create_dir, items_))


class RevitFileInRevitServer:

    def __init__(
        self,
        server_name: str,
        model_info_for_rs: ModelInfo,
        backup_path: Path,
        nwc_path: Path,
        ftp_path: Path,
    ) -> None:
        self.server_name: str = server_name

        self.model_path: Path = self.__get_path_in_rs(model_info_for_rs)

        self.name: str = self.model_path.name

        self.backup_path: Path = backup_path / self.name
        self.ftp_path: Path = ftp_path / self.name
        self.nwc_path: Path = nwc_path / self.name

    def __get_path_in_rs(self, model_info: ModelInfo) -> Path:
        return Path(model_info.path[1:])

    def copy_to_ftp(self) -> Path:
        return command_run_model_in_rs(
            server_name=self.server_name,
            source_path_model=self.model_path,
            end_path_model=self.ftp_path,
        )

    def copy_to_backup(self) -> Path:
        return command_run_model_in_rs(
            server_name=self.server_name,
            source_path_model=self.model_path,
            end_path_model=self.backup_path,
        )

    def load_rvt_to_nwc(self) -> Path:
        return command_run_export_rvt_to_nwc(
            source_path=self.backup_path,
            end_dir_path=self.nwc_path,
        )


class RevitFileInLocal:
    def __init__(self, model_path: Path, backup_path: Path, nwc_path: Path) -> None:
        self.model_path: Path = model_path

        self.name: str = self.model_path.name

        self.backup_path: Path = backup_path / self.name
        self.nwc_path: Path = nwc_path / self.name

    def copy_to_backup(self) -> Path:
        if self.model_path.is_file():
            return shutil.copy2(self.model_path, self.backup_path)

    def load_rvt_to_nwc(self) -> Path:
        return command_run_export_rvt_to_nwc(
            source_path=self.model_path, end_dir_path=self.nwc_path
        )


class Project:
    def __init__(
        self,
        server_name: str,
        project_name: str,
        search_pattern: str,
        project_dir_path: Path,
        arch_dir_path: Path,
        ftp_dir_path: Path,
    ) -> None:
        self.server_name: str = server_name
        self.name: str = project_name
        self.search_pattern: str = search_pattern
        self.project_dir: ProjectDirThree = ProjectDirThree(
            project_dir_path, project_name
        )
        self.arch_dir: ArchDirThree = ArchDirThree(arch_dir_path, project_name)
        self.ftp_dir: FTPDirThree = FTPDirThree(ftp_dir_path, project_name)

        self.project_dir.create_dirs()
        self.arch_dir.create_dirs()
        self.ftp_dir.create_dirs()

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
        return get_file_from_extention(self.ftp_dir.revit_models, RVT_EXTENTION)

    @property
    def nwf_models(self) -> list[Path]:
        return get_file_from_extention(self.project_dir.nawis_nwf, NWF_EXTENTION)

    @property
    def nwc_models(self) -> list[Path]:
        return get_file_from_extention(self.project_dir.nawis_nwc, NWC_EXTENTION)

    @property
    def nwd_models(self) -> list[Path]:
        return get_file_from_extention(self.project_dir.nawis_nwd, NWD_EXTENTION)

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
        pool_items: list[RevitFileInRevitServer | RevitFileInLocal] = [
            *self.revit_files_in_rs,
            *self.revit_files,
        ]
        pool_func(start_backup_process_from_pool, pool_items)

    def load_in_ftp(self) -> None:
        pool_items: list[RevitFileInRevitServer] = self.revit_files_in_rs
        pool_func(start_ftp_process_from_pool, pool_items)

    def load_in_nwc(self) -> None:
        with control_workdir(PATH_WORKDIR_NAWIS):
            pool_items: list[RevitFileInRevitServer | RevitFileInLocal] = [
                *self.revit_files_in_rs,
                *self.revit_files,
            ]
            pool_func(start_nwc_process_from_pool, pool_items)

    def load_in_nwd(self) -> None:
        for nwf_path in self.nwf_models:
            if nwf_path.is_file():
                nwd_path: Path = self.project_dir.nawis_nwd / (
                    nwf_path.stem + NWD_EXTENTION
                )
                nwd_path: Path = run_load_nwd(nwd_path=nwd_path, nwf_path=nwf_path)

                rename_nwd: Path = nwd_path.parent / (
                    nwd_path.stem + "_" + DATE_NOW + nwd_path.suffix
                )
                nwd_path.rename(rename_nwd)
            else:
                logging.warning(f"Файл {nwf_path} не существует.")

    def load_in_arch(self, name_album: str = None) -> Path:
        items = self.arch_or_pub_items

        for extention, files in items.items():
            files: list[Path] = files

            if name_album:
                name_dir = "_".join((DATE_NOW, extention, name_album))
            else:
                name_dir = "_".join((DATE_NOW, extention))

            copy_dir = self.arch_dir.arch / name_dir

            copy_dir.mkdir(exist_ok=True)

            for file in files:
                path_copy_file = copy_dir / file.name
                shutil.copy2(file, path_copy_file)

        return self.arch_dir.arch

    def load_in_publish(self) -> Path:
        items: dict[str : list[Path]] = self.arch_or_pub_items

        pub_dir: Path = self.ftp_dir.publish / (f"{self.name}_{DATE_NOW}")
        with control_workdir(pub_dir) as new_dir:
            for extention, files in items.items():
                files: list[Path] = files

                copy_dir: Path = new_dir / extention
                copy_dir.mkdir()
                for file in files:
                    path_copy_file = copy_dir / file.name
                    shutil.copy2(file, path_copy_file)

            make_achive(new_dir, new_dir)

        return pub_dir.parent

