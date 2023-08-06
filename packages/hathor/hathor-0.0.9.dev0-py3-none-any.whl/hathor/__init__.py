import logging
import os
import sys

__version__ = "0.0.9.dev0"

logging.basicConfig(
    stream=sys.stderr,
    level=getattr(logging, os.environ.get("LOG_LEVEL", "INFO"), logging.INFO)
)

LOG = logging.getLogger(__name__)
LOG.info(f"Running version {__version__}")
