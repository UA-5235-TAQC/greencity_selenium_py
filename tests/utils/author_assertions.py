import pytest_check as check


def assert_author(actual_author: dict, expected_author: dict | None):
    """Author validation used across API assertions."""
    check.is_not_none(actual_author, "Author should not be null")

    if expected_author:
        check.equal(
            actual_author.get("id"),
            expected_author.get("id"),
            "Author ID should match"
        )

        check.equal(
            actual_author.get("name"),
            expected_author.get("name"),
            "Author name should match"
        )
