from cumplo_common.models import StrEnum


class TestStrEnum:
    class HTTPVerb(StrEnum):
        """HTTP verbs."""

        GET = "GET"
        POST = "post"
        PATCH = "Patch"

    def test_in_statement(self) -> None:
        """Should be able to use `in` statement with StrEnum members case-insensitively."""
        for verb in ("GET", "POST", "PATCH"):
            for verb_case in (verb.upper(), verb.lower(), verb.title()):
                assert self.HTTPVerb.has_member(verb_case)
        for verb in ("RUN", "JUMP", "SWIM", "FLY"):
            for verb_case in (verb.upper(), verb.lower(), verb.title()):
                assert not self.HTTPVerb.has_member(verb_case)

    def test_instance(self) -> None:
        """Should be able to create instances of StrEnum members case-insensitively."""
        for verb in ("GET", "POST", "PATCH"):
            for verb_case in (verb.upper(), verb.lower(), verb.title()):
                assert self.HTTPVerb(verb_case) == getattr(self.HTTPVerb, verb.upper())
