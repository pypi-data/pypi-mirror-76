import click

from .logic import clone, submit

@click.group()
def cli():
    pass

@cli.command()
@click.argument('api_url', required=True)
def clone(api_url):
    run_clone(api_url)

@cli.command()
@click.argument('flag', required=True)
def submit(flag):
    run_submit(flag)