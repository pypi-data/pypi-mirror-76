from fefu_admission.settings import *

from threading import Thread
import datetime
import logging
import os
from shutil import copyfile
from enum import Enum
from typing import Dict, List, Any, Union

from colorama import Back, Fore, Style
from tabulate import tabulate


class Enrollee:

    def __init__(self, name, points, agreement):
        self.name = name
        self.points = points
        self.agreement = agreement

    def get_name(self):
        return self.name

    def get_agreement(self):
        return self.agreement

    def get_points_sum(self):
        return sum([int(x) for x in self.points])

    @staticmethod
    def parse_from_csv_line(line):
        """
        Parses a string like: Second_name First_name Middle_name,72,83,85,0,False

        :param line:
        :return: Enrollee
        """
        line_split: List[str] = line.split(",")
        name = line_split[0]
        points = [int(line_split[i]) for i in range(1, len(line_split) - 1)]
        agreement = line_split[len(line_split) - 1].replace("\n", "").replace(" ", "") == "True"
        enrollee = Enrollee(name, points, agreement)
        return enrollee

    def __str__(self):
        string = self.name + ","
        for item in self.points:
            string += str(item)
            string += ","
        string += str(self.agreement)
        return string

    def __lt__(self, other):
        first = self.get_points_sum()
        seconds = other.get_points_sum()
        if first < seconds:
            return False
        if first > seconds:
            return True
        for i in range(0, len(self.points) - 1):
            if self.points[i] < other.points[i]:
                return False
            elif self.points[i] == other.points[i]:
                continue
            else:
                return True
        return False

    def __eq__(self, other):
        return self.name == other.name

    # May be here bug
    def __hash__(self):
        return hash(self.name)


class TypeOfCompletion(Enum):
    Budget = "На общих основаниях"
    SpecialQuota = 'Особая квота'
    TargetQuota = "Целевая квота"
    Contract = "Договор"

    @staticmethod
    def get_through_value(type_of_completion):
        item: Union[type, Any]
        for item in TypeOfCompletion:
            if item.value == type_of_completion:
                return item

        return None


class ApplicantsHolderBase:

    def __init__(self):
        self.applicants = {
            TypeOfCompletion.Budget: [],
            TypeOfCompletion.SpecialQuota: [],
            TypeOfCompletion.TargetQuota: [],
            TypeOfCompletion.Contract: [],
        }
        self.applicants_with_agreement = {
            TypeOfCompletion.Budget: [],
            TypeOfCompletion.SpecialQuota: [],
            TypeOfCompletion.TargetQuota: [],
            TypeOfCompletion.Contract: [],
        }
        self.places = {
            TypeOfCompletion.Budget: 0,
            TypeOfCompletion.SpecialQuota: 0,
            TypeOfCompletion.TargetQuota: 0,
            TypeOfCompletion.Contract: 0,
        }

    def get_fixed_budget_places(self):
        return self.places[TypeOfCompletion.Budget]

    def get_budget_places_for_now(self):
        """
        If a special quota, contract places are not occupied, then they will be added to the budget.
        Just returns the budget places at the moment.

        :return: budget_places: int
        """
        budget_places = self.get_fixed_budget_places()

        for type_of_completion in TypeOfCompletion:
            if type_of_completion == TypeOfCompletion.Budget:
                continue

            if self.places[type_of_completion] > len(self.applicants_with_agreement[type_of_completion]):
                budget_places += self.places[type_of_completion] - len(
                    self.applicants_with_agreement[type_of_completion])

        return budget_places

    def get_budget_places_for_now_of_the_first_round(self):
        return int(self.get_budget_places_for_now() * .8)

    def get_list_with_me(self, type_of_completion, agreement=False):
        if agreement:
            applicants_set = set(self.applicants_with_agreement[type_of_completion])
        else:
            applicants_set = set(self.applicants[type_of_completion])
        me = Enrollee.parse_from_csv_line(Settings.me)
        applicants_set.add(me)
        applicants_list = sorted(list(applicants_set))
        return applicants_list

    def get_list_with_me_without_high_scores(self, type_of_completion, agreement, high_scores):
        applicants_list = self.get_list_with_me(type_of_completion, agreement)
        applicants_list_new = []
        for enrollee in applicants_list[::-1]:
            if enrollee.get_points_sum() > high_scores:
                break
            applicants_list_new.append(enrollee)

        return applicants_list_new[::-1]

    def get_position_of_me(self, type_of_completion, agreement=False):
        return self.__get_position_of_me(self.get_list_with_me(type_of_completion=type_of_completion,
                                                               agreement=agreement))

    def get_position_of_me_without_high_scores(self, type_of_completion, agreement, high_scores):
        return self.__get_position_of_me(self.get_list_with_me_without_high_scores(type_of_completion, agreement,
                                                                                   high_scores))

    @staticmethod
    def __get_position_of_me(list_enrolle):
        me = Enrollee.parse_from_csv_line(Settings.me)
        return list_enrolle.index(me) + 1

    def get_len_applicants(self, type_of_completion=None, agreement=False):
        total = 0
        if type_of_completion is not None:
            if agreement:
                total += len(self.applicants_with_agreement[type_of_completion])
            else:
                total += len(self.applicants[type_of_completion])
        else:
            for type_of_completion_for in TypeOfCompletion:
                if agreement:
                    total += len(self.applicants_with_agreement[type_of_completion_for])
                else:
                    total += len(self.applicants[type_of_completion_for])
        return total


