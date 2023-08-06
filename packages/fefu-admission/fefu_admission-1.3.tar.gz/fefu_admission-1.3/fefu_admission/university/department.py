from fefu_admission.university.applicants_holder_base import ApplicantsHolderBase
from fefu_admission.university.enrollee import Enrollee
from fefu_admission.university.type_of_completion import TypeOfCompletion
from fefu_admission.university.department_serialization import DepartmentSerialization


from typing import Dict, List


class Department(ApplicantsHolderBase):
    applicants: Dict[TypeOfCompletion, List[Enrollee]]
    NAME_UNIVERSITY = ""

    def __init__(self, n, university):
        super().__init__()
        self.name = n
        self.serialization = DepartmentSerialization(self)
        self.university = university
        self.settings = university.settings

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

    def __str__(self):
        return self.name
