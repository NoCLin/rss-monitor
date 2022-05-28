# -*- coding: utf-8 -*-
# @Time    : 2022/5/28 13:31
# @Author  : Mrli
# @File    : factory.py
from enum import Enum
from typing import Union

from monitor.storage.jfile import JsonFile
from monitor.storage.memory import MemoryStorage


class FactoryEnum(Enum):
    Memory = "memory"
    JsonFile = "json_file"


class StorageFactory:
    @staticmethod
    def create_storage(typ: Union[str, FactoryEnum]):
        """工厂"""
        if isinstance(typ, FactoryEnum):
            typ = typ.value

        s = {
            FactoryEnum.Memory.value: MemoryStorage,
            FactoryEnum.JsonFile.value: JsonFile
        }.get(typ)()
        return s
