# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from typing import Annotated

from fastapi import Header
from fastapi.requests import Request

from cumplo_common.database.firestore import firestore_client

async def authenticate(request: Request, x_api_key: Annotated[str | None, Header] = ...) -> None: ...
