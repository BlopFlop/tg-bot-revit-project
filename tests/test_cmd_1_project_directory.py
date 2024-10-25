from pathlib import Path

import pytest

from cmd_revit_program.core.exceptions import DirectoryNotFoundError
from cmd_revit_program.loader.dit_three import (
    ArchDirThree,
    FTPDirThree,
    ProjectDirThree,
)
from tests.constants import PROJECT_NAME


def test_create_arch_directory(tmpdir):
    mkdir_arch = tmpdir.mkdir("Archive")
    mkdir_arch.mkdir(ArchDirThree._ARCH_DIR)
    mkdir_arch.mkdir(ArchDirThree._BACKUP_DIR)

    path_arch: Path = Path(mkdir_arch)

    arch_dir_obj: ArchDirThree = ArchDirThree(path_arch, PROJECT_NAME)
    arch_dir_obj.create_dirs()

    directories: list[Path] = [arch_dir_obj.arch, arch_dir_obj.backup]

    for dir in directories:
        assert dir.is_dir(), f"У класса ArchDirThree директория {dir} не создана."


def test_incorrect_path_arch_directory(tmpdir):
    incorrect_path_arch: Path = Path("incorrect_dir")
    with pytest.raises(DirectoryNotFoundError) as exc:
        arch_dir_obj: ArchDirThree = ArchDirThree(incorrect_path_arch, PROJECT_NAME)
        arch_dir_obj.create_dirs()
        assert exc, (
            "При инициализации класса ArchDirThree с неккоректным путем"
            " должна выдавться ошибка DirectoryNotFoundError."
        )


def test_incorrect_arch_directory(tmpdir):
    path_arch: Path = Path(tmpdir.mkdir("Archive"))

    with pytest.raises(DirectoryNotFoundError) as exc:
        arch_dir_obj: ArchDirThree = ArchDirThree(path_arch, PROJECT_NAME)
        arch_dir_obj.create_dirs()
        assert exc, (
            "При инициализации класса ArchDirThree с неккоректной"
            " директорией должна выдавться ошибка DirectoryNotFoundError."
        )


def test_create_ftp_directory(tmpdir):
    path_ftp: Path = Path(tmpdir.mkdir("FTP"))
    obj_ftp_dir: FTPDirThree = FTPDirThree(path_ftp, PROJECT_NAME)

    directories: list[Path] = obj_ftp_dir.create_dirs()

    for dir in directories:
        assert dir.is_dir(), f"У класса FTPDirThree директория {dir} не создана."


def test_incorrect_path_ftp_directory():
    incorrect_path_ftp: Path = Path("incorrect_path")
    with pytest.raises(DirectoryNotFoundError) as exc:
        obj_ftp_dir: FTPDirThree = FTPDirThree(incorrect_path_ftp, PROJECT_NAME)
        obj_ftp_dir.create_dirs()
        assert exc, (
            "При инициализации класса FTPDirThree с неккоректной"
            " директорией должна выдавться ошибка DirectoryNotFoundError."
        )


def test_create_project_directory(tmpdir):
    path_project: Path = Path(tmpdir.mkdir("Project"))
    obj_project_dir: ProjectDirThree = ProjectDirThree(path_project, PROJECT_NAME)
    directories: list[Path] = obj_project_dir.create_dirs()
    for dir in directories:
        assert dir.is_dir(), f"У класса ProjectDirThree директория {dir} не создана."


def test_incorrect_path_project_directory():
    incorrect_path: Path = Path("incorrect_path")
    with pytest.raises(DirectoryNotFoundError) as exc:
        obj_project_dir: ProjectDirThree = ProjectDirThree(incorrect_path, PROJECT_NAME)
        obj_project_dir.create_dirs()
        assert exc, (
            "При инициализации класса ProjectDirThree с неккоректной"
            " директорией должна выдавться ошибка DirectoryNotFoundError."
        )
