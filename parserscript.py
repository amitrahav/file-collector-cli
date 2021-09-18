from pyfiglet import Figlet
from csv import reader
from pathlib import Path
from datetime import datetime

import click
from typing import List

COLORS_BY_STAGE=['blue', 'green', 'yellow']


def file_copier(file_path: str, output_folder: str) -> bool:
    return True


def file_finder(file_index:int, overall_files:int, file_contains: str, search_folder: str) -> List[str]:
    click.secho(f'{file_index} of {overall_files}: ', fg=COLORS_BY_STAGE[1], nl=False)
    click.secho(f'Indexing files including {file_contains} inside {str(search_folder)}', blink=True)
    return [str(path) for path in sorted(Path(search_folder).rglob("*py*"))]


def output_folder_creator(output_folder: str) -> str:
    sofix = f"covid-parser-{datetime.today().strftime('%Y-%m-%d')}"
    todays_folders = len(list(Path(output_folder).glob(f'*{sofix}/')))
    if todays_folders > 0:
        container_folder = Path(output_folder, f"({todays_folders})-{sofix}/")
    else:
        container_folder = Path(output_folder, f"{sofix}/")
    click.secho(f'Creating output folder at path {container_folder}', fg=COLORS_BY_STAGE[0], blink=True)
    container_folder.mkdir()

    return str(container_folder)


@click.command()
def cli():
    """Example script."""
    f = Figlet(font='slant')
    click.echo(f.renderText('COVID Helper'))

    # Step 1 - csv info
    click.secho('STEP 1', bold=True, underline=True, fg=COLORS_BY_STAGE[0], nl=False)
    click.secho('   ',  nl=False)
    click.secho('CSV information', bg=COLORS_BY_STAGE[0])

    csv = click.prompt('Please enter a readable csv file that includes all file names', type=click.File('r'),
                       default=open("/Users/amitrahav/Downloads/new_user_credentials.csv", "r"))
    with_header = click.prompt('Should ignore csv first line (got header)?', type=click.BOOL, default=True)

    # Step 2 - files location
    click.secho('STEP 2', bold=True, underline=True, fg=COLORS_BY_STAGE[1], nl=False)
    click.secho('   ',  nl=False)
    click.secho('Files location', bg=COLORS_BY_STAGE[1])
    search_folder = click.prompt('Please enter an existing folder to search files in',
                                 type=click.Path(dir_okay=True, writable=False, file_okay=False, allow_dash=True),
                                 default="/Users/amitrahav/Downloads/")

    # Step 3 - files location
    click.secho('STEP 3', bold=True, underline=True, fg=COLORS_BY_STAGE[2], nl=False)
    click.secho('   ',  nl=False)
    click.secho('Output information', bg=COLORS_BY_STAGE[2])
    output_folder = click.prompt('Please enter an existing folder destination for copying all found files',
                                 type=click.Path(dir_okay=True, writable=False, file_okay=False, allow_dash=True),
                                 default="/Users/amitrahav/Downloads/")

    container_folder = output_folder_creator(output_folder)
    csv_reader = reader(csv)
    csv_rows = list(csv_reader)
    csv_rows_num = len(csv_rows)

    for row_index, row in enumerate(csv_rows):
        if bool(with_header) and row_index == 0:
            continue

        output = file_finder(row_index, csv_rows_num, row[0], "/Users/amitrahav/Projects/")
        for file in output:
            click.echo(file)

