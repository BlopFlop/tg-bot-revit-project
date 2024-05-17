from datetime import datetime as dt
from subprocess import run
from pathlib import Path
from multiprocessing import Pool
import subprocess
import shutil
import logging

from _constants import (
    COUNT_PROCESSES, DATE_NOW, NAME_PROJECT, NAME_FIELD_PUBLISH,
    ROAMER_FLAG_NWD, SEC_IN_MIN,

    PATH_NAWIS_FTR, PATH_WORKDIR_NAWIS, PATH_REVIT_RST,
    PATH_NAWIS_ROAMER,

    RVT_EXTENTION, NWC_EXTENTION, NWF_EXTENTION, NWD_EXTENTION, IFC_EXTENTION,

    START_LOAD_MESSAGE_ARCH, START_LOAD_MESSAGE_ARCH_ALBUM,
    START_LOAD_MESSAGE_BACKUP, START_LOAD_MESSAGE_FTP,
    START_LOAD_MESSAGE_NAWISWORKS, START_LOAD_MESSAGE_PUBLISH,

    END_LOAD_MESSAGE_ARCH, END_LOAD_MESSAGE_ARCH_ALBUM,
    END_LOAD_MESSAGE_BACKUP, END_LOAD_MESSAGE_FTP, END_LOAD_MESSAGE_NAWISWORKS,
    END_LOAD_MESSAGE_PUBLISH,

    FTR_FIRST_FLAG, FTR_SECOND_FLAG, FTR_THIRD_FLAG,

    RST_COMMAND_CREATE_LOCAL_MODEL, RST_FLAG_SERVER, RST_FLAG_DESTINATION,
    RST_FLAG_OVERWRITE,

    KEY_JSON_ARCH, KEY_JSON_DIR_PATHS,
    KEY_JSON_FTP, KEY_JSON_NWC, KEY_JSON_NWD, KEY_JSON_PUB,

    TG_TOKEN
)
from _json_data import JSON_OBJ
from _utils import (
    make_achive, get_file_from_extention, check_file_creation_date
)
from tg_bot import TgBot


