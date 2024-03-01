
from .firefly_sync_cli import FireflySyncCli
from .utils.file_watcher_handler import FileWatcherHandler
from .utils.env_mapper import EnvMapper

import logging
from watchdog.observers import Observer
from apscheduler.schedulers.background import BackgroundScheduler
import os


class FireflySyncDaemon():

    # Cronjob runs at midnight by default
    MANDATORY_ENV_KEYS = {
        "DAEMON_WATCHER_PATH": None,
        "DAEMON_CRON_EXPRESSION": "0 0 * * *"
    }

    def __init__(self, firefly_sync_cli: FireflySyncCli, disable_cron_job: bool) -> None:
        self.firefly_sync_cli = firefly_sync_cli
        self.env_mapper = EnvMapper(FireflySyncDaemon.MANDATORY_ENV_KEYS)
        self.disable_cron_job = disable_cron_job

    def start(self) -> None:
        path = self.env_mapper.get("DAEMON_WATCHER_PATH")
        if not os.path.isdir(path):
            logging.error(f'Path is not a directory: {path}')
            return

        observer = Observer()
        observer.schedule(FileWatcherHandler(self.firefly_sync_cli), path=path, recursive=False)
        logging.info(f'Adding file watcher to the job list (path: {path})')
        observer.start()

        if not self.disable_cron_job:
            logging.info(f'Adding cronjob to the job list (expression: {self.env_mapper.get("DAEMON_CRON_EXPRESSION")})')
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.firefly_sync_cli.cron, 'cron',
                              **{part: value for part, value in zip(["minute", "hour", "day", "month", "day_of_week"],
                                                                    self.env_mapper.get("DAEMON_CRON_EXPRESSION").split())})
            scheduler.start()

        try:
            observer.join()
        except KeyboardInterrupt:
            logging.info("Requested to stop watcher.")
            observer.stop()
        observer.join()
