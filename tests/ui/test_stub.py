from data.config import Config
from pages.home_page import HomePage


def test_greencity_is_work(get_driver):
    title = get_driver.title
    assert title.startswith("GreenCity")

def test_base_navigate(get_driver):
    page = HomePage(get_driver).open()
    assert page.get_title().startswith("GreenCity")
    page = page.header.click_news_link()
    assert page.get_current_url() == f"{Config.BASE_UI_GREEN_CITY_URL}/news", f"Expected URL to be {Config.BASE_UI_GREEN_CITY_URL}/news, but got {page.get_current_url()}"
    page = page.header.click_logo()
    assert page.get_current_url() == Config.BASE_UI_GREEN_CITY_URL, f"Expected URL to be {Config.BASE_UI_GREEN_CITY_URL}, but got {page.get_current_url()}"
