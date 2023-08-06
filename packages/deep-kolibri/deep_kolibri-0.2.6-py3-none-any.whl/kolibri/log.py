"""
Basic Hey_Computer logging tools
"""
import logging
from os.path import join
from kolibri import settings



def get_logger(module_name=settings.LOG_NAME, log_level=settings.LOG_LEVEL):
    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    fh =logging.FileHandler(join(settings.LOGS_DIR, module_name+'.log'))
    fh.setFormatter(logging.Formatter("[%(asctime)s %(levelname)s]: %(message)s"))
    fh.setLevel(log_level)
    logger.addHandler(fh)
    return logger

