"""
Utility functions for LLM search auditing.
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional

import tldextract


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: Optional[bool] = None,
    append_mode: bool = False,
) -> logging.Logger:
    """
    Set up logging configuration with explicit output destination requirements.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If provided, logs will be written to file.
        console_output: Whether to output logs to console/stdout. Must be explicitly set.
        append_mode: Whether to append to existing log file (True) or overwrite (False)

    Returns:
        Configured logger instance

    Raises:
        ValueError: If neither console_output nor log_file destination is clearly specified
    """
    # Require explicit specification of output destination
    if console_output is None and log_file is None:
        raise ValueError(
            "Must specify logging destination: either set console_output=True/False "
            "or provide log_file path, or both"
        )

    # Default console_output to False if only log_file is provided
    if console_output is None and log_file is not None:
        console_output = False

    # Require at least one output destination
    if not console_output and log_file is None:
        raise ValueError(
            "Must specify at least one logging destination: "
            "either console_output=True or provide log_file path"
        )

    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Add file handler if log_file is specified
    if log_file is not None:
        # Ensure the directory exists
        log_dir = os.path.dirname(os.path.abspath(log_file))
        os.makedirs(log_dir, exist_ok=True)

        # Use append mode if requested
        file_mode = "a" if append_mode else "w"
        file_handler = logging.FileHandler(log_file, mode=file_mode)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def extract_domain(url: str) -> Optional[str]:
    """
    Extract base domain from URL using tldextract (without subdomains).

    Parameters
    ----------
    url : str
        The URL to extract domain from

    Returns
    -------
    str or None
        The extracted domain (e.g., 'example.com') or None if extraction fails
    """
    try:
        extracted = tldextract.extract(url)
        # Combine domain and suffix (e.g., 'example' + 'co.uk' = 'example.co.uk')
        if extracted.domain and extracted.suffix:
            return f"{extracted.domain}.{extracted.suffix}".lower()
        elif extracted.domain:
            return extracted.domain.lower()
        return None
    except Exception:
        return None


def load_jsonl(filepath: str) -> List[str]:
    """
    Load jsonl file contents into a list.

    Args:
        filepath: Path to the jsonl file

    Returns:
        List of strings, one per line
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line]
