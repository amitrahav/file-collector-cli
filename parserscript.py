from pyfiglet import Figlet
from csv import reader, DictWriter, DictReader
from pathlib import Path
from datetime import datetime
import fileinput
import shutil

import click
from typing import List

COLORS_BY_STAGE = ['blue', 'green', 'yellow', 'red']
FIELDS_NAMES = ['String query', 'Found file', 'Copied location']


def file_copier(index_file_path: str, output_folder: str) -> None:
    click.secho(f'Copying files into {output_folder}', fg=COLORS_BY_STAGE[2])
    with fileinput.input(files=index_file_path, inplace=True, mode='r') as f:
        content = DictReader(f)
        headers = content.fieldnames
        print(",".join(headers))  # print back the headers
        for row in content:
            file_origin_path = Path(row['Found file'])
            file_destination_path = Path(output_folder, file_origin_path.name)
            shutil.copyfile(file_origin_path, file_destination_path)
            row['Copied location'] = str(file_destination_path)
            print(",".join(list(row.values())))  # print back the headers
        f.close()


def file_finder(file_index: int, overall_files: int, file_contains: str, search_folder: str) -> List[str]:
    click.secho(f'{file_index} of {overall_files}: ', fg=COLORS_BY_STAGE[1], nl=False)
    click.secho(f'Indexing files including {file_contains} inside {str(search_folder)}', blink=True)
    return [str(path) for path in Path(search_folder).rglob(f"*{file_contains}*.*")]


def write_files_to_csv(searched_string: str, found_files: List[str], container_folder: str) -> str:
    sum_path = Path(container_folder, 'summary.csv')
    if sum_path.exists():
        click.secho(f'Creating index file in {str(sum_path)}', fg=COLORS_BY_STAGE[1])

    else:
        click.secho(f'Adding indexes to index file at {str(sum_path)}', fg=COLORS_BY_STAGE[1])

    rows_dict = [
        {'String query': searched_string, 'Found file': file_path, 'Copied location': ''}
        for file_path in found_files
    ]
    with open(str(sum_path), 'w', newline='') as summary:
        file = DictWriter(summary, fieldnames=['String query', 'Found file', 'Copied location'])
        file.writeheader()
        file.writerows(rows_dict)
        summary.close()

    return str(sum_path)


def output_folder_creator(output_folder: str) -> str:
    suffix = f"covid-parser-{datetime.today().strftime('%Y-%m-%d')}"
    today_folders = len(list(Path(output_folder).glob(f'*{suffix}/')))
    if today_folders > 0:
        container_folder = Path(output_folder, f"({today_folders})-{suffix}/")
    else:
        container_folder = Path(output_folder, f"{suffix}/")
    click.secho(f'Creating output folder at path {container_folder}', fg=COLORS_BY_STAGE[0], blink=True)
    container_folder.mkdir()

    return str(container_folder)


@click.command()
def cli():
    """Example script."""
    f = Figlet(font='slant')
    click.echo(f.renderText('Files Collector'))

    # Step 1 - csv info
    click.secho('STEP 1', bold=True, underline=True, fg=COLORS_BY_STAGE[0], nl=False)
    click.secho('   ', nl=False)
    click.secho('CSV information', bg=COLORS_BY_STAGE[0])

    csv = click.prompt('Please enter a readable csv file that includes all file names', type=click.File('r'),
                       default=open("/Users/amitrahav/Downloads/new_user_credentials.csv", "r"))
    without_header = click.prompt('Should ignore csv first line (got header)?', type=click.Choice(['Y', 'N']),
                                  default='Y')
    without_header = without_header is 'Y'

    # Step 2 - files location
    click.secho('STEP 2', bold=True, underline=True, fg=COLORS_BY_STAGE[1], nl=False)
    click.secho('   ', nl=False)
    click.secho('Files location', bg=COLORS_BY_STAGE[1])
    search_folder = click.prompt('Please enter an existing folder to search files in',
                                 type=click.Path(dir_okay=True, writable=False, file_okay=False, allow_dash=True))

    # Step 3 - files location
    click.secho('STEP 3', bold=True, underline=True, fg=COLORS_BY_STAGE[2], nl=False)
    click.secho('   ', nl=False)
    click.secho('Output information', bg=COLORS_BY_STAGE[2])
    output_folder = click.prompt('Please enter an existing folder destination for copying all found files',
                                 type=click.Path(dir_okay=True, writable=False, file_okay=False, allow_dash=True))

    # Step 4 - files location
    click.secho('STEP 4', bold=True, underline=True, fg=COLORS_BY_STAGE[3], nl=False)
    click.secho('   ', nl=False)
    click.secho('Style', bg=COLORS_BY_STAGE[2])
    safe = click.prompt('1 - Safe and slow\n2 - Fast and dirty',
                        type=click.Choice(['1', '2']),
                        default='1')
    safe = safe is '1'

    # Starting to do the magic

    container_folder = output_folder_creator(output_folder)

    csv_reader = reader(csv)
    csv_rows = list(csv_reader)
    csv_rows_num = len(csv_rows)

    if not safe:
        for row in csv_rows:
            click.echo(row[0])
            for filename in file_finder(0, 0, row[0], search_folder):
                click.echo(filename)
                if Path(filename).is_file():
                    shutil.copy(Path(filename), Path(container_folder))
        click.secho('DONE', bold=True, underline=True, bg=COLORS_BY_STAGE[3])

    else:
        index_file_path = None
        for row_index, row in enumerate(csv_rows):
            if without_header and row_index == 0:
                continue
            if not without_header:
                row_index = row_index + 1
            files_found = file_finder(row_index, csv_rows_num, row[0], search_folder)
            index_file_path = write_files_to_csv(row[0], files_found, container_folder)
        file_copier(index_file_path, container_folder)
        click.secho('DONE', bold=True, underline=True, bg=COLORS_BY_STAGE[3])

