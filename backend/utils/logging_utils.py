import logging

LOGS = []

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message: str):
    """Logs an event to file and memory."""
    logging.info(message)
    LOGS.append(message)
