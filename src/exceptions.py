"""
Custom exceptions used by the LLM Router.
"""
class ProviderError(Exception):
    """Base exception for provider-related errors."""
    pass


class TimeoutError(ProviderError):
    """Raised when a provider request times out."""
    pass


class RateLimitError(ProviderError):
    """Raised when a provider reaches its rate limit."""
    pass


class EmptyResponseError(ProviderError):
    """Raised when a provider returns an empty response."""
    pass