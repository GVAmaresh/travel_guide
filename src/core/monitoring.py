import logging
import sys

def setup_logging(log_level: int = logging.INFO) -> None:
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    formatter = logging.Formatter(log_format)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.addHandler(handler)

    logging.info("Logging has been successfully configured.")

if __name__ == '__main__':
    setup_logging(logging.DEBUG)
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")