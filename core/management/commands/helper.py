import locale
import logging
from core.services.logger.client import LogClient

logger = logging.getLogger(__name__)


class CommandHelper:
    job_id = None
    log_client = LogClient(mode=LogClient.MODE_CRON)
    cron_name = 'DEFAULT'
    live = None
    user = None
    items = None

    def __init__(self):
        locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')

    def start_log(self):
        self.log_client.insert(
            message={
                "job": self.cron_name,
                "status": "Job STARTED",
            }
        )

    def error_log(self, message):
        self.log_client.insert(
            level=LogClient.LEVEL_ERROR,
            message=message
        )

    def end_log(self):
        self.log_client.insert(
            message={
                "job": self.cron_name,
                "status": "Job FINISHED",
            }
        )

    def in_progress_log(self, message):
        self.log_client.insert(
            message=message
        )
