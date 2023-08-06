import time
import logging


class Utils:

    @staticmethod
    def log_time_of_function(function):
        def wrapped(*args):
            start_time = time.time()
            res = function(*args)
            arguments_str = ", ".join([str(item) for item in args])
            logging.info("function {func}, args: ({args_str}),secs: {delta_time:.3f}"
                         .format(func=function.__name__, args_str=arguments_str, delta_time=time.time() - start_time))
            return res
        return wrapped
