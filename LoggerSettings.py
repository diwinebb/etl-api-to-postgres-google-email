import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

def get_log():
    BASE_DIR = Path(__file__).resolve().parent
    LOGS_DIR = BASE_DIR / 'logs'
    LOGS_DIR.mkdir(exist_ok=True)

    logger = logging.getLogger("Grader")
    logger.propagate = False

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        log_file = LOGS_DIR / "log" 

        file_handler = TimedRotatingFileHandler(
            log_file, 
            when='D', 
            interval=1, 
            backupCount=3, 
            encoding='utf-8'
        )
        file_handler.suffix = "%Y-%m-%d.txt"
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger