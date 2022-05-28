class BaseStorage:

    def __init__(self):
        pass

    def get(self, _id):
        pass

    def set(self, _id, value):
        pass

    def list_all(self):
        pass

    def is_empty(self):
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        """持久化"""
        pass

    def read(self, *args, **kwargs):
        """读取"""
        pass
