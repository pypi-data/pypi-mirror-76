#!/usr/bin/env python3
import click
import os
import yaml
from dam.colors import *
import subprocess
from pprint import pprint as pp

# -----------------------------------------------------------------------------
# Group setup
# -----------------------------------------------------------------------------


@click.group(help=yellow('DAM-Sync utility'))
def cli():
    pass


# -----------------------------------------------------------------------------
# Commands
# -----------------------------------------------------------------------------

config_dir = os.path.expanduser('~/.dam-sync')
config_path = os.path.join(config_dir, 'config.yml')


def get_config():
    """
    Returns current config for your environment
    """
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    if not os.path.isfile(config_path):
        return None

    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)

    return config


@cli.command(name='configure')
@click.option(
    '--source',
    default=None,
    prompt=True,
    help='Local library path to backup'
)
@click.option(
    '--destination',
    default=None,
    prompt=True,
    help='Target local path to backup to'
)
@click.option(
    '--s3-bucket',
    default=None,
    prompt=True,
    help='AWS S3 bucket name. Can also contain name/path.'
)
@click.option(
    '--aws-profile',
    default='default',
    prompt=True,
    help='AWS CLI profile to use for authentication'
)
def configure(source, destination, s3_bucket, aws_profile):
    """ Configure sync"""
    print(green('\nConfiguring DAM-Sync!'))
    print(green('-' * 80))
    print()

    # check config
    config = get_config()
    if config:
        print(red('Found configuration at "{}" '.format(config_path)))
        if not click.confirm(red('Do you want to continue and overwrite it?')):
            print(cyan('Skipping...\n'))
            return

    # check source
    if not os.path.isdir(source):
        print(red('Backup source "{}" doesn\'t exist\n'.format(source)))
        return

    # check destination
    if not os.path.isdir(destination):
        err = 'Backup destination "{}" doesn\'t exist. If it\'s an external '
        err += 'volume - check that t\'s mounted.\n'
        print(red(err.format(destination)))
        return

    # write config
    with open(config_path, 'w') as file:
        config = dict(
            source=source,
            destination=destination,
            s3_bucket=s3_bucket,
            aws_profile=aws_profile,
            exclude=[
                '.DS_Store',
                '*.DS_Store',
            ]
        )
        yaml.dump(config, file, default_flow_style=False, sort_keys=False)

    # report success
    print(green('\nSuccessfully written config to "{}"\n'.format(config_path)))
    return


@cli.command(name='run')
@click.option('--disk/--skip-disk', default=False)
@click.option('--cloud/--skip-cloud', default=False)
def run(disk, cloud):
    """ Backup your assets """
    print(yellow('\nBacking up your assets'))
    print(yellow('-' * 80))
    print()

    """
    Collect options
    """

    sync_disk = False
    sync_cloud = False

    # by default sync all (no flags)
    if not disk and not cloud:
        sync_disk = True
        sync_cloud = True

    # sync all if both flags (weird, but ok)
    if disk and cloud:
        sync_disk = True
        sync_cloud = True

    # just sync disk
    if disk and not cloud:
        sync_disk = True
        sync_cloud = False

    # or just sync cloud
    if cloud and not disk:
        sync_disk = False
        sync_cloud = True

    """
    Do the sync
    """
    config = get_config()

    excludes = config['exclude'] + [
        '*.lrdata',
        '*.lrdata/*',
        '*.lrcat.zip',
        '*.lock',
        '*.lock',
        '*.lrcat-wal',
        '*.DS_Store',
        '*/Lightroom/Backups/*',
    ]

    # sync disk
    if sync_disk:
        cmd = [
            'rsync',
            '-vhrt',
            config['source'],
            config['destination'],
            '--delete',
        ]

        for x in excludes:
            cmd.append('--exclude={}'.format(x))

        print(green('Synchronizing to local storage:'))
        subprocess.run(cmd)
        print()

    # sync cloud
    if sync_cloud:
        cmd = [
            'aws',
            '--profile={}'.format(config['aws_profile']),
            's3',
            'sync',
            config['source'],
            's3://{}'.format(config['s3_bucket']),
            '--delete'
        ]

        for x in excludes:
            cmd.append('--exclude={}'.format(x))

        print(green('Synchronizing to S3:'))
        print('building file list...')
        subprocess.run(cmd)

    print(green('\nAll done. Your data is safe now. Good job :)\n'))
    return

