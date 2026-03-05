from math import ceil
import pytest_check as check

from tests.api.utils.author_assertions import assert_author


def assert_comment_response(actual: dict, expected: dict, check_author: bool = False):
    """Validate a single comment response returned by the API."""
    check.is_not_none(actual, "Actual comment should not be null")
    check.is_not_none(expected, "Expected comment should not be null")

    if actual and expected:
        check.equal(actual.get("id"), expected.get("id"), "Comment ID should match")
        check.equal(
            actual.get("parentCommentId"),
            expected.get("parentCommentId"),
            "ParentCommentId should match"
        )
        check.equal(actual.get("text"), expected.get("text"), "Text should match")
        check.equal(
            actual.get("createdDate"),
            expected.get("createdDate"),
            "Created date should match"
        )
        check.equal(
            actual.get("modifiedDate"),
            expected.get("modifiedDate"),
            "Modified date should match"
        )
        check.equal(
            actual.get("replies"),
            expected.get("replies"),
            "Replies count should match"
        )
        check.equal(actual.get("likes"), expected.get("likes"), "Likes should match")
        check.equal(
            actual.get("dislikes"),
            expected.get("dislikes"),
            "Dislikes should match"
        )
        check.equal(actual.get("status"), expected.get("status"), "Status should match")

        if check_author:
            assert_author(actual.get("author"), expected.get("author"))

        check.equal(
            actual.get("currentUserLiked"),
            expected.get("currentUserLiked"),
            "currentUserLiked should match"
        )
        check.equal(
            actual.get("currentUserDisliked"),
            expected.get("currentUserDisliked"),
            "currentUserDisliked should match"
        )

        actual_images = actual.get("additionalImages")
        expected_images = expected.get("additionalImages")
        if not expected_images:
            check.is_true(
                actual_images is None or len(actual_images) == 0,
                "Additional images should be null or empty"
            )
        else:
            check.is_not_none(actual_images, "Additional images should not be null")

            if actual_images:
                check.equal(
                    len(actual_images),
                    len(expected_images),
                    "Additional images length should match"
                )

                for i in range(len(expected_images)):
                    check.equal(
                        actual_images[i],
                        expected_images[i],
                        f"Additional image at index {i} should match"
                    )


def assert_page_meta(page_response: dict,
                     expected_total_elements: int,
                     expected_current_page: int):
    """Validate pagination metadata for comment list responses."""
    page = page_response.get("page")
    check.is_not_none(page, "Page list should not be null")

    total_elements = page_response.get("totalElements")
    check.equal(
        total_elements,
        expected_total_elements,
        "Total elements should match"
    )

    check.equal(
        page_response.get("currentPage"),
        expected_current_page,
        "Current page should match"
    )

    if page:
        page_size = len(page)
        expected_total_pages = ceil(total_elements / page_size)

        check.equal(
            page_response.get("totalPages"),
            expected_total_pages,
            "Total pages should match"
        )
