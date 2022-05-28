from monitor.storage.base import BaseStorage


class MemoryStorage(BaseStorage):

    def __init__(self):
        super().__init__()
        self.data = {}

    def get(self, _id):
        return self.data.get(_id)

    def set(self, _id, value):
        self.data[_id] = value

    def list_all(self):
        return self.data

    def is_empty(self):
        if self.data:
            return False
        else:
            return True
