# -*- coding: utf-8 -*-
import click
from poetry_optional_cython import fib


@click.command()
def cli():
    click.echo("Hello Poetry with optional cython extension")
    click.echo("Calculating fib(36)")
    click.echo(f"{fib.fib(36)}")


if __name__ == '__main__':
    cli()
