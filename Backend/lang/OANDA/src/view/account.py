import sys
from tabulate import tabulate

DEFAULT_TITLE_DELINEATE = "="
DEFAULT_SUBTITLE_DELINEATE = "-"


def _print_delineator(s, fill):
    print(s)
    print(len(s)*fill)
    print()


def _print_subtitle(s, lineator=DEFAULT_SUBTITLE_DELINEATE):
    _print_delineator(s, lineator)


def _print_title(s, lineator=DEFAULT_TITLE_DELINEATE):
    _print_delineator(s, lineator)


def print_entity(entity, title=None):
    if title is not None and len(title) > 0:
        _print_title(title)

    headers = []
    table_format = 'rst'
    body = []

    for field in entity.fields():
        name = field.displayName
        value = field.value

        if field.typeClass.startswith("array"):
            value = "[{}]".format(len(field.value))
        elif field.typeClass.startswith("object"):
            value = "<{}>".format(field.typeName)

        body.append([name,value])

    getattr(sys.stdout, 'buffer', sys.stdout).write(
        tabulate
        (
            tabular_data=body,
            headers=headers,
            tablefmt=table_format
        ).encode('utf-8')
    )
    print()


# TODO print_collection
def print_collection(title, entities, columns):
    raise NotImplementedError


# TODO test stability
def print_response_entity(
        response,
        expected_status,
        title,
        transaction_name
    ):

    try:
        transaction = response.get(transaction_name, expected_status)
        print_entity(transaction, title=title)
        print()

    except:
        pass

