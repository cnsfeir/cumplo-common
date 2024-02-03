from pydantic import TypeAdapter
from pytest import raises

from cumplo_common.models.notification import Notification
from cumplo_common.models.template import Template


class TestNotification:
    base_notification = {"date": "2021-01-01T00:00:00+00:00"}

    def test_invalid_id_format(self) -> None:
        """
        Should raise a ValueError if the ID format is invalid
        """
        invalid_ids = ("123_alpha", "alpha-beta_123", "alpha_", "_123", "alpha123")
        for id_ in invalid_ids:
            with raises(ValueError) as error:
                TypeAdapter(Notification).validate_python({"id": id_, **self.base_notification})
            assert "Invalid ID format" in str(error.value)

    def test_invalid_id_values(self) -> None:
        """
        Should raise a ValueError if the ID value is invalid
        """
        invalid_ids = ("alpha_123", "BETA_456", "MixEDCaSe_789")
        for id_ in invalid_ids:
            with raises(ValueError):
                TypeAdapter(Notification).validate_python({"id": id_, **self.base_notification})

    def test_valid_id(self) -> None:
        """
        Should process the ID correctly
        """
        invalid_ids = ("PROMISING_123", "Promising_456", "promising_789")
        for id_ in invalid_ids:
            notification = TypeAdapter(Notification).validate_python({"id": id_, **self.base_notification})
            assert notification.template == Template.PROMISING
            assert notification.content_id == int(id_.split("_")[1])

    def test_build_id(self) -> None:
        """
        Should build the ID correctly
        """
        for template in Template.members():
            id_ = Notification.build_id(template, 1001)
            assert id_ == f"{template.value}_1001"
