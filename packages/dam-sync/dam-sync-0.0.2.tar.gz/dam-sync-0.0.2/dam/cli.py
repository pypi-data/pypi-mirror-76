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

# build artifacts
cwd = os.getcwd()
build = os.path.join(cwd, 'build')
dist = os.path.join(cwd, 'dist')
egg = os.path.join(cwd, 'dam_sync.egg-info')


@cli.command(name='build')
@click.option('--initial/--normal', default=False)
def build_project(initial=False):
    """ Build release """
    print(yellow('\nBuilding release: v{}'.format(version)))
    print(yellow('-' * 80))

    # package name
    package = 'dam-sync'

    # check version
    if not initial:
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
    print(green('Removing old build'))
    for dir in [build, dist, egg]:
        if os.path.exists(dir):
            shutil.rmtree(dir)
    print('success\n')

    # setuptools
    print(green('Running setup.py clean:'))
    subprocess.run(['python', 'setup.py', 'clean'])
    print()

    print(green('Building distribution:'))
    subprocess.run(['python', 'setup.py', 'sdist'])
    print()

    print(green('Building wheel:'))
    subprocess.run(['python', 'setup.py', 'bdist_wheel', '--python-tag=py3'])
    print()

    print(green('BUILD SUCCESSFUL\n'))


@cli.command(name='publish')
def publish():
    """ Publish release """
    print(yellow('\nPublish release'))
    print(yellow('-' * 80))
    print()
    for dir in [build, dist, egg]:
        if not os.path.exists(dir):
            err = 'Build artifacts missing. Please build distribution first.\n'
            print(red(err))
            return

    print(green('Publishing to PyPI with twine:'))
    subprocess.run(['twine', 'upload', 'dist/*'])
    print()

