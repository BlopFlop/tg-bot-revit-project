from cmd_revit_program.core.constants import (
    CMD_NAWIS_OR_REVIT_VERSION,
    PATH_NAWIS_FTR,
    PATH_NAWIS_ROAMER,
    PATH_NAWISWORKS,
    PATH_REVIT,
    PATH_REVIT_RST,
)
from cmd_revit_program.core.validations import is_dir_or_file

revit_setup = (
    f"Программа Revit {CMD_NAWIS_OR_REVIT_VERSION} присутсвует на пк."
)
revit_not_setup_message = (
    f"Программа Revit {CMD_NAWIS_OR_REVIT_VERSION} не установленна или "
    "установленна с ошибкой на данном пк"
)
is_dir_or_file(PATH_REVIT, revit_setup, revit_not_setup_message)

rst_setup_message = "Утилита RevitServerTool присутсвует на пк."
rst_not_setup_message = (
    "Утилита RevitServerTool отсутвует на пк."
    f"По пути {PATH_REVIT_RST}, программа Revit была неккоректно установлена"
)
is_dir_or_file(PATH_REVIT_RST, rst_setup_message, rst_not_setup_message)


nawis_setup_message = (
    f"Программа Navisworks {CMD_NAWIS_OR_REVIT_VERSION} установлена."
)
nawis_not_setup_message = (
    f"Программа Navisworks {CMD_NAWIS_OR_REVIT_VERSION} не установлена на пк."
)
is_dir_or_file(PATH_NAWISWORKS, nawis_setup_message, nawis_not_setup_message)

ftr_setup_message = "Утилита FiletoolsTaskRunner присутсвует на пк."
ftr_not_setup_message = (
    "Утилита FiletoolsTaskRunner отсутсвует на пк. "
    f"По пути {PATH_NAWIS_FTR}, программа Navisworks была неккоректно"
    " установлена."
)
is_dir_or_file(PATH_NAWIS_FTR, ftr_setup_message, ftr_not_setup_message)

roamer_setup_message = "Утилита Roamer присутствует на пк."
roamer_not_setup_message = (
    "Утилита Roamer отсутствует на пк."
    f"По пути {PATH_NAWIS_ROAMER}, программа Roamer была неккоректно "
    "установлена."
)
is_dir_or_file(
    PATH_NAWIS_ROAMER, roamer_setup_message, roamer_not_setup_message
)
