import pytest
import logging
from src.logConfigure import configure_logger

@pytest.fixture
def get_logger():
    return configure_logger("test_logger")


def test_configure_logger(get_logger):
    get_logger.debug("Info test log entry")

    assert get_logger.name == "test_logger"
    assert get_logger.level == logging.DEBUG

