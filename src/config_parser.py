"""Configuration parser for loading and validating YAML config."""

import os
from pathlib import Path
from typing import Any, Dict

import yaml


class ConfigParser:
    """Parse and validate the configuration file."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the config parser.
        
        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load the YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}"
            )
        
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def _validate_config(self) -> None:
        """Validate the required configuration fields."""
        required_sections = [
            'email', 'arxiv', 'openai', 'zotero', 'interests'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(
                    f"Missing required section: {section}"
                )
        
        # Validate email section
        email_fields = [
            'smtp_server', 'smtp_port', 
            'from_email', 'password', 'to_email'
        ]
        for field in email_fields:
            if field not in self.config['email']:
                raise ValueError(
                    f"Missing email field: {field}"
                )
        
        # Validate arxiv section
        if 'categories' not in self.config['arxiv']:
            raise ValueError(
                "Missing arxiv.categories"
            )

        # Validate OpenAI section
        if 'api_key' not in self.config['openai']:
            raise ValueError(
                "Missing openai.api_key"
            )

        # Validate Feishu section when enabled
        feishu_config = self.config.get('feishu', {}) or {}
        if feishu_config and not isinstance(feishu_config, dict):
            raise ValueError("Feishu configuration must be a mapping")

        if feishu_config.get('enabled'):
            feishu_store = self.config.setdefault('feishu', {})
            if not isinstance(feishu_store, dict):
                raise ValueError("Feishu configuration must be a mapping")

            webhook_url = feishu_config.get('webhook_url', '').strip()
            webhook_secret_name = feishu_config.get('webhook_url_secret', '').strip()

            if webhook_url:
                feishu_store['webhook_url'] = webhook_url
            elif webhook_secret_name:
                secret_value = os.environ.get(webhook_secret_name, '').strip()
                if not secret_value:
                    raise ValueError(
                        "Feishu webhook secret referenced by "
                        "feishu.webhook_url_secret is not set in the environment"
                    )

                # Store the resolved webhook URL for later retrieval.
                feishu_store['webhook_url'] = secret_value
            else:
                raise ValueError(
                    "Missing Feishu webhook URL. Provide either "
                    "feishu.webhook_url or feishu.webhook_url_secret"
                )

    def get_email_config(self) -> Dict[str, Any]:
        """Get email configuration."""
        return self.config['email']
    
    def get_arxiv_config(self) -> Dict[str, Any]:
        """Get arxiv configuration."""
        return self.config['arxiv']
    
    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI configuration."""
        return self.config['openai']
    
    def get_zotero_config(self) -> Dict[str, Any]:
        """Get Zotero configuration."""
        return self.config['zotero']
    
    def get_interests(self) -> Dict[str, Any]:
        """Get user interests."""
        return self.config['interests']

    def get_feishu_config(self) -> Dict[str, Any]:
        """Get Feishu configuration (optional)."""
        return self.config.get('feishu', {}) or {}

