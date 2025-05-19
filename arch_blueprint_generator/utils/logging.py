"""
Logging utilities for the arch_blueprint_generator module.
"""

import logging
import structlog
from colorama import Fore, Style, init as colorama_init


# Initialize colorama
colorama_init()


def add_colors(_, __, event_dict: dict) -> dict:
    """
    Add colors to log level.
    
    Args:
        event_dict: The event dictionary to process
        
    Returns:
        Modified event dictionary with colored level
    """
    level = event_dict.get("level", "info").upper()
    if level == "DEBUG":
        event_dict["colored_level"] = f"{Fore.BLUE}{level}{Style.RESET_ALL}"
    elif level == "INFO":
        event_dict["colored_level"] = f"{Fore.GREEN}{level}{Style.RESET_ALL}"
    elif level == "WARNING":
        event_dict["colored_level"] = f"{Fore.YELLOW}{level}{Style.RESET_ALL}"
    elif level == "ERROR":
        event_dict["colored_level"] = f"{Fore.RED}{level}{Style.RESET_ALL}"
    elif level == "CRITICAL":
        event_dict["colored_level"] = f"{Fore.MAGENTA}{level}{Style.RESET_ALL}"
    else:
        event_dict["colored_level"] = level
    return event_dict


def configure_logging(log_level: int = logging.INFO) -> None:
    """
    Configure structured logging.
    
    Args:
        log_level: The minimum log level to display
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            add_colors,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


def get_logger(name: str = "architectum"):
    """
    Get a logger instance.
    
    Args:
        name: The logger name
        
    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)
