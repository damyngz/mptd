"""
package for holding sql query wrappers
"""

import os, yaml, logging
from .args import DEFAULT_PRIVILEGE_LIST

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InvalidQueryError(Exception):
    pass


class Query:

    @staticmethod
    def select_values(
                      table_name,
                      list_cols=None,
                      limit=None):

        # limit can be tuple, int, or specific str (eg. top 500, bot 500)
        # TODO implement extended 'limit' param functionality

        if list_cols is None:
            cols = '*'
        elif isinstance(list, list_cols):
            cols = ''
            for col in list_cols:
                cols += col + ', '
            cols.strip().strip(',')
        elif isinstance(str, list_cols):
            cols = list_cols
        else:
            raise InvalidQueryError('Invalid list_cols passed. Must be list, str or None')

        outp = 'select {} from {}'.format(cols, table_name)
        if limit and (isinstance(tuple, limit) or isinstance(int, limit)):
            limit_s = 'limit {}'.format(limit)
        else:
            raise InvalidQueryError('Invalid limit passed. Must be tuple (of ints) or int.')

        return outp + ';'

    @staticmethod
    def insert_value(values, table_name):
        def get_type(t, val):
            print(t, t.lower() in ['char(255)','varchar(255)','time','datetime','timestamp'])
            if t.lower() in ['char(255)','varchar(255)','time','datetime','timestamp']:
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

        try:
            try:
                if attr_file:
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
                if len(list(v)) > 1:
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

        user_s = 'create user \'{user_name}\'@\'{user_host}\' \
        identified with native_mysql_password by {user_passwd};'.format(
            user_name=user_name,
            user_host=user_host,
            user_passwd=user_password
        )

        # TODO implement privilege validation

        if not isinstance(dict, p):
            raise InvalidQueryError("user_privileges must be a dict. \
                                    {tables: [list_privileges]}")

        privilege_s = ''
        for tables in list(user_privileges):
            privilege_s_ = 'grant '
            if not isinstance(list, user_privileges[tables]):
                raise InvalidQueryError("{} is not a list.".format(user_privileges[tables]))

            for p in user_privileges[tables]:
                if p.upper() in DEFAULT_PRIVILEGE_LIST:
                    privilege_s_ += '{}, '.format(p)
                else:
                    # TODO raise warning or Error for invalid privilege passed
                    pass

            privilege_s_.strip().strip(',')
            privilege_s_ += ' on {} to {};'.format(tables, user_name)
            privilege_s += privilege_s_

        return user_s + privilege_s


