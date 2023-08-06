class Enrollee:

    def __init__(self, name, points, agreement):
        self.name = name
        self.points = points
        self.agreement = agreement

    def get_points_sum(self):
        return sum([int(x) for x in self.points])

    @staticmethod
    def get_from_json(enrolle_json):
        """
        :param enrolle_json
        :return: Enrollee
        """
        try:
            return Enrollee(name=enrolle_json["name"],
                            points=enrolle_json["points"],
                            agreement=enrolle_json["agreement"])
        except KeyError:
            return None
        except TypeError:
            return None

    def __str__(self):
        string = self.name + ","
        for item in self.points:
            string += str(item)
            string += ","
        string += str(self.agreement)
        return string

    def __lt__(self, other):
        first = self.get_points_sum()
        seconds = other.get_points_sum()
        if first < seconds:
            return False
        if first > seconds:
            return True
        for i in range(0, len(self.points) - 1):
            if self.points[i] < other.points[i]:
                return False
            elif self.points[i] == other.points[i]:
                continue
            else:
                return True
        return False

    def __eq__(self, other):
        return self.name == other.name

    # May be here bug
    def __hash__(self):
        return hash(self.name)
