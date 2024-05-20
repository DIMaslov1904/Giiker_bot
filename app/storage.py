import asyncio
from datetime import datetime
from threading import Thread
from time import sleep
from types import FunctionType
from typing import TypeVar

from aiogram import Bot

_KT = TypeVar("_KT")


class Storage(dict):
    _thread: Thread
    _storage_time: int
    _function_deleting: FunctionType
    _bot: Bot  # Имеенно для этого проекта

    def __init__(self, *args, **kwargs) -> None:
        """
        Хранилище с авто-очищением через заданное время
        :param args:
        :param storage_time: время в секундах
        :param function_deleting: функция в которую будет передан удалённый элемент отдаёт (key, value)
        :param kwargs:
        """
        self._storage_time = 300
        self._is_running = False
        self._loop = None
        super().__init__(*args, **kwargs)

    def __setitem__(self, key: _KT, value: dict, /) -> None:
        value['del_time'] = int(datetime.now().timestamp()) + self._storage_time
        super().__setitem__(key, value)

    def _delete_item(self, key):
        del_value = self.pop(key)
        if self._function_deleting:
            self._loop.create_task(self._function_deleting(key, del_value, self._bot))

    def _loop_checked(self):
        while True:
            if not self._is_running:
                break
            time_now = int(datetime.now().timestamp())
            timeout = self._storage_time
            if len(self):
                key = next(iter(self))

                if self[key]['del_time'] <= time_now:
                    self._delete_item(key)
                    continue
                else:
                    timeout = self[key]['del_time'] - time_now
            sleep(timeout)

    def setting(self, storage_time: int = 300, function_deleting: FunctionType | None = None,
                bot: Bot | None = None) -> None:
        """
       Установка параметров хранилища с авто-очищением через заданное время.
       :param storage_time: время в секундах
       :param function_deleting: функция в которую будет передан удалённый элемент отдаёт (key, value)
       :param bot: бот
       """
        self._storage_time = storage_time
        self._function_deleting = self._function_deleting or function_deleting
        self._bot = bot

    def start(self):
        """Запуск авто-очищения"""
        self._loop = asyncio.get_event_loop()
        self._is_running = True
        self._thread = Thread(target=self._loop_checked, daemon=True)
        self._thread.start()

    def stop(self):
        """Остановка авто-очищения"""
        self._is_running = False

    def set_function_deleting(self, function_deleting: FunctionType):
        self._function_deleting = function_deleting


storage = Storage()


def set_function_deleting(func: FunctionType) -> FunctionType:
    """Декоратор для функции выполняемой при удалении элемента"""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    storage.set_function_deleting(wrapper)
    return wrapper
