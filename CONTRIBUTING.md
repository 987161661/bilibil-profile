# Contributing

Thank you for helping make privacy-first personal analytics easier to use.

## Before opening an Issue

- Search existing Issues.
- Remove all credentials, identifiers, account exports, and personal data.
- Reproduce against synthetic fixtures when possible.
- Use a security report instead of an Issue for credential or privacy vulnerabilities.

## Development

Requirements: Python 3.10+ and a POSIX shell.

```bash
python3 -m py_compile analyze-bilibili-profile/scripts/*.py
./analyze-bilibili-profile/tests/test_offline.sh
./analyze-bilibili-profile/tests/test_exporter.sh
python3 /path/to/skill-creator/scripts/quick_validate.py analyze-bilibili-profile
```

The last command is optional for contributors without Codex's skill-creator utilities; CI validates the scripts and fixtures independently.

## Pull requests

- Keep collection read-only and local-first.
- Add or update synthetic tests.
- Do not commit real account data or secrets.
- Document observable API behavior without claiming unofficial endpoints are stable.
- Preserve reported-versus-exported counts and explicit pagination boundaries.
- Update documentation for user-visible behavior.

By contributing, you agree that your contribution is licensed under the repository's MIT License.
