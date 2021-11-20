from typing import (
    Any,
    DefaultDict,
    Deque,
    Dict,
    FrozenSet,
    Iterable,
    List,
    Sequence,
    Set,
    Tuple,
    Union,
)

import pytest
from pydantic import BaseModel

from pydantic_factories import ModelFactory
from pydantic_factories.exceptions import ParameterError


def test_handles_complex_typing():
    class MyModel(BaseModel):
        nested_dict: Dict[str, Dict[Union[int, str], Dict[Any, List[Dict[str, str]]]]]
        dict_str_any: Dict[str, Any]
        nested_list: List[List[List[Dict[str, List[Any]]]]]
        sequence_dict: Sequence[Dict]
        iterable_float: Iterable[float]
        tuple_ellipsis: Tuple[int, ...]
        tuple_str_str: Tuple[str, str]
        default_dict: DefaultDict[str, List[Dict[str, int]]]
        deque: Deque[List[Dict[str, int]]]
        set_union: Set[Union[str, int]]
        frozen_set: FrozenSet[str]

    class MyFactory(ModelFactory):
        __model__ = MyModel

    result = MyFactory.build()
    assert result.nested_dict
    assert result.dict_str_any
    assert result.nested_list
    assert result.sequence_dict
    assert result.iterable_float
    assert result.tuple_ellipsis
    assert result.tuple_str_str
    assert result.default_dict
    assert result.deque
    assert result.set_union
    assert result.frozen_set


def test_raises_for_user_defined_types():
    class MyClass:
        pass

    class MyModel(BaseModel):
        my_class_field: Dict[str, MyClass]

        class Config:
            arbitrary_types_allowed = True

    class MyFactory(ModelFactory):
        __model__ = MyModel

    with pytest.raises(ParameterError):
        MyFactory.build()