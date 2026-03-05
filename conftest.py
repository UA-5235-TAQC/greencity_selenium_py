"""Root conftest – applies to all test sessions (UI and API).

Responsibilities
----------------
* Activate the logging configuration so that Allure steps are mirrored to
  stdout in CI/CD environments (real-time visibility without waiting for the
  Allure HTML report).
* Provide the ``worker_id`` fixture used by UI conftest fixtures to isolate
  parallel xdist workers.
"""

from __future__ import annotations

import pytest

from utils.logging_config import setup_logging

# Activate once at collection time (before any fixture or test runs).
setup_logging()


@pytest.fixture(scope="session")
def worker_id(request: pytest.FixtureRequest) -> str:
    """Return the pytest-xdist worker identifier, or ``"master"`` for serial runs.

    Use this fixture to avoid shared-state collisions when tests are executed
    in parallel with ``pytest -n auto``.

    Example
    -------
    ::

        @fixture(scope="session")
        def unique_user_email(worker_id):
            return f"test+{worker_id}@example.com"
    """
    return getattr(request.config, "workerinput", {}).get("workerid", "master")
