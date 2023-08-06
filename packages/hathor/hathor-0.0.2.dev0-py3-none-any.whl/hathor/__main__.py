import click

from hathor.project.builders.modular import build_modular


@click.group()
def cli():
    pass


@cli.command()
def build():
    from hathor.project.information.project import find_projects

    projects = find_projects()
    for project in projects:
        build_modular(project)


if __name__ == '__main__':
    cli()
