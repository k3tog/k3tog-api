import logging

from enum import Enum

logger = logging.getLogger(__name__)


class APITags(Enum):
    users = "USERS"
    projects = "PROJECTS"
    patterns = "PATTERNS"
    yarns = "YARNS"
    needles = "NEEDLES"
