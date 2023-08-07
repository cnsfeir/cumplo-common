# pylint: disable=unused-import, missing-function-docstring, unused-argument
# flake8: noqa: F401

from datetime import datetime
from typing import Annotated

from google.cloud.tasks_v2 import HttpMethod, Task

from cumplo_common.utils.constants import LOCATION, PROJECT_ID

def create_http_task(
    url: str,
    queue: str,
    payload: dict,
    task_id: str,
    dispatch_deadline: int | None = ...,
    schedule_time: datetime | None = ...,
    http_method: Annotated[int, HttpMethod] = ...,
) -> Task: ...
