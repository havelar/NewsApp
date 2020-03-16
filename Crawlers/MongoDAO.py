from pymongo import MongoClient


class MongoDAO:
    def __init__(self, host, port, dbnm, collection=None):
        self.__port = port
        self.__host = host
        self.__dbnm = dbnm

        self.__cursor = None
        self.__connection = None
        self.collection = collection

    @property
    def host(self):
        return self.__host

    @property
    def dbnm(self):
        return self.__dbnm

    def connect(self):
        self.__connection = MongoClient(self.__host, self.__port)
        self.__cursor = self.__connection[self.__dbnm]
        return self.__cursor

    def disconnect(self):
        self.__connection.close()

        self.__connection = None
        self.__cursor = None

    def __call__(self, collection):
        self.collection = collection
        return self

    def __enter__(self):
        return self.connect()[self.collection]

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


class articleDB(MongoDAO):
    def __init__(self, collection=None):
        super(articleDB, self).__init__(
            'localhost', 27017, 'NewsDB', collection)
