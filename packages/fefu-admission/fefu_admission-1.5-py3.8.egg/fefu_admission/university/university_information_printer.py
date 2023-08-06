from fefu_admission.university.applicants_holder_information_printer import ApplicantsHolderInformationPrinter
from fefu_admission.university.type_of_completion import TypeOfCompletion

from colorama import Back, Fore, Style
from tabulate import tabulate


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
                me = self.applicants_holder.settings.me
                if me is not None:
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
                elif enrollee.agreement:
                    style_start = Back.GREEN + Fore.BLACK
                    note = "Подал на это направление"

                rows_list.append([index_of_enrollee + 1, "{}{}{}".format(style_start, enrollee.name, Style.RESET_ALL),
                                  *enrollee.points, enrollee.get_points_sum(), note])

        return rows_list

    def print_list_of_department(self, index, with_agreement=False):
        dep = self.applicants_holder.departments[index]
        ApplicantsHolderInformationPrinter(dep).print_info()
        print(tabulate(self.get_list_of_department(index, with_agreement), tablefmt='fancy_grid'))
