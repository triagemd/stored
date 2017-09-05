import click

from .sync import sync
from .list_files import list_files


@click.group()
def cli():
    pass


@cli.command(help='Sync from an input to output')
@click.argument('input')
@click.argument('output')
def sync(input, output):
    click.echo('Synching...')
    sync(input, output)


@cli.command(help='List files in target storage URL')
@click.argument('target')
def list(target):
    for file in list_files(target):
        click.echo(file)
