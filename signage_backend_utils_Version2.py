import logging
import os

def setup_logging(log_dir, level="INFO"):
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_dir, "signage.log"),
        level=getattr(logging, level),
        format="%(asctime)s %(levelname)s %(message)s"
    )