class UniversitySerialization:

    def __init__(self, university):
        self.university = university

    def load_from_file_all(self, d=None):
        for department in self.university.departments:
            department.serialization.load_data_from_file(d)

    def save_data_to_file_all(self):

        for department in self.university.departments:
            department.serialization.save_data_to_file()
