# greencity_selenium_py

Selenium + pytest UI test suite for the GreenCity web app.

## Project layout
- `pages/`: Page Object classes (e.g., `home_page.py`, `news_page.py`).
- `components/`: Reusable UI components (e.g., header, base component).
- `tests/ui/`: UI tests.
- `data/config.py`: Environment-driven configuration.

## Requirements
- Python 3.12.
- Chrome and/or Firefox installed.
- Matching WebDriver binaries available on PATH (ChromeDriver, GeckoDriver).

## Setup
Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip  
pip install -r requirements.txt
```

## Configuration
This project reads configuration from environment variables (via `python-dotenv`).
Create a `.env` file in the repo root:

```ini
BASE_GREEN_CITY_API_URL=https://example/api
BASE_GREEN_CITY_USER_API_URL=https://example/user-api
BASE_UI_GREEN_CITY_URL=https://example
HEADLESS_MODE=True
IMPLICITLY_WAIT=10
USER_EMAIL=someone@example.com
USER_ID=123
USER_LOCATION=Kyiv
USER_NAME=Someone
USER_PASSWORD=secret
```

## Run tests
Run all UI tests (both Chrome and Firefox are parameterized in `tests/conftest.py`):

```powershell
pytest -q
```

Run only UI tests:

```powershell
pytest -q tests\ui
```

## Optional: Allure reports
If you use Allure, you can generate a report after a test run:

```powershell
pytest -q --alluredir=allure-results
allure serve allure-results
```
