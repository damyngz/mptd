import os, yaml
from .args import Privilege, InvalidPrivilegeError


class InvalidRoleError(Exception):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "{} is not a valid file. No roles config found here.".format(self.path)


class MySQLRole:
    """
    wrapper for MySQL roles, used by DB superuser
    """
    def __init__(self, name=None, roles_path=None):
        self.name = name
        self.privileges = []
        self.roles_path = roles_path

    def load(self):
        path = os.path.expanduser(self.roles_path)
        try:
            if not os.path.isfile(path):
                raise InvalidRoleError
            with open(path) as file:
                yml_file = yaml.load(file)
                self.name = yml_file.get("name", self.name)
                privilege_list = yml_file.get("privileges", [])
                for k, v in privilege_list.items():
                    self.privileges.append(Privilege(k, v))

        except InvalidRoleError as e:
            print(e)

    # ------------------------------------------------------------------------------------------------------
    def create_role(self, cursor):
        # TODO setup methods for setting up all roles in container
        cursor.execute("CREATE ROLE {};".format(self.name))
        for privilege in self.privileges:
            cursor.execute(privilege.grant(self.name))

    def grant_role(self, cursor, name, addr):
        # TODO use private key to authenticate role

        cursor.execute("GRANT {role_name} TO \'{user_name}\'@\'{user_addr}\';".format(role_name=self.name,
                                                                                      user_name=name,
                                                                                      user_addr=addr))

    def revoke_role(self, cursor, name, addr):
        cursor.execute("REVOKE {role_name} TO \'{user_name}\'@\'{user_addr}\';".format(role_name=self.name,
                                                                                       user_name=name,
                                                                                       user_addr=addr))



