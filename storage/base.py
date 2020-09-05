class BaseStorage():

    def __init__(self, config):
        self.config = config
        pass

    def get(self, _id):
        pass

    def set(self, _id, value):
        pass

    def list_all(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__}({self.config})"

    def __repr__(self):
        return self.__str__()
