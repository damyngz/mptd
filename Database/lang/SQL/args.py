"""
wrapper for prvilege and role granting
"""


class InvalidPrivilegeError(Exception):
    def __init__(self, p):
        self.p = p

    def __str__(self):
        return "{} is not a valid MySQL privilege. Check syntax or vocab.".format(self.p)


class Privilege:
    """
    wrapper for granting and revoking privileges
    """
    def __init__(self, action, items):
        self.action = action
        self.items = items

    def _str(self):
        return '{} ON {}'.format(self.action, self.items)

    def grant(self, name):
        return 'GRANT {} TO {};'.format(self._str(), name)

    def revoke(self, name):
        return 'REVOKE {} TO {};'.format(self._str(), name)

    def validate(self):
        try:
            if self.action not in DEFAULT_PRIVILEGE_LIST:
                raise InvalidPrivilegeError(self.action)
        except InvalidPrivilegeError as e:
            print(e)


DEFAULT_PRIVILEGE_LIST = ["ALL",
                          "ALTER",
                          "ALTER_ROUTINE",
                          "CREATE",
                          "CREATE ROLE",
                          "CREATE ROUTINE",
                          "CREATE TABLESPACE",
                          "CREATE TEMPORARY TABLE",
                          "CREATE USER",
                          "CREATE VIEW",
                          "DELETE",
                          "DROP",
                          "DROP_ROLE",
                          "EVENT",
                          "EXECUTE",
                          "FILE",
                          "GRANT OPTION",
                          "INDEX",
                          "INSERT",
                          "LOCK TABLES",
                          "PROCESS",
                          "PROXY",
                          "REFERENCES",
                          "RELOAD",
                          "REPLICATION CLIENT",
                          "REPLICATION SLAVE",
                          "SELECT",
                          "SHOW DATABASES",
                          "SHOW VIEW",
                          "SHUTDOWN",
                          "SUPER",
                          "TRIGGER",
                          "UPDATE",
                          "USAGE"]


# DEFAULT_PRIVILEGE_DICT = {}
# for p in DEFAULT_PRIVILEGE_LIST:
#     DEFAULT_PRIVILEGE_LIST[p] = p.replace(" ", "_")

