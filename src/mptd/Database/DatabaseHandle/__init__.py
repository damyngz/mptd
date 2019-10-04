from DatabaseSocket import DatabaseSocket
from resource import *
import falcon


class DatabaseHandle:

    def __init__(self,
                 db_user,
                 db_host,
                 db_password,
                 db_port=None,
                 db_name=None):

        self.dbsock = DatabaseSocket(user=db_user,
                                     host=db_host,
                                     password=db_password,
                                     port=db_port)

        self.dbsock.connect(db=db_name)

        self.api = falcon.API()

    def run(self):
        while True:
            pass




