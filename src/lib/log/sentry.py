import logging
from typing import Dict

from raven.contrib.django.raven_compat.models import client

from infra.configure.config import GeneralConfig
from .logger import logger


def message(msg: str, extra: Dict=None) -> None:
    _message(msg, logging.INFO, extra=extra)


def error_message(msg: str, extra: Dict=None) -> None:
    _message(msg, logging.ERROR, extra=extra)


def _message(msg: str, log_level: int, extra: Dict=None) -> None:
    if GeneralConfig.is_dev():
        logger.log(log_level, msg)
        return

    client.captureMessage(
        message=msg,
        level=log_level,
        stack=True,
        extra=extra,
    )


def exception() -> None:
    if GeneralConfig.is_dev():
        return

    client.captureException()
