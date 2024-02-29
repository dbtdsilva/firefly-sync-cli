import argparse
import logging

from src.firefly_sync_cli import FireflySyncCli
from src.firefly_sync_watcher import FireflySyncWatcher


def init_logging():
    logging.basicConfig()
    logging.root.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s %(name)s-%(threadName)s %(levelname)s] %(message)s')
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)


if __name__ == "__main__":
    init_logging()
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', help='File to be imported')
    group.add_argument('--file-watcher-path', help='Path location for the file watcher')

    parser.add_argument("--dry-run",
                        action=argparse.BooleanOptionalAction,
                        help="Execute import as dry-run (it will not persist anything)",
                        default=False)
    myargs = parser.parse_args()

    firefly_sync_cli = FireflySyncCli(myargs.dry_run)
    if myargs.file_watcher_path:
        FireflySyncWatcher.watch_path(firefly_sync_cli, myargs.file_watcher_path)
    else:
        firefly_sync_cli.import_file(myargs.file)
