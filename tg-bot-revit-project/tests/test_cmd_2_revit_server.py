from pathlib import Path

import pytest
from rpws.models import ModelInfo

from cmd_revit_program.loader.functions import (
    get_all_models_in_revit_server,
    get_model_for_mask,
)
from tests.constants import (
    INCORRECT_SEARCH_NAME,
    INCORRECT_SERVER_NAME,
    REVIT_MODEL_NAME,
    REVIT_SERVER_NAME,
    SEARCH_NAME,
    TEST_PATH_MODEL,
)


def test_get_all_models_for_server_name():
    all_revit_models: list[ModelInfo] = get_all_models_in_revit_server(
        REVIT_SERVER_NAME
    )
    assert isinstance(all_revit_models, list), (
        "В результате получения моделей из ревит серевера, "
        "должен вернуться список."
    )


def test_get_all_models_for_incorrect_server_name():
    all_revit_models: list[ModelInfo] = get_all_models_in_revit_server(
        INCORRECT_SERVER_NAME
    )
    assert isinstance(all_revit_models, list), (
        "В результате получения моделей из неккоректного ревит серевера, "
        "должен вернуться список."
    )
    assert len(all_revit_models) == 0, (
        "При попытке получения моделей из неккоректного ревит сервера, "
        "должен вернуться пустой список."
    )


def test_get_model_for_mask(all_revit_models: list[ModelInfo]):
    result_revit_models: list[ModelInfo] = get_model_for_mask(
        all_revit_models, SEARCH_NAME
    )
    count_revit_models = len(result_revit_models)

    assert isinstance(result_revit_models, list), (
        "В результате получения моделей из ревит серевера, "
        "должен вернуться список."
    )

    assert count_revit_models == 1, (
        "На тестовом ревит сервере должна найтись "
        f"только одна модель по маске {SEARCH_NAME}, "
        f"а найдено {count_revit_models}"
    )

    item_revit_model = result_revit_models[0]

    assert item_revit_model.name == REVIT_MODEL_NAME, (
        f"Имя полученной модели должно равнятся {REVIT_MODEL_NAME}, "
        f"а итоговое имя равно {item_revit_model}."
    )
    assert Path(item_revit_model.path) == Path(TEST_PATH_MODEL), (
        f"Путь полученной модели должен равнятся {TEST_PATH_MODEL}, "
        f"а итоговый путь равен {item_revit_model.path}."
    )


def test_get_model_for_incorrect_mask(all_revit_models: list[ModelInfo]):
    result_revit_models: list[ModelInfo] = get_model_for_mask(
        all_revit_models, INCORRECT_SEARCH_NAME
    )
    assert isinstance(
        result_revit_models, list
    ), "При передаче неккоректной маски должен вернуться список."
    assert (
        not result_revit_models
    ), "При передаче неккоректной маски должен вернуться пустой список."
