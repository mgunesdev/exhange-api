from django.core.management.base import BaseCommand
from core.management.commands.helper import CommandHelper


class Command(BaseCommand, CommandHelper):
    help = "JOB_GET_RATES"
    cron_name = 'JOB_GET_RATES'

    def handle(self, *args, **options):
        print("********** JOB_GET_RATES STARTED **********")
        self.start_log()

        try:
            print("JOB_GET_RATES")
        except Exception as exc:
            self.error_log(message={
                "job": self.cron_name,
                "live_id": self.live.id,
                "message": exc,
            })

        self.end_log()
        print("********** JOB_GET_RATES ENDED **********")
