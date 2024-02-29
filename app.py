import argparse

from src.firefly_sync_cli import FireflySyncCli

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50))

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', help='File to be imported')
    group.add_argument('--file-watcher-path', help='Path location for the file watcher')

    parser.add_argument("--dry-run",
                        action=argparse.BooleanOptionalAction,
                        help="Execute import as dry-run (it will not persist anything)",
                        default=True)
    myargs = parser.parse_args()

    firefly_sync_cli = FireflySyncCli()
    if myargs.file_watcher_path:
        firefly_sync_cli.watch_directory(myargs.file_watcher_path)
    else:
        firefly_sync_cli.import_file(myargs.file, myargs.dry_run)
