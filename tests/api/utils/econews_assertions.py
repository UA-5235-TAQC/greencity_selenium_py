from jsonschema import validate, ValidationError

from schemas.greencity.eco_news import eco_news_response_schema


def assert_eco_news_json(response_json: dict):
    """ Assertions for validating the EcoNews API JSON response. """
    try:
        validate(instance=response_json, schema=eco_news_response_schema)
    except ValidationError as e:
        raise AssertionError(f"JSON does not match EcoNews schema: {e.message}")

    assert isinstance(response_json["id"], int), f"ID should be integer, got {type(response_json['id'])}"
    assert isinstance(response_json["title"], str), f"Title should be string, got {type(response_json['title'])}"
    assert isinstance(response_json["content"],
                      str), f"Content should be string, got {type(response_json['content'])}"
    assert isinstance(response_json["tagsEn"], list), f"tagsEn should be list, got {type(response_json['tagsEn'])}"
    assert isinstance(response_json["tagsUk"], list), f"tagsUk should be list, got {type(response_json['tagsUk'])}"
    assert response_json.get("likes", 0) == 0, f"Likes should be 0, got {response_json.get('likes')}"
    assert response_json.get("dislikes", 0) == 0, f"Dislikes should be 0, got {response_json.get('dislikes')}"
    assert response_json.get("countComments",
                             0) == 0, f"CountComments should be 0, got {response_json.get('countComments')}"
    assert response_json.get("hidden", False) is False, f"Hidden should be False, got {response_json.get('hidden')}"
