import shutil
from pathlib import Path

import pytest
from rpws.models import ModelInfo

from cmd_revit_program.loader.functions import (
    get_all_models_in_revit_server,
    get_model_for_mask,
)
from cmd_revit_program.loader.project import (
    ArchDirThree,
    FTPDirThree,
    Project,
    ProjectDirThree,
    RevitFileInLocal,
    RevitFileInRevitServer,
)
from tests.constants import (
    BASE_DIR,
    LOCAL_MODEL_PATH,
    PROJECT_NAME,
    REVIT_SERVER_NAME,
    SEARCH_NAME,
    TEST_NWF_PATH,
)


@pytest.fixture
def all_revit_models() -> list[ModelInfo]:

    return get_all_models_in_revit_server(REVIT_SERVER_NAME)


@pytest.fixture
def arch_dir_obj(tmpdir) -> ArchDirThree:

    mkdir_arch = tmpdir.mkdir("Archive")
    mkdir_arch.mkdir(ArchDirThree._ARCH_DIR)
    mkdir_arch.mkdir(ArchDirThree._BACKUP_DIR)
    arch_dir_three: ArchDirThree = ArchDirThree(Path(mkdir_arch), PROJECT_NAME)
    arch_dir_three.create_dirs()
    return arch_dir_three


@pytest.fixture
def project_dir_obj(tmpdir) -> ProjectDirThree:

    path_project: Path = Path(tmpdir.mkdir("Project"))
    project_dir_three: ProjectDirThree = ProjectDirThree(
        path_project, PROJECT_NAME
    )
    project_dir_three.create_dirs()
    return project_dir_three


@pytest.fixture
def ftp_dir_obj(tmpdir) -> FTPDirThree:

    path_ftp: Path = Path(tmpdir.mkdir("FTP"))
    ftp_dir_three: FTPDirThree = FTPDirThree(path_ftp, PROJECT_NAME)
    ftp_dir_three.create_dirs()
    return ftp_dir_three


@pytest.fixture
def mk_test_env(
    project_dir_obj: ProjectDirThree,
    ftp_dir_obj: FTPDirThree,
    arch_dir_obj: ArchDirThree,
) -> None:
    ENV_DATA: list[tuple[str:str]] = [
        ("CMD_SERVER_NAME", REVIT_SERVER_NAME),
        ("CMD_NAME_PROJECT", PROJECT_NAME),
        ("CMD_SEARCH_PATTERN", SEARCH_NAME),
        ("CMD_NAWIS_OR_REVIT_VERSION", "2021"),
        ("CMD_PROJECT_DIR", str(project_dir_obj.project)),
        ("CMD_ARCH_DIR", str(arch_dir_obj.project)),
        ("CMD_FTP_DIR", str(ftp_dir_obj.project)),
        ("TG_TOKEN", "6979385723:AAGCMzzNJaYr2-7ZvGyH9LomyrzZHh0x9nk"),
    ]

    path_env_file = BASE_DIR / ".test.env"

    with open(file=path_env_file, mode="w", encoding="utf-8") as env_file:
        for item in ENV_DATA:
            env_file.write("=".join(item) + "\n")


@pytest.fixture
def revit_model(
    all_revit_models: list[ModelInfo],
    arch_dir_obj: ArchDirThree,
    project_dir_obj: ProjectDirThree,
    ftp_dir_obj: FTPDirThree,
) -> RevitFileInRevitServer:

    model: ModelInfo = get_model_for_mask(all_revit_models, SEARCH_NAME)[0]
    revit_obj: RevitFileInRevitServer = RevitFileInRevitServer(
        server_name=REVIT_SERVER_NAME,
        model_info_for_rs=model,
        backup_path=arch_dir_obj.backup,
        nwc_path=project_dir_obj.nawis_nwc,
        ftp_path=ftp_dir_obj.revit_models,
    )
    return revit_obj


@pytest.fixture
def local_revit_model(
    arch_dir_obj: ArchDirThree,
    project_dir_obj: ProjectDirThree,
) -> RevitFileInLocal:

    revit_obj: RevitFileInLocal = RevitFileInLocal(
        model_path=LOCAL_MODEL_PATH,
        backup_path=arch_dir_obj.backup,
        nwc_path=project_dir_obj.nawis_nwc,
    )
    return revit_obj


@pytest.fixture
def project(
    revit_model: RevitFileInRevitServer,
    project_dir_obj: ProjectDirThree,
    arch_dir_obj: ArchDirThree,
    ftp_dir_obj: FTPDirThree,
) -> Project:

    project_dir_path: Path = project_dir_obj.base_dir
    arch_dir_path: Path = arch_dir_obj.base_dir
    ftp_dir_path: Path = ftp_dir_obj.base_dir

    copy_local_model: Path = ftp_dir_obj.revit_models / LOCAL_MODEL_PATH.name
    shutil.copy2(LOCAL_MODEL_PATH, copy_local_model)

    copy_nwf_model: Path = project_dir_obj.nawis_nwf / TEST_NWF_PATH.name
    shutil.copy2(TEST_NWF_PATH, copy_nwf_model)

    revit_model.copy_to_ftp()

    return Project(
        server_name=REVIT_SERVER_NAME,
        project_name=PROJECT_NAME,
        search_pattern=SEARCH_NAME,
        project_dir_path=project_dir_path,
        arch_dir_path=arch_dir_path,
        ftp_dir_path=ftp_dir_path,
    )


@pytest.fixture
def exe_program() -> Path:
    exe_file = BASE_DIR / "cmd_program.exe"
    assert (
        exe_file.is_file()
    ), f"Файл {exe_file.name} не найден, тест не будет запущен."
    return exe_file
