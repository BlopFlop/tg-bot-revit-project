from multiprocessing import freeze_support

from constants import (
    PATH_NAWISWORKS, PATH_NAWIS_FTR, PATH_NAWIS_ROAMER, PATH_REVIT,
    PATH_REVIT_RST
)
from configs import configure_logging
from cmd_parser import parser_
from utils import check_dir_or_file


if __name__ == '__main__':
    configure_logging()
    freeze_support()
    except_message = (
        'Программа Nawisworks не установленна или установленна неправильно.'
    )
    check_dir_or_file(PATH_NAWISWORKS, except_message)
    check_dir_or_file(PATH_NAWIS_FTR, except_message)
    check_dir_or_file(PATH_NAWIS_ROAMER, except_message)
    except_message = (
        'Программа Revit не установленна или установленна неправильно.'
    )
    check_dir_or_file(PATH_REVIT, except_message)
    check_dir_or_file(PATH_REVIT_RST, except_message)
    parser_()
