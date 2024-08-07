import logging

import click
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rich.logging import RichHandler

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

# static list of origins
origins = ["http://localhost:3000", "https://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
