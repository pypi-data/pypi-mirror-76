from fefu_admission.university.type_of_completion import TypeOfCompletion
from fefu_admission.university.applicants_holder_base import ApplicantsHolderBase
from fefu_admission.university.department_load_from_web_thread import DepartmentLoadFromWebThread
from fefu_admission.university.university_serialization import UniversitySerialization

import logging


class University(ApplicantsHolderBase):

    def __init__(self):
        super().__init__()
        self.name = ""
        self.departments = []
        self.data_path = ""
        self.serialization = UniversitySerialization(self)
        self.settings = None

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
