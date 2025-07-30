from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configuration settings for the dirt detection microservice
    """

    # Dirt detection parameters
    dirt_threshold: float = 5.0  # Percentage threshold for considering surface dirty
    min_dirt_area: int = 100  # Minimum area (pixels) to consider as dirt
    confidence_threshold: float = 0.7  # Minimum confidence for reliable detection

    # Image processing parameters
    max_image_size: int = 1024  # Maximum image dimension for processing
    blur_kernel_size: int = 5  # Gaussian blur kernel size

    # API settings
    max_file_size: int = 10 * 1024 * 1024  # 10MB max file size
    allowed_extensions: list = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False