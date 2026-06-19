<p align="center">
  <img src="assets/banner.svg" alt="Bilibili Profile" width="900">
</p>

<p align="center">
  <strong>Turn your Bilibili follows, favorites, and watch history into a local, evidence-weighted, auditable interest profile.</strong>
</p>

<p align="center">
  <a href="README.md">中文</a> ·
  <a href="PRIVACY.md">Privacy</a> ·
  <a href="SECURITY.md">Security</a> ·
  <a href="https://github.com/987161661/bilibil-profile/issues">Issues</a> ·
  <a href="https://github.com/sponsors/987161661">Sponsor</a>
</p>

Created and maintained by [Zeng Zi'an (@987161661)](https://github.com/987161661).

## Why

Bilibili knows what you watched, but it does not explain:

- which interests are durable and which are recent bursts;
- whether you follow creators or explore topics across many creators;
- why Bilibili discovery may feel more surprising than YouTube;
- how to turn your history into learning paths and better recommendations.

This project analyzes each data source at an appropriate evidence level instead of treating every click as a preference.

## Highlights

- Local-first data flow with no project-operated analytics server.
- QR login in an isolated local directory; never paste cookies into chat.
- Read-only collection: no likes, coins, follows, posts, or account changes.
- Completeness checks for pagination, retention boundaries, and deleted favorites.
- Evidence-weighted interpretation of favorites, cross-day viewing, follows, bursts, and feed supply.
- Structured JSON plus an auditable Markdown report.
- Works as a Codex Skill or as standalone analysis scripts.

## Install as a Codex Skill

```bash
git clone https://github.com/987161661/bilibil-profile.git
mkdir -p ~/.codex/skills
ln -s "$PWD/bilibil-profile/analyze-bilibili-profile" \
  ~/.codex/skills/analyze-bilibili-profile
```

Then ask:

```text
Use $analyze-bilibili-profile to export my Bilibili data read-only and create an interest profile.
```

## Analyze an existing export

```bash
python3 analyze-bilibili-profile/scripts/validate_export.py /path/to/export

python3 analyze-bilibili-profile/scripts/analyze_profile.py \
  --input /path/to/export \
  --output /path/to/profile.md
```

## Safety

Use this project only for your own data, explicitly authorized data, or synthetic fixtures. Do not post credentials or raw account exports in issues. Do not use it for bulk harvesting, surveillance, bypassing platform controls, or automated account interactions.

This is an independent project and is not affiliated with Bilibili. Unofficial web interfaces can change. Read [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), [ACCEPTABLE_USE.md](ACCEPTABLE_USE.md), and [LEGAL.md](LEGAL.md).

## Support

Star the repository, share a redacted insight, contribute a test, or use the repository's Sponsor button. Funding supports compatibility work, privacy review, and a smoother one-command experience.

Licensed under the [MIT License](LICENSE).
