from fefu_admission.university.type_of_completion import TypeOfCompletion

from tabulate import tabulate


class ApplicantsHolderInformationPrinter:

    def __init__(self, applicants_holder):
        self.applicants_holder = applicants_holder

    def print_info(self):
        rows_list = [
            ["Всего подало", self.applicants_holder.get_len_applicants()],
            ["Бюджетников подало", self.applicants_holder.get_len_applicants(
                type_of_completion=TypeOfCompletion.Budget)],
            ["Бюджетные места на данный момент", self.applicants_holder.get_budget_places_for_now()],
            ["Подало согласие", self.applicants_holder.get_len_applicants(agreement=True)],
            ["Подало согласие(На общий основаниях)", self.applicants_holder.get_len_applicants(
                type_of_completion=TypeOfCompletion.Budget, agreement=True)],
        ]
        me_enrollee = self.applicants_holder.settings.me
        if me_enrollee is not None:
            rows_list.append(
                ["Мое место среди бюджетников", self.applicants_holder.get_position_of_me(TypeOfCompletion.Budget)])
            rows_list.append(
                ["Мое место среди бюджетников без высокобальников[250]",
                 self.applicants_holder.get_position_of_me_without_high_scores(
                     type_of_completion=TypeOfCompletion.Budget, agreement=False, high_scores=250)])
            rows_list.append(["Мое место среди бюджетинков, подавших солгасие",
                              self.applicants_holder.get_position_of_me(type_of_completion=TypeOfCompletion.Budget,
                                                                        agreement=True)])
        print(tabulate(rows_list, tablefmt='fancy_grid'))
