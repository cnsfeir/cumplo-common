import json
from base64 import b64decode
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware


class PubSubMessage(BaseModel):
    """A wrapped Pub/Sub message"""

    publish_time: str | None = Field(None)
    attributes: dict = Field(default_factory=dict)
    message_id: str = Field(alias="messageId")
    data: str = Field(...)


class PubSubEvent(BaseModel):
    """A Pub/Sub event"""

    message: PubSubMessage = Field(...)
    subscription: str = Field(...)

    @property
    def id_user(self) -> str | None:
        """Returns the ID of the user who triggered the event"""
        return self.message.attributes.get("id_user")  # pylint: disable=no-member


class PubSubMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        """
        Middleware to handle PubSub messages.

        Args:
            request (Request): The request object.
            call_next (Callable[[Request], Awaitable[Response]]): The next middleware or endpoint to call.

        Returns:
            Response: A response object.
        """

        try:
            body = await request.body()
            content = json.loads(body.decode("utf-8"))
            event = PubSubEvent.model_validate(content)

        except ValueError:
            pass

        else:
            request._body = b64decode(event.message.data)  # pylint: disable=protected-access

        response = await call_next(request)
        return response
