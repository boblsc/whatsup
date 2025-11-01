# Changelog

All notable changes to the ArXiv Daily Digest project 
will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.0] - 2025-11-01

### Added

- Initial release of ArXiv Daily Digest
- Core functionality:
  - Configuration management via YAML
  - Zotero library parsing (BibTeX and JSON)
  - ArXiv paper fetching with category and keyword filters
  - LLM-based paper evaluation using OpenAI API
  - Email digest delivery via SMTP
- Documentation:
  - Comprehensive README with setup instructions
  - Zotero export guide (ZOTERO_EXPORT.md)
  - Gmail SMTP setup guide (GMAIL_SETUP.md)
  - Cron automation guide (CRON_SETUP.md)
- Helper scripts:
  - setup.sh for first-time installation
  - run_digest.sh for manual and automated runs
- Configuration template (config.yaml.example)
- Dependencies management (requirements.txt)

### Features

- Smart pre-filtering by arXiv categories and keywords
- Intelligent paper matching using GPT-4o-mini or GPT-4o
- Customizable relevance threshold
- Support for multiple arXiv categories
- Automated daily digest via cron/launchd
- Detailed logging

### Documentation

- Complete setup guide in README.md
- Step-by-step Zotero library export instructions
- Gmail app password configuration guide
- Cron job scheduling examples for macOS and Linux
- Cost estimation and optimization tips
- Troubleshooting section

[0.0.0]: https://github.com/yourusername/whatsup/releases/tag/v0.0.0

