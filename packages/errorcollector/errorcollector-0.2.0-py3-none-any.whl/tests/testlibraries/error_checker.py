"""This module implements error checker."""


class ErrorChecker:
    """This class implements error checker."""

    @staticmethod
    def assert_error(error, error_message, error_class_to, error_class_from):
        # Reason: Using type() is required to check perfectly same class. pylint: disable=unidiomatic-typecheck
        assert type(error) is error_class_to
        # Reason: Using type() is required to check perfectly same class. pylint: disable=unidiomatic-typecheck
        assert type(error.__cause__) is error_class_from
        assert str(error) is error_message
