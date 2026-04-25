import structlog
from typing import Any
from config.settings import get_settings


def setup_logger() -> None:
    """Configure structured logging for the application."""
    settings = get_settings()
    
    log_level = getattr(__import__("logging"), settings.log_level.upper())
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.debug else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = __name__) -> Any:
    """Get a logger instance with the given name."""
    return structlog.get_logger(name)
