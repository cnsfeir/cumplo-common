# pylint: disable=raise-missing-from

from http import HTTPStatus
from typing import Annotated

from fastapi import Header
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from cumplo_common.database import firestore


async def authenticate(request: Request, x_api_key: Annotated[str | None, Header()] = None) -> None:
    """
    Authenticates a request using either the X-API-KEY header or the user's ID in the event attributes.

    Args:
        request (Request): The request to authenticate
        x_api_key (Annotated[str  |  None, Header], optional): API key header. Defaults to None.

    Raises:
        HTTPException: When the API key is not present or invalid
    """
    if x_api_key:
        try:
            user = firestore.client.users.get(api_key=x_api_key)
        except (KeyError, ValueError):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    elif event := getattr(request.state, "event", None):
        try:
            user = firestore.client.users.get(id_user=event.id_user)
        except (KeyError, ValueError):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    request.state.user = user
