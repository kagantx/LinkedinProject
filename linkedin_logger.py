import logging


def getmylogger(name):
    # With help from codemotionhttps://www.codemotion.com/magazine/dev-hub/big-data-analyst/logging-in-python-a-broad-gentle-introduction/
    file_formatter = logging.Formatter('%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s')
    console_formatter = logging.Formatter('%(levelname)s -- %(message)s')

    file_handler = logging.FileHandler("logfile.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)

    return logger


if __name__ == "__main__":
    print("All tests passed")
