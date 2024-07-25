import argparse
import inspect
import logging
import sys
from datetime import datetime

from src.utils.env_mapper import EnvMapper
from src.firefly_sync_cli import FireflySyncCli
from src.firefly_sync_daemon import FireflySyncDaemon


def init_logging(env_mapper: EnvMapper):
    class LoggingModuleNameFilter(logging.Filter):
        def filter(self, record):
            frame = inspect.currentframe().f_back
            while frame is not None:
                module = inspect.getmodule(frame)
                if module and module != logging:
                    record.name = module.__name__
                    break
                frame = frame.f_back
            return True

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(LoggingModuleNameFilter())
    logging.basicConfig(format='[%(asctime)s %(name)s-%(threadName)s %(levelname)s] %(message)s',
                        level=logging.INFO,
                        handlers=[handler])

    logging_def_str = env_mapper.get('LOGGING')
    if logging_def_str is None:
        return

    logging_def_list = [tuple(item.split(':')) for item in logging_def_str.split(',') if len(item.split(':')) == 2]
    for logger_name, level in logging_def_list:
        logging.getLogger(logger_name).setLevel(level)


def get_help_format(prog):
    class MyFormatter(argparse.HelpFormatter):
        """
        Corrected _max_action_length for the indenting of subactions
        """
        def add_argument(self, action):
            if action.help is not argparse.SUPPRESS:
                # find all invocations
                get_invocation = self._format_action_invocation
                invocations = [get_invocation(action)]
                current_indent = self._current_indent
                for subaction in self._iter_indented_subactions(action):
                    # compensate for the indent that will be added
                    indent_chg = self._current_indent - current_indent
                    added_indent = 'x'*indent_chg
                    invocations.append(added_indent+get_invocation(subaction))

                invocation_length = max([len(s) for s in invocations])
                action_length = invocation_length + self._current_indent
                self._action_max_length = max(self._action_max_length, action_length)
                # add the item to the list
                self._add_item(self._format_action, [action])

    return MyFormatter(prog, max_help_position=100)


if __name__ == "__main__":
    init_logging(EnvMapper())
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
                                help="Specific the end-date to link accounts (format: YYYY-MM-DD)",
                                type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser_tx_link.add_argument('--amount-diff',
                                type=float,
                                help="Acceptable transaction amount difference (in percentage) to link transactions")
    parser_tx_link.add_argument('--date-diff',
                                help="Acceptable transaction date difference (in days) to link transactions",
                                type=int)

    # Categorize transactions
    parser_tx_category = jobs.add_parser('tx-category', help="Categorize existing transactions (interactive)")
    parser_tx_category.add_argument('--start-date',
                                    help="Specific the start-date to categorize accounts (format: YYYY-MM-DD)",
                                    type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser_tx_category.add_argument('--end-date',
                                    help="Specific the end-date to categorize accounts (format: YYYY-MM-DD)",
                                    type=lambda s: datetime.strptime(s, '%Y-%m-%d'))
    parser_tx_category.add_argument('--account-ids',
                                    type=str,
                                    help="Account IDs separated by comma (e.g: 3,4,7)",
                                    default="")

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
        firefly_sync_cli.categorize(
            start_date=args.start_date, end_date=args.end_date,
            account_ids=[account_id
                         for account_ids in args.account_ids
                         for account_id in account_ids.split(',')
                         if account_id])
