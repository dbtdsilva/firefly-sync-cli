# Firefly Sync CLI

This can be used to import files into Firefly III (https://www.firefly-iii.org) rather than using the Data Importer, which I found quite limited in terms of visibility and my personal use case.

## How to use

This can be executed as a simple python script or be run as a container.

### Docker

You can also setup a file watcher that checks for new file transactions that will be automatically parsed, imported and tagged in Firefly.

```yaml
firefly-sync-cli:
    image: ghcr.io/dbtdsilva/firefly-sync-cli
    container_name: firefly-sync-cli
    environment:
        - FILE_WATCHER_PATH=/app/uploads
        - FIREFLY_URL=<YOUR_FIREFLY_URL>
        - FIREFLY_TOKEN=<YOUR_TOKEN_HERE>
    volumes:
        - <YOUR_PATH_FOR_UPLOADS>:/app/uploads
    network_mode: firefly
    restart: always
```

With this docker-compose, you will be able to upload your file to a directory of your preference.

The parsers are loaded dynamically (you can even provide your own, check 'Custom transactions' section), so you also need to indicate how to load them.

Go to the account that you want to load in Firefly and modify its note to:

```
sync: <transaction_file_prefix>,<parser_name_without_extension>

e.g. sync: montepio,montepio_parser
```

Meaning that it will be mapping files like 'montepio_20140505.csv' to the 'montepio_parser'.

### Script

```bash
pip install -r requirements.txt
python app.py [-h] (--file FILE | --file-watcher-path FILE_WATCHER_PATH) [--dry-run | --no-dry-run]
```

You can either leave it as a file watcher (similar to the container) or choose to import a specific file. Feel free to test by using the --dry-run option.

## Custom transactions

Feel free to modify the codebase and add new parsers as you might need.
They can even be provided to the docker container instead of opening a PR or forking.

```yaml
firefly-sync-cli:
    image: ghcr.io/dbtdsilva/firefly-sync-cli
    container_name: firefly-sync-cli
    environment:
        - FILE_WATCHER_PATH=/app/uploads
        - FIREFLY_URL=<YOUR_FIREFLY_URL>
        - FIREFLY_TOKEN=<YOUR_TOKEN_HERE>
    volumes:
        - <YOUR_PATH_FOR_REPO>:/app
    network_mode: firefly
    restart: always
```

This way you can simply add custom parsers to the 'src/parsers' folder.

