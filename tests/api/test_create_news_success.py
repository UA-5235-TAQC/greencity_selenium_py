from clients.eco_news_client import EcoNewsClient
from data.config import Config
from data.ui_news_test_data import NewsTestData
from enums.news_tag import EcoNewsTag
from models.queries import EcoNewsQuery
from models.eco_news_request import EcoNewsRequest
from schemas.greencity.eco_news import eco_news_response_schema, eco_news_page_schema
from tests.utils.validators import validate_json


def test_create_and_verify_news(auth_token):
    eco_news_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)

    news_payload: EcoNewsRequest = EcoNewsRequest(
        title="Eco title " + str(Config.USER_ID),
        text="Test content with more than 20 characters",
        tags=[EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
        source="https://chatgpt.com/",
        short_info="short description 12341"
    )
    create_response = eco_news_client.post_eco_news_with_image(
        news_payload, image_path=NewsTestData.TEST2_FILE
    )

    assert create_response.status_code == 201

    created_news_data = create_response.json()
    news_id = created_news_data.get("id")

    assert news_id is not None, "News ID was not returned!"
    query: EcoNewsQuery = EcoNewsQuery(
        title=news_payload.title,
        author_id=Config.USER_ID,
        sort="id,desc"
    )
    get_news_response = eco_news_client.get_eco_news_by_query(query)

    assert get_news_response.status_code == 200

    full_response_json = get_news_response.json()
    news_list = full_response_json.get("page", [])

    actual_news = next((item for item in news_list if item["id"] == news_id), None)

    assert actual_news is not None, f"News with ID {news_id} not found in the list!"

    is_valid, msg = validate_json(actual_news, eco_news_response_schema)
    assert is_valid, msg

    assert actual_news["title"] == news_payload.title
    assert actual_news["content"] == news_payload.text
    assert actual_news["source"] == news_payload.source
    assert actual_news["shortInfo"] == news_payload.short_info

    for tag in news_payload.tags:
        assert tag in actual_news["tagsEn"], f"Tag {tag} missing in response"

    is_valid_page, page_msg = validate_json(full_response_json, eco_news_page_schema)
    assert is_valid_page, page_msg

    delete_news_response = eco_news_client.delete_eco_news_by_id(news_id)
    assert delete_news_response.status_code == 200


def test_get_news_success(auth_token):
    eco_news_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=auth_token)
    query: EcoNewsQuery = EcoNewsQuery(
        tags=[EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
        author_id=Config.USER_ID,
        sort="title"
    )
    get_created_news = eco_news_client.get_eco_news_by_query(query)

    assert get_created_news.status_code == 200
    response_json = get_created_news.json()

    is_valid, msg = validate_json(response_json, eco_news_page_schema)
    assert is_valid, msg

    author = response_json["page"][0]["author"]["name"]
    assert author == Config.USER_NAME, f"Expected author {Config.USER_NAME}, but got {author}"
