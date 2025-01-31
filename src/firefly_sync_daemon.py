
from .firefly_sync_cli import FireflySyncCli
from .utils.file_watcher_handler import FileWatcherHandler
from .utils.env_mapper import EnvMapper

import logging
from watchdog.observers import Observer
from apscheduler.schedulers.background import BackgroundScheduler
import os


class FireflySyncDaemon():

    def __init__(self, firefly_sync_cli: FireflySyncCli, disable_firefly_cron_job: bool, disable_stock_cron_job) -> None:
        # Cronjob runs at midnight by default
        MANDATORY_ENV_KEYS = {
            "DAEMON_WATCHER_PATH": None
        }

        if not disable_firefly_cron_job:
            MANDATORY_ENV_KEYS['DAEMON_FIREFLY_CRON_CLI_TOKEN'] = None
            MANDATORY_ENV_KEYS['DAEMON_FIREFLY_CRON_EXPRESSION'] = "0 0 * * *"

        if not disable_stock_cron_job:
            MANDATORY_ENV_KEYS['DAEMON_STOCK_CRON_EXPRESSION'] = "0 0 * * *"

        self.firefly_sync_cli = firefly_sync_cli
        self.disable_firefly_cron_job = disable_firefly_cron_job
        self.disable_stock_cron_job = disable_stock_cron_job
        self.env_mapper = EnvMapper(MANDATORY_ENV_KEYS)

    def start(self) -> None:
        path = self.env_mapper.get("DAEMON_WATCHER_PATH")
        if not os.path.isdir(path):
            logging.error(f'Path is not a directory: {path}')
            return

        observer = Observer()
        observer.schedule(FileWatcherHandler(self.firefly_sync_cli), path=path, recursive=False)
        logging.info(f'Adding file watcher to the job list (path: {path})')
        observer.start()

        if not self.disable_firefly_cron_job:
            logging.info(f'Adding firefly cronjob to the job list (expression: \
                         {self.env_mapper.get("DAEMON_FIREFLY_CRON_EXPRESSION")})')
            firefly_scheduler = BackgroundScheduler()
            firefly_scheduler.add_job(
                self.firefly_sync_cli.create_firefly_cron_job, 'firefly_cron',
                args=[self.env_mapper.get("DAEMON_FIREFLY_CRON_CLI_TOKEN")],
                **{part: value for part, value in zip(["minute", "hour", "day", "month", "day_of_week"],
                                                      self.env_mapper.get("DAEMON_FIREFLY_CRON_EXPRESSION").split())})
            firefly_scheduler.start()

        if not self.disable_stock_cron_job:
            logging.info(f'Adding stock update cronjob to the job list (expression: \
                         {self.env_mapper.get("DAEMON_STOCK_CRON_EXPRESSION")})')
            stock_scheduler = BackgroundScheduler()
            stock_scheduler.add_job(
                self.firefly_sync_cli.create_firefly_cron_job, 'stock_cron',
                **{part: value for part, value in zip(["minute", "hour", "day", "month", "day_of_week"],
                                                      self.env_mapper.get("DAEMON_STOCK_CRON_EXPRESSION").split())})
            stock_scheduler.start()

        try:
            observer.join()
        except KeyboardInterrupt:
            logging.info("Requested to stop watcher.")
            observer.stop()
        observer.join()
