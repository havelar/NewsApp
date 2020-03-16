import mysql.connector as connector

class DAO:
    def __init__(self, user, pswd, host, dbnm, to_commit=False):
        self.user = user
        self.pswd = pswd
        self.__host = host
        self.__dbnm = dbnm

        self.__cursor = None
        self.__connection = None
        self.__to_commit = to_commit

    @property
    def host(self):
        return self.__host

    @property
    def dbnm(self):
        return self.__dbnm

    def connect(self):
        self.__connection = connector.connect(host=self.host, database=self.dbnm, user=self.user, password=self.pswd)
        self.__cursor = self.__connection.cursor(buffered=True)
        return self.__cursor

    def disconnect(self, to_commit=False, to_rollback=False):
        if to_commit: self.__connection.commit()
        if to_rollback: self.__connection.rollback()
        self.__cursor.close()
        self.__connection.close()

        self.__connection = None
        self.__cursor = None

    def __call__(self, to_commit=False):
        self.__to_commit = to_commit
        return self

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        to_roll = False
        if exc_type == connector.Error:
            to_roll = True
        
        self.disconnect(
            to_commit = self.__to_commit,
            to_rollback = to_roll
        )

class autoConnect(DAO):
    def __init__(self, to_commit=False):
        super(autoConnect, self).__init__(
            user='henrique',
            pswd='pass',
            host='localhost',
            dbnm='Links',
            to_commit=to_commit
        )