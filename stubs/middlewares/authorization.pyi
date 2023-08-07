# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from fastapi.requests import Request

async def is_admin(request: Request) -> None: ...
