import shutil
import subprocess
from pathlib import Path

from cmd_revit_program import Project, main
from cmd_revit_program.core.constants import (
    ARG_NAME_ALBUM_SHORT,
    ARG_START_ARCH,
    ARG_START_BACKUP,
    ARG_START_FTP,
    ARG_START_NAWIS,
    ARG_START_PUBLISH,
)
from cmd_revit_program.loader.dit_three import (
    ArchDirThree,
    FTPDirThree,
    ProjectDirThree,
)
from tests.constants import BASE_DIR
from tests.functions import get_file_from_extention


def test_main_backup(
    project: Project,
):
    result_path = main.start_backup(project=project)

    backup_files = get_file_from_extention(project.arch_dir.backup, ".rvt")
    count_load_files = len(backup_files)

    assert result_path == project.arch_dir.backup, (
        f"Результирующий путь должен быть {project.arch_dir.backup}, "
        f"а сейчас {result_path}."
    )
    assert count_load_files == 2, (
        f"В папку {project.arch_dir.backup} должено выгрузится 2 файла с "
        f"расширением .rvt, а выгрузилось {count_load_files}."
    )


def test_main_ftp(project: Project):
    result_path = main.start_ftp(project=project)

    ftp_files = get_file_from_extention(project.ftp_dir.revit_models, ".rvt")
    count_load_files = len(ftp_files)

    assert result_path == project.ftp_dir.revit_models, (
        f"Результирующий путь должен быть {project.ftp_dir.revit_models}, "
        f"а сейчас {result_path}."
    )
    assert count_load_files == 2, (
        f"В папку {project.ftp_dir.revit_models} должено выгрузится 2 файла с "
        f"расширением .rvt, а выгрузилось {count_load_files}."
    )


# def test_main_nawisworks(
#     project: Project
# ):
#     result_path = main.start_backup(project=project)

#     backup_files = get_file_from_extention(project.arch_dir.backup, '.rvt')
#     count_load_files = len(backup_files)

#     assert result_path == project.arch_dir.backup, (
#         f'Результирующий путь должен быть {project.arch_dir.backup}, '
#         f'а сейчас {result_path}.'
#     )
#     assert count_load_files == 2, (
#         f'В папку {project.arch_dir.backup} должено выгрузится 2 файла с '
#         f'расширением .rvt, а выгрузилось {count_load_files}.'
#     )


# def test_main_arch(project: Project):
#     result_path = main.start_arch(project=project)

#     arch_files = get_file_from_extention(project.arch_dir.arch, ".zip")
#     count_load_files = len(arch_files)

#     assert result_path == project.arch_dir.arch, (
#         f"Результирующий путь должен быть {project.arch_dir.arch}, "
#         f"а сейчас {result_path}."
#     )
#     assert count_load_files == 2, (
#         f"В папку {project.arch_dir.backup} должено выгрузится 2 файла с "
#         f"расширением .rvt, а выгрузилось {count_load_files}."
#     )


# def test_main_arch_album(project: Project):
#     result_path = main.start_backup(project=project)

#     backup_files = get_file_from_extention(project.arch_dir.backup, ".rvt")
#     count_load_files = len(backup_files)

#     assert result_path == project.arch_dir.backup, (
#         f"Результирующий путь должен быть {project.arch_dir.backup}, "
#         f"а сейчас {result_path}."
#     )
#     assert count_load_files == 2, (
#         f"В папку {project.arch_dir.backup} должено выгрузится 2 файла с "
#         f"расширением .rvt, а выгрузилось {count_load_files}."
#     )


# def test_main_publish(project: Project):
#     result_path = main.start_backup(project=project)

#     backup_files = get_file_from_extention(project.arch_dir.backup, ".rvt")
#     count_load_files = len(backup_files)

#     assert result_path == project.arch_dir.backup, (
#         f"Результирующий путь должен быть {project.arch_dir.backup}, "
#         f"а сейчас {result_path}."
#     )
#     assert count_load_files == 2, (
#         f"В папку {project.arch_dir.backup} должено выгрузится 2 файла с "
#         f"расширением .rvt, а выгрузилось {count_load_files}."
#     )
