import logging

def setup_logger():
    logger = logging.getLogger("MultiFileLogger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    log_levels = {
        "DEBUG": "debug.log",
        "INFO": "info.log",
        "WARNING": "warning.log",
        "ERROR": "error.log",
        "CRITICAL": "critical.log",
    }

    for level, filename in log_levels.items():
        handler = logging.FileHandler(filename)
        handler.setLevel(getattr(logging, level))
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
