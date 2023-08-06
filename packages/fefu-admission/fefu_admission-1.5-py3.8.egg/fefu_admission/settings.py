import json
import os


class Settings:

    DIR_PATH = os.path.join(os.path.expanduser('~'), ".fefu_admission")
    FILE_PATH = os.path.join(os.path.expanduser('~'), ".fefu_admission", "settings.json")

    @staticmethod
    def create_default_settings():
        settings_content = {
            "me": "null",
            "list_of_departments": [
                "01.03.02 Прикладная математика и информатика",
                "02.03.01 Математика и компьютерные науки",
                "09.03.03 Прикладная информатика",
                "09.03.04 Программная инженерия"
            ]
        }
        if not os.path.exists(Settings.DIR_PATH):
            os.makedirs(Settings.DIR_PATH)
        with open(Settings.FILE_PATH, 'w') as settings_file:
            json.dump(settings_content, settings_file)

    @staticmethod
    def get():
        try:
            read_file = open(Settings.FILE_PATH, "r")
            data = json.load(read_file)
            read_file.close()
            return data
        except FileNotFoundError:
            Settings.create_default_settings()
            return Settings.get()
