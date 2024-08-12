# import shutil
# import subprocess
# from pathlib import Path

# from cmd_revit_program.core.constants import (
#     ARG_NAME_ALBUM_SHORT,
#     ARG_START_ARCH,
#     ARG_START_BACKUP,
#     ARG_START_FTP,
#     ARG_START_NAWIS,
#     ARG_START_PUBLISH,
# )
# from cmd_revit_program.loader.dit_three import ArchDirThree
# from tests.constants import BASE_DIR


# def test_exe_ftp(exe_program: Path):
#     subprocess.run(args=(str(exe_program), ARG_START_FTP))


# def test_exe_backup(exe_program: Path):
#     subprocess.run(args=(str(exe_program), ARG_START_BACKUP))


# def test_exe_nawisworks(exe_program: Path):
#     subprocess.run(args=(str(exe_program), ARG_START_NAWIS))


# def test_exe_arch(exe_program: Path):
#     subprocess.run(args=(str(exe_program), ARG_START_ARCH))


# def test_exe_ftp_arch_album(exe_program: Path):
#     TEST_ALBUM = "AR12"
#     subprocess.run(
#         args=(
#             str(exe_program),
#             ARG_START_ARCH,
#             ARG_NAME_ALBUM_SHORT,
#             TEST_ALBUM,
#         )
#     )


# def test_exe_publish(exe_program: Path):
#     subprocess.run(args=(str(exe_program), ARG_START_PUBLISH))
