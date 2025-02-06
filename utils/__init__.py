# utils/__init__.py
from pathlib import Path
import logging
from datetime import datetime
import os


def setup_logging(log_level: str = 'INFO') -> None:
    """Configura el sistema de logging"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / \
        f"task_alchemist_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def ensure_directories() -> None:
    """Asegura que existan los directorios necesarios"""
    dirs = ['documents', 'logs', 'templates']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """Sanitiza el nombre del archivo para que sea válido en el sistema de archivos"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()
