from rich.console import Console
from rich.table import Table


def pprint_table(data: 'list[dict]'):
    """
    Given a list of dicts, print as Rich table.
    """
    console = Console()

    table = Table(show_header=True, header_style="#FFF000")
    for k in data[0].keys():
        table.add_column(k)

    for d in data:
        table.add_row(
            *[str(v) for _, v in d.items()]
        )

    console.print(table)
