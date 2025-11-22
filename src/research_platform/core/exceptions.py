"""Custom exceptions for the research platform."""


class PlatformException(Exception):
    """Base exception for research platform."""

    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class DataFetchException(PlatformException):
    """Exception raised during data fetching."""

    pass


class AnalysisException(PlatformException):
    """Exception raised during analysis."""

    pass


class ValidationException(PlatformException):
    """Exception raised for validation errors."""

    pass


class ConfigurationException(PlatformException):
    """Exception raised for configuration errors."""

    pass


class CacheException(PlatformException):
    """Exception raised for cache operations."""

    pass


class RateLimitException(PlatformException):
    """Exception raised when API rate limit is exceeded."""

    def __init__(self, message: str, retry_after: int = None, details: dict = None):
        super().__init__(message, details)
        self.retry_after = retry_after
