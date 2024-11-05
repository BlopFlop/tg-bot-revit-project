from pathlib import Path

from src.core.constants import LOCAL_NAWISWORKS_PATH
from src.revit_project.project_models import (
    RevitFileInFTP,
    RevitFileInRevitServer,
)
from src.revit_project.functions import control_workdir


def test_load_ftp(revit_model: RevitFileInRevitServer) -> None:
    revit_model.load_ftp()
    assert revit_model.ftp_path.is_file(), (
        f"Должна выгрузится модель по пути {revit_model.ftp_path}"
        ", ее не существует."
    )


def test_load_backup(
    revit_model: RevitFileInRevitServer,
    local_revit_model: RevitFileInFTP
) -> None:
    for revit_item in (revit_model, local_revit_model):
        revit_item.load_backup()
        assert revit_item.backup_path.is_file(), (
            f"Должна выгрузится модель по пути {revit_item.backup_path}"
            ", ее не существует."
        )


def test_load_nwc(
    revit_model: RevitFileInRevitServer,
    local_revit_model: RevitFileInFTP
) -> None:
    with control_workdir(LOCAL_NAWISWORKS_PATH):
        for revit_item in (revit_model, local_revit_model):
            revit_item.load_backup()
            nwc_path: Path = revit_item.load_nwc()

            assert nwc_path.is_file(), (
                f"Должна выгрузится модель по пути {nwc_path},"
                " ее не существует."
            )
