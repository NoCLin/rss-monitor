from .base import BaseStorage


class MemoryStorage(BaseStorage):

    def __init__(self, config):
        super().__init__(config)
        self.data = {}

    def get(self, _id):
        return self.data.get(_id)

    def set(self, _id, value):
        self.data[_id] = value

    def list_all(self):
        return self.data
