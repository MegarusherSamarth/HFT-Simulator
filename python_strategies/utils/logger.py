# Centralized logging utility for the HFT Simulator.
# Provides colored console logs and rotating file logs.

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Log Directory
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "hft_simulator.log"

class LogColors:
    # ANSI color codes for pretty console output
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    CYAN = "\033[34m"
    
class ColorFormatter(logging.Formatter):
    # Custom formatter that adds colors based on log level.
    
    FORMATS = {
        logging.DEBUG: LogColors.CYAN + "%(asctime)s [DEBUG] %(message)s" + LogColors.RESET, 
        logging.INFO: LogColors.GREEN + "%(asctime)s [INFO] %(message)s" + LogColors.RESET, 
        logging.WARNING: LogColors.YELLOW + "%(asctime)s [WARNING] %(message)s" + LogColors.RESET, 
        logging.ERROR: LogColors.RED + "%(asctime)s [ERROR] %(message)s" + LogColors.RESET, 
        logging.CRITICAL: LogColors.RED + "%(asctime)s [CRITICAL] %(message)s" + LogColors.RESET, 
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)
    
def get_logger(name: str = "HFT"):
    # Create and return a configured logger.
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorFormatter())
        logger.addHandler(console_handler)
        
        # Rotating File Handler
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5_000_000, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s %(message)s]")
        )
        logger.addHandler(file_handler)
    return logger

# Example Usage
if __name__ == "__main__":
    log = get_logger("DEMO") 
    log.info("Logger initialized successfully.") 
    log.debug("Debug message for tracing.") 
    log.warning("This is a warning.") 
    log.error("This is an error.")