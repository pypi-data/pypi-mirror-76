from threading import Thread

from fefu_admission.university.department import Department


class DepartmentWebLoaderThread(Thread):
    """
    To asynchronously download data from the web
    """

    def __init__(self, department: Department):
        Thread.__init__(self)
        self.department: Department = department
        self.name: str = "Thread: {}".format(department.name)

    def run(self):
        self.department.load_from_web()
