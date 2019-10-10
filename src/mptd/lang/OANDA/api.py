import v20
import os, yaml, logging

DEFAULT_ENV = "V20_CONF"
DEFAULT_PATH = "~/.v20.conf"
DEFAULT_APPLICATION_NAME = "mptd_proto"
api_logger = logging.getLogger(__name__)


class ConfigPathError(Exception):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "Config file '{}' could not be loaded.".format(self.path)


class ConfigValueError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Config is missing value for '{}'.".format(self.value)


class API:
    def __init__(self):

        self.application_name = DEFAULT_APPLICATION_NAME
        self.context, self.streaming_context = None, None
        self.__active_account = None

    def build_context(self, path):
        c = Config(application_name=self.application_name)
        c.load(path=path, validate=True)
        self.active_account = c.active_account
        #
        self.context = c.create_context()
        self.streaming_context = c.create_streaming_context()

    @property
    def active_account(self):
        return self.__active_account

    @active_account.setter
    def active_account(self, acc_id):
        self.__active_account = acc_id


class Config:
    def __init__(self, application_name):
        self.hostname = None
        self.streaming_hostname = None
        self.__port = 443
        self.ssl = True
        self.__token = None
        self.__username = None
        self.__accounts = None
        self.__active_account = None
        self.path = None
        self.datetime_format = 'RFC3339'

        self.application_name = application_name

    def __str__(self):

        s = ""
        s += "hostname: {}\n".format(self.hostname)
        s += "streaming_hostname: {}\n".format(self.streaming_hostname)
        s += "port: {}\n".format(self.__port)
        s += "ssl: {}\n".format(str(self.ssl).lower())
        s += "token: {}\n".format(self.__token)
        s += "username: {}\n".format(self.__username)
        s += "datetime_format: {}\n".format(self.datetime_format)
        s += "accounts:\n"
        for a in self.__accounts:
            s += "- {}\n".format(a)
        s += "active_account: {}".format(self.__active_account)

        return s

    def dump(self, path):

        path = os.path.expanduser(path)
        with open(path, "w") as file:
            print(str(self), file=file)

    def load(self, path, validate=False):

        self.path = path
        api_logger.debug("Load config from {}.".format(os.path.expanduser(path)))
        try:
            with open(os.path.expanduser(path)) as file:
                yml_f = yaml.load(file, Loader=yaml.FullLoader)
                self.hostname = yml_f.get("hostname", self.hostname)
                self.streaming_hostname = yml_f.get("streaming_hostname", self.streaming_hostname)
                self.__port = yml_f.get("port", self.__port)
                self.ssl = yml_f.get("ssl", self.ssl)
                self.__username = yml_f.get("ssl", self.ssl)
                self.__token = yml_f.get("token", self.__token)
                self.__accounts = yml_f.get("accounts", self.__accounts)
                self.__active_account = yml_f.get("active_account", self.__active_account)
                self.datetime_format = yml_f.get("datetime_format", self.datetime_format)
        except:
            raise ConfigPathError(path)

        if validate:
            self.validate()

    def validate(self):
        if self.hostname is None:
            raise ConfigValueError("hostname")
        if self.streaming_hostname is None:
            raise ConfigValueError("hostname")
        if self.__port is None:
            raise ConfigValueError("port")
        if self.ssl is None:
            raise ConfigValueError("ssl")
        if self.__username is None:
            raise ConfigValueError("username")
        if self.__token is None:
            raise ConfigValueError("token")
        if self.__accounts is None:
            raise ConfigValueError("account")
        if self.__active_account is None:
            raise ConfigValueError("account")
        if self.datetime_format is None:
            raise ConfigValueError("datetime_format")

    # TODO implement following methods
    def update_from_input(self):
        raise NotImplementedError

    def create_context(self):
        context = v20.Context(
            hostname=self.hostname,
            port=self.__port,
            ssl=self.ssl,
            application=self.application_name,
            token=self.__token,
            datetime_format=self.datetime_format
        )
        return context

    def create_streaming_context(self):
        context = v20.Context(
            hostname=self.streaming_hostname,
            port=self.__port,
            ssl=self.ssl,
            application=self.application_name,
            token=self.__token,
            datetime_format=self.datetime_format
        )
        return context

    @property
    def active_account(self):
        return str(self.__active_account)


def build_api_instance(path):
    api = API()
    api.build_context(path)
    return api
