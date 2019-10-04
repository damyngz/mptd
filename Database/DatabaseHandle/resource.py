import falcon, yaml, json
from lang.SQL.queries import Query


class BaseResource(object):
    def __init__(self, dbsock, config_path):
        self.dbsock = dbsock

        with open(config_path,'r') as f:
            f_yaml = yaml.load(f, Loader=yaml.FullLoader)
            self.config = f_yaml


class MySQLUserResource(BaseResource):

    def on_post(self, req, resp):

        # TODO currently all similar roles use same account
        # TODO implement separate accounts for different components for security purposes
        try:
            acct_type = req.get_param('acct_type')
            acct_pwd = req.get_param('acct_pwd') or '1234'
            acct_name = self.config[acct_type]['name']
            acct_privileges = self.config[acct_type]['privileges']
            acct_host = self.config[acct_type]['host'] or None

            self.dbsock.pass_query(Query.create_user(user_name=acct_name,
                                                     user_password=acct_pwd,
                                                     user_privileges=acct_privileges,
                                                     user_host=acct_host
                                                     ))

            resp.body = json.dumps('{}_{}@{}'.format(acct_type,
                                                     acct_name,
                                                     acct_host))
            resp.status = falcon.HTTP_200

        except Exception as ex:
            # TODO implement logger
            print(ex)


class PollResource(BaseResource):

    def on_get(self, req, resp, data_type, specifier):
        try:
            list_cols = req.get_param('cols')
            limit = req.get_param('limit') or None

            resp.status = falcon.HTTP_200
            resp.body = self.dbsock.pass_query(Query.select_values(table_name=data_type,
                                                                   list_cols=list_cols,
                                                                   limit=limit))

        except Exception as ex:
            pass


def add_routes(api):

    api.add_route('/account/req',
                  mysqluser_resource)

    api.add_route('/{data_type:str}/{specifier:str}',
                  pollresource)


mysqluser_resource = MySQLUserResource()
pollresource = PollResource()

