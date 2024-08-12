from pathlib import Path

from cmd_revit_program.loader.functions import PATH_WORKDIR_NAWIS
from cmd_revit_program.loader.project import (
    RevitFileInLocal,
    RevitFileInRevitServer,
)


def test_load_ftp_revit_model(revit_model: RevitFileInRevitServer):
    revit_model.copy_to_ftp()
    ftp_path: Path = revit_model.ftp_path
    assert (
        ftp_path.is_file()
    ), f"Должна выгрузится модель по пути {ftp_path}, ее не существует."


def test_load_backup_revit_model(revit_model: RevitFileInRevitServer):
    revit_model.copy_to_backup()
    backup_path: Path = revit_model.backup_path
    assert (
        backup_path.is_file()
    ), f"Должна выгрузится модель по пути {backup_path}, ее не существует."


def test_load_backup_local_revit_model(local_revit_model: RevitFileInLocal):
    local_revit_model.copy_to_backup()
    backup_path: Path = local_revit_model.backup_path
    assert (
        backup_path.is_file()
    ), f"Должна выгрузится модель по пути {backup_path}, ее не существует."


def test_load_nwc_revit_model(revit_model: RevitFileInRevitServer):
    PATH_WORKDIR_NAWIS.mkdir(exist_ok=True)
    revit_model.copy_to_backup()
    nwc_path: Path = revit_model.load_rvt_to_nwc()
    assert (
        nwc_path.is_file()
    ), f"Должна выгрузится модель по пути {nwc_path}, ее не существует."
    PATH_WORKDIR_NAWIS.rmdir()


def test_load_nwc_local_revit_model(local_revit_model: RevitFileInLocal):
    PATH_WORKDIR_NAWIS.mkdir(exist_ok=True)
    local_revit_model.copy_to_backup()
    nwc_path: Path = local_revit_model.load_rvt_to_nwc()
    assert (
        nwc_path.is_file()
    ), f"Должна выгрузится модель по пути {nwc_path}, ее не существует."
