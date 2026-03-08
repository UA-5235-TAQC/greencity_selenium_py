from typing import Dict

from jsonschema import validate, ValidationError
import pytest_check as check
from schemas.greencity.eco_news import eco_news_response_schema
from tests.utils.author_assertions import assert_author


def assert_eco_news_response(actual: Dict, expected: Dict,
                             check_image: bool = False, check_author: bool = False):
    """
    Validate EcoNews response against schema and expected values.
    :param actual: API JSON response
    :param expected: Expected values dict
    :param check_image: If True, asserts imagePath exists
    :param check_author: If True, asserts author exists and matches expected
    """
    try:
        validate(instance=actual, schema=eco_news_response_schema)
    except ValidationError as e:
        raise AssertionError(
            f"JSON does not match EcoNews schema: {e.message}"
        ) from e

    check.equal(actual.get("id"), expected.get("id"), "ID should match")
    check.equal(actual.get("title"), expected.get("title"), "Title should match")
    check.equal(actual.get("content"), expected.get("content"), "Content should match")
    check.equal(actual.get("shortInfo"), expected.get("shortInfo"), "ShortInfo should match")

    check.is_not_none(actual.get("tagsEn"), "Tags EN should not be null")
    check.equal(actual.get("tagsEn"), expected.get("tagsEn"), "Tags EN should match")
    check.is_not_none(actual.get("tagsUk"), "Tags UK should not be null")
    check.equal(actual.get("tagsUk"), expected.get("tagsUk"), "Tags UK should match")

    if check_image:
        check.is_not_none(actual.get("imagePath"), "Image path should not be null")
    else:
        check.is_none(actual.get("imagePath"), "Image path should be null")

    if check_author:
        assert_author(actual.get("author"), expected.get("author"))

    check.equal(actual.get("likes", 0), 0, "Likes should be 0")
    check.equal(actual.get("dislikes", 0), 0, "Dislikes should be 0")
    check.equal(actual.get("countComments", 0), 0, "Count of comments should be 0")
    check.is_false(actual.get("hidden", False), "Hidden should be False")
