import logging
from datetime import datetime
import os
from from_root import from_root

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

LOG_FILE_DIR = os.path.join(from_root(), 'Logs')

os.makedirs(LOG_FILE_DIR, exist_ok=True)

log_file_path = os.path.join(LOG_FILE_DIR, LOG_FILE)

logging.basicConfig(filename=log_file_path, format="[%(asctime)s]-%(levelname)s-%(module)s-%(lineno)s-%(message)s", 
                     level=logging.INFO)
