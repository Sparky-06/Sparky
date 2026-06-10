from loguru import logger
import sys
import os


# ----------------------
# CREATE LOGS DIRECTORY
# ----------------------
def log_init():
    LOG_DIR = "logs"
    os.makedirs(LOG_DIR, exist_ok=True)


    # ----------------------
    # REMOVE DEFAULT LOGGER
    # ----------------------

    logger.remove()


    # ----------------------
    # CONSOLE LOGGER
    # ----------------------

    logger.add(
        sys.stdout,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
    )


    # ----------------------
    # FILE LOGGER
    # ----------------------

    logger.add(
        f"{LOG_DIR}/assistant.log",
        rotation="5 MB",          # New log file after 5MB
        retention="10 days",      # Keep logs for 10 days
        compression="zip",        # Compress old logs
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )


# ----------------------
# EXAMPLE USAGE
# ----------------------

# def test_logging():
#     logger.debug("Debugging details for your inevitable future suffering.")
#     logger.info("Assistant started successfully.")
#     logger.warning("Something mildly suspicious happened.")
#     logger.error("Something broke because computers enjoy chaos.")
#     logger.critical("Catastrophic failure. Humanity had a good run.")


# if __name__ == "__main__":
#     logger.info("Initializing voice assistant...")
    
#     try:
#         test_logging()
#     except Exception as e:
#         logger.exception(f"Unhandled exception: {e}")