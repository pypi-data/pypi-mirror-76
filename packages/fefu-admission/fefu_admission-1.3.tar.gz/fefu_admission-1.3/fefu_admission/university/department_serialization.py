from fefu_admission.university.enrollee import Enrollee
from fefu_admission.university.type_of_completion import TypeOfCompletion

import json
import os
from shutil import copyfile
import datetime


class DepartmentSerialization:

    def __init__(self, department):
        self.department = department

    def load_data_from_file(self, d=None):
        """
        Parse local files by adding applicants to the lists. Call this method only if local files exist
        :return: None
        """
        with open(self.get_path_to_data_file(d), "r") as file_json:
            data_from_jsom = json.load(file_json)
            for type_of_completion_json in data_from_jsom["type_of_completion"]:
                type_of_completion = TypeOfCompletion.get_through_value(type_of_completion_json["name"])
                self.department.places[type_of_completion] = type_of_completion_json["places"]
                for enrollee_json in type_of_completion_json["list"]:
                    enrollee = Enrollee.get_from_json(enrollee_json)
                    self.department.applicants[type_of_completion].append(enrollee)
                    if enrollee.agreement:
                        self.department.applicants_with_agreement[type_of_completion].append(enrollee)

    def save_data_to_file(self):
        applicants_for_save = {"name": self.department.name, "type_of_completion": []}
        for type_of_completion in TypeOfCompletion:
            type_of_completion_save = {
                "name": type_of_completion.value,
                "places": self.department.places[type_of_completion],
                "list": []
            }
            for enrollee in self.department.applicants[type_of_completion]:
                type_of_completion_save["list"].append({
                    "name": enrollee.name,
                    "points": enrollee.points,
                    "agreement": enrollee.agreement
                })
            applicants_for_save["type_of_completion"].append(type_of_completion_save)

        self.create_data_folder_if_is_not_exist()
        with open(self.get_path_to_data_file(), "w") as write_file:
            json.dump(applicants_for_save, write_file)
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
            return os.path.join(self.department.settings.get_data_path(), "data", str(d.year), str(d.month),
                                str(d.day))
        return os.path.join(self.department.settings.get_data_path(), "data")

    def get_path_to_data_file(self, d=None):
        return os.path.join(self.get_path_to_data_dir(d), "{}.{}".format(self.department.name, "json"))
