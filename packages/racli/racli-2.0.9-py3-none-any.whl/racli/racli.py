import click

from .logic import run_clone, run_submit, run_instance

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

@cli.command()
def instance():
    run_instance()