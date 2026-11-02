import logging
from pathlib import Path

from ezdmb.Utility.path_utility import get_appdata_path, is_android

logger = logging.getLogger()


def setupLogging():
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    log_path = Path(get_appdata_path()) / "log.txt" if is_android() else "log.txt"
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
