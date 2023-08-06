"""Tests for error_collector.py"""
from errorcollector.error_collector import MultipleErrorCollector, SingleErrorCollector
from tests.testlibraries.error_checker import ErrorChecker
from tests.testlibraries.exceptions import ErrorForTestFrom1, ErrorForTestFrom2, ErrorForTestTo


class TestSingleErrorCollector:
    """Tests for Single Error Collector."""

    @staticmethod
    def test():
        """should"""
        error_message = "test"
        error_collector = SingleErrorCollector(ErrorForTestTo, error_message)
        with error_collector:
            raise ErrorForTestFrom1()
        error = error_collector.error
        ErrorChecker.assert_error(error, error_message, ErrorForTestTo, ErrorForTestFrom1)


class TestMultipleErrorCollector:
    """Tests for Multiple Error Collector."""

    @staticmethod
    def test():
        """should"""
        error_message = "test"
        error_collector = MultipleErrorCollector(ErrorForTestTo, error_message, [])
        with error_collector:
            raise ErrorForTestFrom1()
        with error_collector:
            raise ErrorForTestFrom2()
        list_error = error_collector.list_error
        assert len(list_error) == 2
        ErrorChecker.assert_error(list_error[0], error_message, ErrorForTestTo, ErrorForTestFrom1)
        ErrorChecker.assert_error(list_error[1], error_message, ErrorForTestTo, ErrorForTestFrom2)

    @staticmethod
    def test_no_error():
        """should"""
        error_message = "test"
        error_collector = MultipleErrorCollector(ErrorForTestTo, error_message, [])
        with error_collector:
            pass
        list_error = error_collector.list_error
        assert len(list_error) == 0
