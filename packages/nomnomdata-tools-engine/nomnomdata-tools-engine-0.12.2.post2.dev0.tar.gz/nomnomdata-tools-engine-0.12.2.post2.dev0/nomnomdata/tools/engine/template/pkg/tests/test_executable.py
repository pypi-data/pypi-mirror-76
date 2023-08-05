from ..executable import hello_world


def test_no_name():
    args = {"repeat": 1}
    api_calls, results = hello_world(**args)
    assert results == (args["repeat"], f"Hello World")


def test_with_name():
    args = {"repeat": 3, "name": "Joe"}
    api_calls, results = hello_world(**args)
    assert results == (args["repeat"], f"Hello Joe")


# Nominode API calls are returned along with function results.
# The api_calls variable is used to capture this data.
