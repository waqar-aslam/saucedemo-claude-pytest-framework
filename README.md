# Saucedemo UI tests (Playwright + Pytest)

UI automation for https://www.saucedemo.com using the Page Object Model.

## Setup
```
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
```

## Run
```
.venv\Scripts\python -m pytest                # everything
.venv\Scripts\python -m pytest -m smoke       # quick sanity checks
.venv\Scripts\python -m pytest -m negative    # invalid input / error handling
.venv\Scripts\python -m pytest -m e2e         # full purchase journey
.venv\Scripts\python -m pytest --headed       # watch the browser
```
Config can be overridden with env vars: `BASE_URL`, `DEFAULT_TIMEOUT_MS`, `VIEWPORT_WIDTH`, `VIEWPORT_HEIGHT`, `LOG_LEVEL`.

## Layout
- `pages/`, `components/` – page objects (locators and actions only, no assertions)
- `tests/` – tests and fixtures (`conftest.py`); all assertions live here
- `models/`, `utils/`, `config/`, `test_data/` – data models, helpers, settings, JSON data
- `reports/logs/test.log` – run log; `reports/artifacts/` – traces and screenshots for failed tests

## Not covered
`docs/testscenarios.md` asks for API-vs-UI validation. Saucedemo has no product, cart, order or order-history API, so that layer is deferred and the suite validates through the UI only.
