import pytest
from api.core.model import CoreModel
from dataclasses import dataclass


# fake class to test the funcitonalites of copy
@dataclass(repr=True, frozen=True, kw_only=True, eq=True)
class InnerSampleModelFake(CoreModel):
    data_str: str


# fake class to test the funcitonalites of copy
@dataclass(repr=True, frozen=True, kw_only=True, eq=True)
class SampleModelFake(CoreModel):
    data_str: str
    data_int: int
    data_inner_model: InnerSampleModelFake


model_data = [
    (
        {
            "data_str": "Sample",
            "data_int": 1,
            "data_inner_model": {
                "data_str": "inner sample",
            },
        },
        SampleModelFake(
            data_str="Sample",
            data_int=1,
            data_inner_model=InnerSampleModelFake(data_str="inner sample"),
        ),
    ),
    (
        {
            "data_str": "3@$#&*&~!)@",
            "data_int": -1,
            "data_inner_model": {
                "data_str": "inner sample",
            },
        },
        SampleModelFake(
            data_str="3@$#&*&~!)@",
            data_int=-1,
            data_inner_model=InnerSampleModelFake(data_str="inner sample"),
        ),
    ),
]

model_copy_data = [
    (
        SampleModelFake(
            data_str="Sample",
            data_int=1,
            data_inner_model=InnerSampleModelFake(data_str="inner sample"),
        ),
        {
            "data_str": "Changed",
        },
        SampleModelFake(
            data_str="Changed",
            data_int=1,
            data_inner_model=InnerSampleModelFake(data_str="inner sample"),
        ),
    ),
    (
        SampleModelFake(
            data_str="Sample",
            data_int=-1,
            data_inner_model=InnerSampleModelFake(data_str="inner sample"),
        ),
        {
            "data_int": -10,
        },
        SampleModelFake(
            data_str="Sample",
            data_int=-10,
            data_inner_model=InnerSampleModelFake(data_str="inner sample"),
        ),
    ),
]


@pytest.mark.parametrize("model_data, expected", model_data)
def test_model_create(
    model_data: dict[str, any],
    expected: SampleModelFake,
):
    created_model = SampleModelFake(**model_data)
    assert created_model == expected


@pytest.mark.parametrize("model_data, changes, update_model_data", model_copy_data)
def test_model_copy(
    model_data: SampleModelFake,
    changes: dict[str, any],
    update_model_data: SampleModelFake,
):
    update_model = model_data.copy(**changes)
    assert update_model == update_model_data

