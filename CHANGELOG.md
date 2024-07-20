# CHANGELOG

## v1.2.3 (2024-07-19)

### Fix

* fix: revolut parser not processing fees properly ([`c6ddb06`](https://github.com/dbtdsilva/firefly-sync-cli/commit/c6ddb06d53c9bef4006e52b1e0779d2eea7eb2a8))

## v1.2.2 (2024-07-18)

### Unknown

* Fixed transaction import comparison references across account only ([`d2a9b57`](https://github.com/dbtdsilva/firefly-sync-cli/commit/d2a9b5716fd2343ff05f25d05d3cffee0cb70335))

* Split internal reference when there are multiple ([`2ea9580`](https://github.com/dbtdsilva/firefly-sync-cli/commit/2ea9580498cc50c4c2f0fb907b34cd22cb32d8c7))

## v1.2.1 (2024-03-13)

### Unknown

* Hotfix module loading ([`671bd63`](https://github.com/dbtdsilva/firefly-sync-cli/commit/671bd632bf9ea8e2423e8494b64e9e583580b26d))

## v1.2.0 (2024-03-13)

### Unknown

* Small fixup with the filename length matching ([`21deadd`](https://github.com/dbtdsilva/firefly-sync-cli/commit/21deaddab006c2f8cdaa64c1034b813bc03a9c12))

* Removed extra default parameters, left only one ([`e5433f6`](https://github.com/dbtdsilva/firefly-sync-cli/commit/e5433f61c28624298fc91224a7b0a40ec0767412))

* Small tweak in README.md for readability ([`2238bf2`](https://github.com/dbtdsilva/firefly-sync-cli/commit/2238bf2ca80317419ab4e4ce474bbe911d0a795e))

* Updated Dockerfile with daemon option ([`b04a793`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b04a793fc7551dead99fe1446ffeccdf1e25e342))

* Updated README.md with a more reasonable explanation for the possible operations ([`244d4b1`](https://github.com/dbtdsilva/firefly-sync-cli/commit/244d4b187f3874379eca670500e6921be197504f))

* Improved argparse with subparsers ([`a4b0f25`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a4b0f25090a70eca4f5e05738a886a40ddc57d33))

* Passed extra parameters to link service ([`b927678`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b92767865c849018083c7b44508b90c29fccd78f))

* Some cleanup on the encapsulation of some methods ([`3b93312`](https://github.com/dbtdsilva/firefly-sync-cli/commit/3b93312f90840ef133cfc9717ef6e1e1d8df7e72))

* Added categorization base and link of transactions ([`861fb50`](https://github.com/dbtdsilva/firefly-sync-cli/commit/861fb50f5370f11f37cb56e0dbeb56670fe427bf))

* Improved README.md with cron information and environment variables ([`7d9c0f9`](https://github.com/dbtdsilva/firefly-sync-cli/commit/7d9c0f9d781bb1b5c82170b159220b9023271383))

## v1.1.0 (2024-03-01)

### Unknown

* Supported cron job ([`a3a19ee`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a3a19ee495df43650b9c01a9ba21fd6bf4a84e76))

* Updated Dockerfile with --daemon option ([`b4ea560`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b4ea5603b7f7f879b029c7f2169ce8d2192bb153))

* Added cron job request and respective environment variables ([`12498dd`](https://github.com/dbtdsilva/firefly-sync-cli/commit/12498dda8bca809972333c06f6d6a3e23af161cf))

* Added initial support for firefly cron job ([`0943589`](https://github.com/dbtdsilva/firefly-sync-cli/commit/0943589429db0456cc356c487927db800d4ca378))

* Updated actions/setup-python workflow to v5 ([`b49b0ff`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b49b0ffbc2a2f2596efd6a7b2d36fe5a3455f4f0))

* Updated workflow versions ([`b8a050c`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b8a050ceac6580f15648997e02014d4639b9174a))

## v1.0.2 (2024-03-01)

### Unknown

* Skip file with no transactions and amount of 0 ([`114cef9`](https://github.com/dbtdsilva/firefly-sync-cli/commit/114cef9c4daf7320d440375b00a86e68cebb1b17))

## v1.0.1 (2024-02-29)

### Unknown

* Improved logging and CPU usage ([`4f672c3`](https://github.com/dbtdsilva/firefly-sync-cli/commit/4f672c3b2b7200879a0279f2398f8ba49ef61066))

## v1.0.0 (2024-02-29)

### Unknown

* Create tag if the error is while retrieving 404 ([`8a8e4ac`](https://github.com/dbtdsilva/firefly-sync-cli/commit/8a8e4ac991908081841ed360aa8f21d9cecf18eb))

* Updated README.md with changes to docker-compose ([`9fa1068`](https://github.com/dbtdsilva/firefly-sync-cli/commit/9fa10680f8da7016191e5355f6c11454924ed855))

* Changed default dry-run to false ([`8e1307f`](https://github.com/dbtdsilva/firefly-sync-cli/commit/8e1307faaceab2fbe9ef909189604cf60d4ec0b6))

* Fixed FILE_WATCHER_PATH loading from environment ([`237cf26`](https://github.com/dbtdsilva/firefly-sync-cli/commit/237cf26ecdb5cc332dc4e7cdbc193cb2b399f646))

* Added possibility to load variables from actual env ([`72536c5`](https://github.com/dbtdsilva/firefly-sync-cli/commit/72536c5ffdb7a9228f0309495e3914cca4bbbb50))

* Updated README.md ([`4a6d2f9`](https://github.com/dbtdsilva/firefly-sync-cli/commit/4a6d2f97be8700009dbec8fe04b3c24184a619cd))

* Fixed publish ([`0a71232`](https://github.com/dbtdsilva/firefly-sync-cli/commit/0a7123251a379385617abe5754b00afdf54c9bed))

* Fixed image name ([`e1ba9ae`](https://github.com/dbtdsilva/firefly-sync-cli/commit/e1ba9ae9df0679c97219edf5861baadf7f8bd08c))

* Some fixes in the workflow ([`70e7a74`](https://github.com/dbtdsilva/firefly-sync-cli/commit/70e7a747161fa6a1e25c27c36bc57581772a8209))

* Added publish workflow and Dockerfile ([`1f563e0`](https://github.com/dbtdsilva/firefly-sync-cli/commit/1f563e090f9d5ed643b3670d5bebeffb79372fd8))

* Added file watcher for firefly_sync_cli ([`38aaa9c`](https://github.com/dbtdsilva/firefly-sync-cli/commit/38aaa9cfb6475be28312394a8f77958d87f88970))

* Improved logging and added file watcher boilerplate ([`dfa7cf8`](https://github.com/dbtdsilva/firefly-sync-cli/commit/dfa7cf8b9104ca5aba9a13938c6fdd061e8576d0))

* Upsi: Removed dependency wrongly declared ([`e13e44d`](https://github.com/dbtdsilva/firefly-sync-cli/commit/e13e44dc8ec564036c0906c07bc67d42975dd01f))

* Added more logs and fixed dependencies ([`e691f89`](https://github.com/dbtdsilva/firefly-sync-cli/commit/e691f897bd5eae3482831a6dd4e81a63b7b78550))

* Added dry-run option ([`26b6d97`](https://github.com/dbtdsilva/firefly-sync-cli/commit/26b6d97187a73ba30dd8ce1198a7420091754ff2))

* Added last two parsers (revolut and activobank) ([`eb738ab`](https://github.com/dbtdsilva/firefly-sync-cli/commit/eb738ab279e8cc439933151c9e36758168a65798))

* Added parser for wise and montepio ([`e76bf96`](https://github.com/dbtdsilva/firefly-sync-cli/commit/e76bf96a5bdcc253089bc5fb182b92c70cb10ae0))

* Disable &#39;error_if_duplicate_hash&#39;, already have my own mechanism ([`6d5d13e`](https://github.com/dbtdsilva/firefly-sync-cli/commit/6d5d13e68a2cb82a3dd8a764fb77c1c1f89ca508))

* Allows script to keep importing if the tag already exists ([`cf48244`](https://github.com/dbtdsilva/firefly-sync-cli/commit/cf48244537f11170e236ff8758d5a5d7ef5596e4))

* Added logging with progress information ([`7ba9517`](https://github.com/dbtdsilva/firefly-sync-cli/commit/7ba9517de7c660a01dd022ce5d40fc743155f1e1))

* Added attachments and tags, now import will be tag for all transactions ([`9069ee2`](https://github.com/dbtdsilva/firefly-sync-cli/commit/9069ee2ce0ecd53e6f0426d3649aabee7b9dc5b1))

* Changed pipeline to make it crash when there are actual errors with flake8 ([`3147804`](https://github.com/dbtdsilva/firefly-sync-cli/commit/31478040d213cfe9122b41dfb9225c62be812299))

* Fixed flake8 warnings in tests ([`2934ad3`](https://github.com/dbtdsilva/firefly-sync-cli/commit/2934ad3e9ac7d5c05901eacb0496f31120ddfe0e))

* Fixed flake8 warnings ([`08ff8d1`](https://github.com/dbtdsilva/firefly-sync-cli/commit/08ff8d102e45c344ac4527d06acc32292941e608))

* Fixed f-string two-liner ([`1a050fe`](https://github.com/dbtdsilva/firefly-sync-cli/commit/1a050fe625835cb13f4040c0c44600186b0b4d60))

* Added logic to map and ignore if it was already stored ([`9b086cc`](https://github.com/dbtdsilva/firefly-sync-cli/commit/9b086ccbf48549c572a1efcfed7bc72201ecde8c))

* Moved also csv parser to the Parser object ([`590e9ea`](https://github.com/dbtdsilva/firefly-sync-cli/commit/590e9ead223102d4426584d3870ef9dd4830d2aa))

* Moved excel parsing to parser ([`a5395c5`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a5395c5bc2c1c7ec55703645c39760db0af20e23))

* Some cleanup, removed prints ([`57eaa21`](https://github.com/dbtdsilva/firefly-sync-cli/commit/57eaa21c697933eeba2994528b6562b130a36c21))

* Added parsed types ([`a827e94`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a827e941f28b799dc9790a26af38b041ea46eb5f))

* Fixed tests ([`63913b2`](https://github.com/dbtdsilva/firefly-sync-cli/commit/63913b2c1ff8af36c0824a4a435a0ce33d145cd2))

* Updated with existing dependencies ([`1dd01bb`](https://github.com/dbtdsilva/firefly-sync-cli/commit/1dd01bbe52d1ed661310e5da6fb26249b593d822))

* Added dynamic loading for parsing files ([`53f9a45`](https://github.com/dbtdsilva/firefly-sync-cli/commit/53f9a453246c63502630ef131d463c671d90333f))

* Added config for pytest ([`5806a8f`](https://github.com/dbtdsilva/firefly-sync-cli/commit/5806a8f60b24f72f6d6009844e3ff38bd8e67ecf))

* Added tests and fixed some calls to the API ([`9b985e1`](https://github.com/dbtdsilva/firefly-sync-cli/commit/9b985e150526f0475e7267c7871ee31f7e29d0f1))

* Added a base api class to implement Firefly requests ([`f26439b`](https://github.com/dbtdsilva/firefly-sync-cli/commit/f26439b94e177700f518ac8f901b8bd96569db37))

* Removed old codeql ([`4bbf0a1`](https://github.com/dbtdsilva/firefly-sync-cli/commit/4bbf0a1f8f8f35fc70fce2a85a08d392810bff15))

* Create codeql.yml ([`11a2129`](https://github.com/dbtdsilva/firefly-sync-cli/commit/11a2129ad5d8e08baa3fd62c8bc4251857285ddc))

* Renamed master to main ([`f55cbbf`](https://github.com/dbtdsilva/firefly-sync-cli/commit/f55cbbf4cf6f830c8b7519824a9fe838a50adb5f))

* Renamed codeql ([`aa67903`](https://github.com/dbtdsilva/firefly-sync-cli/commit/aa679033887215ff39fff5a26df08fecd7106d92))

* Disable tests until there are any (pytest returns an exit code 5 when there are no tests) ([`875f540`](https://github.com/dbtdsilva/firefly-sync-cli/commit/875f540ec886e4f4dc575dc23ce406f699f58666))

* Updated python version in workflow ([`a5195f3`](https://github.com/dbtdsilva/firefly-sync-cli/commit/a5195f336f4a7c5c3a535f10f7d1a958d628da1e))

* Updated requirements ([`dc1cb92`](https://github.com/dbtdsilva/firefly-sync-cli/commit/dc1cb920504ca5abe8092dfe8927e4c3feefea28))

* Added workflow and dependencies for test and linter ([`700534a`](https://github.com/dbtdsilva/firefly-sync-cli/commit/700534a6bafee7c6ee3e1527a8b6f52504f2dce0))

* Initial setup with communication to the firefly api ([`b35dd5c`](https://github.com/dbtdsilva/firefly-sync-cli/commit/b35dd5cba307c3f1d9202e72804e4206a336371a))

* Initial commit ([`4716702`](https://github.com/dbtdsilva/firefly-sync-cli/commit/4716702fdc7cfc8974699085f4342d5520428923))