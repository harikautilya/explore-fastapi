import pytest
from api.core.model import CoreModel
from dataclasses import dataclass


# fake class to test the funcitonalites of copy
@dataclass(repr=True, frozen=True, kw_only=True, eq=True)
class InnerSampleModel(CoreModel):
    data_str: str


# fake class to test the funcitonalites of copy
@dataclass(repr=True, frozen=True, kw_only=True, eq=True)
class SampleModel(CoreModel):
    data_str: str
    data_int: int
    data_inner_model: InnerSampleModel


model_data = [
    (
        {
            "data_str": "Sample",
            "data_int": 1,
            "data_inner_model": {
                "data_str": "inner sample",
            },
        },
        SampleModel(
            data_str="Sample",
            data_int=1,
            data_inner_model=InnerSampleModel(data_str="inner sample"),
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
        SampleModel(
            data_str="3@$#&*&~!)@",
            data_int=-1,
            data_inner_model=InnerSampleModel(data_str="inner sample"),
        ),
    ),
]

model_copy_data = [
    (
        SampleModel(
            data_str="Sample",
            data_int=1,
            data_inner_model=InnerSampleModel(data_str="inner sample"),
        ),
        {
            "data_str": "Changed",
        },
        SampleModel(
            data_str="Changed",
            data_int=1,
            data_inner_model=InnerSampleModel(data_str="inner sample"),
        ),
    ),
    (
        SampleModel(
            data_str="Sample",
            data_int=-1,
            data_inner_model=InnerSampleModel(data_str="inner sample"),
        ),
        {
            "data_int": -10,
        },
        SampleModel(
            data_str="Sample",
            data_int=-10,
            data_inner_model=InnerSampleModel(data_str="inner sample"),
        ),
    ),
]


@pytest.mark.parametrize("model_data, expected", model_data)
def test_model_create(
    model_data: dict[str, any],
    expected: SampleModel,
):
    created_model = SampleModel(**model_data)
    assert created_model == expected


@pytest.mark.parametrize("model_data, changes, update_model_data", model_copy_data)
def test_model_copy(
    model_data: SampleModel,
    changes: dict[str, any],
    update_model_data: SampleModel,
):
    update_model = model_data.copy(**changes)
    assert update_model == update_model_data

