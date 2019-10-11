import socket, sys, traceback, yaml, json


def get_host_address():
    return socket.gethostbyname(socket.gethostname())


class BaseResourceConfigError(Exception):
    def __init__(self, e):
        self.err_log = e

    def __str__(self):
        if isinstance(self.err_log, tuple):
            err_type = self.err_log[0].__name__
            err_msg = self.err_log[1]
            return 'An error occured while loading BaseResource config.({}:{})'.format(err_type, err_msg)
        elif isinstance(self.err_log, str):
            return self.err_log
        else:
            return 'Unexpected YAMLConfigError: {}'.format(self.err_log)

    def get_traceback(self):
        traceback.print_tb(self.err_log[-1])


class BaseResource(object):
    def __init__(self, service_name, **kwargs):
        __supported_args = ['dbsock',
                            'config']

        self.service = service_name
        self.host = get_host_address()

        if 'dbsock' in kwargs:
            self.dbsock = kwargs['dbsock']

        if 'config_path' in kwargs:
            if kwargs['config_path'].startswith('.yaml', -5):
                config_path = kwargs['config_path']
                try:
                    with open(config_path, 'r') as f:
                        f_dict = yaml.load(f, Loader=yaml.FullLoader)
                        self.config = f_dict

                except:
                    raise BaseResourceConfigError(sys.exc_info())

            elif kwargs['config_path'].startswith('.json', -5):
                config_path = kwargs['config_path']
                try:
                    with open(config_path, 'r') as f:
                        f_dict = json.load(f)
                        self.config = f_dict
                except:
                    raise BaseResourceConfigError(sys.exc_info())

            else:
                raise BaseResourceConfigError('config path {} is not a .yml file'.format(kwargs['config_path']))
