import json, logging
from src.mptd.lang.SQL import Query

logger = logging.getLogger(__name__)


def load_schema(fp, return_query_string=False, method='graceful'):
    try:
        with open(fp) as f:
            f_dict = json.load(f)
    except FileNotFoundError as err:
        # TODO implement logging
        logger.error(err)

    if return_query_string:
        return Query.create_table(name=f_dict['name'],
                                  attr_dict=f_dict['columns'],
                                  method=method)

    return f_dict
