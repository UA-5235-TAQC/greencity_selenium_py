from __future__ import annotations
import logging
import sys
import allure_commons

_LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(name)s - %(message)s"
_DATE_FORMAT = "%H:%M:%S"


def _build_handler(stream=None) -> logging.StreamHandler:
    handler = logging.StreamHandler(stream or sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))
    return handler


class _AllureStepLogger:
    """Allure plugin that mirrors step start/stop events to the Python logger."""

    LOGGER_NAME = "allure.step"

    def __init__(self) -> None:
        self._log = logging.getLogger(self.LOGGER_NAME)

    @allure_commons.hookimpl
    def start_step(self, uuid, title, params) -> None:  # pylint: disable=unused-argument
        param_str = ", ".join(f"{k}={v}" for k, v in (params or {}).items())
        msg = f">> STEP  {title}"
        if param_str:
            msg += f"  [{param_str}]"
        self._log.info(msg)

    @allure_commons.hookimpl
    def stop_step(self, uuid, exc_type, exc_val, exc_tb) -> None:  # pylint: disable=unused-argument
        if exc_type is None:
            self._log.info("STEP PASSED")
        else:
            self._log.warning(
                "STEP FAILED  %s: %s",
                exc_type.__name__ if exc_type else "",
                exc_val,
            )


_configured = False


def setup_logging(level: int = logging.INFO, stream=None, *, mirror_allure_steps: bool = True) -> None:
    """Configure the root logger and optionally attach the Allure step bridge."""
    global _configured  # noqa: PLW0603
    if _configured:
        return
    _configured = True

    root = logging.getLogger()
    root.setLevel(level)

    if not any(isinstance(h, logging.StreamHandler) for h in root.handlers):
        root.addHandler(_build_handler(stream))

    if mirror_allure_steps:
        plugin = _AllureStepLogger()
        try:
            allure_commons.plugin_manager.register(plugin, name="greencity_step_logger")
        except ValueError:
            pass
