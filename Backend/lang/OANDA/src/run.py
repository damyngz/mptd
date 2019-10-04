#!/usr/bin/env python3
import sys
sys.path.append('../../../../Database')
import api
import action
import v20

from DatabaseSocket import DatabaseSocket
from lang.SQL.queries import Query
#from Database.lang.SQL.queries import Query

t_dict={
    'instrument': 'varchar(255)',
    'date_time': 'datetime',
    'ms': 'int',
    'bid': 'double',
    'ask': 'double'
}

c_dict = {
    'instrument': {'dtype': 'varchar(255)', 'args': ['not null']},
    'date_time': {'dtype': 'datetime', 'args': ['not null']},
    'open': {'dtype': 'double', 'args': ['not null']},
    'low': {'dtype': 'double', 'args': ['not null']},
    'high': {'dtype': 'double', 'args': ['not null']},
    'close': {'dtype': 'double', 'args': ['not null']},
    'volume': {'dtype': 'int', 'args': ['not null']},
    'granularity': {'dtype': 'varchar(255)', 'args': ['not null']},
    'tick': {'dtype': 'bigint', 'args': ['not null']}
}


#  docker run -d -v /home/ubuntu/db:/var/lib/mysql --env="MYSQL_ROOT_PASSWORD=1234" mysql
# mysql -u root -h 172.17.0.2 -P 3306 -p
def main():
    api_ = api.build_api_instance('~/fxproj/cfg/.v20.conf')
    dbsock = DatabaseSocket(host='172.17.0.2', user='root', password='1234', port='3306')
    dbsock.connect(db='mptd_test')
    dbsock.pass_query(Query.create_table('oanda_instrument_candles', c_dict, method='graceful'))
    # action.stream.instrument_candle_poll(api=api_,
    #                                      instrument='EUR_USD')

    # a = action.stream.instrument_candle_stream(api=api_,
    #                                            instruments=['EUR_USD','EUR_JPY'],
    #                                            include_time=True)

    while True:
        try:
            a = action.stream.instrument_candle_poll(api=api_,
                                                     instrument='EUR_USD',
                                                     granularity='S5',
                                                     tick_label=True)
            for i in a:
                print(i)
                dbsock.pass_query(Query.insert_value(i, table_name='oanda_instrument_candles'), v=True)
        except v20.errors.V20Timeout:
            pass

        # dbsock.pass_query(Query.insert_value([{'instrument': i[0],
        #                                        'date_time': i[-1].split('.')[0],
        #                                        'ms': i[-1].split('.')[1],
        #                                        'bid': i[1],
        #                                        'ask': i[2]}], table_name='oanda_instrument_pricing'))




if __name__ == "__main__":
    main()
