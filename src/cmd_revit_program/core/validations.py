import logging
from pathlib import Path

from cmd_revit_program.core.exceptions import ProgramNotSetup


def is_dir_or_file(
    path: Path, confirm_message: str, except_message: str
) -> None | ProgramNotSetup:
    if not (path.is_dir() or path.is_file()):
        logging.error(except_message)
        raise ProgramNotSetup(except_message)

    logging.info(confirm_message)
