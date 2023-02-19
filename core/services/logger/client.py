# -*- coding: utf-8 -*-
import json

from django.utils import timezone
from core.models import _createHash
import logging

logger = logging.getLogger(__name__)


class LogClient:
    MODE_CRON = 1
    MODE_USER = 2

    LEVEL_INFO = 'INFO'
    LEVEL_ERROR = 'ERROR'
    LEVEL_EMERGENCY = 'EMERGENCY'

    mode = None
    level = None
    job_id = None
    message = None
    data = None

    def __init__(
            self,
            mode=MODE_CRON,
            job_id=_createHash(),
    ):
        self.mode = mode
        self.job_id = job_id

    def insert(
            self,
            level=LEVEL_INFO,
            message=None,
    ):
        self.message = message
        self.level = level
        self.data = json.dumps({
            "date": str(timezone.now()),
            'level': self.level,
            "message": self.message,
            "job_id": self.job_id
        })

        if self.level == self.LEVEL_EMERGENCY:
            logger.critical(self.data)
        elif self.level == self.LEVEL_ERROR:
            logger.error(self.data)
        elif self.level == self.LEVEL_INFO:
            logger.info(self.data)

        print(self.message)

        return True
