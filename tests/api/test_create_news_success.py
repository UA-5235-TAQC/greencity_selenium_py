from clients.create_eco_news_client import EcoNewsClient
from clients.own_security_client import OwnSecurityClient
from data.config import Config
from enums.news_tag import EcoNewsTag


def test_create_news_success():
    auth_client = OwnSecurityClient(Config.BASE_GREEN_CITY_USER_API_URL)
    login_response = auth_client.sign_in(Config.USER_EMAIL, Config.USER_PASSWORD)

    assert login_response.status_code == 200, f"Login failed: {login_response.status_code}"

    token = login_response.json().get("accessToken")

    create_news_client = EcoNewsClient(Config.BASE_GREEN_CITY_API_URL, access_token=token)

    news_payload = {
        "title": "Eco title",
        "text": "Test test Test test Test test",
        "tags": [EcoNewsTag.NEWS.en, EcoNewsTag.ADS.en],
        "source": "https://chatgpt.com/",
        "shortInfo": "short description"
    }
    image_path = "data/images/test2.png"

    response = create_news_client.add_eco_news(news_payload, image_path)
    print(f"\nResponse Body: {response.text}")
    assert response.status_code == 201, f"Expected 201, but got {response.status_code}"