from .utils import elk_log_format
import json
import logging


logger = logging.getLogger('elastic-logger')


def elk_log(log_data, log_level):
    if log_level == 'info':
        logger.info(json.dumps(log_data))
    elif log_level == 'error':
        logger.error(json.dumps(log_data))


class MiddlewareLog:
    def __init__(self, response):
        self.response = response

    def __call__(self, request):
        response = self.response(request)
        log_data = elk_log_format(request, response)
        elk_log(log_data=log_data, log_level='info')

    def handle_exception(self, request, exception):
        log_data = elk_log_format(request, None, exception)
        elk_log(log_data=log_data, log_level='error')

