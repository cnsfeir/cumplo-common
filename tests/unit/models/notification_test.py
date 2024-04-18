from pytest import raises

from cumplo_common.models.event import Event
from cumplo_common.models.notification import Notification


class TestNotification:
    base_notification = {"date": "2021-01-01T00:00:00+00:00"}

    def test_invalid_id_format(self) -> None:
        """
        Should raise a ValueError if the ID format is invalid
        """
        invalid_ids = [
            "abcdef-123",
            "abc_def-456",
            "123.abc-789",
            "abc.-def-010",
            "abc.def.ghi-234",
            "abc_def-",
            "-abc.def-123",
            "abc.def-12a",
            ".abc-def",
            "abc_def.-123",
        ]
        for id_ in invalid_ids:
            with raises(ValueError) as error:
                Notification.model_validate({"id": id_, **self.base_notification})
            assert "Invalid ID format" in str(error.value)

    def test_invalid_id_values(self) -> None:
        """
        Should raise a ValueError if the ID value is invalid
        """
        invalid_ids = ("alpha.beta-123", "investment.dead-456", "alpha_beta.gamma-789")
        for id_ in invalid_ids:
            with raises(ValueError):
                Notification.model_validate({"id": id_, **self.base_notification})

    def test_valid_id(self) -> None:
        """
        Should process the ID correctly
        """
        valid_ids = (
            "FUNDING_REQUEST.PROMISING-123",
            "funding_REQUEST.PROMIsing-456",
            "funding_request.PROMISING-789",
        )
        for id_ in valid_ids:
            notification = Notification.model_validate({"id": id_, **self.base_notification})
            assert notification.event == Event.FUNDING_REQUEST_PROMISING
            assert notification.content_id == int(id_.split("-")[1])

    def test_build_id(self) -> None:
        """
        Should build the ID correctly
        """
        for event in Event.members():
            id_ = Notification.build_id(event, 1001)
            assert id_ == f"{event.value}-1001"
