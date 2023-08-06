from fefu_admission.university.department import Department
from fefu_admission.university.university import University
from fefu_admission.university.type_of_completion import TypeOfCompletion
from fefu_admission.university.enrollee import Enrollee

import time

import requests
import logging
from lxml import html


class FefuDepartment(Department):
    """
        Загружает таблицу с сайта или из файлов
    """

    URL_TABLE = "https://www.dvfu.ru/admission/spd/"

    def __init__(self, n: str, u: University):
        super().__init__(n, u)

    def get_html_table(self):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }

        logging.info("Try to send GET request " + self.name)
        response = requests.get(self.URL_TABLE, headers=headers, verify=True)
        logging.info("Status code: " + str(response.status_code))

        headers["cookie"] = '; '.join([x.name + '=' + x.value for x in response.cookies])
        headers["content-type"] = 'application/x-www-form-urlencoded'
        payload = {
            "PROPERTY_1647": "Прием на обучение на бакалавриат/специалитет",
            "PROPERTY_1677": "Бюджетная основа",
            "PROPERTY_1648": "Очная",
            "PROPERTY_1652": "Владивосток",
            "PROPERTY_1642": self.name
        }

        logging.info("Try to send POST request " + self.name)
        response = requests.post(self.URL_TABLE, data=payload, headers=headers,
                                 verify=True)
        logging.info("Status code: " + str(response.status_code))
        return response.text

    def load_from_web(self):
        load_flag = False
        page = None
        while load_flag is not True:
            try:
                page = html.fromstring(self.get_html_table())
                load_flag = True
            except AttributeError:
                logging.info("{}: The data is processed on the site, so the table is not currently available.\
                I will try to load data in 5 seconds. To stop the program press Ctrl-C".format(self.name))
                time.sleep(5)

        table = page.get_element_by_id("abitur")
        tbody = table.find("tbody")

        type_of_competition = TypeOfCompletion.SpecialQuota
        for element in tbody:
            if element.find_class("block-header"):
                type_of_competition_str = element[1][0].text_content()
                places = int(element[1].text_content().split(" ")[-1])
                type_of_competition = TypeOfCompletion.get_through_value(type_of_competition_str)
                if type_of_competition is None:
                    assert False
                self.places[type_of_competition] = places
            else:
                name = element[1].text_content()
                points = []
                for i in range(2, 6):
                    point = element[i].text_content()
                    if point == "-":
                        point = 100
                    points.append(int(point))
                if len(element[7]):
                    agreement = True
                else:
                    agreement = False
                enrollee = Enrollee(name, points, agreement)
                if agreement:
                    self.add_enrollee_with_agreement(type_of_competition, enrollee)
                self.add_enrollee(type_of_competition, enrollee)
