from datetime import datetime

import click
import logging

from fefu_admission.university import UniversityInformationPrinter
from fefu_admission.fefu import Fefu
from fefu_admission.settings import Settings

fefu = Fefu(Settings.list_of_departments)

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    print_settings()


@cli.command("load", help="Load data from website and save to ./data/")
def load():
    global fefu
    fefu.load_from_web_all()
    fefu.serialization.save_data_to_file_all()


@cli.command("show_total_information", help="Get statistics of the competitive situation")
@click.option('--date', default=None, required=False)
def show_total_information(date):
    global fefu
    if date is not None:
        date_list = [int(item) for item in date.split('.')]
        d = datetime.today().replace(year=date_list[0], month=date_list[1], day=date_list[2])
        fefu.serialization.load_from_file_all(d)
    else:
        fefu.serialization.load_from_file_all()
    fefu.processing_all_departments()
    UniversityInformationPrinter(fefu).print_info()


@cli.command("show_list", help="Show list of any department")
@click.option('--index', default=0, prompt='Index of department', help='Index of department')
@click.option('--agreement', is_flag=True)
@click.option('--date', default=None, required=False)
def show_list(index, agreement, date):
    global fefu
    if date is not None:
        date_list = [int(item) for item in date.split('.')]
        d = datetime.today().replace(year=date_list[0], month=date_list[1], day=date_list[2])
        fefu.serialization.load_from_file_all(d)
    else:
        fefu.serialization.load_from_file_all()
    UniversityInformationPrinter(fefu).print_list_of_department(int(index), agreement)


def print_settings():
    print("Your settings: ")
    print("\t", Settings.me)
    for index, dep in enumerate(Settings.list_of_departments):
        print("\t", str(index) + ")", dep)


if __name__ == '__main__':
    cli()
