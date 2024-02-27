import argparse

from src.firefly_sync_cli import FireflySyncCli

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File to be imported")
    myargs = parser.parse_args()

    firefly_sync_cli = FireflySyncCli()
    firefly_sync_cli.import_file(myargs.file)
