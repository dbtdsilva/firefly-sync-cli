import argparse
import logging

from src.firefly_sync_cli import FireflySyncCli
from src.firefly_sync_daemon import FireflySyncDaemon


def init_logging():
    logging.basicConfig(format='[%(asctime)s %(name)s-%(threadName)s %(levelname)s] %(message)s',
                        level=logging.INFO)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG)


if __name__ == "__main__":
    init_logging()
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', help='File to be imported')
    group.add_argument('--daemon',
                       action='store_true',
                       help='Runs a file watcher and a daily Firefly cronjob',
                       default=False)

    parser.add_argument("--dry-run",
                        action='store_false',
                        help="Execute import as dry-run (it will not persist anything)",
                        default=False)
    parser.add_argument("--no-cron-job",
                        action='store_true',
                        help="Prevents cron from being executed when using --daemon",
                        default=False)
    myargs = parser.parse_args()

    firefly_sync_cli = FireflySyncCli(myargs.dry_run)
    if myargs.daemon:
        firefly_sync_daemon = FireflySyncDaemon(firefly_sync_cli, myargs.no_cron_job)
        firefly_sync_daemon.start()
    else:
        firefly_sync_cli.import_file(myargs.file)
