# ArXiv Daily Digest

A personalized daily arXiv paper recommendation system 
powered by AI. Get relevant papers delivered to your inbox 
based on your research interests and Zotero library.

## Features

- 🔍 **Smart Filtering**: Pre-filters papers by category 
  and keywords
- 🤖 **LLM Evaluation**: Uses OpenAI GPT models to 
  intelligently match papers to your interests
- 📚 **Zotero Integration**: Learns from your existing 
  research library
- 📧 **Email Delivery**: Sends daily digest with relevant
  papers, abstracts, and links
- 🔔 **Feishu Alerts**: Optional webhook push for quick
  notifications in Feishu (Lark)
- ⏰ **Automated**: Set it up once, get digests daily via 
  cron/launchd
- ⚙️ **Configurable**: Customize categories, keywords, 
  relevance threshold

## Quick Start

### Prerequisites

- Python 3.7+
- pip
- OpenAI API key
- Gmail account (or other SMTP email)
- Zotero library export (optional but recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/whatsup.git
cd whatsup
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure the system**

```bash
cp config.yaml.example config.yaml
nano config.yaml  # Edit with your settings
```

Required configuration:
- Email SMTP settings (see [docs/GMAIL_SETUP.md](docs/GMAIL_SETUP.md))
- OpenAI API key
- ArXiv categories and keywords
- Research interests description
- Zotero library path (see [docs/ZOTERO_EXPORT.md](docs/ZOTERO_EXPORT.md))
- (Optional) Feishu webhook details for push notifications
  (store the webhook URL in an environment variable for security)

4. **Run manually (test)**

```bash
python src/main.py
```

5. **Set up automation (optional)**

See [docs/CRON_SETUP.md](docs/CRON_SETUP.md) for 
instructions on scheduling daily runs.

## Configuration

### Feishu Webhook Secrets

If you enable Feishu alerts, store the webhook URL in an
environment variable (for example `FEISHU_WEBHOOK_URL`) and set
`feishu.webhook_url_secret` in `config.yaml`. The application will
resolve the value at runtime so the raw webhook URL never needs to be
checked into version control.

### ArXiv Categories

Find categories at https://arxiv.org/category_taxonomy

Common physics/astronomy categories:
- `cond-mat.supr-con` - Superconductivity
- `cond-mat.mes-hall` - Mesoscale and Nanoscale Physics
- `physics.ins-det` - Instrumentation and Detectors
- `astro-ph.IM` - Instrumentation and Methods
- `quant-ph` - Quantum Physics

### Keywords

Use keywords for pre-filtering to improve speed and reduce 
OpenAI API costs. Papers matching ANY keyword will be 
evaluated by the LLM.

Example:
```yaml
keywords:
  - superconductor
  - quasiparticle
  - THz detector
  - single photon
```

### Relevance Threshold

Papers are scored 0-10 by the LLM. The default threshold 
is 7.0. Adjust based on your needs:

- `5.0-6.0`: More papers, some less relevant
- `7.0`: Balanced (recommended)
- `8.0-9.0`: Fewer papers, highly relevant only

### Research Interests

Be specific about your current interests. The LLM uses 
this along with your Zotero library to evaluate papers.

Example:
```yaml
interests:
  description: |
    I study superconducting quantum devices, specifically:
    1. Athermal quasiparticle dynamics and trapping
    2. THz single-photon detectors for cosmology
    3. Microwave kinetic inductance detectors (MKIDs)
    4. Quantum sensing applications
```

## Project Structure

```
whatsup/
├── config.yaml             # Your configuration
├── config.yaml.example     # Configuration template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── __init__.py
│   ├── config_parser.py   # Load and validate config
│   ├── zotero_parser.py   # Parse Zotero exports
│   ├── arxiv_client.py    # Fetch papers from arXiv
│   ├── llm_evaluator.py   # OpenAI-based evaluation
│   ├── email_sender.py    # Send digest emails
│   └── main.py            # Main orchestrator
└── docs/
    ├── ZOTERO_EXPORT.md   # Zotero export guide
    ├── GMAIL_SETUP.md     # Gmail app password setup
    └── CRON_SETUP.md      # Automation scheduling
```

## Usage

### Manual Run

Run the digest manually:

```bash
python src/main.py
```

With custom config file:

```bash
python src/main.py /path/to/custom_config.yaml
```

### Automated Daily Run

See [docs/CRON_SETUP.md](docs/CRON_SETUP.md) for full 
instructions.

Quick example (runs daily at 8 AM):

```bash
crontab -e
```

Add:
```cron
0 8 * * * cd /path/to/whatsup && python src/main.py
```

### Output

The system will:
1. Load your configuration
2. Parse your Zotero library
3. Fetch papers from arXiv (last 24 hours by default)
4. Evaluate each paper with OpenAI
5. Send email with relevant papers (score >= threshold)

Example email:
```
ArXiv Digest: 3 relevant papers - 2025-11-01

======================================================================

1. Quasiparticle Dynamics in Disordered Superconductors
   Authors: Smith, J., Doe, A.
   Published: 2025-10-31
   Relevance: 8.5/10 - Directly addresses athermal 
              quasiparticle dynamics
   URL: https://arxiv.org/abs/2510.12345
   PDF: https://arxiv.org/pdf/2510.12345.pdf
   
   Abstract:
   We study the dynamics of athermal quasiparticles...
```

## Documentation

- [Zotero Export Guide](docs/ZOTERO_EXPORT.md) - How to 
  export your library
- [Gmail Setup Guide](docs/GMAIL_SETUP.md) - Configure 
  email sending
- [Cron Setup Guide](docs/CRON_SETUP.md) - Automate daily 
  runs

## Cost Estimation

### OpenAI API Costs

Using `gpt-4o-mini` (recommended):
- ~$0.15 per 1M input tokens
- ~$0.60 per 1M output tokens

Typical daily run:
- 10-50 papers to evaluate
- ~1000 tokens per paper evaluation
- **Estimated cost: $0.01-0.05 per day** (~$1-2/month)

Using `gpt-4o`:
- ~10x more expensive
- Better quality, but usually unnecessary

### Reducing Costs

1. Use narrow arXiv categories
2. Add specific keywords for pre-filtering
3. Reduce `max_days_back` to 1
4. Increase relevance threshold

## Troubleshooting

### No papers found

- Check arXiv categories are correct
- Verify papers were published recently (within 
  `max_days_back`)
- Remove or broaden keyword filters

### No relevant papers

- Lower the relevance threshold (try 6.0)
- Update your interests description to be more specific
- Check OpenAI API key is valid

### Email not received

- Verify Gmail app password (see docs/GMAIL_SETUP.md)
- Check spam folder
- Review email configuration in config.yaml
- Check logs for errors

### "Config file not found"

- Ensure config.yaml exists (copy from 
  config.yaml.example)
- Use absolute path or run from project directory

### OpenAI API errors

- Verify API key is correct
- Check you have API credits
- Check OpenAI service status

## Development

### Adding New Features

The code is modular:
- `config_parser.py`: Add new config sections
- `zotero_parser.py`: Support new export formats
- `arxiv_client.py`: Change arXiv query logic
- `llm_evaluator.py`: Modify evaluation prompt/scoring
- `email_sender.py`: Change email format

### Testing

Test individual components:

```python
from src.config_parser import ConfigParser
config = ConfigParser('config.yaml')
print(config.get_arxiv_config())
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests if applicable
4. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [arxiv Python package](https://github.com/lukasschwab/arxiv.py)
- Powered by [OpenAI](https://openai.com/)
- Inspired by researchers tired of manually browsing arXiv

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation in `docs/`

## Version

Current version: 0.0.0

---

**Happy paper hunting! 📚🔬**
