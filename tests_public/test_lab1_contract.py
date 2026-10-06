import inspect
from labs.lab1_flow import starter


def test_lab1_api_is_present():
    assert callable(starter.canonical_flow_key)
    assert callable(starter.build_flows)
    assert callable(starter.iter_flows)


def test_lab1_streaming_api_is_a_generator_function():
    assert inspect.isgeneratorfunction(starter.iter_flows)
