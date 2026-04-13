"""
Custom logging utility for framework
"""
import logging
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utilities.json_config import get_path, get_str

LOGS_DIR = get_path("paths", "logs_dir", "reports/logs")
LOG_LEVEL = get_str("logging", "log_level", "INFO").upper()

class Logger:
    """Custom logger class for test execution logging"""
    _logs_cleared = False
    
    @staticmethod
    def get_logger(name=__name__):
        """
        Creates and returns logger instance
        Args:
            name (str): Logger name
        Returns:
            Logger: Configured logger instance
        """
        # Create logs directory if not exists
        os.makedirs(LOGS_DIR, exist_ok=True)
        Logger._clear_old_logs_once()
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # File handler
        log_file = os.path.join(
            LOGS_DIR,
            f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.log"
        )
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Add handlers
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except PermissionError:
            logging.getLogger(__name__).warning(
                "Could not create log file at %s. Continuing with console logging only.",
                log_file,
            )
        logger.addHandler(console_handler)
        
        return logger

    @staticmethod
    def _clear_old_logs_once():
        """
        Delete old test log files once per run before creating new log handlers.
        """
        if Logger._logs_cleared:
            return

        for entry in os.scandir(LOGS_DIR):
            if not entry.is_file():
                continue
            if not entry.name.startswith("test_log_") or not entry.name.endswith(".log"):
                continue
            try:
                os.remove(entry.path)
            except OSError:
                # Non-blocking cleanup; logging should continue even if one file is locked.
                pass

        Logger._logs_cleared = True
