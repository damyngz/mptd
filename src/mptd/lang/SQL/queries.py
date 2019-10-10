"""
package for holding sql query wrappers
"""
import os, yaml, logging
from re import sub
from .args import DEFAULT_PRIVILEGE_LIST

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InvalidQueryError(Exception):
    pass


class QueryError:
    # _errors = [Error, DatabaseError, IntegrityError]

    def __init__(self, sql_error):

        # TODO typechecking for SQL errors? <circular imports, DatabaseSocket>
        # if True in [isinstance(sql_error, err) for err in self._errors]:
        #
        #     self.err_type = 'unexpected error <{}>'.format(type(sql_error).__name__)
        #     self.err_msg = '{}'.format(sql_error.__str__())
        # else:
        self.err_type = type(sql_error).__name__
        self.err_msg = sql_error.__str__()

    def __str__(self):
        return '{} : {}'.format(self.err_type, self.err_msg)


class Select:
    @staticmethod
    def select_candles():
        pass

    @staticmethod
    def select():
        pass


class Query:

    # TODO rethink need for query method for select
    # @staticmethod
    # def select_values(table_name,
    #                   list_cols=None,
    #                   limit=None,
    #                   order=None,
    #                   group=None):
    #
    #     #
    #     # list_cols, list of columns to return in query
    #     if list_cols is None:
    #         cols = '*'
    #     elif isinstance(list_cols, list):
    #         cols = ''
    #         for col in list_cols:
    #             cols += col + ', '
    #         cols.strip().strip(',')
    #     elif isinstance(list_cols, str):
    #         cols = list_cols
    #     else:
    #         raise InvalidQueryError('Invalid list_cols passed. Must be list, str or None')
    #
    #     #
    #     # limit number of queries returned
    #     outp = 'select {} from {}'.format(cols, table_name)
    #     if limit and (isinstance(limit, tuple) or isinstance(limit, int)):
    #         limit_s = 'limit {}'.format(sub(r"[()]", '', str(limit)))
    #     else:
    #         raise InvalidQueryError('Invalid limit passed. Must be tuple (of ints) or int.')
    #
    #     #
    #     # order by parameters eg. {'param(s)': 'asc'}
    #     return outp + ';'

    @staticmethod
    def insert_value(values, table_name):
        def get_type(t, val):
            print(t, t.lower() in ['char(255)', 'varchar(255)', 'time', 'datetime', 'timestamp'])
            if t.lower() in ['char(255)', 'varchar(255)', 'time', 'datetime', 'timestamp']:
                print('\'' + str(val) + '\'')
                return '\'' + str(val) + '\''
            return str(val)

        """
        :param table_name:
        :param values:
        :return: string in sql
        """

        if not values:
            return None

        outp, col_s = '', ''
        cols = []
        for col in values[0].keys():
            cols.append(col)

        for col in cols:
            col_s += col + ', '

        col_s = col_s.strip().strip(',')
        s = "insert into {t_name} ({column_string}) values ".format(t_name=table_name,
                                                                    column_string=col_s, )
        vals_s = ''
        for value in values:
            val_s = ''
            for col in cols:
                if isinstance(value[col], str):
                    val_s += '\'' + value[col] + '\'' + ', '
                else:
                    val_s += str(value[col]) + ', '

            val_s = val_s.strip().strip(',')
            vals_s += '({}),'.format(val_s)

        vals_s = vals_s.strip(',')
        outp = s + vals_s
        return outp + ';'

    @staticmethod
    def create_table(name, attr_dict, attr_file=None, **kwargs):
        """
        eg attr_dict
        {columns:{{'x': {'dtype':'int'},
                  'id': {'dtype': 'int', 'args':['not null', 'auto increment']},
                  'primary key': {'struct':['x', 'id']{
                  }

         }

         kwargs:
            mode: returns query for method of creating table
                accepted parameters:
                (str)
                'graceful': creates a table if none exists
                'force':    forces a new table, will override old table
                'safe' TODO

        :param name: name of table;
        :param attr_dict: dict() of column names to dtype (in str);
        :param attr_file: file path to a .yml file with appropriate scheme for the table, overrides attr_dict if defined;
        :param kwargs:
            primary_key;
        :return: string in sql syntax for creating a table;
        """
        # TODO stabilize the functionality of file loading table creation
        # TODO add checks for primary key declaration syntax?

        class InvalidTableSchemeError(Exception):
            pass

        if attr_file is not None:
            try:
                try:
                    if not os.path.isfile(attr_file):
                        raise FileNotFoundError

                    else:
                        try:
                            yml_file = open(attr_file, 'r')
                            attr_dict = yaml.load(yml_file)
                        except yaml.YAMLError as err:
                            logging.error(err)

                except FileNotFoundError as err:
                    logging.error('{}: {} is not a valid path.'.format(type(err).__name__, attr_file))

                if not(isinstance(attr_dict, dict)):
                    raise InvalidTableSchemeError
                else:
                    # TODO add multiple primary key declaration checks?
                    for k, v in attr_dict.items():
                        if 'dtpye' not in v and k != 'primary key':
                            raise InvalidTableSchemeError
                        if not(isinstance(k, str)) or not(isinstance(v, dict)):
                            raise InvalidTableSchemeError

            except InvalidTableSchemeError as err:
                logging.error('{}: Invalid datatype or values, values must be in dicts.'.format(type(err).__name__))

        outp = 'create table {} ('.format(name)
        for k, v in attr_dict.items():
            p_str = ''

            if k != 'primary key':
                # TODO error checking for additional args
                if len(list(v)) > 1 and 'args' in v and len(v['args']) > 1:
                    for param in v['args']:
                        p_str += '{} '.format(param)

                outp += '{} {} {},'.format(k, v['dtype'], p_str.strip())

            # TODO change to else if no other params to add
            elif k == 'primary key':
                outp += '{} ('.format(k)
                for col in v['struct']:
                    outp += '{}, '.format(col)
                outp.strip().strip(',')
                outp += ') '
        # kwargs optional arguments
        # if ("primary_key" in kwargs and kwargs['primary_key'] is not None) or \
        #         False:
        #     outp += 'primary key ({}),'.format(kwargs['primary_key'])

        # removes last ','
        outp = outp[:-1] + ')'
        if "method" in kwargs:
            if kwargs['method'].lower() == 'graceful':
                outp = outp.replace('create table', 'create table if not exists')
            elif kwargs['method'].lower() == 'force':
                outp = 'drop table {} if exists;'.format(name) + outp

        return outp + ';'

    @staticmethod
    def create_user(user_name,
                    user_password,
                    user_privileges,
                    user_host=None):

        """
        # TODO creates user if it dosen't exist, might create problems with namespace clash
        :param user_name:
        :param user_password:
        :param user_privileges:
        :param user_host:
        :return:
        """

        user_s = 'create user if not exists \'{user_name}\'@\'{user_host}\' \
identified with mysql_native_password by \'{user_passwd}\';'.format(
            user_name=user_name,
            user_host=user_host,
            user_passwd=user_password
        )

        # TODO implement privilege validation

        if not isinstance(user_privileges, dict):
            raise InvalidQueryError("user_privileges must be a dict. \
                                    {tables: [list_privileges]}")

        privilege_s = ''
        for tables in list(user_privileges):
            privilege_s_ = 'grant '
            if not isinstance(user_privileges[tables], list):
                raise InvalidQueryError("{} is not a list.".format(user_privileges[tables]))

            for p in user_privileges[tables]:
                if p.upper() in DEFAULT_PRIVILEGE_LIST:
                    privilege_s_ += '{}, '.format(p)
                else:
                    raise InvalidQueryError('{} is not a valid sql privilege'.format(p))

            privilege_s_ = privilege_s_.strip().strip(',')
            privilege_s_ += ' on {} to \'{}\'@\'{}\';'.format(tables, user_name, user_host)
            privilege_s += privilege_s_

        return [user_s, privilege_s]


