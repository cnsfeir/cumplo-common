from pytest import raises

from cumplo_common.models import Notification, Template

BASE_NOTIFICATION = {"date": "2021-01-01T00:00:00+00:00"}


class TestNotification:
    def test_invalid_id_format(self) -> None:
        """Should raise a ValueError if the ID format is invalid."""
        invalid_ids = ("123_alpha", "alpha-beta_123", "alpha_", "_123", "alpha123")
        for id_ in invalid_ids:
            with raises(ValueError, match="Invalid ID format"):
                Notification.model_validate({"id": id_, **BASE_NOTIFICATION})

    def test_invalid_id_values(self) -> None:
        """Should raise a ValueError if the ID value is invalid."""
        invalid_ids = ("alpha_123", "BETA_456", "MixEDCaSe_789")
        for id_ in invalid_ids:
            with raises(ValueError):
                Notification.model_validate({"id": id_, **BASE_NOTIFICATION})

    def test_valid_id(self) -> None:
        """Should process the ID correctly."""
        invalid_ids = ("PROMISING_123", "Promising_456", "promising_789")
        for id_ in invalid_ids:
            notification = Notification.model_validate({"id": id_, **BASE_NOTIFICATION})
            assert notification.template == Template.PROMISING
            assert notification.content_id == int(id_.split("_")[1])

    def test_build_id(self) -> None:
        """Should build the ID correctly."""
        for template in Template.members():
            id_ = Notification.build_id(template, 1001)
            assert id_ == f"{template.value}_1001"
