import asyncio

import click

from .utils import CONTEXT_SETTINGS
from ..utils import handle_credentials


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-s", "--server", help="Coiled server to use")
@click.option("-t", "--token", help="Coiled user token")
def login(server, token):
    """ Configure your Coiled account credentials
    """
    try:
        asyncio.get_event_loop().run_until_complete(
            handle_credentials(server=server, token=token, save=True)
        )
        print(
            '\nNext: see the "Run your first computation" guide at ... \n'
            "https://docs.coiled.io/getting_started.html#run-your-first-computation"
        )
    except ImportError as e:
        print(e)
