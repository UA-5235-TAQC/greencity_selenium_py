from jsonschema import validate

from clients.eco_new_client import EcoNewsClient
from data.config import Config
from enums.news_tag import EcoNewsTag
from schemas.eco_news_response_schema import eco_news_page_schema, eco_news_item_schema


def test_create_and_verify_news(auth_token):

    eco_news_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)

    news_payload = {
        "title": "Eco title " + str(Config.USER_ID),
        "text": "Test content with more than 20 characters",
        "tags": [EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
        "source": "https://chatgpt.com/",
        "shortInfo": "short description 12341"
    }
    image_path = "data/images/test2.png"

    create_response = eco_news_client.add_eco_news(news_payload, image_path)
    assert create_response.status_code == 201

    created_news_data = create_response.json()
    new_id = created_news_data.get("id")

    get_news_response = eco_news_client.find_eco_news_by_page(
        title=news_payload["title"],
        author_id=Config.USER_ID,
        sort=["id,desc"]
    )

    assert get_news_response.status_code == 200
    news_list = get_news_response.json().get("page", [])

    actual_news = next((item for item in news_list if item["id"] == new_id), None)

    validate(instance=actual_news, schema=eco_news_item_schema)

    assert actual_news is not None, f"News with ID {new_id} not found in the list!"

    assert actual_news["title"] == news_payload["title"]
    assert actual_news["content"] == news_payload["text"]
    assert actual_news["source"] == news_payload["source"]
    assert actual_news["shortInfo"] == news_payload["shortInfo"]

    for tag in news_payload["tags"]:
        assert tag in actual_news["tagsEn"], f"Tag {tag} missing in response"

    validate(instance=get_news_response.json(), schema=eco_news_page_schema)

def test_get_news_success(auth_token):
    eco_news_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)
    get_created_news = eco_news_client.find_eco_news_by_page(tags=[EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
                                                             author_id=Config.USER_ID,
                                                             sort=["title"],
                                                             )

    assert get_created_news.status_code == 200, f"Expected 200, but got {get_created_news.status_code}"

    validate(instance=get_created_news, schema=eco_news_page_schema)
