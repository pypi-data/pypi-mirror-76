import click
import os
import shutil
import sys
import subprocess
import requests
from pprint import pprint as pp

from dam.colors import *
from dam.version import version

# -----------------------------------------------------------------------------
# Group setup
# -----------------------------------------------------------------------------


@click.group(help=yellow('DAM-Sync developer console'))
def cli():
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

@cli.command(name='build')
def build():
    """ Build release """
    print(yellow('\nBuilding release: v{}'.format(version)))
    print(yellow('-' * 80))

    # check version
    package = 'dam-sync'
    package = 'shiftboiler'
    resp = requests.get('https://pypi.org/pypi/{}/json'.format(package))
    if resp.status_code == 404:
        print(red('Package "{}" does not exist on PyPI\n'.format(package)))
        return

    info = resp.json()
    latest = info['info']['version']
    all = list(info['releases'].keys())
    all.append(latest)
    releases = [release.lstrip('v') for release in all]
    if version in releases:
        err = 'Package "{}" already has a version "{}" published to PyPI.\n'
        print(red(err.format(package, version)))
        return




    # cleanup
    cwd = os.getcwd()
    build = os.path.join(cwd, 'build')
    dist = os.path.join(cwd, 'dist')
    egg = os.path.join(cwd, 'dist')
    print(green('Cleanup: OK'))


    # setuptools




@cli.command(name='publish')
def publish():
    """ Publish release """
    print(green('\nPublish release'))
    print(green('-' * 80))
    print()
