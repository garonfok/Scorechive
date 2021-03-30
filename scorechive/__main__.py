import click
import scripts
import sys
import warnings

from _version import __version__
from pathlib import Path

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return '%s: %s: %s: %s\n' % (filename, lineno, category.__name__, message)

warnings.formatwarning = warning_on_one_line


@click.group()
def cli():
    pass


@cli.command("create", help="Create a database.")
@click.argument("database_name", type=click.Path(exists=True), nargs=1)
def create_db(database_name):
    validate_db_exists(database_name,True)
    validate_db_extension(database_name)

    main.create_db(database_name)


@cli.command("view", help="View all scores.")
@click.argument("database_name", type=click.Path(exists=False), nargs=1)
@click.option("--part", help="View parts in a score.", is_flag=True)
@click.option(
    "--instrumentation", help="View instrumentation of a score.", is_flag=True
)
@click.option(
    "--dates", help="View all dates that a score was performed.", is_flag=True
)
def view_score(database_name, part, instrumentation, dates):
    validate_db_exists(database_name)

    main.view_score(database_name, part, instrumentation, dates)


@cli.command("add", help="Add a score.")
@click.argument("database_name", type=click.Path(exists=False), nargs=1)
def add_score(database_name):
    validate_db_exists(database_name)

    main.add_score(database_name)


@cli.command("insert", help="Insert instrumentation to a score.")
@click.argument("database_name", type=click.Path(exists=False), nargs=1)
def insert_parts(database_name):
    validate_db_exists(database_name)

    main.insert_parts(database_name)

@cli.command("delete", help="Delete a score.")
@click.argument("database_name", type=click.Path(exists=False), nargs=1)
def delete_score(database_name):
    validate_db_exists(database_name)

    main.delete_score(database_name)

@cli.command("version", help="Show version number.")
def show_version():
    print(__version__)


# Check if database_name is valid
def validate_db_exists(database_name,existing = False):
    if not existing:
        if not Path(database_name).is_file():
            raise OSError(f"{database_name} does not exist.")
    else:
        if Path(database_name).is_file():
            raise OSError(f"{database_name} already exists.")

# Checks if database_name has a file extension
def validate_db_extension(database_name):
    if len(database_name.split(".")) == 1:
        warnings.warn("No file extension dectected.", SyntaxWarning)
        while True:
            continue_input = input("Are you sure you want to continue? (y/n) ")
            if continue_input == "y":
                break
            elif continue_input == "n":
                sys.exit()


# runs on initialization
if __name__ == "__main__":
    cli()
