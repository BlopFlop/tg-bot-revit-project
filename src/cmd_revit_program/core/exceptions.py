class DirectoryNotFoundError(Exception):
    """Выбрасывается если директории не сущестует."""

    pass


class RevitFileNotFoundError(Exception):
    """Выбрасывается если ревит моделей не существует."""

    pass


class ProgramNotSetup(Exception):
    """Выбрасывается если какой либо программы или компонента не существует."""

    pass
