"""
Defines DatabaseSocket class
; connects to a mysql database

"""
import logging
import mysql.connector
from lang.SQL.queries import Query, InvalidQueryError


log_fmt = '%(levelname)s\t: %(filename)s\t:%(lineno)d\t:%(funcName)s\t:%(message)s'
logging.basicConfig(format=log_fmt, level=logging.WARNING)
logger = logging.getLogger(__name__)


class IncompleteAuthError(Exception):
    pass


class NotConnectedError(Exception):
    pass


class DatabaseSocket:
    def __init__(self, **kwargs):
        req_args = ['host', 'user', 'password']

        self.db, self.cursor, self.verbose = None, None, False
        try:
            for arg in req_args:
                if arg not in kwargs:
                    raise IncompleteAuthError

            self.host = kwargs['host']
            self.user = kwargs['user']
            self.__password = kwargs['password']

        except IncompleteAuthError as err:
            missing_args = []
            for key in ['host', 'user', 'password']:
                if key not in kwargs.keys():
                    missing_args.append(key)

            logger.error("{}: Incomplete population of database information. Missing: {}\n".format(type(err).__name__,
                                                                                            str(missing_args).strip('[]')))
        if 'port' in kwargs:
            self.port = kwargs['port']

    def __check_connection(self):
        try:
            if self.cursor is None:
                raise NotConnectedError
        except NotConnectedError as err:
            print("{}: DatabaseSocket for {dbsock_user}@{dbsock_host} has no active connection.".format(type(err).__name__,
                                                                                                        dbsock_user=self.user,
                                                                                                        dbsock_host=self.host))

    def set_verbosity(self, v):
        if isinstance(v, bool):
            self.verbose = v
        else:
            logger.warning('v is a {}, not a bool. verbosity not changed.'.format(type(v).__name__))

    def commit(self):
        self.db.commit()

    def connect(self, db=None):
        if db is None:
            logging.warning("connect {db_user}@{db_host} No db set. May cause future errors".format(db_user=self.user,
                                                                                                    db_host=self.host))

        if self.port:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.__password,
                port=self.port,
                database=db
            )
        else:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.__password,
                database=db
            )

        self.cursor = self.db.cursor()
        pass

    def disconnect(self):
        self.cursor = None
        self.db.disconnect()

    def pass_query(self, q, v=None):
        self.__check_connection()
        if v is None:
            v = self.verbose
        if q is None:
            return
        # if v is True:
        #     print(q)
        try:
            # TODO validate query strings
            # if isinstance(q, Query):
            self.cursor.execute(q)
            self.db.commit()
            # else:
            #     raise InvalidQueryError
        except InvalidQueryError:
            print('{}: Invalid query passed.'.format(type(InvalidQueryError.__name__)))

        if v is True:
            for line in self.cursor:
                logger.info(line)
                print(line)
