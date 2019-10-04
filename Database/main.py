#!/usr/bin/env python3

import DatabaseSocket as DBsock
from lang.SQL import queries

# will be added into docker compose???
o_dict = {'traderID':'varchar(255)',
          'platform': 'varchar(255)',
          'instrument': 'varchar(255)',
          'position': 'int',
          'units': 'float',
          'others': 'varchar(255)'}

p_dict = {'traderID':'varchar(255)',
          'platform': 'varchar(255)',
          'instrument': 'varchar(255)'}


dbsock = DBsock.DatabaseSocket(host='localhost', user='mptd_protoDBuser', password='fxprotoDBp19,')
dbsock.connect(db='mptd_master')
q = queries.Query.create_table('Orders', o_dict)
print(q)
dbsock.pass_query(q)
# dbsock.commit()

