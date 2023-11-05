from config import settings
import json
import logging
import time
from datetime import datetime
from elasticsearch import Elasticsearch


class ElkHandler(logging.Handler):

    def __init__(self):
        super().__init__()
        self.elk = Elasticsearch(f"http://{settings.ELASTICSEARCH_HOST}:{settings.ELASTICSEARCH_PORT}")
        self.sender = LogSender(self.elk)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.sender.createlog(message=record, formatter=self.format)
        except Exception:
            self.handleError(record)


class LogSender:

    def __init__(self, elk):
        self.elk = elk

    def createlog(self, message: logging.LogRecord, formatter):

        index_name = f"LogDate {time.strftime('%Y_%m_%d')}"
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_data = json.loads(formatter(message))
        log_data['timestamp'] = timestamp

        return self.elk.index(index=index_name, document=log_data)

