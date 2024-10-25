from pathlib import Path


def get_file_from_extention(source_dir: Path, extention: str = None) -> list[Path]:
    """Рекурсивное получение путей до файлов в древе директориий."""
    DOT_SYMBOL: str = "."

    if DOT_SYMBOL not in extention:
        except_message: str = (
            "Расширение файла должно быть обязательно"
            f" с точкой, а передан {extention}."
        )
        raise ValueError(except_message)

    pattern = "*" if extention is None else f"*{extention}"
    return [Path(file) for file in source_dir.rglob(pattern)]
