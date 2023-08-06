import os

import click


@click.command()
@click.option("--format-code", "-f", is_flag=True, help="Auto format the code.")
@click.option("--inplace", "-i", is_flag=True, help="Make changes in place")
@click.option(
    "--exclude-path", "-e", default="", help="Exclude some path from processing"
)
@click.option("--lint", "-l", is_flag=True, help="Lint the code")
def worker(format_code, inplace, exclude_path, lint):
    if format_code:
        click.echo(f"Formatting code... \nInplace -> {inplace}")
        run_commands("format", inplace, exclude_path)
    elif lint:
        click.echo("Running lint...")
        run_commands("linter", inplace=False, exclude_path=exclude_path)


def run_commands(name, inplace, exclude_path=""):
    click.echo("Running auto-flake... ")
    os.system(
        f"autoflake -r {'--in-place' if inplace else ''} "
        "--remove-unused-variables --remove-all-unused-imports "
        f"{'--exclude ' + exclude_path if exclude_path else ''} "
    )

    click.echo("Running isort...")
    os.system(
        "isort . --multi-line 3 --trailing-comma --line-width 88 "
        f"{'--skip ' + exclude_path if exclude_path else ''} "
        f"{'--check-only' if not inplace else ''} "
    )

    click.echo("Running black...")
    os.system(
        f"black **/*.py "
        f"{'--exclude ' + exclude_path if exclude_path else ''} "
        f"{'--check' if not inplace else ''}"
    )

    if name == "linter":
        click.echo("Running mypy...")
        os.system("mypy **/*.py --ignore-missing-imports")

        click.echo("Running flake8...")
        os.system("flake8 .")


def main():
    worker()


if __name__ == "__main__":
    main()
