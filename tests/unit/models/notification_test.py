import random

import arrow
import pytest
from pydantic import ValidationError

from cumplo_common.models import Event, Notification


class TestNotification:
    def test_build_id(self) -> None:
        """Should build the ID correctly."""
        for event in Event.members():
            content_id = random.randint(1, 1000)  # noqa: S311
            id_ = Notification.build_id(event, content_id)
            assert id_ == f"{event.value}-{content_id}"

            notification = Notification.model_validate({"id": id_, "date": arrow.utcnow().datetime})
            assert notification.content_id == int(id_.split("-")[1])
            assert notification.event == event

    @pytest.mark.parametrize(
        "invalid_id",
        [
            "event_type..action-123",  # Extra dot
            "event_type.action123",  # Missing dash
            "event_type@action-123",  # Special character
            ".action-123",  # Missing part before the dot
            "event_type.-123",  # Missing part after the dot
            "event_type action-123",  # Space instead of dot
            "event_type/action-123",  # Slash instead of dot
            "event_type.action.123",  # Extra dot after event
            "event_type.action-",  # Missing content_id after the dash
        ],
    )
    def test_invalid_id_formats_raise_error(self, invalid_id: str) -> None:
        with pytest.raises(ValidationError, match="Invalid ID format"):
            Notification.model_validate({"id": invalid_id, "date": arrow.utcnow().datetime})
