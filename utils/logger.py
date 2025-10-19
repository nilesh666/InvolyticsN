import logging
from datetime import datetime
import os

LOGFILE_NAME = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
logfile_path = os.path.join(os.getcwd(), "logs", LOGFILE_NAME)
os.makedirs(logfile_path, exist_ok=True)

LOGFILE_CURRENT = os.path.join(logfile_path, LOGFILE_NAME)

logging.basicConfig(
    filename=LOGFILE_CURRENT,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)