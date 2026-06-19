# Third-party notices

The repository's shipped analysis and validation scripts use only the Python standard library.

Live collection expects a separately installed Bilibili CLI or API client capable of structured JSON output. That external software is not vendored, redistributed, or relicensed by this repository. Review its source, release integrity, privacy behavior, and license before installation.

The workflow was developed against:

- [`public-clis/bilibili-cli`](https://github.com/public-clis/bilibili-cli), an independent third-party project.

Its transitive dependencies may include `bilibili-api-python`, `click`, `rich`, `aiohttp`, `browser-cookie3`, `PyYAML`, and QR-code libraries. Dependency names are informational and are not endorsements. Their own licenses and notices apply when installed.

This project deliberately instructs users not to enable browser-cookie extraction. Prefer isolated QR login.
