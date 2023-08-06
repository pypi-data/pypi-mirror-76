from enum import Enum
from typing import Any, Union


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
