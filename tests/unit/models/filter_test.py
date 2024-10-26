from cumplo_common.models import FilterConfiguration


class TestFilterConfiguration:
    id_1 = "01HNQV9YFK3JZW69Z0CT3QK1QB"
    id_2 = "01HNQVAV9GFV5NB80ZEVV9AWC1"

    @classmethod
    def test_equal_empty(cls) -> None:
        """Should be equal if two empty filters are compared."""
        filter_1 = FilterConfiguration.model_validate({"id": cls.id_1})
        filter_2 = FilterConfiguration.model_validate({"id": cls.id_2})
        assert filter_1 == filter_2

    @classmethod
    def test_equal_ignored_attributes(cls) -> None:
        """Should ignore the ID, name and expiration_minutes when comparing two filters."""
        filter_1 = FilterConfiguration.model_validate({"id": cls.id_1, "name": "Name"})
        filter_2 = FilterConfiguration.model_validate({"id": cls.id_2, "name": "Name"})
        assert filter_1 == filter_2

    @classmethod
    def test_equal_same_attributes(cls) -> None:
        """Should be equal if the key attributes are the same."""
        filter_1 = FilterConfiguration.model_validate({
            "id": cls.id_1,
            "minimum_irr": "1.1",
            "minimum_score": 0.5,
            "minimum_duration": 30,
        })
        filter_2 = FilterConfiguration.model_validate({
            "id": cls.id_2,
            "minimum_irr": "1.1",
            "minimum_score": 0.5,
            "minimum_duration": 30,
        })
        assert filter_1 == filter_2

    @classmethod
    def test_different_attributes(cls) -> None:
        """Should NOT be equal if one of the key attributes are the different."""
        filter_1 = FilterConfiguration.model_validate({
            "id": cls.id_1,
            "minimum_irr": "1.1",
            "minimum_score": 0.5,
            "minimum_duration": 30,
        })
        filter_2 = FilterConfiguration.model_validate({
            "id": cls.id_2,
            "minimum_irr": "1.1",
            "minimum_score": 0.5,
            "minimum_duration": 10,
        })
        assert filter_1 != filter_2
