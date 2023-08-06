"""Errors module."""

__all__ = ['Error', 'ConfigError', 'DuplicateError', 'ReadonlyError',
           'SpecError']


class Error(Exception):
    """Base Exception."""


class ConfigError(Error):
    """Raised if there is a problem with the configuration."""


class DuplicateError(Error):
    """Raised if an option already exists in a section."""


class SpecError(Error):
    """Raised if there is a problem with the specification."""


class ReadonlyError(Error):
    """Raised on an attempt to set a readonly option."""
