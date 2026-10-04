"""Central configuration. Every value can be overridden with an environment variable."""
import json
import os
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TEST_DATA_DIR = ROOT_DIR / "test_data"
REPORTS_DIR = ROOT_DIR / "reports"


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    test_id_attribute: str = "data-test"
    default_timeout_ms: int = int(os.getenv("DEFAULT_TIMEOUT_MS", "10000"))
    viewport_width: int = int(os.getenv("VIEWPORT_WIDTH", "1366"))
    viewport_height: int = int(os.getenv("VIEWPORT_HEIGHT", "768"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()


def load_json(name: str) -> dict:
    """Load a JSON file from the test_data directory."""
    with open(TEST_DATA_DIR / name, encoding="utf-8") as fh:
        return json.load(fh)
