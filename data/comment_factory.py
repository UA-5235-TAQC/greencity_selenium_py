from faker import Faker

PARENT_SUB_COMMENT = "Test subComment for parent subcomment for API testing"
COMMENT_MESSAGE = "Hello"
COMMENT_UPDATE_MESSAGE = "Привіт"

fake = Faker()


def parent_comment():
    return f"API Auto parent comment {fake.uuid4()}"


def comment_with_images():
    return f"API Auto comment with images {fake.uuid4()}"


def sub_comment():
    return f"API Auto subcomment {fake.uuid4()}"


def sub_comment_with_images():
    return f"API Auto subcomment with images {fake.uuid4()}"


def another_sub_comment():
    return f"Another API Auto subcomment {fake.uuid4()}"
