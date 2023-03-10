from pickle import dump, load

from monitor.exceptions import FileNameInputError
from monitor.ext import LOG
from monitor.storage.base import BaseStorage
from settings import CACHE_FILE_DIR


class JsonFile(BaseStorage):
    def __init__(self):
        super().__init__()

    def get(self, _id):
        return self.data.get(_id)

    def set(self, _id, value):
        self.data[_id] = value

    def list_all(self):
        return self.data

    def save(self, *args, **kwargs):
        file_name = CACHE_FILE_DIR.joinpath(kwargs.get("task_hash")) if kwargs.get("task_hash") else None
        if not file_name:
            raise FileNameInputError()
        with open(file_name, "wb") as f:
            dump(self.data, f)
        LOG.info(f"持久化成功, {file_name}")

    def read(self, *args, **kwargs):
        file_name = CACHE_FILE_DIR.joinpath(kwargs.get("task_hash")) if kwargs.get("task_hash") else None
        if not file_name:
            raise FileNameInputError()
        if not file_name.exists():
            self.data = {}
        else:
            with open(file_name, "rb") as f:
                self.data = load(f)

    def is_empty(self):
        if self.data:
            return False
        else:
            return True
