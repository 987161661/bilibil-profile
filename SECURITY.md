# Security policy

## Supported version

Security fixes are provided for the latest commit on the default branch.

## Report privately

Do not open a public Issue for vulnerabilities involving credentials, account access, private exports, or personally identifiable data.

Use GitHub's **Security → Report a vulnerability** private reporting flow when available. If private vulnerability reporting is not enabled, open a minimal Issue containing no secrets and ask the maintainer for a private contact channel.

Include:

- affected commit or version;
- operating system and Python version;
- the smallest safe reproduction;
- impact and realistic attack scenario;
- suggested remediation, if known.

Never include real `SESSDATA`, `bili_jct`, passwords, QR-login links, raw Cookie headers, or unredacted account exports.

## Security design

- QR login should run in an isolated local `HOME`.
- Browser Cookie databases must not be scanned.
- Only read-only account endpoints are permitted.
- Logs and deliverables must be scanned for credential markers.
- Temporary credential files must be removed after export.
- Anti-bot controls, CAPTCHAs, access restrictions, and rate limits must not be bypassed.

## Disclosure

Please allow a reasonable remediation period before public disclosure. The maintainer will acknowledge a valid report, assess impact, prepare a fix, and credit the reporter unless anonymity is requested.
