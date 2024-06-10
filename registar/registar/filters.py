import logging

class ExactLevelFilter:
    def __init__(self, levelno):
        self.levelno = levelno

    def filter(self, record):
        return record.levelno == self.levelno


class DisableAutoreload(logging.Filter): 
    def filter(self, record):
        is_autoreload = record.name.startswith("django.utils.autoreload")
        is_server = record.name.startswith("django.server")

        return not is_autoreload and not is_server