class Department(ApplicantsHolderBase):
    applicants: Dict[TypeOfCompletion, List[Enrollee]]
    NAME_UNIVERSITY = ""

    def __init__(self, n):
        super().__init__()
        self.name = n
        self.serialization = DepartmentSerialization(self)

    def get_places(self):
        return self.places

    def get_html_table(self):
        """
        Get html page with a table with information of applicants
        :return: html_text: str
        """
        pass

    def load_from_web(self):
        """
        Calls a method serialization.get_html_table() and parses the table data, adding applicants to the lists
        :return: None
        """
        pass

    def add_enrollee(self, type_of_competition, enrollee):
        self.applicants[type_of_competition].append(enrollee)

    def add_enrollee_with_agreement(self, type_of_competition, enrollee):
        self.applicants_with_agreement[type_of_competition].append(enrollee)

    def search_enrollee_in_list(self, type_of_completion, name):
        return self.__search_enrollee_in_list(self.applicants[type_of_completion], name)

    def search_enrollee_in_list_with_agreement(self, type_of_completion, name):
        return self.__search_enrollee_in_list(self.applicants_with_agreement[type_of_completion],
                                              name)

    @staticmethod
    def __search_enrollee_in_list(list_enrollee, name):
        for enrolle in list_enrollee:
            if enrolle.name == name:
                return enrolle

        return None

    def __str__(self):
        return self.name


class DepartmentSerialization:

    def __init__(self, department):
        self.department = department

    def load_data_from_file(self, d=None):
        """
        Parse local files by adding applicants to the lists. Call this method only if local files exist
        :return: None
        """
        file = self.get_path_to_data_file(d)
        try:
            type_of_competition = TypeOfCompletion.SpecialQuota
            for line in open(file, 'r'):
                if len(line.split(",")) == 2:
                    type_of_competition_str = line.split(",")[0]
                    type_of_competition = TypeOfCompletion.get_through_value(type_of_competition_str)
                    if type_of_competition is None:
                        assert False
                    places = int(line.split(",")[1])
                    self.department.places[type_of_competition] = places
                else:
                    enrollee = Enrollee.parse_from_csv_line(line)
                    if enrollee.agreement:
                        self.department.add_enrollee_with_agreement(type_of_competition, enrollee)
                    self.department.add_enrollee(type_of_competition, enrollee)
        except FileNotFoundError:
            print("File not founded: ", file)

    def save_data_to_file(self):
        # Record data for work as actual
        self.create_data_folder_if_is_not_exist()
        file_current_data = open(self.get_path_to_data_file(), 'w')

        for type_of_completion in TypeOfCompletion:
            file_current_data.write(type_of_completion.value + "," +
                                    str(self.department.places[type_of_completion]) + "\n")
            for enrollee in self.department.applicants[type_of_completion]:
                file_current_data.write(str(enrollee) + " \n")

        file_current_data.close()

        # Copy data to work as with archived
        current_date = datetime.date.today()
        self.create_data_folder_if_is_not_exist(current_date)
        copyfile(self.get_path_to_data_file(), self.get_path_to_data_file(current_date))

    def create_data_folder_if_is_not_exist(self, d=None):
        dir_path = self.get_path_to_data_dir(d)
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        except OSError:
            print('Error: Creating directory. {}'.format(dir_path))

    def get_path_to_data_dir(self, d=None):
        if d is not None:
            return os.path.join("~", ".fefu_admission", "data", str(d.year), str(d.month), str(d.day),
                                self.department.NAME_UNIVERSITY, self.department.name + ".csv")
        return os.path.join("~", ".fefu_admission", "data", self.department.NAME_UNIVERSITY,
                            "{}.{}".format(self.department.name, "csv"))

    def get_path_to_data_file(self, d=None):
        return os.path.join(self.get_path_to_data_dir(d), "{}.{}".format(self.department.name, ".csv"))


class DepartmentLoadFromWebThread(Thread):
    """
    To asynchronously download data from the web
    """

    def __init__(self, dep):
        Thread.__init__(self)
        self.department = dep
        self.name = "Thread: {}".format(dep.name)

    def run(self):
        self.department.load_from_web()


