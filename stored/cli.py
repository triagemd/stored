import click
import stored


@click.group()
def cli():
    pass


@cli.command(help='Sync from an input to output')
@click.argument('input')
@click.argument('output')
@click.option('--force-unpack', is_flag=True)
def sync(input, output, force_unpack):
    click.echo('Syncing %s to %s...' % (input, output))
    stored.sync(input, output, force_unpack=force_unpack)


@cli.command(help='List files in target storage URL')
@click.argument('target')
def list(target):
    for file in stored.list_files(target):
        click.echo(file)
