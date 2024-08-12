from multiprocessing import freeze_support

from cmd_revit_program import (
    CMD_ARCH_DIR,
    CMD_FTP_DIR,
    CMD_NAME_PROJECT,
    CMD_PROJECT_DIR,
    CMD_SEARCH_PATTERN,
    CMD_SERVER_NAME,
    Project,
    parser,
)

project = Project(
    server_name=CMD_SERVER_NAME,
    project_name=CMD_NAME_PROJECT,
    search_pattern=CMD_SEARCH_PATTERN,
    project_dir_path=CMD_PROJECT_DIR,
    arch_dir_path=CMD_ARCH_DIR,
    ftp_dir_path=CMD_FTP_DIR,
)

if __name__ == "__main__":
    freeze_support()
    parser(project)
