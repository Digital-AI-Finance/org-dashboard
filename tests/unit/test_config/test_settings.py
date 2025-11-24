"""Tests for Settings configuration."""

import json
import os
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from research_platform.config.settings import (
    CacheConfig,
    DatabaseConfig,
    GitHubConfig,
    LoggingConfig,
    Settings,
)


class TestDatabaseConfig:
    """Tests for DatabaseConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = DatabaseConfig()
        assert config.enabled is False
        assert config.host == "localhost"
        assert config.port == 5432
        assert config.pool_size == 10

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"enabled": True, "host": "db.example.com", "port": 3306}
        config = DatabaseConfig.from_dict(data)
        assert config.enabled is True
        assert config.host == "db.example.com"
        assert config.port == 3306


class TestGitHubConfig:
    """Tests for GitHubConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = GitHubConfig()
        assert config.token == ""
        assert config.organization == ""
        assert config.rate_limit_pause == 60
        assert config.max_retries == 3

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"token": "test-token", "organization": "test-org"}
        config = GitHubConfig.from_dict(data)
        assert config.token == "test-token"
        assert config.organization == "test-org"

    def test_validate_missing_token(self):
        """Test validation fails without token."""
        config = GitHubConfig(organization="test-org")
        with pytest.raises(ValueError, match="token is required"):
            config.validate()

    def test_validate_missing_org(self):
        """Test validation fails without organization."""
        config = GitHubConfig(token="test-token")
        with pytest.raises(ValueError, match="organization is required"):
            config.validate()

    def test_validate_success(self):
        """Test successful validation."""
        config = GitHubConfig(token="test-token", organization="test-org")
        assert config.validate() is True


class TestCacheConfig:
    """Tests for CacheConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = CacheConfig()
        assert config.enabled is True
        assert config.ttl == 3600
        assert config.max_size_mb == 100

    def test_from_dict_with_path(self):
        """Test creating from dictionary with path string."""
        data = {"enabled": False, "directory": "/custom/cache"}
        config = CacheConfig.from_dict(data)
        assert config.enabled is False
        assert config.directory == Path("/custom/cache")


class TestLoggingConfig:
    """Tests for LoggingConfig."""

    def test_default_values(self):
        """Test default configuration values."""
        config = LoggingConfig()
        assert config.level == "INFO"
        assert config.console is True
        assert config.retention == 7

    def test_from_dict(self):
        """Test creating from dictionary."""
        data = {"level": "DEBUG", "file": "/var/log/app.log"}
        config = LoggingConfig.from_dict(data)
        assert config.level == "DEBUG"
        assert config.file == "/var/log/app.log"


class TestSettings:
    """Tests for Settings."""

    def test_default_values(self):
        """Test default settings values."""
        settings = Settings()
        assert settings.app_name == "GitHub Research Platform"
        assert settings.version == "2.0.0"
        assert settings.environment == "development"
        assert settings.debug is False

    def test_from_yaml(self, temp_dir):
        """Test loading from YAML file."""
        config_content = """
app_name: Test Platform
environment: testing
debug: true
github:
  token: yaml-token
  organization: yaml-org
cache:
  enabled: false
  ttl: 1800
"""
        config_path = temp_dir / "config.yaml"
        config_path.write_text(config_content)

        settings = Settings.from_yaml(config_path)
        assert settings.app_name == "Test Platform"
        assert settings.environment == "testing"
        assert settings.debug is True
        assert settings.github.token == "yaml-token"
        assert settings.github.organization == "yaml-org"
        assert settings.cache.enabled is False
        assert settings.cache.ttl == 1800

    def test_from_yaml_with_database(self, temp_dir):
        """Test loading YAML with database config."""
        config_content = """
app_name: DB Test
database:
  enabled: true
  host: db.test.com
