"""
Defines DatabaseSocket class
; connects to a mysql database

"""
import sys, logging, traceback
import mysql.connector
from ..lang.SQL.queries import InvalidQueryError

log_fmt = '%(levelname)s\t: %(filename)s\t:%(lineno)d\t:%(funcName)s\t:%(message)s'
logging.basicConfig(format=log_fmt, level=logging.WARNING)
logger = logging.getLogger(__name__)


class IncompleteAuthError(Exception):
    pass


# class NotConnectedError(Exception):
#     pass


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

    # TODO redo and stabilise check_connection method
    def __check_connection(self, correct=False):
        pass

# try:
#     if self.cursor is None:
#         if correct:
#             if self.db is None:
#                 raise NotConnectedError
#             self.cursor = self.db.cursor()
#     else:
#         raise NotConnectedError
#
# except NotConnectedError as err:
#     logger.error("{}: DatabaseSocket for {dbsock_user}@{dbsock_host} has no active connection.".format(type(err).__name__,
#                                                                                                        dbsock_user=self.user,
#                                                                                                        dbsock_host=self.host))

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

    def disconnect(self):
        self.cursor = None
        self.db.disconnect()

    def pass_query(self, q, return_result=False):

        def __execute_and_commit(q_str, print_traceback=self.verbose):
            try:
                self.cursor.execute(q_str)
                if not q_str.lower().startswith('select'):
                    self.db.commit()
                return 1

            except InvalidQueryError:
                print('{}: Invalid query passed.'.format(type(InvalidQueryError.__name__)))

            except:
                err_log = sys.exc_info()
                if print_traceback:
                    traceback.print_tb(err_log[-1])
                if self.verbose:
                    logger.error("{err_type} -> {err_msg}".format(err_type=err_log[0].__name__,
                                                                  err_msg=err_log[1]))
                return 0
        # self.__check_connection()
        # if v is None:
        #     v = self.verbose
        if q is None:
            return

        # TODO validate query strings?
        # TODO need more elegant way to decide db.commit() or not
        count_pass = 0
        if isinstance(q, str):
            count_pass = __execute_and_commit(q)
            num_queries = 1
        elif isinstance(q, list):
            num_queries = 0
            for q_ in q:
                if isinstance(q_, str):
                    # redacted log
                    if self.verbose:
                        logger.debug('passing query of {} chars'.format(len(q_)))
                        logger.debug('query->{}'.format(q_))
                    count_pass += __execute_and_commit(q_)
                    num_queries += 1
                else:
                    logger.warning("q_ is not str, q_ is {} type".format(type(q_).__name__))

        else:
            num_queries = 0

        logging.info("{}/{} queries successful. ({:5f}%)".format(count_pass,
                                                                 num_queries,
                                                                 100 * (count_pass/num_queries)))

            # self.db.commit()



        if return_result is True:
            output = []
            columns = tuple([col_tuple[0] for col_tuple in self.cursor.description])
            output.append(columns)

            result = self.cursor.fetchall()
            for line in result:
                output.append(line)

            logging.info('query returned {} results'.format(len(output)-1))
            if self.verbose:
                logging.info(output)
            return output

    def pulse(self, db, query):
        logger.debug('pulse query -> {}'.format(query))
        try:
            self.connect(db=db)
            self.pass_query(query)
            self.disconnect()

        except:
            err_log = sys.exc_info()
            # TODO create separate logger for tracebacks?
            # logger.error(traceback.print_tb(sys.exc_info()[-1]))
            logger.error('Error during DBsock pulse:{}:{}'.format(err_log[0].__name__,
                                                                  err_log[1]))


