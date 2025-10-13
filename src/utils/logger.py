"""
Logging configuration for the Air Quality Forecasting System
"""
import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from config.settings import settings


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages toward loguru sinks."""
    
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(
    log_level: str = settings.LOG_LEVEL,
    log_file: Optional[str] = settings.LOG_FILE,
    json_logs: bool = False,
) -> None:
    """
    Setup logging configuration
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        json_logs: Whether to use JSON format for logs
    """
    # Remove default logger
    logger.remove()
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Console logging
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        colorize=True,
    )
    
    # File logging
    if log_file:
        if json_logs:
            logger.add(
                log_file,
                level=log_level,
                format="{time} | {level} | {name}:{function}:{line} | {message}",
                serialize=True,
                rotation="10 MB",
                retention="30 days",
            )
        else:
            logger.add(
                log_file,
                level=log_level,
                format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                       "{name}:{function}:{line} | {message}",
                rotation="10 MB",
                retention="30 days",
            )
    
    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    
    # Set specific loggers to WARNING to reduce noise
    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logging.getLogger(logger_name).handlers = [InterceptHandler()]


def get_logger(name: str) -> "logger":
    """Get a logger instance"""
    return logger.bind(name=name)