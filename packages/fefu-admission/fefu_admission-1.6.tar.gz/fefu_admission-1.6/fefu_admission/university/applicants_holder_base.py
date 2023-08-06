from fefu_admission.university.type_of_completion import TypeOfCompletion


class ApplicantsHolderBase:
    """
    Base class containing lists of applicants and methods for working with them.
    """

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
        # This is instance of fefu_admission.settings
        self.settings = None

    def get_places(self, type_of_completion):
        return self.places[type_of_completion]

    def get_budget_places_for_now(self):
        """
        If a special quota, contract places are not occupied, then they will be added to the budget.
        Just returns the budget places at the moment.

        :return: budget_places: int
        """
        budget_places = self.get_places(TypeOfCompletion.Budget)

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
        me = self.settings.me
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

    def __get_position_of_me(self, list_enrolle):
        me = self.settings.me
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

    def add_enrollee(self, type_of_competition, enrollee):
        self.applicants[type_of_competition].append(enrollee)

    def add_enrollee_with_agreement(self, type_of_competition, enrollee):
        self.applicants_with_agreement[type_of_competition].append(enrollee)

    def search_enrollee_in_list(self, type_of_completion, name):
        return self.__search_enrollee_in_list(self.applicants[type_of_completion], name)

    def search_enrollee_in_list_with_agreement(self, type_of_completion, name):
        return self.__search_enrollee_in_list(self.applicants_with_agreement[type_of_completion], name)

    @staticmethod
    def __search_enrollee_in_list(list_enrollee, name):
        for enrolle in list_enrollee:
            if enrolle.name == name:
                return enrolle

        return None