class University(ApplicantsHolderBase):

    def __init__(self):
        super().__init__()
        self.name = ""
        self.departments = []
        self.serialization = UniversitySerialization(self)

    def load_from_web_all(self):
        thread_list = []

        for department in self.departments:
            thread_list.append(DepartmentLoadFromWebThread(department))

        for thread in thread_list:
            thread.start()
        for thread in thread_list:
            thread.join()
        logging.info("Done")

    def processing_all_departments(self):
        for type_of_completion in TypeOfCompletion:
            applicants_set = set()
            applicants_set_with_agreement = set()
            places = 0
            for department in self.departments:
                for enrolle in department.applicants[type_of_completion]:
                    applicants_set.add(enrolle)
                    if enrolle.agreement:
                        applicants_set_with_agreement.add(enrolle)
                places += department.places[type_of_completion]

            self.applicants[type_of_completion] = sorted(list(applicants_set))
            self.applicants_with_agreement[type_of_completion] = sorted(list(applicants_set_with_agreement))
            self.places[type_of_completion] = places


class UniversitySerialization:

    def __init__(self, university):
        self.university = university

    def load_from_file_all(self, d=None):
        for department in self.university.departments:
            department.serialization.load_data_from_file(d)

    def save_data_to_file_all(self):

        for department in self.university.departments:
            department.serialization.save_data_to_file()


class ApplicantsHolderInformationPrinter:

    def __init__(self, applicants_holder):
        self.applicants_holder = applicants_holder

    def print_info(self):
        rows_list = [
            ["Всего подало", self.applicants_holder.get_len_applicants()],
            ["Бюджетников подало", self.applicants_holder.get_len_applicants(
                type_of_completion=TypeOfCompletion.Budget)],
            ["Бюджетные места на данный момент", self.applicants_holder.get_budget_places_for_now()],
            ["Мое место среди бюджетников", self.applicants_holder.get_position_of_me(TypeOfCompletion.Budget)],
            ["Мое место среди бюджетников без высокобальников[250]",
             self.applicants_holder.get_position_of_me_without_high_scores(
                 type_of_completion=TypeOfCompletion.Budget, agreement=False, high_scores=250)],
            ["Подало согласие", self.applicants_holder.get_len_applicants(agreement=True)],
            ["Подало согласие(На общий основаниях)", self.applicants_holder.get_len_applicants(
                type_of_completion=TypeOfCompletion.Budget, agreement=True)],
            ["Мое место среди бюджетинков, подавших солгасие",
             self.applicants_holder.get_position_of_me(type_of_completion=TypeOfCompletion.Budget, agreement=True)]
        ]
        print(tabulate(rows_list, tablefmt='fancy_grid'))


class UniversityInformationPrinter(ApplicantsHolderInformationPrinter):

    def __init__(self, applicants_holder):
        super().__init__(applicants_holder)

    def get_list_of_department(self, index, with_agreement=False):
        rows_list = []
        dep = self.applicants_holder.departments[index]
        for type_of_completion in [TypeOfCompletion.SpecialQuota,
                                   TypeOfCompletion.TargetQuota,
                                   TypeOfCompletion.Budget]:
            if with_agreement:
                list_applicants = dep.applicants_with_agreement[type_of_completion]
            else:
                list_applicants = dep.applicants[type_of_completion]

            for index_of_enrollee, enrollee in enumerate(list_applicants):
                me = Enrollee.parse_from_csv_line(Settings.me)
                if me < enrollee:
                    break
                applied_for_another_dep = None
                another_dep = None
                for index_of_department, item in enumerate(self.applicants_holder.departments):
                    if index == index_of_department:
                        continue
                    applied_for_another_dep = item.search_enrollee_in_list_with_agreement(
                        type_of_completion, enrollee.name) is not None
                    if applied_for_another_dep:
                        another_dep = item
                        break
                style_start = ""
                note = ""
                if applied_for_another_dep:
                    style_start = Back.RED + Fore.BLACK
                    note = "Подал на {}".format(another_dep.name)
                elif enrollee.get_agreement():
                    style_start = Back.GREEN + Fore.BLACK
                    note = "Подал на это направление"

                rows_list.append([index_of_enrollee + 1, "{}{}{}".format(style_start, enrollee.name, Style.RESET_ALL),
                                  *enrollee.points, enrollee.get_points_sum(), note])

        return rows_list

    def print_list_of_department(self, index, with_agreement=False):
        dep = self.applicants_holder.departments[index]
        ApplicantsHolderInformationPrinter(dep).print_info()
        print(tabulate(self.get_list_of_department(index, with_agreement), tablefmt='fancy_grid'))
