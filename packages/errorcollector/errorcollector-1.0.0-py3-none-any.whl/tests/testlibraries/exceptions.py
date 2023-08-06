"""This module implements exceptions for this package."""


class Error(Exception):
    """
    Base class for exceptions in this module.
    @see https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """


class ErrorForTestFrom1(Error):
    """This error is used only for test."""


class ErrorForTestFrom2(Error):
    """This error is used only for test."""


class ErrorForTestTo(Error):
    """This error is used only for test."""
