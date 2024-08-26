from datetime import datetime, timedelta, timezone

import pytest
from pydantic import BaseModel

from aiogram.types import DateTime


class TestDateTime:
    @pytest.mark.parametrize(
        "value,python_dump,json_dump",
        [
            (
                datetime.fromtimestamp(1494994302, timezone.utc),
                datetime.fromtimestamp(1494994302, timezone.utc),
                1494994302,
            ),
            (
                1494994302,
                datetime.fromtimestamp(1494994302, timezone.utc),
                1494994302,
            ),
        ],
        ids=[
            "datetime in",
            "timestamp in",
        ],
    )
    def test_datetime_dump(self, value, python_dump, json_dump):
        class TestModel(BaseModel):
            field: DateTime

        model = TestModel(field=value)
        assert model.model_dump(mode="python")["field"] == python_dump
        assert model.model_dump(mode="json")["field"] == json_dump

    def test_timedelta_dump(self):
        class TestModel(BaseModel):
            field: DateTime

        value = timedelta(minutes=2)
        model = TestModel(field=value)
        python_dump = model.model_dump(mode="python")["field"]
        assert python_dump == value
        json_dump = model.model_dump(mode="json")["field"]
        assert isinstance(json_dump, int)
        assert json_dump > datetime.now(timezone.utc).timestamp()
