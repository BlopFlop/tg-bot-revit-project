import logging
from pathlib import Path
from typing import Final

from cmd_revit_program.core.exceptions import DirectoryNotFoundError


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


def get_or_create_dir(path_dir: Path) -> Path:
    if path_dir.is_file():
        except_message = (
            "Произошла ошибка вы передали в функцию путь до" " файла, а не директории."
        )
        logging.error(except_message, stack_info=True)
        raise DirectoryNotFoundError(except_message)

    if not path_dir.is_dir():
        path_dir.mkdir()
        info_message = f"Директория {path_dir.name} создана"
        logging.info(info_message)

    return path_dir
