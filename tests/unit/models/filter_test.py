from pydantic import TypeAdapter

from cumplo_common.models.filter import FilterConfiguration


class TestFilterConfiguration:
    def test_equal_empty(self) -> None:
        """Should be equal if two empty filters are compared"""
        filter_1 = TypeAdapter(FilterConfiguration).validate_python({"id": 1})
        filter_2 = TypeAdapter(FilterConfiguration).validate_python({"id": 2})
        assert filter_1 == filter_2

    def test_equal_ignored_attributes(self) -> None:
        """Should ignore the ID, name and expiration_minutes when comparing two filters"""
        filter_1 = TypeAdapter(FilterConfiguration).validate_python({"id": 1, "name": "Name", "expiration_minutes": 15})
        filter_2 = TypeAdapter(FilterConfiguration).validate_python({"id": 2, "name": "Name", "expiration_minutes": 15})
        assert filter_1 == filter_2

    def test_equal_same_attributes(self) -> None:
        """Should be equal if the key attributes are the same"""
        filter_1 = TypeAdapter(FilterConfiguration).validate_python(
            {"id": 1, "filter_dicom": True, "irr": "1.1", "score": 0.5, "duration": 30}
        )
        filter_2 = TypeAdapter(FilterConfiguration).validate_python(
            {"id": 2, "filter_dicom": True, "irr": "1.1", "score": 0.5, "duration": 30}
        )
        assert filter_1 == filter_2

    def test_different_attributes(self) -> None:
        """Should NOT be equal if one of the key attributes are the different"""
        filter_1 = TypeAdapter(FilterConfiguration).validate_python(
            {"id": 1, "filter_dicom": True, "irr": "1.1", "score": 0.5, "duration": 30}
        )
        filter_2 = TypeAdapter(FilterConfiguration).validate_python(
            {"id": 2, "filter_dicom": True, "irr": "1.1", "score": 0.5, "duration": 10}
        )
        assert filter_1 != filter_2
