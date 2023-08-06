import json
import os

from .enrollee import Enrollee


class Settings:

    def __init__(self, university):
        self.university = university
        self.settings_file = os.path.join(self.university.data_path, "settings.json")

        data = self.get()
        self.me: Enrollee = Enrollee.get_from_json(data["me"])
        self.list_of_departments = data["list_of_departments"]

    def get(self):
        try:
            read_file = open(self.settings_file, "r")
            data = json.load(read_file)
            read_file.close()
            return data
        except FileNotFoundError:
            self.create_default_settings()
            self.get()

    def get_data_path(self):
        return self.university.data_path

    def create_default_settings(self):
        settings_content = {
            "me": None,
            "list_of_departments": [
                "01.03.02 Прикладная математика и информатика",
                "02.03.01 Математика и компьютерные науки",
                "09.03.03 Прикладная информатика",
                "09.03.04 Программная инженерия"
            ]
        }
        if not os.path.exists(self.university.data_path):
            os.makedirs(self.university.data_path)
        with open(self.settings_file, 'w') as settings_file:
            json.dump(settings_content, settings_file)
