import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = "outputs/careflow.log") -> logging.Logger:
    """
    Set up a robust logger with both console and file handlers.
    Ensures structured timestamp formatting for runtime tracing and debugging
    across all CareFlow pipeline modules.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers if already configured
    if logger.hasHandlers():
        return logger

    # Create formatters with detailed timestamps
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler for real-time terminal output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler for persistent log storage (ensures outputs directory exists)
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger