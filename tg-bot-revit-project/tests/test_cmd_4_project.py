from pathlib import Path

from cmd_revit_program.loader.project import (
    Project,
    RevitFileInLocal,
    RevitFileInRevitServer,
)
from tests.constants import (
    LOCAL_MODEL_NAME,
    REVIT_MODEL_NAME,
    TEST_NWF_PATH,
    TEST_PATH_MODEL,
)
from tests.functions import get_file_from_extention


def test_get_models_in_project(project: Project):
    local_revit_model: list[RevitFileInLocal] = project.revit_files
    revit_model_in_rs: list[RevitFileInRevitServer] = project.revit_files_in_rs
    nwf_models: list[Path] = project.nwf_models

    count_items_in_rs: int = len(local_revit_model)
    assert count_items_in_rs == 1, (
        "Из ревит сервера должна найтись одна модель,"
        f" а найдено {revit_model_in_rs}."
    )

    count_items_in_local: int = len(revit_model_in_rs)
    assert count_items_in_local == 1, (
        "В локальной директории должна найтись одна модель, "
        f"а найдено {count_items_in_local}."
    )

    count_items_in_nwf: int = len(nwf_models)
    assert count_items_in_nwf == 1, (
        "В директории с nwf моделями должна быть одна модель, "
        f"а найдено {count_items_in_nwf}."
    )

    item_in_local: RevitFileInLocal = local_revit_model[0]

    assert (
        item_in_local.model_path.is_file()
    ), f"Модели {item_in_local.name} не существует."

    assert item_in_local.name == LOCAL_MODEL_NAME, (
        f"Локальная модель должна называться {REVIT_MODEL_NAME}, "
        f"а итоговая модель {item_in_local.name}."
    )

    item_in_rs: RevitFileInRevitServer = revit_model_in_rs[0]
    assert item_in_rs.name == REVIT_MODEL_NAME, (
        f"Модель из ревит сервера должна называться {REVIT_MODEL_NAME}, "
        f"а итоговая модель {item_in_rs.name}."
    )

    assert item_in_rs.model_path == Path(TEST_PATH_MODEL[1:]), (
        f"Модель из ревит сервера должна иметь путь {TEST_PATH_MODEL[1:]}, "
        f"а итоговая модель {item_in_rs.model_path}."
    )

    item_nwf: Path = nwf_models[0]
    assert item_nwf.name == TEST_NWF_PATH.name, (
        "Имя nwf модели должно быть равно "
        f"{TEST_NWF_PATH.name}, а сейчас {item_nwf.name}."
    )


def test_load_models(project: Project):
    project.load_in_ftp()
    ftp_revit_files: list[Path] = project.ftp_models

    assert len(ftp_revit_files) == 2, (
        "После выгузки моделей на FTP, в папке FTP с ревит моделями должно"
        f" быть 2 модели, а сейчас {len(ftp_revit_files)}"
    )

    project.load_in_backup()
    backup_revit_files: list[Path] = project.backup_models

    assert len(backup_revit_files) == 2, (
        "После выгузки моделей бэкап, в папке backup с ревит моделями должно"
        f" быть 2 модели, а сейчас {len(backup_revit_files)}"
    )

    project.load_in_nwc()
    nwc_revit_files: list[Path] = project.nwc_models

    assert len(nwc_revit_files) == 2, (
        "После выгузки моделей в Nawisworks, в папке FTP с ревит моделями"
        f" должно быть 2 модели, а сейчас {len(nwc_revit_files)}."
    )

    project.load_in_nwd()
    nwd_items: list[Path] = project.nwd_models

    assert len(nwd_items) == 1, (
        "После выгрузки nwd модели должна выгрузиться одна модель, "
        f"а выгрузилась {len(nwd_items)}."
    )

    arch_dir: Path = project.load_in_arch()
    files: list[Path] = get_file_from_extention(
        source_dir=arch_dir, extention=".zip"
    )
    assert len(files) == 4, (
        "После архивации моделей должно получится 4 архива, "
        f"а выгрузилось {len(files)}"
    )

    NAME_ALBUM = "AR_TEST_ALBUM"
    arch_dir: Path = project.load_in_arch(NAME_ALBUM)
    files: list[Path] = get_file_from_extention(
        source_dir=arch_dir, extention=".zip"
    )
    assert len(files) == 8, (
        "После архивации моделей должно получится 8 архивов, "
        f"а выгрузилось {len(files)}"
    )

    publish_dir: Path = project.load_in_publish()
    publish_files: list[Path] = get_file_from_extention(
        source_dir=publish_dir, extention=".zip"
    )
    assert len(publish_files) == 1, (
        "После архивации моделей должен получится 1 архив, "
        f"а выгрузилось {len(publish_files)}"
    )
