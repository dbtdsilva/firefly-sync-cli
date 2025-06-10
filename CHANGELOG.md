# CHANGELOG


## v1.5.3 (2025-01-31)

### Bug Fixes

- Exchange rates are closed on weekend, closest open interval is fetched
  ([`bb7f3f2`](https://github.com/dbtdsilva/firefly-sync-cli/commit/bb7f3f2fe36e2a9a7b6bc2295dd8852455db603d))


## v1.5.2 (2025-01-31)

### Bug Fixes

- Updated cronjob to call the proper function
  ([`9d31d51`](https://github.com/dbtdsilva/firefly-sync-cli/commit/9d31d51d3d987608386f56e22dbad05cd32228d1))


## v1.5.1 (2025-01-31)

### Bug Fixes

- Renamed keys to cron
  ([`a1ac160`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a1ac160c0242d0e0e69d401242caf424dfe6bd74))


## v1.5.0 (2025-01-31)

### Features

- Added support for stocks update
  ([`784db18`](https://github.com/dbtdsilva/firefly-sync-cli/commit/784db1824cccc67ffc5cfd34c62445169deb504c))


## v1.4.0 (2024-07-25)

### Bug Fixes

- Enumerate was not correct in failed_txs
  ([`2b76037`](https://github.com/dbtdsilva/firefly-sync-cli/commit/2b7603799bdef4d24ab1ded8352895780491e2ec))

- Loggers will now show the class invoking that logger
  ([`2ce637b`](https://github.com/dbtdsilva/firefly-sync-cli/commit/2ce637ba95c2bd9e7a0749b5ee28259077f9bbd4))

### Code Style

- Small fixup
  ([`feeec32`](https://github.com/dbtdsilva/firefly-sync-cli/commit/feeec327ca56d96955cf8a1027f355ed5b0d2f4d))

### Features

- Allow setting specific log level from environment variables
  ([`fe5e34d`](https://github.com/dbtdsilva/firefly-sync-cli/commit/fe5e34d6b99233f51af49e82fabeffd8889aaa20))


## v1.3.0 (2024-07-25)

### Features

- Failed transactions will be retried once
  ([`5fc1f54`](https://github.com/dbtdsilva/firefly-sync-cli/commit/5fc1f548f46ce1e8b530a51f50250d349350e190))


## v1.2.7 (2024-07-24)

### Bug Fixes

- Keep trying insert transactions even if one of them fails
  ([`109c424`](https://github.com/dbtdsilva/firefly-sync-cli/commit/109c4249575caa07ab2c737cb8fb6f4bcede8b8a))


## v1.2.6 (2024-07-22)

### Bug Fixes

- Deploy was not happening properly
  ([`413d3aa`](https://github.com/dbtdsilva/firefly-sync-cli/commit/413d3aa39a985b2d9dfbb316391c1beb0ca39c85))


## v1.2.5 (2024-07-22)

### Bug Fixes

- Bypass firefly mime detection, I still want to upload csvs (sorry not sorry)
  ([`156b41f`](https://github.com/dbtdsilva/firefly-sync-cli/commit/156b41f643ae6b78cb92f22b883adf41d7bdec4c))

- Semantic-release generating undesired extra lines for changelog
  ([`1fb22a4`](https://github.com/dbtdsilva/firefly-sync-cli/commit/1fb22a489506190f09532074124c4d8b48ad0e18))

### Code Style

- Small change in the commit message for semantic release
  ([`b5d0a19`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b5d0a192516d14fe20aa06dafa71524468f51a72))


## v1.2.4 (2024-07-20)

### Bug Fixes

- Changing encoding type to prevent conflicts
  ([`d9128c9`](https://github.com/dbtdsilva/firefly-sync-cli/commit/d9128c97528d8ef08a0a2e207b1d2440accb89b8))

### Continuous Integration

- Added pyproject.toml
  ([`86e608f`](https://github.com/dbtdsilva/firefly-sync-cli/commit/86e608f2f5271db7624ba64dc894c6d328ee8919))

- Added semantic release and renamed workflows
  ([`0bb0b13`](https://github.com/dbtdsilva/firefly-sync-cli/commit/0bb0b1386e42adf9a9d6af0c2b5aaa186789c4df))

- Changed branch from master to main
  ([`4aa2e47`](https://github.com/dbtdsilva/firefly-sync-cli/commit/4aa2e47109dd821414feaf9ccc0fbbaa455235e9))

- Fixed workflow not waiting for build and test
  ([`eb6c146`](https://github.com/dbtdsilva/firefly-sync-cli/commit/eb6c1467a9c2f1c2034759de94bc83c311f977ab))

- Semantic-release only after build, test and codeql
  ([`44f22e5`](https://github.com/dbtdsilva/firefly-sync-cli/commit/44f22e50d8b68d758991de0dd57cc328c903eb10))

- Updated workflow, config and changelog
  ([`a87f4bd`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a87f4bdb9f44b0b8fac72a64bb4c7493568bf148))


## v1.2.3 (2024-07-19)

### Bug Fixes

- Revolut parser not processing fees properly
  ([`c6ddb06`](https://github.com/dbtdsilva/firefly-sync-cli/commit/c6ddb06d53c9bef4006e52b1e0779d2eea7eb2a8))


## v1.2.2 (2024-07-18)


## v1.2.1 (2024-03-13)


## v1.2.0 (2024-03-13)


## v1.1.0 (2024-03-01)


## v1.0.2 (2024-03-01)


## v1.0.1 (2024-02-29)


## v1.0.0 (2024-02-29)
