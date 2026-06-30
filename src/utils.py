import os
import json
from datetime import datetime
from loguru import logger


def setup_logger(log_directory: str = "logs") -> None:
    """Initialize logging system with console and file outputs."""
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(
        log_directory,
        f"scraper_{datetime.now().strftime('%Y-%m-%d')}.log"
    )

    logger.remove()

    # Stream logs to console
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level}</level> | {message}",
        level="INFO"
    )

    # Write logs to file with rotation and retention
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        rotation="1 day", 
        retention="7 days"  
    )

    logger.info(f"Logging initialized. Output directory: {log_file}")


def save_json(data: list, file_path: str) -> None:
    """Save data to a JSON file with automatic directory creation."""
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2, default=str)

    logger.info(f"Successfully persisted {len(data)} records to {file_path}")


def get_image_path(channel_name: str, message_id: int) -> str:
    """Generate and ensure image storage path for a given channel and message."""
    image_dir = os.path.join("data", "raw", "images", channel_name)
    os.makedirs(image_dir, exist_ok=True)
    return os.path.join(image_dir, f"{message_id}.jpg")


def get_json_path(channel_name: str, date: datetime) -> str:
    """Generate and ensure JSON storage path organized by date."""
    formatted_date = date.strftime("%Y-%m-%d")
    message_dir = os.path.join("data", "raw", "telegram_messages", formatted_date)
    os.makedirs(message_dir, exist_ok=True)
    return os.path.join(message_dir, f"{channel_name}.json")