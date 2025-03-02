import logging

import click
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.logging import RichHandler

from routers.v1 import (
    languages,
    users,
    projects,
    user_patterns,
    user_yarns,
    user_needles,
    photos,
    user_gauges,
)
from db.database import Base, get_engine

# configure logger
LOGLEVEL = "DEBUG"
FORMAT = "%(message)s"
logging.basicConfig(
    level=LOGLEVEL,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[click])],
)

logger = logging.getLogger("rich")

# initiate fastapi class
app = FastAPI(
    title="K3tog API",
    summary="K3tog: knitters' favorite app API",
    version="0.0.1",
    openapi_url="/api/v1/openapi.json",
)

app.include_router(languages.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(user_patterns.router)
app.include_router(user_yarns.router)
app.include_router(user_needles.router)
app.include_router(photos.router)
app.include_router(user_gauges.router)
# static list of origins
origins = ["http://localhost:3000", "https://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def load_db():
    Base.metadata.bind = get_engine()


if __name__ == "__main__":
    load_db()
