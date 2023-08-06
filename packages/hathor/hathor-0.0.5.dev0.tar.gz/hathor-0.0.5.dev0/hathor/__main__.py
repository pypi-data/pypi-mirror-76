import os
from pathlib import Path

import click
import requests
import yaml
from click_spinner import spinner

from hathor import resources
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


@cli.command()
def init():
    project_file = Path("hathor.project.yml").absolute()

    if project_file.exists():
        if not click.confirm("The project file will be overwritten if you continue, proceed?"):
            return

    project = {
        "name": click.prompt("Project name"),
        "metadata": {
            "author": click.prompt("Author"),
            "author_email": click.prompt("Author email")
        },
        "build": {
            "directory": click.prompt("Build directory", "./build")
        },
        "serve": {
            "host": "127.0.01",
            "port": 8080,
        },
        "sources": {
            click.prompt("Default source path", "./src"): {
                "enabled": True
            }
        }
    }

    while click.confirm("Add more sources?"):
        project["sources"][click.prompt("Source directory")] = {
            "enabled": True
        }

    with project_file.open("w+") as fp:
        yaml.dump(project, fp, yaml.Dumper, sort_keys=False)

    for source_dir in project["sources"].keys():
        if not source_dir.strip():
            continue

        path = Path(source_dir).absolute()
        os.makedirs(path, exist_ok=True)

    gitignore_path = project_file.parent.joinpath(".gitignore")

    if click.confirm("Add a .gitignore file? This uses the gitignore.io service"):
        ignore_categories = [
            "lua",
            "windows",
            "linux",
            "macos",
            "archive"
        ]

        if click.confirm("Add ignores for IntelliJ?"):
            ignore_categories.append("intellij+all")

        if click.confirm("Add ignores for VSCode?"):
            ignore_categories.append("code")

        click.echo("Downloading gitignore")
        query_string = ",".join(ignore_categories)
        with spinner():
            response = requests.get(f"https://www.toptal.com/developers/gitignore/api/{query_string}")
            if response.status_code > 299:
                click.echo("Gitignore download failed, it will not be appended to the file")
                click.echo(f"{response.request.url}\n{response.status_code} {response.reason}:\n{response.text}")
                response = None

        with gitignore_path.open("w+") as fp:
            fp.write(resources.gitignore_base())

            if response is not None:
                fp.write(response.text)

        click.echo("Gitignore written")

    editorconfig_path = project_file.parent.joinpath(".editorconfig")

    if click.confirm("Add a .editorconfig file?"):
        editorconfig = resources.editorconfig_template({
            "charset": click.prompt("Charset", "utf-8"),
            "end_of_line": click.prompt("End of line", "lf"),
            "indent_size": click.prompt("Indent size", "4"),
            "indent_style": click.prompt("Indent style", "tab"),
            "insert_final_newline": "true" if click.confirm("Insert final newline", True) else "false",
            "max_line_length": click.prompt("Maximum line length", "80"),
            "tab_width": click.prompt("Tab width", "4")
        })

        with editorconfig_path.open("w+") as fp:
            fp.write(editorconfig + "\n")

        click.echo("Editorconfig written")


@cli.command()
def serve():
    from hathor.serve import app
    from hathor.project.information.project import find_projects

    projects = find_projects()
    assert len(projects), f"Only one project can be served at a time, found {len(projects)}"

    app.run(projects[0])


if __name__ == '__main__':
    cli()
