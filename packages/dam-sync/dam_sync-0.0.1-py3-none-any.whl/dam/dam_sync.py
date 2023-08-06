#!/usr/bin/env python3
import click
from dam.colors import *

# -----------------------------------------------------------------------------
# Group setup
# -----------------------------------------------------------------------------


@click.group(help=yellow('DAM-Sync utility'))
def cli():
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

@cli.command(name='run')
def run():
    """ Backup your assets """
    print(green('\nHello from DAM-Sync!'))
    print(green('-' * 80))
    print()
