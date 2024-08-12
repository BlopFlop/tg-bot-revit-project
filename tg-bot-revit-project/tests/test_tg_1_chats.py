from pathlib import Path

from tg_bot.functions import DataChat

FST_TEST_CHAT_ID = 132142
SCD_TEST_CHAT_ID = 3259


def test_chat_file(tmpdir):
    base_dir = Path(tmpdir)
    data_chat = DataChat(base_dir=base_dir).csv_file

    assert (
        data_chat.is_file()
    ), f"По пути {data_chat} должен создаться csv файл."


def test_add_chat(tmpdir):
    base_dir = Path(tmpdir)
    data_chat = DataChat(base_dir=base_dir)

    data_chat.add(FST_TEST_CHAT_ID)

    with open(file=data_chat.csv_file, mode="r", encoding="utf-8") as file:
        assert str(FST_TEST_CHAT_ID) in file.read(), (
            f"В созданный файл {data_chat.csv_file.name} должен "
            f"добавиться id {FST_TEST_CHAT_ID}."
        )

    data_chat.add(SCD_TEST_CHAT_ID)

    with open(file=data_chat.csv_file, mode="r", encoding="utf-8") as file:
        data = file.read()
        assert str(FST_TEST_CHAT_ID) in data, (
            f"В созданный файл {data_chat.csv_file.name} должен "
            f"добавиться id {FST_TEST_CHAT_ID}."
        )
        assert str(SCD_TEST_CHAT_ID) in data, (
            f"В созданный файл {data_chat.csv_file.name} должен "
            f"добавиться id {SCD_TEST_CHAT_ID}."
        )


def test_get_chat(tmpdir):
    base_dir = Path(tmpdir)
    data_chat = DataChat(base_dir=base_dir)

    data_chat.add(FST_TEST_CHAT_ID)
    data_chat.add(SCD_TEST_CHAT_ID)

    data = data_chat.get()

    len_data = len(data)

    assert isinstance(data, list), (
        "Результатом получения всех чатов должен быть список, "
        f"а сейчас {type(data)}."
    )
    assert (
        len_data == 2
    ), f"В результирующем списке должно быть 2 объекта, а сейчас {len_data}"
    assert FST_TEST_CHAT_ID in data, (
        "При получении чатов в результирующем списке должен "
        f"быть id {FST_TEST_CHAT_ID}"
    )
    assert SCD_TEST_CHAT_ID in data, (
        "При получении чатов в результирующем списке должен "
        f"быть id {SCD_TEST_CHAT_ID}"
    )


def test_remowe_chat(tmpdir):
    base_dir = Path(tmpdir)
    data_chat = DataChat(base_dir=base_dir)

    data_chat.add(FST_TEST_CHAT_ID)
    data_chat.add(SCD_TEST_CHAT_ID)

    data_chat.remove(FST_TEST_CHAT_ID)

    with open(file=data_chat.csv_file, mode="r", encoding="utf-8") as file:
        data = file.read()
        assert str(FST_TEST_CHAT_ID) not in data, (
            f"В созданном файле {data_chat.csv_file.name} должен "
            f"удалится id {FST_TEST_CHAT_ID}."
        )
        assert str(SCD_TEST_CHAT_ID) in data, (
            f"В созданном файле {data_chat.csv_file.name} должен "
            f"остаться id {SCD_TEST_CHAT_ID}."
        )
