import logging
import time

from datetime import datetime

logger = logging.getLogger(__name__)


def convert_datetime_to_unixtime(dt: datetime) -> int:
    # convert datetime into an unixtime (epoch)
    return time.mktime(dt.timetuple()) * 1000 if dt else 0