"""
        config_path = temp_dir / "db_config.yaml"
        config_path.write_text(config_content)

        settings = Settings.from_yaml(config_path)
        assert settings.database is not None
        assert settings.database.enabled is True
        assert settings.database.host == "db.test.com"

    def test_from_yaml_missing_file(self, temp_dir):
        """Test loading from nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            Settings.from_yaml(temp_dir / "nonexistent.yaml")

    def test_from_json(self, temp_dir):
        """Test loading from JSON file."""
        config_data = {
            "app_name": "JSON Platform",
            "environment": "production",
        }
        config_path = temp_dir / "config.json"
        config_path.write_text(json.dumps(config_data))

        settings = Settings.from_json(config_path)
        assert settings.app_name == "JSON Platform"
        assert settings.environment == "production"

    def test_from_json_missing_file(self, temp_dir):
        """Test loading from nonexistent JSON file raises error."""
        with pytest.raises(FileNotFoundError):
            Settings.from_json(temp_dir / "nonexistent.json")

    def test_from_env(self):
        """Test loading from environment variables."""
        with patch.dict(
            os.environ,
            {
                "APP_NAME": "Env Platform",
                "ENVIRONMENT": "staging",
                "DEBUG": "true",
                "GITHUB_TOKEN": "env-token",
                "GITHUB_ORG": "env-org",
                "LOG_LEVEL": "DEBUG",
            },
        ):
            settings = Settings.from_env()
            assert settings.app_name == "Env Platform"
            assert settings.environment == "staging"
            assert settings.debug is True
            assert settings.github.token == "env-token"
            assert settings.github.organization == "env-org"
            assert settings.logging.level == "DEBUG"

    def test_override_with_env(self, temp_dir):
        """Test environment variable overrides."""
        config_content = """
app_name: Original
environment: development
github:
  token: original-token
  organization: original-org
"""
        config_path = temp_dir / "override.yaml"
        config_path.write_text(config_content)

        with patch.dict(
            os.environ,
            {
                "GITHUB_TOKEN": "env-override-token",
                "ENVIRONMENT": "production",
            },
        ):
            settings = Settings.from_yaml(config_path)
            assert settings.github.token == "env-override-token"
            assert settings.environment == "production"

    def test_override_with_numeric_env(self, temp_dir):
        """Test numeric environment variable conversion."""
        config_content = """
app_name: Numeric Test
cache:
  ttl: 3600
"""
        config_path = temp_dir / "numeric.yaml"
        config_path.write_text(config_content)

        with patch.dict(os.environ, {"CACHE_TTL": "7200"}):
            settings = Settings.from_yaml(config_path)
            assert settings.cache.ttl == 7200

    def test_to_dict(self, temp_dir):
        """Test converting settings to dictionary."""
        output_dir = temp_dir / "output"
        data_dir = temp_dir / "data"
        settings = Settings(
            app_name="Dict Test",
            output_directory=output_dir,
            data_directory=data_dir,
        )
        data = settings.to_dict()

        assert data["app_name"] == "Dict Test"
        # Use str() for platform-independent comparison
        assert data["output_directory"] == str(output_dir)
        assert data["data_directory"] == str(data_dir)

    def test_save_to_yaml(self, temp_dir):
        """Test saving settings to YAML file."""
        settings = Settings(app_name="Save YAML Test")
        output_path = temp_dir / "saved.yaml"

        settings.save_to_yaml(output_path)

        assert output_path.exists()
        with open(output_path) as f:
            loaded = yaml.safe_load(f)
        assert loaded["app_name"] == "Save YAML Test"

    def test_save_to_json(self, temp_dir):
        """Test saving settings to JSON file."""
        settings = Settings(app_name="Save JSON Test")
        output_path = temp_dir / "saved.json"

        settings.save_to_json(output_path)

        assert output_path.exists()
        with open(output_path) as f:
            loaded = json.load(f)
        assert loaded["app_name"] == "Save JSON Test"

    def test_validate_creates_directories(self, temp_dir):
        """Test validation creates required directories."""
        output_dir = temp_dir / "new_output"
        data_dir = temp_dir / "new_data"
        template_dir = temp_dir / "templates"
        template_dir.mkdir()

        settings = Settings(
            github=GitHubConfig(token="test", organization="test"),
            output_directory=output_dir,
            data_directory=data_dir,
            template_directory=template_dir,
        )

        settings.validate()

        assert output_dir.exists()
        assert data_dir.exists()

    def test_validate_missing_template_dir(self, temp_dir):
        """Test validation fails for missing template directory."""
        settings = Settings(
            github=GitHubConfig(token="test", organization="test"),
            output_directory=temp_dir / "output",
            data_directory=temp_dir / "data",
            template_directory=temp_dir / "nonexistent_templates",
        )

        with pytest.raises(ValueError, match="Template directory does not exist"):
            settings.validate()

    def test_get_phase_config_default(self):
        """Test getting phase config with defaults."""
        settings = Settings()
        config = settings.get_phase_config("unknown_phase")

        assert config["enabled"] is True
        assert config["timeout"] == 300
        assert config["retry_count"] == 3

    def test_get_phase_config_override(self):
        """Test getting phase config with overrides."""
        settings = Settings(phases={"custom_phase": {"enabled": False, "timeout": 600}})
        config = settings.get_phase_config("custom_phase")

        assert config["enabled"] is False
        assert config["timeout"] == 600
        assert config["retry_count"] == 3  # Default preserved

    def test_is_feature_enabled_true(self):
        """Test checking enabled feature."""
        settings = Settings()
        assert settings.is_feature_enabled("ml_topics") is True

    def test_is_feature_enabled_false(self):
        """Test checking disabled feature."""
        settings = Settings(features={"test_feature": False})
        assert settings.is_feature_enabled("test_feature") is False

    def test_is_feature_enabled_unknown(self):
        """Test checking unknown feature returns False."""
        settings = Settings()
        assert settings.is_feature_enabled("unknown_feature") is False

    def test_str_representation(self):
        """Test string representation."""
        settings = Settings(
            app_name="Test App",
            environment="production",
            github=GitHubConfig(organization="test-org"),
        )
        result = str(settings)

        assert "Test App" in result
        assert "production" in result
        assert "test-org" in result

    def test_path_conversion_in_from_yaml(self, temp_dir):
        """Test that path strings are converted to Path objects."""
        config_content = """
output_directory: /custom/output
data_directory: /custom/data
template_directory: /custom/templates
"""
        config_path = temp_dir / "paths.yaml"
        config_path.write_text(config_content)

        settings = Settings.from_yaml(config_path)

        assert isinstance(settings.output_directory, Path)
        assert isinstance(settings.data_directory, Path)
        assert isinstance(settings.template_directory, Path)