class LoadModel:
    EXTENTIONS: dict[str: str] = {
        NWC_EXTENTION: '01_NWC',
        NWF_EXTENTION: '02_NWF',
        NWD_EXTENTION: '03_NWD',
        RVT_EXTENTION: '04_RVT',
        IFC_EXTENTION: '05_IFC'
    }

    def __init__(
            self,
            update_json_mode: bool = False,
            silence_mode: bool = False) -> None:

        self.update_json_mode: bool = update_json_mode
        self.silence_mode: bool = silence_mode

        if self.update_json_mode:
            JSON_OBJ.update_json_from_google_tab()

    def _start_end_load(
            start_message: str,
            end_message: str):
        '''Декоратор, в зависимотсти от режимов работы в параметрах
        update_json_mode и silence_mode, запускает необходимые функции.'''

        def wrapper(func):
            def decorator(*args, **kwargs):
                self: LoadModel = args[0]

                t_start: dt = dt.now()
                self.send_message_(start_message)

                result: str = func(*args, **kwargs)

                t_end: dt = dt.now()
                time_work: int = (t_end - t_start).seconds // SEC_IN_MIN

                self.send_message_(
                    f'{end_message} процесс длился {time_work} минут(ы|у)'
                )
                if result:
                    self.send_message_(f'Модели искать в {result}')
                return result
            return decorator
        return wrapper

    def _copy_file(self, item_path: tuple[Path, Path]) -> None:
        '''Копирование файлов'''
        file, copy_dir = item_path
        shutil.copy2(str(file), str(copy_dir))
        info_message = f'Файл << {file.name} >> скопирован.'
        logging.info(info_message)

    def _arch_model(
            self,
            path_files: list[str, str, str],
            append_name_arch: str = None) -> Path:
        '''Архивация моделей'''
        if not all(path_files):
            except_message = (
                'Ошибка архивации, был передан пустой список с путями'
            )
            logging.error(except_message, stack_info=True)
            raise ValueError(except_message)

        source_dir, end_dir = path_files
        source_dir: Path = Path(source_dir)
        end_dir: Path = Path(end_dir)

        for extention in self.EXTENTIONS.keys():
            files: list[Path] = get_file_from_extention(source_dir, extention)
            name_copy_dir: str = self.EXTENTIONS.get(extention)
            name_copy_dir: str = F'{DATE_NOW}_{name_copy_dir}'

            if append_name_arch is not None:
                name_copy_dir: str = name_copy_dir + '_' + append_name_arch
            copy_dir = end_dir / name_copy_dir

            if files:
                if not copy_dir.is_dir():
                    copy_dir.mkdir()

                pool_items = [
                    (file, copy_dir) for file in files
                    if check_file_creation_date(file)
                ]
                with Pool(COUNT_PROCESSES) as pool:
                    pool.map(self._copy_file, pool_items)
            else:
                warnitg_message = (
                    f'Файлы с расширением {extention} в директории '
                    f'{source_dir} не найдены'
                )
                logging.warning(warnitg_message)

        return source_dir

    @_start_end_load(
        start_message=START_LOAD_MESSAGE_ARCH,
        end_message=END_LOAD_MESSAGE_ARCH
    )
    def arch(self) -> str:
        '''Архивация моделей'''
        path_items = JSON_OBJ.get(KEY_JSON_ARCH)
        for path_item in path_items:
            self._arch_model(path_item)
        return JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(KEY_JSON_ARCH)

    @_start_end_load(
        start_message=START_LOAD_MESSAGE_ARCH_ALBUM,
        end_message=END_LOAD_MESSAGE_ARCH_ALBUM
    )
    def arch_album(self, append_name_arch: str) -> str:
        '''Архивация моделей после выдачи альбомов'''
        LoadModel(update_json_mode=False, silence_mode=True).ftp()
        path_items = JSON_OBJ.get(KEY_JSON_ARCH)
        for path_item in path_items:
            self._arch_model(path_item, append_name_arch)
        return JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(KEY_JSON_ARCH)

    def _run_load_in_revit_server(
            self, path_files: list[str, str, str]) -> Path | None:
        '''Старт выгрузки моделей из ревит сервера'''
        if not all(path_files):
            except_message = (
                'При выгрузке модели с RevitSever возникла ошибка.'
            )
            logging.error(except_message, stack_info=True)
            raise ValueError(except_message)

        server_name, source_path, end_path = path_files

        source_path: Path = Path(source_path)
        end_path: Path = Path(end_path)

        name_model: str = source_path.name
        end_path: Path = end_path / name_model

        logging.info(f'Старт выгрузки моделей << {name_model} >>')
        try:
            run(
                [
                    PATH_REVIT_RST,
                    RST_COMMAND_CREATE_LOCAL_MODEL,
                    source_path,
                    RST_FLAG_DESTINATION,
                    server_name,
                    RST_FLAG_SERVER,
                    end_path,
                    RST_FLAG_OVERWRITE
                ]
            )
            logging.info(f'Модель << {name_model} >> выгружена.')
            return end_path
        except Exception:
            error_message = (
                f'<<< Произошла ошибка при выгрузке модели {name_model}'
                ' она не будет выгружена. >>>'
            )
            logging.error(error_message)
            print(error_message)

    @_start_end_load(
        start_message=START_LOAD_MESSAGE_BACKUP,
        end_message=END_LOAD_MESSAGE_BACKUP
    )
    def backup(self) -> str:
        '''Старт бэкапа моделей'''
        json_data = JSON_OBJ.get(key_data=KEY_JSON_FTP)
        if not json_data:
            warning_message = (
                'Бэкап моделей не был запущен. '
                'Причина: Пути для бэкапа моделей не были найдены.'
            )
            logging.warning(warning_message)
            return warning_message

        with Pool(COUNT_PROCESSES) as pool:
            pool.map(self._run_load_in_revit_server, json_data)

    @_start_end_load(
        start_message=START_LOAD_MESSAGE_FTP,
        end_message=END_LOAD_MESSAGE_FTP
    )
    def ftp(self) -> str:
        '''Старт выгрузки на сервер FTP'''
        json_data = JSON_OBJ.get(key_data=KEY_JSON_FTP)
        if not json_data:
            warning_message = (
                'Выгрузка моделей на сервер FTP не была запущена. '
                'Причина: Пути для выгрузки моделей не были найдены.'
            )
            logging.warning(warning_message)
            return warning_message

        with Pool(COUNT_PROCESSES) as pool:
            pool.map(self._run_load_in_revit_server, json_data)
        return JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(KEY_JSON_FTP)

    def _mk_txt_from_rvt(self, path_rvt_file: Path) -> Path:
        '''Формирование txt из rvt файла'''
        name_txt_file: Path = path_rvt_file.name.replace(RVT_EXTENTION, '.txt')
        path_txt_file: Path = path_rvt_file.parent / name_txt_file

        with open(path_txt_file, mode='w', encoding='utf-8') as txt_file:
            logging.info(f'txt файл, создан по пути {path_txt_file}.')
            txt_file.write(str(path_rvt_file))

        return path_txt_file

    def _run_load_nwc(self, path_files: tuple[str, str, str]) -> Path | None:
        '''Старт выгрузки в формат nwc'''
        path_rvt, move_dir_path, rename_name = path_files
        path_rvt: Path = Path(path_rvt)
        move_dir_path: Path = Path(move_dir_path)

        if not all((path_rvt, move_dir_path, rename_name)):
            warning_message = (
                'Переданы неккоректные или пустые данные для'
                ' выгрузки Nawisworks'
            )
            logging.warning(warning_message)
            return None

        copy_dir: Path = PATH_WORKDIR_NAWIS / path_rvt.stem
        copy_dir.mkdir(exist_ok=True)

        path_rvt: Path = Path(shutil.copy2(path_rvt, copy_dir))

        if RVT_EXTENTION not in path_rvt.name:
            except_message = (
                'Возникла ошибка при создании txt файла, в функцифю передан '
                + f'путь {path_rvt}, без расширения {RVT_EXTENTION}.'
            )
            logging.error(except_message, exc_info=True)
            raise ValueError(except_message)

        path_txt: Path = self._mk_txt_from_rvt(path_rvt)
        name_nwf: str = path_rvt.stem + NWF_EXTENTION
        path_nwf: Path = copy_dir / name_nwf
        name_nwc: str = path_rvt.stem + NWC_EXTENTION
        path_nwc: Path = copy_dir / name_nwc

        info_message = 'Запуск утилиты для выгрузки файла ' + path_rvt.name
        logging.info(info_message)

        subprocess.run((
            PATH_NAWIS_FTR, FTR_FIRST_FLAG, path_txt, FTR_SECOND_FLAG,
            path_nwf, FTR_THIRD_FLAG, '2019'
        ))
        rename_nwc: Path = copy_dir / (rename_name + NWC_EXTENTION)
        path_nwc: Path = path_nwc.rename(rename_nwc)

        shutil.copy(rename_nwc, move_dir_path)
        return path_nwc

    def _run_load_nwd(self, nwd_path: Path, nwf_path: Path) -> Path:
        '''Старт выгрузки моделей в формат nwd'''
        subprocess.run((
            PATH_NAWIS_ROAMER, ROAMER_FLAG_NWD, nwd_path, nwf_path
        ))
        name_nwd = nwd_path.name
        debug_message = f'Сформирован nwd файл {name_nwd}'
        logging.debug(debug_message)
        return nwd_path

    @_start_end_load(
        start_message=START_LOAD_MESSAGE_NAWISWORKS,
        end_message=END_LOAD_MESSAGE_NAWISWORKS,
    )
    def nawisworks(self) -> str:
        '''Старт выгрузки моделей в Nawisworks'''
        PATH_WORKDIR_NAWIS.mkdir(exist_ok=True)

        LoadModel(update_json_mode=False, silence_mode=True).ftp()

        nwc_paths = JSON_OBJ.get(key_data=KEY_JSON_NWC)
        nwf_path, nwd_dir = JSON_OBJ.get(key_data=KEY_JSON_NWD)
        nwf_path: Path = Path(nwf_path)
        nwd_dir: Path = Path(nwd_dir)
        name_nwd: str = f'{nwf_path.stem}_{DATE_NOW}{NWD_EXTENTION}'
        nwd_path: Path = nwd_dir / name_nwd

        with Pool(processes=COUNT_PROCESSES) as pool:
            pool.map(self._run_load_nwc, nwc_paths)
        shutil.rmtree(PATH_WORKDIR_NAWIS, ignore_errors=True)

        nwd_path: Path = (
            self._run_load_nwd(nwf_path=nwf_path, nwd_path=nwd_path)
        )
        return str(nwd_path.parent.parent)

    @_start_end_load(
        start_message=START_LOAD_MESSAGE_PUBLISH,
        end_message=END_LOAD_MESSAGE_PUBLISH
    )
    def publish(self) -> str:
        '''Публикация моделей заказчику'''
        pub_dir_path = Path(
            JSON_OBJ.get(KEY_JSON_DIR_PATHS).get(NAME_FIELD_PUBLISH)
        )
        date_now_: str = dt.now().strftime('%y%m%d')
        arch_dir_path: Path = pub_dir_path / f'{date_now_}_{NAME_PROJECT}'
        arch_dir_path.mkdir(exist_ok=True)

        publish_items: list[str] = JSON_OBJ.get(KEY_JSON_PUB)
        for search_path, extention_file in publish_items:
            end_dir_name: str = self.EXTENTIONS[extention_file]
            end_dir_path: Path = arch_dir_path / end_dir_name
            end_dir_path.mkdir(exist_ok=True)

            search_path: Path = Path(search_path)
            files = get_file_from_extention(search_path, extention_file)
            if extention_file == NWD_EXTENTION:
                files = [max(files)]

            pool_items: list[tuple] = [(file, end_dir_path) for file in files]
            with Pool(COUNT_PROCESSES) as pool:
                pool.map(self._copy_file, pool_items)

        zip_archive: Path = make_achive(
            root_dir=pub_dir_path,
            arch_dir_path=arch_dir_path
        )
        shutil.rmtree(arch_dir_path)
        return str(zip_archive.parent)

    def send_message_(self, message: str) -> None:
        '''Отправка сообщения в телеграм боте.'''
        if not self.silence_mode:
            telegram_bot: TgBot = TgBot(TG_TOKEN)
            telegram_bot.send_message(message)
