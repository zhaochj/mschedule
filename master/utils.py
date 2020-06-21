import logging


def get_logger(mod_name: str, file_name: str):
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.FileHandler(file_name)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt='%(asctime)s [%(name)s %(funcName)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


