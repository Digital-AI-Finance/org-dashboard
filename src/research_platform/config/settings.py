"""Configuration management for the research platform."""

from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field, asdict
import os
import yaml
import json


@dataclass
class DatabaseConfig:
    """Database configuration."""
    enabled: bool = False
    host: str = "localhost"
    port: int = 5432
    name: str = "research_platform"
    user: str = "user"
    password: str = ""
    pool_size: int = 10

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseConfig":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class GitHubConfig:
    """GitHub API configuration."""
    token: str = ""
    organization: str = ""
    rate_limit_pause: int = 60
    max_retries: int = 3
    per_page: int = 100
    timeout: int = 30

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GitHubConfig":
        """Create from dictionary."""
        return cls(**data)

    def validate(self) -> bool:
        """Validate GitHub configuration."""
        if not self.token:
            raise ValueError("GitHub token is required")
        if not self.organization:
            raise ValueError("GitHub organization is required")
        return True


@dataclass
class CacheConfig:
    """Caching configuration."""
    enabled: bool = True
    ttl: int = 3600  # 1 hour
    directory: Path = field(default_factory=lambda: Path("cache"))
    max_size_mb: int = 100
    redis_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheConfig":
        """Create from dictionary."""
        if "directory" in data:
            data["directory"] = Path(data["directory"])
        return cls(**data)


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: Optional[str] = None
    console: bool = True
    rotation: str = "midnight"
    retention: int = 7

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoggingConfig":
        """Create from dictionary."""
        return cls(**data)


@dataclass
class Settings:
    """Application settings."""
    app_name: str = "GitHub Research Platform"
    version: str = "2.0.0"
    environment: str = "development"
    debug: bool = False

    # Directories
    output_directory: Path = field(default_factory=lambda: Path("docs"))
    data_directory: Path = field(default_factory=lambda: Path("data"))
    template_directory: Path = field(default_factory=lambda: Path("templates"))

    # Component configurations
    github: GitHubConfig = field(default_factory=GitHubConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    database: Optional[DatabaseConfig] = None

    # Pipeline phases configuration
    phases: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Feature flags
    features: Dict[str, bool] = field(default_factory=lambda: {
        "academic_data": True,
        "ml_topics": True,
        "collaboration_network": True,
        "advanced_visualizations": True,
        "search_indexing": True
    })

    @classmethod
    def from_yaml(cls, config_path: Path) -> "Settings":
        """Load settings from YAML file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)

        # Override with environment variables
        config_data = cls._override_with_env(config_data)

        # Parse sub-configurations
        if "github" in config_data:
            config_data["github"] = GitHubConfig.from_dict(config_data["github"])

        if "cache" in config_data:
            config_data["cache"] = CacheConfig.from_dict(config_data["cache"])

        if "logging" in config_data:
            config_data["logging"] = LoggingConfig.from_dict(config_data["logging"])

        if "database" in config_data:
            config_data["database"] = DatabaseConfig.from_dict(config_data["database"])

        # Convert path strings to Path objects
        for field_name in ["output_directory", "data_directory", "template_directory"]:
            if field_name in config_data:
                config_data[field_name] = Path(config_data[field_name])

        return cls(**config_data)

    @classmethod
    def from_json(cls, config_path: Path) -> "Settings":
        """Load settings from JSON file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, "r") as f:
            config_data = json.load(f)

        # Override with environment variables
        config_data = cls._override_with_env(config_data)

        return cls(**config_data)

    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables."""
        return cls(
            app_name=os.getenv("APP_NAME", "GitHub Research Platform"),
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            github=GitHubConfig(
                token=os.getenv("GITHUB_TOKEN", ""),
                organization=os.getenv("GITHUB_ORG", "")
            ),
            logging=LoggingConfig(
                level=os.getenv("LOG_LEVEL", "INFO")
            )
        )

    @staticmethod
    def _override_with_env(config: Dict[str, Any]) -> Dict[str, Any]:
        """Override configuration with environment variables."""
        env_mapping = {
            "GITHUB_TOKEN": ("github", "token"),
            "GITHUB_ORG": ("github", "organization"),
            "DEBUG": ("debug",),
            "LOG_LEVEL": ("logging", "level"),
            "ENVIRONMENT": ("environment",),
            "CACHE_ENABLED": ("cache", "enabled"),
            "CACHE_TTL": ("cache", "ttl"),
        }

        for env_var, path in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                current = config
                for key in path[:-1]:
                    current = current.setdefault(key, {})

                # Convert boolean strings
                if value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
                # Convert numeric strings
                elif value.isdigit():
                    value = int(value)

                current[path[-1]] = value

        return config

    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary."""
        data = asdict(self)

        # Convert Path objects to strings
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)

        return data

    def save_to_yaml(self, path: Path) -> None:
        """Save settings to YAML file."""
        data = self.to_dict()

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

    def save_to_json(self, path: Path) -> None:
        """Save settings to JSON file."""
        data = self.to_dict()

        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def validate(self) -> bool:
        """Validate all settings."""
        # Validate GitHub config
        self.github.validate()

        # Check required directories exist or can be created
        for directory in [self.output_directory, self.data_directory]:
            directory.mkdir(parents=True, exist_ok=True)

        # Validate template directory exists
        if not self.template_directory.exists():
            raise ValueError(f"Template directory does not exist: {self.template_directory}")

        return True

    def get_phase_config(self, phase_name: str) -> Dict[str, Any]:
        """Get configuration for a specific phase."""
        default_config = {
            "enabled": True,
            "timeout": 300,
            "retry_count": 3
        }

        phase_config = self.phases.get(phase_name, {})
        return {**default_config, **phase_config}

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled."""
        return self.features.get(feature, False)

    def __str__(self) -> str:
        """String representation."""
        return f"Settings(app='{self.app_name}', env='{self.environment}', org='{self.github.organization}')"