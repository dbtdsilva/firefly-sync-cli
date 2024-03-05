import argparse
import logging
from datetime import datetime

from src.firefly_sync_cli import FireflySyncCli
from src.firefly_sync_daemon import FireflySyncDaemon


def init_logging():
    logging.basicConfig(format='[%(asctime)s %(name)s-%(threadName)s %(levelname)s] %(message)s',
                        level=logging.INFO)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.DEBUG)


def get_help_format(prog):
    return argparse.HelpFormatter(prog, max_help_position=100)


if __name__ == "__main__":
    init_logging()

    parser = argparse.ArgumentParser(formatter_class=get_help_format)
    parser.add_argument("--dry-run",
                        action='store_false',
                        help="Execute the job as dry-run (it will not persist anything)",
                        default=False)

    jobs = parser.add_subparsers(title='required argument', dest='job', metavar='job', required=True)

    # Run as a daemon (used for Dockerfile especially)
    parser_daemon = jobs.add_parser('daemon',
                                    help="File watcher listening for transaction files from banks",
                                    formatter_class=get_help_format)
    parser_daemon.add_argument("--no-cron-job",
                               action='store_true',
                               help="Prevents cron from being executed",
                               default=False)

    # Import a file from your bank
    parser_file = jobs.add_parser('tx-import',
                                  help="Import a transaction file from a bank",
                                  formatter_class=get_help_format)
    parser_file.add_argument('file', type=str, help='File to be imported')

    # Link transactions between banks as transfer
    parser_tx_link = jobs.add_parser('tx-link',
                                     help="Links transfer operation between existing accounts (interactive)",
                                     formatter_class=get_help_format)
    parser_tx_link.add_argument('--start-date',
                                help="Specific the start-date to link accounts (format: YYYY-MM-DD)",
                                type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser_tx_link.add_argument('--end-date',
                                help="Specific the start-date to link accounts (format: YYYY-MM-DD)",
                                type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser_tx_link.add_argument('--amount-diff',
                                type=float,
                                help="Acceptable transaction amount difference (in percentage) to link transactions")
    parser_tx_link.add_argument('--date-diff',
                                help="Acceptable transaction date difference (in days) to link transactions",
                                type=int)

    # Categorize transactions
    parser_tx_category = jobs.add_parser('tx-category', help="Categorize existing transactions (interactive)")

    args = parser.parse_args()

    firefly_sync_cli = FireflySyncCli(args.dry_run)
    if args.job == 'daemon':
        firefly_sync_daemon = FireflySyncDaemon(firefly_sync_cli, args.no_cron_job)
        firefly_sync_daemon.start()
    elif args.job == 'tx-import':
        firefly_sync_cli.import_file(args.file)
    elif args.job == 'tx-link':
        firefly_sync_cli.link_identical_transactions(start_date=args.start_date, end_date=args.end_date,
                                                     amount_diff_percentage=args.amount_diff,
                                                     date_diff_days=args.date_diff)
    elif args.job == 'tx-category':
        firefly_sync_cli.categorize()
