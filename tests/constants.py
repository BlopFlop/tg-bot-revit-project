from pathlib import Path

REVIT_SERVER_NAME: str = "10.10.1.30"
INCORRECT_SERVER_NAME: str = "10.2.3.4"

PROJECT_NAME: str = "999_TEST"
VER_REVIT: int = 2021

SEARCH_NAME: str = "TEST"
INCORRECT_SEARCH_NAME: str = "INCORRECT_TEST"

REVIT_MODEL_NAME: str = "999_TEST_ТестовыйПроект.rvt"
TEST_PATH_MODEL: str = r"\999_TEST\WIP\999_TEST_ТестовыйПроект.rvt"

BASE_DIR: Path = Path(__file__).parent

LOCAL_MODEL_PATH: Path = (
    BASE_DIR / r"test_model_ftp\Проект1.rvt"
)
# LOCAL_MODEL_NAME: str = LOCAL_MODEL_PATH.name

# TEST_NWF_PATH: Path = BASE_DIR / r"tests\nwf_test_model\999_Test.nwf"
