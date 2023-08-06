from threading import Thread


class DepartmentLoadFromWebThread(Thread):
    """
    To asynchronously download data from the web
    """

    def __init__(self, dep):
        Thread.__init__(self)
        self.department = dep
        self.name = "Thread: {}".format(dep.name)

    def run(self):
        self.department.load_from_web()
