import logging
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .firefly_sync_cli import FireflySyncCli


class FireflySyncWatcher:
    @staticmethod
    def watch_path(firefly_sync_cli: FireflySyncCli, path: str):
        if not os.path.isdir(path):
            logging.error(f'Path is not a directory: {path}')
            return

        observer = Observer()
        observer.schedule(FireflySyncWatcherHandler(firefly_sync_cli), path=path, recursive=False)
        observer.start()

        while True:
            try:
                pass
            except KeyboardInterrupt:
                logging.info("Requested to stop watcher.")
                break


class FireflySyncWatcherHandler(FileSystemEventHandler):

    def __init__(self, firefly_sync_cli: FireflySyncCli) -> None:
        super().__init__()
        self.firefly_sync_cli = firefly_sync_cli

    def on_moved(self, event):
        self.import_and_move_file(event.dest_path.strip())

    def on_created(self, event):
        self.import_and_move_file(event.src_path.strip())

    def import_and_move_file(self, file_path):
        folder_path, file_name = os.path.split(file_path)
        if file_name == 'done':
            return

        imported = self.firefly_sync_cli.import_file(file_path)
        if not imported:
            return

        destination_folder_path = os.path.join(folder_path, 'done')
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)
        destination_file_path = os.path.join(destination_folder_path, file_name)
        shutil.move(file_path, destination_file_path)
        logging.info(f"File '{file_name}' moved to '{destination_folder_path}'")
