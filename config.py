"""Configuration management for Lofi Hip Hop Generator"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class Config:
    """Configuration manager for the application"""

    def __init__(self, config_path: str = 'config.yaml'):
        self.config_path = Path(config_path)
        self._config = self._load_config()
        self._validate_paths()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _validate_paths(self):
        """Create necessary directories if they don't exist"""
        dirs_to_create = [
            self.get('data.output_directory', 'output'),
            self.get('data.midi_directory', 'midi_songs'),
            'data'
        ]

        for dir_path in dirs_to_create:
            Path(dir_path).mkdir(parents=True, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        Example: config.get('model.sequence_length')
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set configuration value using dot notation
        Example: config.set('model.epochs', 200)
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self):
        """Save current configuration to file"""
        with open(self.config_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)

    def get_output_filename(self, file_type: str) -> str:
        """
        Get output filename with timestamp
        file_type: 'video', 'audio', or 'midi'
        """
        template = self.get(f'output.{file_type}_filename')
        if template:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            return template.replace('{timestamp}', timestamp)

        # Default fallback
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'{file_type}_output_{timestamp}'

    @property
    def model_config(self) -> Dict[str, Any]:
        """Get model configuration"""
        return self._config.get('model', {})

    @property
    def video_config(self) -> Dict[str, Any]:
        """Get video configuration"""
        return self._config.get('video', {})

    @property
    def streaming_config(self) -> Dict[str, Any]:
        """Get streaming configuration"""
        return self._config.get('streaming', {})

    def __repr__(self):
        return f"Config(config_path='{self.config_path}')"


# Global config instance
_config_instance = None


def get_config(config_path: str = 'config.yaml') -> Config:
    """Get or create global configuration instance"""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
