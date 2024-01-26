import json
from base64 import b64decode
from io import BytesIO
from typing import cast

from fastapi import Request
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, TypeAdapter


class PubSubMessage(BaseModel):
    """A wrapped Pub/Sub message"""

    publish_time: str
    attributes: dict
    message_id: str
    data: str


class PubSubEvent(BaseModel):
    """A Pub/Sub event"""

    message: PubSubMessage
    subscription: str

    @property
    def id_user(self) -> str | None:
        """
        Returns the ID of the user who triggered the event

        Returns:
            str | None: The ID of the user who triggered the event
        """
        return self.message.attributes.get("id_user")


async def manage_event(request: Request) -> None:
    """
    Identifies the event and sets the request body accordingly.

    Args:
        request (Request): The request to manage
    """
    try:
        body = await request.body()
        content = json.loads(body.decode())
    except (HTTPException, json.JSONDecodeError):
        return None

    try:
        event = TypeAdapter(PubSubEvent).validate_python(content)
    except ValueError:
        return

    content = json.loads(b64decode(event.message.data))
    _body = BytesIO(json.dumps(content).encode())
    request._body = cast(bytes, _body)  # pylint: disable=protected-access
    request.state.event = event
