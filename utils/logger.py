import logging

from config.settings import REPORTS_DIR, settings

_configured = False


def get_logger(name: str) -> logging.Logger:
    """Return a logger that also writes to reports/logs/test.log."""
    global _configured
    if not _configured:
        log_dir = REPORTS_DIR / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        handler = logging.FileHandler(log_dir / "test.log", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s"))
        root = logging.getLogger()
        root.setLevel(settings.log_level)
        root.addHandler(handler)
        _configured = True
    return logging.getLogger(name)
